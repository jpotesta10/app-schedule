from flask import Flask, request, render_template_string
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime

app = Flask(__name__)

# Your NewsAPI key
API_KEY = 'your_api_key_here'
BASE_URL = "https://newsapi.org/v2/top-headlines"

# Store the latest search term
latest_search_term = None

# HTML template for the home page
HTML_TEMPLATE = '''
<!doctype html>
<html>
<head><title>News Fetcher</title></head>
<body>
    <h1>Enter your search term for daily news updates</h1>
    <form action="/" method="post">
        <input type="text" name="search_term" />
        <input type="submit" value="Submit" />
    </form>
</body>
</html>
'''

def fetch_news(search_term):
    """Fetches news from NewsAPI based on the search term."""
    params = {
        'q': search_term,
        'apiKey': API_KEY,
        'pageSize': 5  # limit the results to 5 articles
    }
    response = requests.get(BASE_URL, params=params)
    news = response.json().get('articles', [])
    for article in news:
        print(f"{article['title']} - {article['url']}")

def scheduled_job():
    """The job that the scheduler will run daily."""
    if latest_search_term:
        print(f"Fetching news for: {latest_search_term}")
        fetch_news(latest_search_term)
    else:
        print("No search term provided yet.")

@app.route('/', methods=['GET', 'POST'])
def home():
    global latest_search_term
    if request.method == 'POST':
        latest_search_term = request.form['search_term']
        print(f"Updated search term to: {latest_search_term}")
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', days=1, start_date=datetime.datetime.now() + datetime.timedelta(seconds=10))
    scheduler.start()
    app.run(debug=True)
