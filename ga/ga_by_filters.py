import pandas as pd
from ga.auth import initialize_analyticsreporting


DIMS = ['ga:pagePath']
METRI = ['ga:sessions', 'ga:users', 'ga:pageViews']


def get_response(webmaster_service,  VIEW_ID, start_date, end_date, dimensions, metrics):
    return webmaster_service.reports().batchGet(
        body={
            'reportRequests': [{
                'viewId': VIEW_ID,
                'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                'metrics': [{'expression': exp} for exp in metrics],
                'dimensions': [{'name': name} for name in dimensions],
            }]
        }).execute()


def get_report(response, dimensions, metrics):
    data_dic = {f"{i}": [] for i in dimensions + metrics}
    for report in response.get('reports', []):
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            for i, key in enumerate(dimensions):
                data_dic[key].append(row.get('dimensions', [])[i])  # Get dimensions
            dateRangeValues = row.get('metrics', [])
            for values in dateRangeValues:
                all_values = values.get('values', [])  # Get metric values
                for i, key in enumerate(metrics):
                    data_dic[key].append(all_values[i])

    df = pd.DataFrame(data=data_dic)
    df.columns = [col.split(':')[-1] for col in df.columns]
    return df


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
    response: An Analytics Reporting API V4 response.
    """

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ', dimension)

            for i, values in enumerate(dateRangeValues):
                print('Date range:', str(i))
            for metricHeader, value in zip(metricHeaders, values.get('values')):
                print(metricHeader.get('name') + ':', value)


def main():
    analytics = initialize_analyticsreporting()
    response = get_response(analytics, '168176938', '2020-10-12', '2020-10-12', DIMS, METRI)
    df = get_report(response, DIMS, METRI)
    df.to_excel("Output/asd.xlsx")


if __name__ == '__main__':
    main()
