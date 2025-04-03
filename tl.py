import requests
from bs4 import BeautifulSoup

def count_ducks_on_page6():
    url = "https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page=6;template=results;type=batting"

    # Mimic a real browser to prevent blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Error: Received status code {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
     
    # Locate the stats table
    table = soup.find("table", class_="engineTable")
    if not table:
        return "Error: No stats table found on the page."

    # Extract table headers and clean them
    headers = [th.text.strip().lower() for th in table.find_all("th")]
    print("Table Headers:", headers)  # Debugging step

    # Find the correct index for Ducks column (checking multiple possible names)
    possible_duck_headers = {"0", "ducks", "0s"}  # Add variations if needed
    duck_index = next((i for i, h in enumerate(headers) if h in possible_duck_headers), None)

    if duck_index is None:
        return "Error: 'Ducks' column not found."

    # Extract all rows and sum up the ducks
    total_ducks = 0
    for row in table.find_all("tr")[1:]:  # Skip header row
        cells = row.find_all("td")
        if len(cells) > duck_index:
            try:
                total_ducks += int(cells[duck_index].text.strip() or "0")  # Handle empty values
            except ValueError:
                pass  # Ignore non-numeric values

    return f"Total ducks on page 6: {total_ducks}"

# Run function
print(count_ducks_on_page6())
