import pandas as pd
import json
import gzip
import re
import duckdb
from collections import defaultdict
from rapidfuzz import process, fuzz  # For city name clustering
from PIL import Image
import numpy as np

def clean_excel_and_compute_margin(file_path, date_filter, product_filter, country_filter):
    df = duckdb.read_csv(file_path)
    df = df.rename(columns=lambda x: x.strip())
    df['Country'] = df['Country'].str.strip().replace({"USA": "US", "U.S.A": "US"})
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Product'] = df['Product'].str.split('/').str[0].str.strip()
    df['Sales'] = df['Sales'].str.replace('USD', '').str.strip().astype(float)
    df['Cost'] = df['Cost'].replace('', None).astype(float).fillna(df['Sales'] * 0.5)
    
    filtered_df = df[(df['Date'] <= date_filter) & (df['Product'] == product_filter) & (df['Country'] == country_filter)]
    total_sales, total_cost = filtered_df['Sales'].sum(), filtered_df['Cost'].sum()
    total_margin = (total_sales - total_cost) / total_sales if total_sales else 0
    return total_margin

def count_unique_student_ids(file_path):
    with open(file_path, 'r') as f:
        student_ids = {line.strip().split()[0] for line in f}
    return len(student_ids)

def count_successful_get_requests(log_file):
    with gzip.open(log_file, 'rt') as f:
        pattern = re.compile(r'\[(\d{2})/May/2024:(\d{2}):')
        count = sum(1 for line in f if "GET /tamilmp3/" in line and pattern.search(line) and 10 <= int(pattern.search(line).group(2)) < 15)
    return count

def find_top_data_consumer(log_file):
    ip_data = defaultdict(int)
    with gzip.open(log_file, 'rt') as f:
        for line in f:
            if "GET /malayalammp3/" in line and "15/May/2024" in line:
                parts = line.split()
                ip, size = parts[0], int(parts[-4]) if parts[-4].isdigit() else 0
                ip_data[ip] += size
    return max(ip_data.items(), key=lambda x: x[1], default=(None, 0))

def aggregate_sales_by_city(file_path):
    df = duckdb.read_csv(file_path)
    df = df[df['Product'] == 'Mouse']
    df = df[df['Units'] >= 77]
    cities = df['City'].tolist()
    unique_cities = set(cities)
    mapping = {city: process.extractOne(city, unique_cities, scorer=fuzz.ratio)[0] for city in unique_cities}
    df['City'] = df['City'].map(mapping)
    return df.groupby('City')['Units'].sum().to_dict()

def sum_sales_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return sum(row.get('Sales', 0) for row in data)

def count_oi_occurrences(json_file):
    def recursive_count(data):
        if isinstance(data, dict):
            return sum((1 if k == 'OI' else 0) + recursive_count(v) for k, v in data.items())
        elif isinstance(data, list):
            return sum(recursive_count(item) for item in data)
        return 0
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    return recursive_count(data)

def reconstruct_scrambled_image(image_file, mapping_file):
    original = Image.open(image_file)
    mapping = duckdb.read_csv(mapping_file)
    pieces = [original.crop((c*100, r*100, (c+1)*100, (r+1)*100)) for r in range(5) for c in range(5)]
    reassembled = Image.new('RGB', (500, 500))
    for _, row in mapping.iterrows():
        reassembled.paste(pieces[row['Scrambled Row']*5 + row['Scrambled Column']], (row['Original Column']*100, row['Original Row']*100))
    reassembled.save('reconstructed.png')

def calculate_average_temperature(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    temperatures = [entry['temperature'] for entry in data if 'temperature' in entry]
    return sum(temperatures) / len(temperatures) if temperatures else None

def extract_emails_from_text(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return set(emails)