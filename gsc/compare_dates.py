import pandas as pd
from gsc.gsc_without_filter import gsc_query
from gsc.auth import authorize_creds


site = "https://medjol.pl"
start_date = "2020-08-01"
end_date = "2020-09-01"

start_date2 = "2020-09-01"
end_date2 = "2020-10-01"

webmaster_service = authorize_creds()
# dimension = 'query'
# operator = 'notEquals'   # contains, equals, notEquals, notContains
# expression = 'python'   # whatever value that you want


args = webmaster_service, site, start_date, end_date
args2 = webmaster_service, site, start_date2, end_date2

# wczytanie 2 tabel z różnymi zakresami dat
df1 = gsc_query(*args, rowLimit=1000)
df2 = gsc_query(*args2, rowLimit=1000)

# czyszczenie tabel z niepotrzebnych kolumn i ustawianie indeksu na query
#df1.drop(columns='Unnamed: 0', inplace=True)
df1.set_index('query', inplace=True)

#df2.drop(columns='Unnamed: 0', inplace=True)
df2.set_index('query', inplace=True)

# połączenie tabel
df3 = pd.merge(df1, df2, on='query')

# zapisanie tabel wynikowych do excela
with pd.ExcelWriter('output.xlsx') as writer:
    df3.to_excel(writer, sheet_name='Tabela zbiorcza')
    df3[df3['position_x'] >= df3['position_y']].to_excel(writer, sheet_name='Wzrosty')
    df3[(df3['position_x'] > 3) & (df3['position_y'] <= 3)].to_excel(writer, sheet_name='Nowe w TOP3')
    df3[(df3['position_x'] > 10) & (df3['position_y'] <= 10)].to_excel(writer, sheet_name='Nowe w TOP10')
    df3[df3['position_x'] < df3['position_y']].to_excel(writer, sheet_name='Spadki')
    df3[(df3['position_x'] <= 3) & (df3['position_y'] > 3)].to_excel(writer, sheet_name='Wypadło z TOP3')
    df3[(df3['position_x'] <= 10) & (df3['position_y'] > 10)].to_excel(writer, sheet_name='Wydadło z TOP10')
