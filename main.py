import os
import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from keep_alive import keep_alive
import time

TELEGRAM_BOT_TOKEN = os.environ.get('TOKEN')
TELEGRAM_CHAT_ID = '@Hindi_News_In'
RSS_FEED_URL = 'https://hindi-news-aptak.blogspot.com/feeds/posts/default?alt=rss'

CHECK_INTERVAL_SECONDS = 120  # 5 minutes

keep_alive()

# Keep track of the latest processed post's unique identifier
last_processed_post_id = None

def send_telegram_message_with_image(post_title, post_url, image_url):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": f"{post_title}\n\n{post_url}",
        "photo": image_url
    }
    response = requests.post(url, data=data)
    print("Telegram API response:", response.text)

def main():
    global last_processed_post_id
    
    while True:
        feed = feedparser.parse(RSS_FEED_URL)
        
        latest_post = feed.entries[0]
        post_id = latest_post.guid if latest_post.guid else latest_post.link  # Use a unique identifier
        
        if post_id != last_processed_post_id:
            last_processed_post_id = post_id
            
            post_title = latest_post.title
            post_description = latest_post.description

            description_soup = BeautifulSoup(post_description, 'html.parser')
            post_image = description_soup.find('img')['src'] if description_soup.find('img') else None

            if post_image:
                post_url = latest_post.link
                send_telegram_message_with_image(post_title, post_url, post_image)
        
        # Wait for the specified interval before checking again
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == '__main__':
    main()
  
