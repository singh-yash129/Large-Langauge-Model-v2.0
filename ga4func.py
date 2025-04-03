import httpx
import requests
import bs4
from bs4 import BeautifulSoup
import json
import pdfplumber
import github
from datetime import datetime
                # to convert API to json format

from urllib.parse import urlencode

# to parse the webpage

import pandas as pd
import re                     # regular expression operators


WIKI_BASE_URL = "https://en.wikipedia.org/wiki/"


# Task 1: ESPN Cricinfo - Count Ducks on Page 6
def count_ducks_on_page6():
    url = "https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page=6;template=results;type=batting"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    duck_column = [int(td.text) for td in soup.select("td[data-stat='0']")]
    return sum(duck_column)

# Task 2: IMDb - Movies Rated 2 to 5
def fetch_low_rated_movies():

    url = "https://www.imdb.com/search/title/?user_rating=2.0,5.0&count=25"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.select('.ipc-metadata-list-summary-item')

        movie_data = []

        for index, movie in enumerate(movies):
            if index >= 25:
                break  # Stop after collecting 25 movies
        
            title_element = movie.select_one('.ipc-title__text')
            year_element = movie.select_one('.dli-title-metadata-item')
            rating_element = movie.select_one('.ipc-rating-star--rating')
            link_element = movie.select_one('.ipc-title-link-wrapper')
        
            title = title_element.text.strip() if title_element else 'N/A'
            year = year_element.text.strip() if year_element else 'N/A'
            rating = rating_element.text.strip() if rating_element else 'N/A'
        
        # Extract IMDb ID from the href attribute
            id_match = link_element['href'].split('/')[2] if link_element and 'href' in link_element.attrs else 'N/A'
        
            movie_data.append({"id": id_match, "title": title, "year": year, "rating": rating})

    # Print extracted movie data as JSON
        return (json.dumps(movie_data, indent=2))



# Task 3: Wikipedia API - Extract Headings
def fetch_wikipedia_page(country: str) -> str:
    url = WIKI_BASE_URL + country.replace(" ", "_")
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.text

def extract_headings(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    markdown_outline = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])  # Extract heading level from tag name
        title = heading.text.strip()
        markdown_outline += "#" * level + f" {title}\n\n"
    
    return markdown_outline

def fetch_wikipedia_outline(country: str):
    html_content = fetch_wikipedia_page(country)
    if not html_content:
        return {"error": "Country not found or unable to fetch Wikipedia page."}
    
    markdown_outline = extract_headings(html_content)
    return {"country": country, "outline": markdown_outline}

# Task 4: BBC Weather API - Islamabad Forecast
def get_weather_forecast(country):
    test_city = country
    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
   'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
   's': test_city,
   'stack': 'aws',
   'locale': 'en',
   'filter': 'international',
   'place-types': 'settlement,airport,district',
   'order': 'importance',
   'a': 'true',
   'format': 'json'
})
    result = requests.get(location_url).json()
    url      = 'https://www.bbc.com/weather/'+result['response']['results']['results'][0]['id']
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    daily_high_values = soup.find_all('span', attrs={'class': 'wr-day-temperature__high-value'})
    daily_low_values  = soup.find_all('span', attrs={'class': 'wr-day-temperature__low-value'})
    daily_summary = soup.find('div', attrs={'class': 'wr-day-summary'})
    daily_summary_list = re.findall('[a-zA-Z][^A-Z]*', daily_summary.text)
    datelist = pd.date_range(datetime.today(), periods=len(daily_high_values)).tolist()
    datelist = [datelist[i].date().strftime('%y-%m-%d') for i in range(len(datelist))]
    weather_data = {}
    for i in range(len(datelist)):
      weather_data[datelist[i]] = daily_summary_list[i]

    weather_json = json.dumps(weather_data, indent=2)
    print(weather_json)



# Task 5: Nominatim API - Max Latitude of Lima

def get_max_latitude(area):
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent="myGeocoder")

    location = locator.geocode(area)

# Accessing the bounding box information.  Nominatim returns a string like
# "48.8534100,-2.3488000,48.8600000,-2.3330000".  We need to parse it.

    bounding_box_str = location.raw['boundingbox']
    bounding_box = [float(coord) for coord in bounding_box_str]

    max_latitude = max(bounding_box[0], bounding_box[1]) # boundingbox order: south, north, west, east


    return (f"The maximum latitude of the bounding box for {area} is: {max_latitude}")


# Task 6: Hacker News - Latest Go Post with 85+ Points
def get_hn_go_post(points):
    url = f"https://hnrss.org/newest?points={points}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Failed to retrieve data"
    
    soup = BeautifulSoup(response.text, 'xml')
    
    for item in soup.find_all("item"):
        link_tag = item.find("link")
        
        if link_tag:
            return link_tag.text
    
    return "No posts found with 85+ points"

# Task 7: GitHub API - Berlin Users with 140+ Followers
def get_newest_berlin_github_user():
    url = "https://api.github.com/search/users?q=location:Berlin+followers:>140&sort=joined&order=desc"
    response = requests.get(url).json()
    
    if 'items' not in response or not response['items']:
        return "No users found"
    
    newest_user = response['items'][0]
    newest_user=newest_user['login']
    user_url=f"https://api.github.com/users/{newest_user}"
    response = requests.get(user_url).json()

   
    created_at = response.get('created_at', "No creation date available")
    
    return created_at if created_at <= "2025-02-04T22:33:09Z" else "Ignoring ultra-new users"

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
import os
# Task 9: PDF Parsing - Student Marks Analysis
def extract_student_marks(file_name):
    pdf_path=os.path.join(os.getcwd(),'tmp',file_name)
    with pdfplumber.open(pdf_path) as pdf:
        marks = []
        for page in pdf.pages:
            text = page.extract_table()
            for row in text:
                if 19 <= int(row[0]) <= 51 and int(row[4]) >= 37:
                    marks.append(int(row[1]))
    return sum(marks)

# Task 10: PDF to Markdown Conversion
def pdf_to_markdown(file_name):
    pdf_path=os.path.join(os.getcwd(),'tmp',file_name)
    with pdfplumber.open(pdf_path) as pdf:
        markdown_text = ""
        for page in pdf.pages:
            markdown_text += "\n" + page.extract_text() + "\n"
    return markdown_text
