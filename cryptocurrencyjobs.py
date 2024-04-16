import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Telegram Bot settings
TELEGRAM_BOT_TOKEN = #Your telegram bot ID
TELEGRAM_CHAT_ID = #Your telegram chat ID

def send_telegram_message(message):
    """Sends message via Telegram"""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)

def format_job_message(job):
    """Formats the message to send via Telegram"""
    return (
        f"🚨 *NEW JOB ALERT* 🚨\n"
        f"Job Title: *{job['Job Title']}*\n"
        f"Company: *{job['Company']}*\n"
        f"Location: *{job['Location']}*\n"
        f"Categories: *{job['Categories']}*\n"
        f"Job Type: *{job['Job Type']}*\n"
        f"[Read more]({job['Link']})"
    )

def fetch_prose_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if 'charset' in response.headers.get('Content-Type', ''):
                response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            prose_content = soup.find('div', class_='prose')
            return prose_content.get_text(strip=True) if prose_content else "No prose content"
        else:
            return "Failed to fetch page"
    except Exception as e:
        return f"Error: {str(e)}"

def fetch_jobs():
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('li', class_='grid')

        job_titles, company_names, locations, categories, job_types, links, prose_texts = ([] for i in range(7))

        for listing in job_listings:
            job_title_tag = listing.find('h2')
            job_title = job_title_tag.get_text(strip=True) if job_title_tag and job_title_tag.find('a') else "No job title"
            job_link = base_url + job_title_tag.find('a')['href'] if job_title_tag and job_title_tag.find('a') else "No link available"

            job_titles.append(job_title)
            links.append(job_link)

            company_name_tag = listing.find('h3')
            company_names.append(company_name_tag.get_text(strip=True) if company_name_tag else "No company name")

            location_tag = listing.find('h4', string=lambda x: x and ('Remote' in x or 'Location' in x))
            locations.append(location_tag.get_text(strip=True) if location_tag else "No location")

            category_tags = listing.find_all('h4')
            extracted_categories, extracted_types = [], []
            for category_tag in category_tags:
                for link_tag in category_tag.find_all('a'):
                    text, href = link_tag.get_text(strip=True), link_tag['href']
                    if 'full-time' in href or 'non-tech' in href:
                        extracted_types.append(text)
                    else:
                        extracted_categories.append(text)

            categories.append(", ".join(set(extracted_categories)) if extracted_categories else "No categories")
            job_types.append(", ".join(set(extracted_types)) if extracted_types else "No job types")

        prose_texts = [fetch_prose_text(link) for link in links]

        return pd.DataFrame({
            'Job Title': job_titles,
            'Company': company_names,
            'Location': locations,
            'Categories': categories,
            'Job Type': job_types,
            'Link': links,
            'Prose': prose_texts
        })
    else:
        print(f"Failed to fetch the webpage: Status code {response.status_code}")
        return pd.DataFrame()

def check_for_new_jobs(prev_df):
    current_df = fetch_jobs()
    if not prev_df.empty:
        # Compare DataFrames and find new jobs
        new_jobs = current_df[~current_df['Link'].isin(prev_df['Link'])]
        return new_jobs
    return current_df

# Base URL of the website
base_url = "https://cryptocurrencyjobs.co"

prev_df = pd.DataFrame()

# Example loop that runs until manually stopped, checking for new jobs
while True:
    new_jobs = check_for_new_jobs(prev_df)
    if not new_jobs.empty:
        print("New job listings found:")
        for _, job in new_jobs.iterrows():
            message = format_job_message(job)
            print(message)
            send_telegram_message(message)
    else:
        print("No new job listings found.")

    prev_df = new_jobs if not new_jobs.empty else prev_df
    time.sleep(300)  # Delay for 1 hour (3600 seconds)
