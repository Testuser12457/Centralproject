import json
import time
import random
import requests
from bs4 import BeautifulSoup

BLOG_URL = "https://ammuse12345.blogspot.com"

# جلب المقالات من المدونة
def get_articles_from_blog(blog_url, max_articles=100):
    try:
        response = requests.get(blog_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True) if "202" in a['href']]
        links = list(set(links))
        random.shuffle(links)
        return links[:max_articles]
    except Exception as e:
        print(f"[❌] Error scraping blog: {e}")
        return []

# محاكاة زيارة مقال
def simulate_article_visit(url, proxy):
    try:
        print(f"[👣] Visiting: {url} using proxy: {proxy}")
        # يمكن استخدام proxy هنا لو عندك requests مع بروكسيات
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
    articles_count = agent_config["articles_to_visit"]

    all_articles = get_articles_from_blog(BLOG_URL)
    if not all_articles:
        print("[❌] No articles found.")
        return

    selected_articles = random.sample(all_articles, min(articles_count, len(all_articles)))

    for url in selected_articles:
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
