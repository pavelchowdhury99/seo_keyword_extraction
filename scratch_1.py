from googlesearch import search
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup


# Step 1. Getting top n urls from Google's search results

def get_links_from_google(term, num_results=10, lang='en'):
    url_list = [x for x in search(term=term, lang=lang, num_results=num_results)]
    return pd.DataFrame(url_list, columns=['url'])


# Testing step 1
df = get_links_from_google('Latest Mobiles in India', 5)


# Step 2. Getting the content of the top n pages

def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    with HTMLSession() as session:
        try:
            res = session.get(url, headers=headers, timeout=200)
            return BeautifulSoup(res.content, 'html.parser').text
        except:
            return BeautifulSoup('', 'html.parser').text
        finally:
            print(f"Done Scrapping")

# Testing step 2
df['text'] = df['url'].apply(lambda x: get_page_content(x))
df.to_pickle('data.pkl')
