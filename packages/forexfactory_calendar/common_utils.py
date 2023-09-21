import logging
import sys
import requests

def fetch_html(url, headers, logger):
    '''
    Sends request message to url and returns raw html.
    '''
    try:
        resp = requests.get(url, headers=headers)
        assert resp.status_code == 200
        
        logging.info(f'{url}. Connection established.')
        
        return resp
        
    except Exception as get_error:
        logger.error(f'URL: {url}, Connection error: {str(get_error)}')
        sys.exit()


def save_csv(df, pathfile, logger):
    '''
    Save CSV file
    '''
    
    try: 
        df.to_csv(pathfile, sep=';', index=False)
        logger.info(f'CSV file saved: {pathfile}.')
        
    except Exception as csv_save_error:
        logger.error(f'CSV saving error: {str(csv_save_error)}')
        sys.exit()