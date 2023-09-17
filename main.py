import logging
import datetime
from packages.common_utils import *
from  packages.ff_scraper import * 


def forexfactory_calendar(logger):
    
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    logging.info('Forex Factory Calendar.')
    
    # Setting main variables
    url = 'https://www.forexfactory.com/calendar?month=last'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    
    # Fetching calendar data
    response = fetch_html(url, headers, logger=logging)
    raw_calendar = parse_forexfactory_page(response, logger=logging)
    
    # Creating calendar table
    df_calendar = parse_forexfactory_calendar(raw_calendar, logger=logging)
    
    # Saving calendar as CSV
    pathfile = f'ff_calendar_{now}.csv'
    save_csv(df_calendar, pathfile, logger=logging)
    
    return df_calendar


if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO, filename='ForexFactory.log', filemode='w', 
                        format='%(asctime)s :: %(name)s :: %(levelname)-8s :: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    ff_cal = forexfactory_calendar(logging)