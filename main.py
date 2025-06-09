import random
import json
from github_api import push_agent_config
from config import REPOSITORIES, TOTAL_AGENTS_RANGE, AGENT_CONFIG_FILENAME, AGENT_DELAY_RANGE


def generate_agent_distribution(total, num_repos):
    """ يقسم العدد الكلي على المستودعات مع توزيع عادل """
    base = total // num_repos
    remainder = total % num_repos
    distribution = [base + (1 if i < remainder else 0) for i in range(num_repos)]
    return distribution


def generate_unique_proxy_list(repo_index, total_agents):
    """ مولد وهمي للبروكسيات المختلفة لكل مستودع """
    return [f"proxy_{repo_index}_{i}" for i in range(total_agents)]


def generate_unique_accounts(repo_index, total_agents):
    """ مولد وهمي لحسابات فريدة لكل مستودع """
    return [
        {
            "reddit_username": f"reddit_user_{repo_index}_{i}",
            "reddit_password": f"pass_{repo_index}_{i}",
            "pinterest_username": f"pinterest_user_{repo_index}_{i}",
            "pinterest_password": f"pass_{repo_index}_{i}"
        }
        for i in range(total_agents)
    ]


def generate_config_for_repo(repo_index, total_agents):
    proxies = generate_unique_proxy_list(repo_index, total_agents)
    accounts = generate_unique_accounts(repo_index, total_agents)
    agents = []

    for i in range(total_agents):
        agent = {
            "proxy": proxies[i],
            "account": accounts[i],
            "delay": random.randint(*AGENT_DELAY_RANGE),
            "articles_to_visit": random.randint(4, 5),
            "platforms": ["reddit", "pinterest"]
        }
        agents.append(agent)

    return {"agents": agents}


def main():
    total_agents = random.randint(*TOTAL_AGENTS_RANGE)
    repo_keys = list(REPOSITORIES.keys())
    distribution = generate_agent_distribution(total_agents, len(repo_keys))

    print(f"Distributing {total_agents} agents among {len(repo_keys)} repos: {distribution}")

    for i, repo_key in enumerate(repo_keys):
        repo_info = REPOSITORIES[repo_key]
        agent_config = generate_config_for_repo(i + 1, distribution[i])

        # تحويل البيانات إلى JSON
        content_str = json.dumps(agent_config, indent=2)

        # إرسال الملف إلى المستودع
        push_agent_config(
            owner=repo_info["owner"],
            repo=repo_info["repo"],
            path=AGENT_CONFIG_FILENAME,
            content=content_str
        )


if __name__ == "__main__":
    main()
