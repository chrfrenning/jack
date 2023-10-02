import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

def fetch_table_from_page(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table')
        csv_buffer = StringIO(str(table))
        df = pd.read_html(csv_buffer)[0]
        #df = pd.read_html(str(table))[0]
        return df
    except:
        return None

def fetch_all_tables(base_url):
    page_number = 0
    all_dataframes = []
    
    while True:
        url = f"{base_url}?page={page_number}"
        print(f"Fetching page {page_number}...")
        df = fetch_table_from_page(url)
        
        if df is None or df.empty:
            break

        all_dataframes.append(df)
        page_number += 1

    final_df = pd.concat(all_dataframes, ignore_index=True)
    return final_df

if __name__ == '__main__':
    base_url = 'https://www.uio.no/studier/program/informatikk-programmering-master/oppbygging/masteroppgaver/'
    final_df = fetch_all_tables(base_url)
    final_df.to_csv('master_theses.csv', index=False)
