from ga.auth import initialize_analyticsreporting


def get_report(webmaster_service,  VIEW_ID, start_date, end_date, ):
    return webmaster_service.reports().batchGet(
        body={
            'reportRequests': [{
                'viewId': VIEW_ID,
                'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                'metrics': [{'expression': 'ga:sessions'}],
                'dimensions': [{'name': 'ga:pagePath'}],
            }]
        }).execute()


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
    response = get_report(analytics, '168176938', '2020-10-12', '2020-10-12')
    print_response(response)


if __name__ == '__main__':
    main()
