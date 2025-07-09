import feedparser
import time
from datetime import datetime
from email.utils import format_datetime
from html import escape

# Список ваших RSS-лент
FEED_URLS = [
    'https://habr.com/ru/rss/hubs/all/',
    'https://www.opennet.ru/opennews/opennews_rss.rss',
    'https://3dnews.ru/news/rss/',
    # Добавьте сюда свои ленты
]

# Название файла, в который будем сохранять результат
OUTPUT_FILE = "feed.xml"

def fetch_and_merge():
    all_entries = []
    for url in FEED_URLS:
        try:
            feed = feedparser.parse(url)
            if feed.bozo:
                print(f"⚠️ Предупреждение: лента {url} может быть некорректной. {feed.bozo_exception}")
            all_entries.extend(feed.entries)
            print(f"✅ Загружено {len(feed.entries)} записей из {url}")
        except Exception as e:
            print(f"❌ Не удалось загрузить ленту {url}: {e}")

    all_entries.sort(key=lambda x: x.get('published_parsed', time.gmtime()), reverse=True)

    # ЗАМЕНИТЕ YOUR_USERNAME и YOUR_REPO_NAME
    repo_url = "https://serheg.github.io/ainewstelegram"
    
    rss_header = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Моя объединенная RSS-лента</title>
    <link>{repo_url}/</link>
    <description>Все лучшие новости в одном месте</description>
    <lastBuildDate>{format_datetime(datetime.now())}</lastBuildDate>
    <atom:link href="{repo_url}/{OUTPUT_FILE}" rel="self" type="application/rss+xml" />
"""
    
    rss_items = ""
    for entry in all_entries[:100]:
        title = entry.title.replace(']]>', ']]>')
        summary = entry.get('summary', 'Нет описания').replace(']]>', ']]>')
        pub_date = format_datetime(datetime.fromtimestamp(time.mktime(entry.published_parsed))) if 'published_parsed' in entry else ''
        
        # Экранируем ссылку, чтобы она была валидной в XML
        link = escape(entry.link)
        
        rss_items += f"""
    <item>
        <title><![CDATA[{title}]]></title>
        <link>{link}</link>
        <guid isPermaLink="true">{link}</guid>
        <pubDate>{pub_date}</pubDate>
        <description><![CDATA[{summary}]]></description>
    </item>
"""

    rss_footer = """
</channel>
</rss>
"""
    
    full_rss = rss_header + rss_items + rss_footer
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_rss)
    print(f"\nГотово! Файл '{OUTPUT_FILE}' успешно сгенерирован.")

if __name__ == "__main__":
    fetch_and_merge()
