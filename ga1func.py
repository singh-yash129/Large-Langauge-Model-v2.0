import os
import json
import zipfile
import hashlib
import requests
import subprocess
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
from Prebuilt import gunc

def get_vscode_version():
    return gunc('q-vs-code-version')

def make_http_request(email):
    url = f"https://httpbin.org/get?email={email}"
    response = requests.get(url)
    return response.json()

def run_npx_command(filename):
    file_path = os.path.join(os.getcwd(), 'uploads', 'README.md')
    command = f"npx -y prettier@3.4.2 {file_path} | sha256sum"
    return subprocess.getoutput(command)

def google_sheets_formula(s, i):
    return sum(range(s, s + 10 * i, i))

def excel_formula(i_list, s_list, r):
    sorted_list = sorted(zip(i_list, s_list))[:r]
    return sum(i for i, _ in sorted_list)

def count_wednesdays(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return sum(1 for d in pd.date_range(start, end) if d.weekday() == 2)

def extract_csv_from_zip(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall("./extracted")
    df = pd.read_csv("./extracted/extract.csv")
    return df["answer"].iloc[0]

def sort_json(json_list):
    return json.dumps(sorted(json_list, key=lambda x: (x["age"], x["name"])), separators=(",", ":"))

def multi_cursor_to_json(input_text):
    return json.dumps(input_text.splitlines())

def extract_hidden_value(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find("input", {"type": "hidden"})["value"]

def sum_css_values(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return sum(int(div["data-value"]) for div in soup.find_all("div", class_="foo"))

def process_encoded_files(zip_filename, symbols):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall("./data")
    total = 0
    for file in Path("./data").glob("*.csv"):
        df = pd.read_csv(file, encoding='utf-8', names=["symbol", "value"])
        total += df[df["symbol"].isin(symbols)]["value"].sum()
    return total

def use_github(repo_url, email):
    filename = "email.json"
    with open(filename, "w") as f:
        json.dump({"email": email}, f)
    return repo_url + f"/raw/main/{filename}"

def replace_text_in_files(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall("./replace")
    for file in Path("./replace").rglob("*"):
        if file.is_file():
            with open(file, "r") as f:
                content = f.read()
            with open(file, "w") as f:
                f.write(content.replace("IITM", "IIT Madras"))
    return subprocess.getoutput("cat ./replace/* | sha256sum")

def list_large_files(zip_filename, min_size, date):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall("./list")
    total_size = 0
    for file in Path("./list").rglob("*"):
        if file.is_file() and file.stat().st_size >= min_size and datetime.fromtimestamp(file.stat().st_mtime) >= date:
            total_size += file.stat().st_size
    return total_size

def move_and_rename_files(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall("./move")
    for file in Path("./move").rglob("*"):
        if file.is_file():
            new_name = ''.join(str(int(c) + 1) if c.isdigit() else c for c in file.name)
            file.rename(Path("./move") / new_name)
    return subprocess.getoutput("grep . ./move/* | LC_ALL=C sort | sha256sum")

def compare_files(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall("./compare")
    return sum(1 for a, b in zip(open("./compare/a.txt"), open("./compare/b.txt")) if a != b)

def sql_ticket_sales(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT SUM(units * price) FROM tickets WHERE LOWER(type) = 'gold'"
    result = conn.execute(query).fetchone()[0]
    conn.close()
    return result

def find_git_repo_size(repo_path):
    return subprocess.getoutput(f"du -sh {repo_path}")

def check_file_integrity(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def extract_all_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=" ").strip()
