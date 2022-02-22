import hashlib
import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from telegram_news.template import InfoExtractor, NewsPostman, InfoExtractorJSON, NewsPostmanJSON
from telegram_news.utils import xml_to_json

bot_token = os.getenv("TOKEN")
channel = os.getenv("CHANNEL")
channel2 = os.getenv("CHANNEL2")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
db = Session(bind=engine.connect())
def ssc_id_policy(link):
        return hashlib.md5(link.encode("utf-8")).hexdigest()

#-------------------------channel 1----------------------------------#

url1 = "https://doc.ssc.nic.in/Portal/LatestNews"
tag1 = "ssc"
table_name1 = "ssc"

# Info extractor to process data format
ie1 = InfoExtractor()

# Select elements by CSS-based selector
ie1.set_list_selector('#forScrollNews > ul > li')
ie1.set_title_selector('h3')
ie1.set_paragraph_selector('#forScrollNews > ul > li > a')
ie1.set_time_selector('span')
ie1.set_source_selector('span.sourceTemplate')
ie1.max_post_length = 2000

#ie1.set_id_policy(ssc_id_policy)
# News postman to manage sending affair
np1 = NewsPostman(listURLs=[url1, ], sendList=[channel,channel2, ], db=db, tag=tag1)
np1.set_bot_token(bot_token)
np1.set_extractor(ie1)
np1.set_table_name(table_name1)
np1.set_max_list_length(25)
np1.set_max_table_rows(25 * 3, False)
np1.poll()
"""
#-------------------------channel 2----------------------------------#

url2 = "https://www.scmp.com/rss/91/feed"
tag2 = "SCMP"
table_name2 = "scmpnews"

ie2 = InfoExtractorJSON()

# Pre-process the XML string, convert to JSON string
def list_pre_process(text):
    text = json.loads(xml_to_json(text))
    return json.dumps(text)
ie2.set_list_pre_process_policy(list_pre_process)

# Route by key list
ie2.set_list_router(['rss', 'channel', 'item'])
ie2.set_link_router(['link'])
ie2.set_title_router(['title'])
ie2.set_paragraphs_router(['description'])
ie2.set_time_router(['pubDate'])
ie2.set_source_router(['author'])
ie2.set_image_router(['media:thumbnail', '@url'])

# Customize ID for news item
def id_policy(link):
    return hashlib.md5(link.encode("utf-8")).hexdigest()
ie2.set_id_policy(id_policy)

np2 = NewsPostmanJSON(listURLs=[url2, ], sendList=[channel, ], db=db, tag=tag2)
np2.set_extractor(ie2)
np2.set_table_name(table_name2)
np2.set_max_list_length(50)
np2.set_max_table_rows(50 * 3, False)
np2.poll()
"""
