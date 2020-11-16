import pandas as pd
from gsc.gsc_without_filter import gsc_query
from gsc.auth import authorize_creds


site = "https://www.renee.pl"
date_range1 = "2020-09-28:2020-10-04"
date_range2 = "2020-11-02:2020-11-08"

webmaster_service = authorize_creds()


def generate_gsc_report(webmaster_service, domain, d_range1, d_range2, file_path):
    d_range1_splitted = d_range1.split(":")
    d_range2_splitted = d_range2.split(":")

    args = webmaster_service, domain, d_range1_splitted[0], d_range1_splitted[1]
    args2 = webmaster_service, domain, d_range2_splitted[0], d_range2_splitted[1]

    # wczytanie 2 tabel z różnymi zakresami dat
    df1 = gsc_query(*args, rowLimit=2000)
    df2 = gsc_query(*args2, rowLimit=2000)

    # czyszczenie tabel z niepotrzebnych kolumn i ustawianie indeksu na query
    # df1.drop(columns='Unnamed: 0', inplace=True)
    df1.set_index('query', inplace=True)
    df1.rename(columns={"clicks": f"clicks {d_range1}", "ctr": f"ctr {d_range1}",
                        "impressions": f"impressions {d_range1}",
                        "position": f"position {d_range1}", }, inplace=True)

    # df2.drop(columns='Unnamed: 0', inplace=True)
    df2.set_index('query', inplace=True)
    df2.rename(columns={"clicks": f"clicks {d_range2}", "ctr": f"ctr {d_range2}",
                        "impressions": f"impressions {d_range2}",
                        "position": f"position {d_range2}", }, inplace=True)
    # połączenie tabel
    df3 = pd.merge(df1, df2, on='query')

    # zapisanie tabel wynikowych do excela
    with pd.ExcelWriter(file_path) as writer:
        df3.to_excel(writer, sheet_name='Tabela zbiorcza')
        df3[df3[f"position {d_range1}"] >= df3[f"position {d_range2}"]].to_excel(writer, sheet_name='Wzrosty')
        df3[(df3[f"position {d_range1}"] > 3) & (df3[f"position {d_range2}"] <= 3)].\
            to_excel(writer, sheet_name='Nowe w TOP3')
        df3[(df3[f"position {d_range1}"] > 10) & (df3[f"position {d_range2}"] <= 10)].\
            to_excel(writer, sheet_name='Nowe w TOP10')
        df3[df3[f"position {d_range1}"] < df3[f"position {d_range2}"]].to_excel(writer, sheet_name='Spadki')
        df3[(df3[f"position {d_range1}"] <= 3) & (df3[f"position {d_range2}"] > 3)].\
            to_excel(writer, sheet_name='Wypadło z TOP3')
        df3[(df3[f"position {d_range1}"] <= 10) & (df3[f"position {d_range2}"] > 10)].\
            to_excel(writer, sheet_name='Wypadło z TOP10')


generate_gsc_report(webmaster_service, "https://medifem.pl", date_range1, date_range2, "Output/medifem_report.xlsx")
