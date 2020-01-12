# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
from bs4 import BeautifulSoup
import csv
base_url = "https://www.nriol.com/health/calorie-chart.asp"

def get_data(url):
    response = requests.get(url)
    
    html_soup = BeautifulSoup(response.content, 'lxml')
    tables = html_soup.find_all("table")
    table = tables[0]
    raw_trs = table.find_all("tr")
    clean_trs = raw_trs[1:50]
    raw_columns, raw_rows = clean_trs[0], clean_trs[1:]
    columns =[td.text for td in raw_columns.find_all('td')]
    rows =[[td.text for td in row.find_all('td')] for row in raw_rows]
    rows =[row for row in rows if row.__len__()>1]
    return columns, rows

def get_dict(**datas):
    columns = datas.get('columns')
    rows = datas.get('rows')
    return [dict(zip(columns, row)) for row in rows]

def write_to_csv(filename, datas):
    with open(filename, 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas)
        
columns,rows =get_data(base_url)
datas = get_dict(columns=columns, rows=rows)
write_to_csv("food.csv", datas)


# %%



# %%


