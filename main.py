import random
import json
import requests
from bs4 import BeautifulSoup
from github_api import push_agent_config
from Central import REPOSITORIES, TOTAL_AGENTS_RANGE, AGENT_CONFIG_FILENAME, AGENT_DELAY_RANGE

BLOG_URL = "https://ammuse12345.blogspot.com"

def fetch_blog_articles(blog_url):
    """جلب روابط المقالات من المدونة"""
    try:
        response = requests.get(blog_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = list({a["href"] for a in soup.find_all("a", href=True) if blog_url in a["href"]})
        print(f"[✅] Found {len(links)} articles.")
        return links
    except Exception as e:
        print(f"[❌] Error fetching articles: {e}")
        return []

def generate_agent_distribution(total, num_repos):
    base = total // num_repos
    remainder = total % num_repos
    return [base + (1 if i < remainder else 0) for i in range(num_repos)]

def generate_unique_proxy_list(repo_index, total_agents):
    return [f"proxy_{repo_index}_{i}" for i in range(total_agents)]

def generate_unique_accounts(repo_index, total_agents):
    return [
        {
            "reddit_username": f"reddit_user_{repo_index}_{i}",
            "reddit_password": f"pass_{repo_index}_{i}",
            "pinterest_username": f"pinterest_user_{repo_index}_{i}",
            "pinterest_password": f"pass_{repo_index}_{i}"
        }
        for i in range(total_agents)
    ]

def generate_config_for_repo(repo_index, total_agents, article_pool):
    proxies = generate_unique_proxy_list(repo_index, total_agents)
    accounts = generate_unique_accounts(repo_index, total_agents)
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

def main():
    total_agents = random.randint(*TOTAL_AGENTS_RANGE)
    repo_keys = list(REPOSITORIES.keys())
    distribution = generate_agent_distribution(total_agents, len(repo_keys))

    print(f"Distributing {total_agents} agents among {len(repo_keys)} repos: {distribution}")

    article_pool = fetch_blog_articles(BLOG_URL)
    if not article_pool:
        print("[❌] No articles found, aborting.")
        return

    for i, repo_key in enumerate(repo_keys):
        repo_info = REPOSITORIES[repo_key]
        agent_config = generate_config_for_repo(i + 1, distribution[i], article_pool)
        content_str = json.dumps(agent_config, indent=2)

        push_agent_config(
            owner=repo_info["owner"],
            repo=repo_info["repo"],
            path=AGENT_CONFIG_FILENAME,
            content=content_str
        )

if __name__ == "__main__":
    main()
