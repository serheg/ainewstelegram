import feedparser
import time
from datetime import datetime
from email.utils import format_datetime

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
            if feed.bozo: # bozo - признак того, что лента не распарсилась корректно
                print(f"⚠️ Предупреждение: лента {url} может быть некорректной. {feed.bozo_exception}")
            all_entries.extend(feed.entries)
            print(f"✅ Загружено {len(feed.entries)} записей из {url}")
        except Exception as e:
            print(f"❌ Не удалось загрузить ленту {url}: {e}")

    # Сортируем все посты по дате публикации
    all_entries.sort(key=lambda x: x.get('published_parsed', time.gmtime()), reverse=True)

    # Генерируем новый RSS 2.0 фид
    rss_header = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Моя объединенная RSS-лента</title>
    <link>https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/</link>
    <description>Все лучшие новости в одном месте</description>
    <lastBuildDate>{format_datetime(datetime.now())}</lastBuildDate>
    <atom:link href="https://serheg.github.io/ainewstelegram/feed.xml" rel="self" type="application/rss+xml" />
"""
    
    rss_items = ""
    for entry in all_entries[:100]: # Ограничим 100 последними постами
        title = entry.title.replace(']]>', ']]>') # Экранирование для CDATA
        summary = entry.get('summary', 'Нет описания').replace(']]>', ']]>')
        pub_date = format_datetime(datetime.fromtimestamp(time.mktime(entry.published_parsed))) if 'published_parsed' in entry else ''
        
        rss_items += f"""
    <item>
        <title><![CDATA[{title}]]></title>
        <link>{entry.link}</link>
        <guid isPermaLink="true">{entry.link}</guid>
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
