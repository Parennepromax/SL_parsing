import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    news_dict = {}
    n_pages = 2
    for count in range(1, n_pages + 1):
        url = f"https://www.securitylab.ru/news/page1_{count}.php"
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")
        articles_cards = soup.find_all("a", class_="article-card")

        for article in articles_cards:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()
            article_url = f'https://www.securitylab.ru{article.get("href")}'
            article_date_time = article.find("time").get("datetime")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")

            article_id = article_url.split("/")[-1]
            article_id = article_id[:-4]

            print(f"{article_title} | {article_url} | {date_time}")

            news_dict[article_id] = {
                "date_time": date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_fresh_news():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    url = "https://www.securitylab.ru/news/"
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    articles_cards = soup.find_all("a", class_="article-card")

    fresh_news = {}
    for article in articles_cards:
        article_url = f'https://www.securitylab.ru{article.get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()

            article_date_time = article.find("time").get("datetime")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")

            news_dict[article_id] = {
                "date_time": date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_date_timestamp": date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    with open("fresh_news_dict.json", "w") as file:
        json.dump(fresh_news, file, indent=4, ensure_ascii=False)


def main():
    # Создание файла со всеми новостями
    if os.path.exists("news_dict.json"):
        pass
    else:
        get_first_news()
    # Проверка новых новостей
    check_fresh_news()


if __name__ == '__main__':
    main()
