import os
import json
import random
import importlib.util

# إعدادات عامة
TOTAL_AGENTS = 500
AGENT_DELAY_RANGE = (30, 90)  # تأخير بين كل تفاعل لزيادة الواقعية

# قائمة روابط المقالات (مثال)
BLOG_URL = "https://ammuse12345.blogspot.com"
ARTICLE_LINKS = [
    f"{BLOG_URL}/2024/01/article-{i}.html" for i in range(1, 101)
]

# المستودعات التي سيتم توزيع الوكلاء عليها
REPOSITORIES = {
    "repo1": {"repo": "agents_repo_1"},
    "repo2": {"repo": "agents_repo_2"},
    "repo3": {"repo": "agents_repo_3"},
    "repo4": {"repo": "agents_repo_4"},
    "repo5": {"repo": "agents_repo_5"},
}

# تحميل البروكسيات من ملف proxy.py داخل المستودع
def load_proxies_from_repo(repo_path):
    proxy_file = os.path.join(repo_path, "proxy.py")
    spec = importlib.util.spec_from_file_location("proxy", proxy_file)
    proxy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(proxy_module)
    return proxy_module.PROXIES

# تحميل الحسابات من account.json داخل المستودع
def load_accounts_from_repo(repo_path):
    account_file = os.path.join(repo_path, "account.json")
    with open(account_file, "r") as f:
        return json.load(f)

# توزيع البروكسيات لكل مستودع
def generate_unique_proxy_list(repo_path, total_agents):
    all_proxies = load_proxies_from_repo(repo_path)
    return all_proxies[:total_agents]

# توزيع الحسابات لكل مستودع
def generate_unique_accounts(repo_path, total_agents):
    all_accounts = load_accounts_from_repo(repo_path)
    return all_accounts[:total_agents]

# توليد إعدادات الوكلاء لمستودع معين
def generate_config_for_repo(repo_index, total_agents, article_pool, repo_path):
    proxies = generate_unique_proxy_list(repo_path, total_agents)
    accounts = generate_unique_accounts(repo_path, total_agents)
    agents = []

    for i in range(total_agents):
        articles_to_visit = random.sample(article_pool, min(random.randint(4, 5), len(article_pool)))
        agent = {
            "proxy": proxies[i],
            "account": accounts[i],
            "delay": random.randint(*AGENT_DELAY_RANGE),
            "articles_to_visit": articles_to_visit,
            "platforms": ["reddit", "pinterest"]
        }
        agents.append(agent)

    return {"agents": agents}

# حفظ ملف الإعدادات داخل المستودع
def save_agent_config(repo_path, config):
    config_path = os.path.join(repo_path, "agent_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

# توزيع الوكلاء بالتساوي على المستودعات
def distribute_agents(total_agents, repositories):
    repo_count = len(repositories)
    base = total_agents // repo_count
    remainder = total_agents % repo_count
    distribution = [base + (1 if i < remainder else 0) for i in range(repo_count)]
    return distribution

# الدالة الرئيسية
def main():
    distribution = distribute_agents(TOTAL_AGENTS, REPOSITORIES)
    article_pool = ARTICLE_LINKS.copy()

    for i, repo_key in enumerate(REPOSITORIES):
        repo_info = REPOSITORIES[repo_key]
        repo_path = f"./{repo_info['repo']}"

        agent_config = generate_config_for_repo(i + 1, distribution[i], article_pool, repo_path)
        save_agent_config(repo_path, agent_config)

        print(f"[✅] Saved agent config for {repo_info['repo']} with {distribution[i]} agents.")

if __name__ == "__main__":
    main()
