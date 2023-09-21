import pandas as pd
import numpy as np
import requests
import bs4
import datetime
import pytz

def single_contract(url):
    
    print(f'Fetchig data... {url}')

    symbol = url.split('/')[-1]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'lxml')

    # Close value. Quote
    quote_raw = soup.find('ul', class_='c_crinfo_main')
    quote = quote_raw.find('li', class_='crinfo_quote').select_one("span[id=quote_val]").text

    # Volume and Open Interest
    table_raw = soup.find('ul', class_='cr_data_collection cr_charts_info')

    vals, lbls = [symbol, quote], ['FX Contract', 'Quote']

    for row in table_raw.find_all('li'):
        lbl = row.find('span', class_='data_lbl').text
        val = row.find('span', class_='data_data').text

        lbls.append(lbl)
        vals.append(val)

    df = pd.DataFrame(vals).T
    df.columns = lbls

    return df

def scraper(urls):

    # Fetching data for all contracts, concatenating into one single df
    dfs = [single_contract(url) for url in urls]
    full = pd.concat(dfs).reset_index(drop=True)

    # Fixing data type
    full['Quote'] = full['Quote'].astype('float')
    full['Volume'] = full['Volume'].str.replace(',', '').astype('int')
    full['Open Interest'] = full['Open Interest'].str.replace(',', '').astype('int')

    # Adding Time
    utc_time = datetime.datetime.now(pytz.timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S")
    local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ny_time = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")

    full['UTC'] = utc_time
    full['Local'] = local_time
    full['NY'] = ny_time

    return full

def save_to_csv(df):

    save_time = datetime.datetime.now(pytz.timezone('UTC')).strftime("%Y%m%dT%H%M%SZ")

    file = f'futures_wsj_{save_time}.csv'
    pathfile = f'../../data/futures_contracts_wsj/{file}'

    df.to_csv(pathfile, index=False, sep=';')
    
    print(f'File saved: {pathfile}')

    return None


if __name__ == '__main__':

    print('Futures Contracts WSJ... Initializing')

    urls = ['https://www.wsj.com/market-data/quotes/futures/CL00',
            'https://www.wsj.com/market-data/quotes/futures/GC00',
            'https://www.wsj.com/market-data/quotes/futures/DX00',
            'https://www.wsj.com/market-data/quotes/futures/EC00',
            'https://www.wsj.com/market-data/quotes/futures/BP00',
            'https://www.wsj.com/market-data/quotes/futures/JY00',
            'https://www.wsj.com/market-data/quotes/futures/CD00',
            'https://www.wsj.com/market-data/quotes/futures/AD00',
            'https://www.wsj.com/market-data/quotes/futures/SFC00'
            ]

    df = scraper(urls)
    save_to_csv(df)

    print('Futures Contracts WSJ... Done!')