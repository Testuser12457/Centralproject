import json
import time
import random
import requests

# محاكاة زيارة مقال
def simulate_article_visit(url, proxy):
    try:
        print(f"[👣] Visiting: {url} using proxy: {proxy}")
        # مكان تنفيذ الزيارة باستخدام البروكسي لو أردت
        time.sleep(random.uniform(2, 5))  # محاكاة القراءة
    except Exception as e:
        print(f"[❌] Error visiting article: {e}")

# نشر على Reddit
def post_to_reddit(article_url, account):
    print(f"[📢] Reddit post by {account['reddit_username']}: {article_url}")
    # مكان الكود الفعلي للنشر

# نشر على Pinterest
def post_to_pinterest(article_url, account):
    print(f"[📌] Pinterest post by {account['pinterest_username']}: {article_url}")
    # مكان الكود الفعلي للنشر

# تنفيذ مهام كل Agent
def run_agent(agent_config):
    proxy = agent_config["proxy"]
    account = agent_config["account"]
    delay = agent_config["delay"]
    article_urls = agent_config.get("articles_to_visit", [])

    if not article_urls:
        print("[❌] No articles assigned to agent.")
        return

    for url in article_urls:
        simulate_article_visit(url, proxy)

        if "reddit" in agent_config["platforms"]:
            post_to_reddit(url, account)
        if "pinterest" in agent_config["platforms"]:
            post_to_pinterest(url, account)

        time.sleep(delay)

def main():
    with open("agent_config.json") as f:
        config = json.load(f)

    agents = config["agents"]
    for agent_config in agents:
        run_agent(agent_config)

if __name__ == "__main__":
    main()
