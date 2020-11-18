import pandas as pd

from ga.ga_by_filters import initialize_analyticsreporting, get_response, get_report

ID_PROJECT = '168176938'
date_range = "2020-09-01:2020-09-30"
FILTER = ['/ru/tipstricks-ru/', '/ru/trendy-ru/', '/тренди/', '/поради-та-рекомендації/']


def generate_ga_report(id, d_range, filters, file_name):
    d_range_splitted = d_range.split(":")
    analytics = initialize_analyticsreporting()
    dims = ['ga:segment', 'ga:month', 'ga:pagePath']
    metri = ['ga:sessions', 'ga:users', 'ga:pageViews']
    response = get_response(analytics, VIEW_ID=id, start_date=d_range_splitted[0], end_date=d_range_splitted[1],
                            dimensions=dims,
                            metrics=metri,
                            filters=filters)
    df1 = get_report(response, dims, metri).astype({'sessions': 'int64', 'users': 'int64', 'pageViews': 'int64',
                                                    'month': 'int64'})
    dims = ['ga:segment', 'ga:date']
    response = get_response(analytics, VIEW_ID=id, start_date=d_range_splitted[0], end_date=d_range_splitted[1],
                            dimensions=dims,
                            metrics=metri,
                            filters=filters)
    df2 = get_report(response, dims, metri).astype({'sessions': 'int64', 'users': 'int64', 'pageViews': 'int64'})
    df2['date'] = pd.to_datetime(df2['date'], format='%Y%m%d')
    dims = ['ga:segment', 'ga:month']
    response = get_response(analytics, VIEW_ID=id, start_date=d_range_splitted[0], end_date=d_range_splitted[1],
                            dimensions=dims,
                            metrics=metri,
                            filters=filters)
    df3 = get_report(response, dims, metri).astype({'sessions': 'int64', 'users': 'int64', 'pageViews': 'int64',
                                                    'month': 'int64'})

    print(df1.dtypes)
    print(df2.dtypes)
    print(df3.dtypes)

    with pd.ExcelWriter(f"Output/{file_name}.xlsx") as writer:
        df1.to_excel(writer, sheet_name='Miesiąc i URL')
        df2.to_excel(writer, sheet_name='Dni')
        df3.to_excel(writer, sheet_name='Miesiące')


generate_ga_report(ID_PROJECT, date_range, FILTER, "born")
