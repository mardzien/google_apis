import pandas as pd
from pytrends.request import TrendReq
import files

keywords = files.load_file_to_list("keywords.txt")


def get_trends(phrase):
    pytrends = TrendReq(hl='ua-UA', tz=360)
    pytrends.build_payload([phrase], cat=0, timeframe='today 12-m', geo='UA', gprop='')
    return pytrends.interest_over_time()


def get_trends_df():
    df = pd.DataFrame(get_trends(keywords[0]))

    for phrase in keywords[1:]:
        temp_df = get_trends(phrase)
        df = pd.merge(df, temp_df, on=["date", "isPartial"])

    df_transposed = df.T    # or df1.transpose()
    return df_transposed
