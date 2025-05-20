import requests
import json
import pandas as pd
import os
import time

# Token autentikasi
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMJ60gEAAAAASSnwdOzTNqepSAuAQKwIxVvMw68%3DEFcnmXorm7w3zYs5CsagxQhgZRYEtn0CVvqi2jlH8IMZO8yEf2'

# Kata kunci pencarian
query = 'perang dagang china amerika'

# Endpoint Twitter API
search_url = "https://api.twitter.com/2/tweets/search/recent"

# Parameter pencarian
query_params = {
    'query': query,
    'max_results': 50,
    'tweet.fields': 'author_id,created_at,public_metrics,text',
    'expansions': 'author_id',
    'user.fields': 'username'
}

# Header autentikasi
headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
    'User-Agent': 'v2RecentSearchPython'
}

# Fungsi koneksi ke endpoint API dengan retry
def connect_to_endpoint(url, headers, params, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            retry_count += 1
            print(f"[{retry_count}] Terkena rate limit (429). Menunggu 60 detik sebelum mencoba ulang...")
            time.sleep(60)  # Tunggu 60 detik sebelum retry
        else:
            raise Exception(f"Request gagal: {response.status_code}, {response.text}")
    raise Exception("Gagal terus setelah beberapa kali percobaan (429 Rate Limit).")

# Proses pengambilan data
try:
    json_response = connect_to_endpoint(search_url, headers, query_params)
except Exception as e:
    print(f"Gagal mengambil data: {e}")
    exit()

# Validasi isi data
if 'data' not in json_response:
    print("Tidak ada tweet ditemukan untuk query tersebut.")
    exit()

# Ambil data tweet
tweets_data = []
for tweet in json_response.get('data', []):
    metrics = tweet.get('public_metrics', {})
    tweets_data.append({
        'Tweet ID': tweet.get('id'),
        'Author ID': tweet.get('author_id'),
        'Tanggal': tweet.get('created_at'),
        'Isi Tweet': tweet.get('text'),
        'Retweet Count': metrics.get('retweet_count', 0),
        'Reply Count': metrics.get('reply_count', 0),
        'Like Count': metrics.get('like_count', 0),
        'Quote Count': metrics.get('quote_count', 0)
    })

# Simpan ke CSV jika data tersedia
if tweets_data:
    filename = os.path.join(os.getcwd(), 'DimasOktavianPrasetyo_22230016.csv')
    df = pd.DataFrame(tweets_data)
    df.to_csv(filename, index=False)
    print(f"Sukses! Data disimpan di {filename}")
else:
    print("Data kosong, tidak ada yang disimpan.")
