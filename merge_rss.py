import feedparser
import time
from datetime import datetime
from email.utils import format_datetime
from html import escape

# Список ваших RSS-лент
FEED_URLS = [
   'https://rss.datuan.dev/telegram/channel/casetapai',
   'https://rss.datuan.dev/telegram/channel/HelloAlesha',
   'https://rss.datuan.dev/telegram/channel/iSimplify',
   'https://rss.datuan.dev/telegram/channel/solokumi',
   'https://rss.datuan.dev/telegram/channel/erdman_ai',
   'https://rss.datuan.dev/telegram/channel/the_ai_architect',
   'https://rss.datuan.dev/telegram/channel/t2fmedia',
   'https://rss.datuan.dev/telegram/channel/gscrm',
   'https://rss.datuan.dev/telegram/channel/misha_davai_po_novoi',
   'https://rss.datuan.dev/telegram/channel/shromarketing',
   'https://rss.datuan.dev/telegram/channel/aihacki',
   'https://rss.datuan.dev/telegram/channel/dzenopulse',
   'https://rss.datuan.dev/telegram/channel/TochkiNadAI',
   'https://rss.datuan.dev/telegram/channel/prompt_design',
   'https://rss.datuan.dev/telegram/channel/gptdoit',
   'https://rss.datuan.dev/telegram/channel/NeuralProfit',
   'https://rss.datuan.dev/telegram/channel/neyroseti_dr',
   'https://rss.datuan.dev/telegram/channel/neuron_media',
   'https://rss.datuan.dev/telegram/channel/gptdoit',
   'https://rss.datuan.dev/telegram/channel/neurogen_news',
   'https://rss.datuan.dev/telegram/channel/denissexy',
   'https://rss.datuan.dev/telegram/channel/neiroit_world',
   'https://rss.datuan.dev/telegram/channel/v_neuro',
   'https://rss.datuan.dev/telegram/channel/neurocry',
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
