import os
import json
import cloudscraper
import feedparser

def ensure_out_dir():
    if not os.path.exists('./out'):
        os.makedirs('./out', exist_ok=True)

def do_fetch(item):
    print(f"1️⃣开始获取：{item['name']}")
    scraper = cloudscraper.create_scraper()
    info = scraper.get(item['url'])
    print("the status code is ", info.status_code)

    res = info.text
    
    if 'type' not in item or item['type'] == 'rss':
        with open(f"./out/{item['name']}.xml", 'w', encoding='utf-8') as f:
            f.write(res)
        
        parsed_feed = feedparser.parse(res)
        format_type = parsed_feed.version if hasattr(parsed_feed, 'version') else 'unknown'
        print({"format": format_type})
        
        # 转换为类似feedsmith的输出格式
        feed_data = {
            "title": parsed_feed.feed.title if hasattr(parsed_feed.feed, 'title') else '',
            "link": parsed_feed.feed.link if hasattr(parsed_feed.feed, 'link') else '',
            "description": parsed_feed.feed.description if hasattr(parsed_feed.feed, 'description') else '',
            "entries": []
        }
        
        for entry in parsed_feed.entries:
            entry_data = {
                "title": entry.title if hasattr(entry, 'title') else '',
                "link": entry.link if hasattr(entry, 'link') else '',
                "published": entry.published if hasattr(entry, 'published') else '',
                "description": entry.description if hasattr(entry, 'description') else ''
            }
            feed_data["entries"].append(entry_data)
        
        with open(f"./out/{item['name']}.json", 'w', encoding='utf-8') as f:
            json.dump(feed_data, f, ensure_ascii=False, indent=2)

def main():
    ensure_out_dir()
    
    with open("./rss.json", "r", encoding="utf-8") as f:
        rss = json.load(f)
    
    for item in rss:
        try:
            do_fetch(item)
        except Exception as e:
            print(f"错误：{e}")

if __name__ == "__main__":
    main()