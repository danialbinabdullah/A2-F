from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import threading
import random
import time
import csv
import re
import urllib.request
import xml.etree.ElementTree as ET
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup as bs

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_articles(dir, website):
    try:
        if website == 'BBC':
            tree = ET.parse(source=urllib.request.urlopen('http://feeds.bbci.co.uk/news/'+dir+'/rss.xml'))
        else:
            return None
    except HTTPError as err:
        print(err)
        return None
    except ET.ParseError as err:
        return None
    else:
        root = tree.getroot()
        all_articles = []
        for item in root.iter('item'):
            article = {}
            for elem in item:
                if elem.tag == 'title':
                    article['title'] = elem.text.strip()
                elif elem.tag == 'link':
                    article['link'] = elem.text.strip()
                elif elem.tag == 'description':
                    article['description'] = elem.text.strip()
                elif elem.tag == 'pubDate':
                    article['pubDate'] = elem.text.strip()
                elif website == 'BBC' and elem.tag.endswith('creator'):
                    article['author'] = elem.text.strip()
            all_articles.append(article)
        return all_articles

def extract_data(url):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    articles = soup.find_all('article')
    article_data = []
    for idx, article in enumerate(articles):
        title = article.find('h2').text.strip() if article.find('h2') else None
        description = article.find('p', class_='story__excerpt').text.strip() if article.find('p', class_='story__excerpt') else None
        time = article.find('time').text.strip() if article.find('time') else None
        article_data.append({'id': idx+1, 'title': title, 'description': description, 'time': time, 'source': url})

    return article_data

def preprocess(text):
    clean_text = re.sub('<.*?>', '', text)
    clean_text = re.sub('[^a-zA-Z]', ' ', clean_text)
    clean_text = clean_text.lower()
    clean_text = re.sub(' +', ' ', clean_text)
    return clean_text

def clean_data(data):
    cleaned_data = []
    for article in data:
        article['title'] = preprocess(article['title']) if article.get('title') else None
        article['description'] = preprocess(article['description']) if article.get('description') else None
        cleaned_data.append(article)
    return cleaned_data

def save_to_csv(file_name, articles):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'description', 'time', 'source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

def write_csv(article_list, dir, invalid, website, curr_date):
    if invalid:
        with open('errorLog.csv', 'a', encoding="utf-8") as file:
            fields = ['date', 'website', 'dir', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')

            for article in article_list:
                writeObj.writerow({
                    'date': curr_date,
                    'website': website,
                    'dir': dir,
                    'articleTitle': article['title'],
                    'author': article.get('author', ''),
                    'description': article.get('description', ''),
                    'pubDate': article.get('pubDate', '')
                })
    else:
        if website == 'BBC':
            with open('BBCinfoXML.csv', 'a', encoding="utf-8") as file:
                fields = ['date', 'dir', 'articleTitle', 'author', 'description', 'pubDate']
                writeObj = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')

                for article in article_list:
                    writeObj.writerow({
                        'date': curr_date,
                        'dir': dir,
                        'articleTitle': article['title'],
                        'author': article.get('author', ''),
                        'description': article.get('description', ''),
                        'pubDate': article.get('pubDate', '')
                    })

def scrape(dir, website, curr_date):
    all_articles = get_articles(dir, website)
    if all_articles is not None:
        write_csv(all_articles, dir, 0, website, curr_date)
        print('Downloaded articles from section: {} - {}'.format(website, dir))
    else:
        bad_scrape_msg = 'Error could not scrape from section: {}'.format(dir)
        bad_scrape = []
        bad_scrape.append(bad_scrape_msg)
        write_csv(bad_scrape, dir, 1, website, curr_date)
        print('############ Failed to download articles from section: {} ############ '.format(dir))

def bbc_control():
    curr_date = '{}/{}/{}'.format(datetime.now().day, datetime.now().month, datetime.now().year)
    for target in BBCArticleURLs:
        scrape(target, 'BBC', curr_date)
        time.sleep(random.random())

def transform(dawn_file, bbc_file, output_file):
    combined_data = []
    dawn_id = 0
    bbc_id = 0
    
    # Read data from dawn.csv
    with open(dawn_file, 'r', newline='', encoding='utf-8') as dawn_csv:
        dawn_reader = csv.DictReader(dawn_csv)
        for row in dawn_reader:
            dawn_id += 1
            combined_data.append({'Id': dawn_id, 'title': row['title'], 'source': 'Dawn'})

    # Read data from BBCinfoXML.csv
    with open(bbc_file, 'r', newline='', encoding='utf-8') as bbc_csv:
        bbc_reader = csv.reader(bbc_csv)
        for row in bbc_reader:
            if row:
                bbc_id += 1
                combined_data.append({'Id': dawn_id + bbc_id, 'title': row[2], 'source': 'BBC'})

    # Write the combined data to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        fieldnames = ['Id', 'title', 'source']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)

def main():
    urls = ['https://www.dawn.com/', 'https://www.bbc.com/']
    filename = "dawn.csv"

    all_data = []
    for url in urls:
        articles = extract_data(url)
        all_data.extend(articles)

    cleaned_data = clean_data(all_data)
    save_to_csv(filename, cleaned_data)
    threading.Thread(target=bbc_control).start()

dag = DAG(
    'news_scraper',
    default_args=default_args,
    description='A DAG to scrape news articles from Dawn and BBC',
    schedule_interval=timedelta(days=1),
)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=main,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id='preprocess_task',
    python_callable=preprocess,
    provide_context=True,
    dag=dag,
)

save_task = PythonOperator(
    task_id='save_task',
    python_callable=save_to_csv,
    provide_context=True,
    dag=dag,
)

dvc_push_task = PythonOperator(
    task_id='dvc_push_task',
    python_callable=transform,
    provide_context=True,
    dag=dag,
)

git_push_task = PythonOperator(
    task_id='git_push_task',
    python_callable=transform,
    provide_context=True,
    dag=dag,
)

extract_task >> preprocess_task >> save_task >> dvc_push_task >> git_push_task
