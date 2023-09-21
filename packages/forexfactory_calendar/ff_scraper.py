import sys
import bs4
import numpy as np
import pandas as pd


def parse_forexfactory_page(response, logger):
    '''
    Parses raw html from ForexFactory.com/calendar. Returns bs4 object containing calendar table information.
    '''
    try:
        soup = bs4.BeautifulSoup(response.content)
        table = soup.find('table', class_='calendar__table')
        rows_raw = table.find_all('tr')
        
        # Removing unnecessary rows.
        rows = [row for row in rows_raw if not isinstance(row, bs4.element.NavigableString) and row['class'][0] == 'calendar__row']
        
        logger.info(f'Forex Factory calendar page parsed successfully.')    
        return rows
        
    except Exception as initial_parsing_error:
        logger.error(f'Error parsing Forex Factory calendar table. Error: {str(initial_parsing_error)}')
        sys.exit()


def parse_forexfactory_calendar(raw_calendar, logger):
    '''
    Parses previously fetched data and creates pandas dataframe
    '''
    
    element_errors = []
    table_data = []

    # Iterate over each row element getting the text. Appends to a list at the end of every loop.
    for indx, row in enumerate(raw_calendar):#self._rows):
        
        # Date
        try:
            date = row.find('td' , class_='calendar__cell calendar__date').text.strip()
        except AttributeError:
            date = None
        except Exception as element_error:
            element_errors.append([indx, 'date'])

        # Time
        try:
            time = row.find('td' , class_='calendar__cell calendar__time').text.strip()
        except AttributeError:
            time = None
        except Exception as element_error:
            element_errors.append([indx, 'time'])

        # Currency
        try:
            currency = row.find('td' , class_='calendar__cell calendar__currency').text.strip()
        except AttributeError:
            currency = None
        except Exception as element_error:
            element_errors.append([indx, 'currency'])

        # Impact
        try:
            impact_color = row.find('td' , class_='calendar__cell calendar__impact').find('span')['class'][1].split('-')[-1]
            
            if impact_color == 'ora':
                impact = 'Medium'
            elif impact_color == 'yel':
                impact = 'Low'
            elif impact_color == 'red':
                impact = 'High'
            elif impact_color == 'gra':
                impact = 'Non-Economic'
                
        except AttributeError:
            impact = None
        except Exception as element_error:
            element_errors.append([indx, 'impact'])

        # Event
        try:
            event = row.find('span' , class_='calendar__event-title').text.strip()
        except AttributeError:
            event = None
        except Exception as element_error:
            element_errors.append([indx, 'event'])

        # Actual Value
        try:
            actual_val = row.find('td' , class_='calendar__cell calendar__actual').text.strip()
        except AttributeError:
            actual_val = None
        except Exception as element_error:
            element_errors.append([indx, 'actual_val'])

        # Actual Status
        try:
            actual_status = row.find('td' , class_='calendar__cell calendar__actual').span['class']
            
            if len(actual_status) > 0:
                actual_status = actual_status[0]
            else:
                actual_status = 'same'
                
        except AttributeError:
            actual_status = None
        except TypeError:
            actual_status = None
        except Exception as element_error:
            element_errors.append([indx, 'actual_st'])

        # Forecast
        try:
            forecast = row.find('td' , class_='calendar__cell calendar__forecast').text.strip()
        except AttributeError:
            forecast = None
        except Exception as element_error:
            element_errors.append([indx, 'forecast'])

        # Previous
        try:
            previous = row.find('td' , class_='calendar__cell calendar__previous').text.strip()
        except AttributeError:
            previous = None
        except Exception as element_error:
            element_errors.append([indx, 'previous'])

        # Appending new row to list of rows
        table_data.append([date, time, currency, impact, event, actual_val, actual_status, forecast, previous])
    
    cols = ['event_date', 'event_time', 'currency', 'impact', 'event', 
            'actual_val', 'actual_status', 'forecast', 'previous']
    df = pd.DataFrame(data=table_data, columns=cols)
        
    # Checking whether the number of rows in the html is the same in the table.
    try:
        assert len(raw_calendar) == len(table_data)
        logger.info(f'Records found: {len(table_data)-1}.')
    except AssertionError as parsing_error:
        logger.error(f'Parsing Error: Parsed data has {len(raw_calendar)-1} rows, table has {len(table_data)-1}.')

    # Checking all elements were parsed correctly.
    try:
        assert len(element_errors) == 0
        logger.info(f'Forex Factory calendar table parsed successfully.')
    except AssertionError as data_mismatch:
        for err in element_errors:
            logger.error(f'Data mismatch: {element_errors[0]}, {element_errors[1]}')
            
    return df
