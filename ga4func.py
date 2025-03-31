import httpx
import requests
import bs4
import json
import pdfplumber
import github
from datetime import datetime

# Task 1: ESPN Cricinfo - Count Ducks on Page 6
def count_ducks_on_page6():
    url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?page=6"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    duck_column = [int(td.text) for td in soup.select("td[data-stat='0']")]
    return sum(duck_column)

# Task 2: IMDb - Movies Rated 2 to 5
def fetch_low_rated_movies():
    url = "https://www.imdb.com/search/title/?user_rating=2.0,5.0&count=25"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    movies = []
    for item in soup.select(".lister-item-content")[:25]:
        title = item.h3.a.text
        year = item.h3.find("span", class_="lister-item-year").text.strip()
        rating = item.select_one(".ratings-imdb-rating strong").text.strip()
        movie_id = item.h3.a['href'].split('/')[2]
        movies.append({"id": movie_id, "title": title, "year": year, "rating": rating})
    return json.dumps(movies, indent=2)

# Task 3: Wikipedia API - Extract Headings
def fetch_wikipedia_outline(country):
    url = f"https://en.wikipedia.org/wiki/{country}"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    headings = [tag.text for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    return "\n".join(["#" * (int(tag.name[1])) + " " + tag.text for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])

# Task 4: BBC Weather API - Islamabad Forecast
def get_islamabad_forecast(api_key):
    locator_url = f"https://weather.api.bbc.com/locator?city=Islamabad&api_key={api_key}"
    location_id = requests.get(locator_url).json()["locationId"]
    forecast_url = f"https://weather.api.bbc.com/forecast/{location_id}?api_key={api_key}"
    forecast_data = requests.get(forecast_url).json()
    return {day['localDate']: day['enhancedWeatherDescription'] for day in forecast_data['forecasts']}

# Task 5: Nominatim API - Max Latitude of Lima
def get_max_latitude_lima():
    url = "https://nominatim.openstreetmap.org/search?city=Lima&country=Peru&format=json"
    response = requests.get(url).json()
    return max(float(item['boundingbox'][1]) for item in response)

# Task 6: Hacker News - Latest Go Post with 85+ Points
def get_hn_go_post():
    url = "https://hnrss.org/newest?q=Go"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'xml')
    for item in soup.find_all("item"):
        if int(item.find("points").text) >= 85:
            return item.find("link").text
    return None

# Task 7: GitHub API - Berlin Users with 140+ Followers
def get_newest_berlin_github_user():
    url = "https://api.github.com/search/users?q=location:Berlin+followers:>140"
    response = requests.get(url).json()
    users = sorted(response['items'], key=lambda x: x['created_at'], reverse=True)
    return users[0]['created_at'] if users else None

# Task 8: GitHub Actions - Daily Commit
def generate_github_action():
    action_yaml = """
    name: Daily Commit
    on:
      schedule:
        - cron: '0 0 * * *'
    jobs:
      commit:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v2
          - name: Make a commit (23f2004644@ds.study.iitm.ac.in)
            run: |
              date > update.txt
              git add update.txt
              git commit -m "Daily update"
              git push
    """
    return action_yaml

# Task 9: PDF Parsing - Student Marks Analysis
def extract_student_marks(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        marks = []
        for page in pdf.pages:
            text = page.extract_table()
            for row in text:
                if 19 <= int(row[0]) <= 51 and int(row[4]) >= 37:
                    marks.append(int(row[1]))
    return sum(marks)

# Task 10: PDF to Markdown Conversion
def pdf_to_markdown(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        markdown_text = ""
        for page in pdf.pages:
            markdown_text += "\n" + page.extract_text() + "\n"
    return markdown_text
