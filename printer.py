import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Function to extract value based on partial text match
def extract_value_by_partial_text(soup, partial_text):
    matching_element = soup.find('td', class_='labelSpsFont', string=lambda s: partial_text in s)
    if matching_element:
        value_element = matching_element.find_next('td', class_='itemSpsFont')
        value = value_element.get_text(strip=True)
        return value
    else:
        return None

# Step 1: Get page source
url = "http://192.168.100.213/hp/device/info_suppliesStatus.html?tab=Home&menu=SupplyStatus"
response = requests.get(url)
page_source = response.text

# Step 2: Extract text using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Extract values
current_datetime = datetime.now()
date_str = current_datetime.strftime("%Y-%m-%d")
time_str = current_datetime.strftime("%H:%M:%S")
pages_printed_with_supply = extract_value_by_partial_text(soup, "Pages Printed With This Supply")

# CSV file path and header
csv_file_path = r'X:\Sumit\print\status.csv'
csv_header = ["date", "time", "pages_printed"]

# Append the information to the CSV file
is_new_file = not os.path.isfile(csv_file_path)
with open(csv_file_path, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    if is_new_file:
        csv_writer.writerow(csv_header)  # Write header only if the file is newly created
    csv_writer.writerow([date_str, time_str, pages_printed_with_supply])

# Print the output to the console
print(f'Date: {date_str} | Time: {time_str} | Pages Printed With This Supply: {pages_printed_with_supply}')
