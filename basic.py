import tweepy
import re
import requests

# ========== Step 1: Twitter API Setup ==========
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# ========== Step 2: Fetch Tweets ==========
def fetch_tweets(query, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode='extended').items(count)
    return [tweet.full_text for tweet in tweets]

# ========== Step 3: Extract URLs ==========
def extract_urls(text):
    url_pattern = r'(https?://\S+)'
    return re.findall(url_pattern, text)

# ========== Step 4: Expand Shortened URLs ==========
def expand_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except:
        return url  # If it fails, just return original

# ========== Step 5: Check if URL looks scammy ==========
def is_scammy(url):
    scammy_keywords = ['airdrop', 'giveaway', 'free crypto', 'verify', 'wallet drain']
    suspicious_domains = ['bit.ly', 'tinyurl.com', 't.co', 'grabify', 'rebrand.ly']

    for keyword in scammy_keywords:
        if keyword in url.lower():
            return True

    for domain in suspicious_domains:
        if domain in url:
            return True

    if len(url) > 100:
        return True

    return False

# ========== Step 6: Main ==========
if __name__ == "__main__":
    query = "airdrop OR giveaway OR free crypto"
    tweets = fetch_tweets(query)

    scammy_links = []

    for tweet in tweets:
        urls = extract_urls(tweet)
        for url in urls:
            full_url = expand_url(url)
            if is_scammy(full_url):
                scammy_links.append(full_url)

    # Remove duplicates
    scammy_links = list(set(scammy_links))

    # Output
    print("🚨 Scammy Links Found:")
    for link in scammy_links:
        print(link)

    # Optionally, save to a file
    with open("scammy_links.txt", "w") as f:
        for link in scammy_links:
            f.write(link + "\n")
