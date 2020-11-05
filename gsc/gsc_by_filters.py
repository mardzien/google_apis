import pandas as pd

from collections import defaultdict
import datetime
from dateutil import relativedelta

from gsc.auth import authorize_creds, execute_request

today = datetime.datetime.now()
days = relativedelta.relativedelta(days=3)
default_end = today - days


# Run the extraction
def gsc_by_filters(webmasters_service, site, dimension, operator, expression, start_date, end_date, rowLimit=1000):
    scDict = defaultdict(list)  # Create a dict to populate with extraction
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page', 'query'],  # country, device, page, query, searchAppearance
        'dimensionFilterGroups': [{
            'filters': [{
                'dimension': dimension,
                'operator': operator,
                'expression': expression
            }]
        }],
        'aggregationType': 'byPage',
        'rowLimit': rowLimit,
    }
    response = execute_request(webmasters_service, site, request)
    try:
        for row in response['rows']:
            # scDict['date'].append(row['keys'][0] or 0)
            scDict['page'].append(row['keys'][0] or 0)
            scDict['query'].append(row['keys'][1] or 0)
            scDict['clicks'].append(row['clicks'] or 0)
            # scDict['ctr'].append(row['ctr'] or 0)
            # scDict['impressions'].append(row['impressions'] or 0)
            scDict['position'].append(row['position'] or 0)
    except Exception as e:
        print(f'An error occurred: {e}')

    # Add response to dataframe
    df = pd.DataFrame(data=scDict)
    return df
