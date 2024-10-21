import sys
from tabula import read_pdf
import pandas as pd
import numpy as np

columns = ['Flight number', 'Departure', 'Arrival', 'Departure date', 'Arrival date', 'Departure time', 'Arrival time', 'Change time zone', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Aircraft type', 'Flight time']

def add_code(table, from_code, to_code) :
    dep = pd.Series(data=from_code, index=np.arange(table.shape[0]),
                    name='Departure_code')
    arr = pd.Series(data=to_code, index=np.arange(table.shape[0]),
                    name='Arrival_code')

    table.index = [i for i in range(table.shape[0])]
    table.insert(0, column='Departure', value=dep)
    table.insert(1, column='Arrival', value=arr)

    return table

def main(pdf_path, pages, file_name):
    df_temp = read_pdf(pdf_path, area=(50, 50, 100, 290), pages=pages)
    df_table_without_cell = read_pdf(pdf_path, area=[(50, 15, 810, 300)], pages=pages, pandas_options={'header': None}, columns=[80, 115, 140, 180, 220, 250])
    #df_temp = read_pdf(pdf_path, area=(50, 340, 100, 580), pages=pages, stream=True)
    #df_table_without_cell = read_pdf(pdf_path, area=[(50, 305, 810, 580)], pages=pages, pandas_options={'header': None}, columns=[370, 405, 430, 470, 510, 540])

    print(len(df_table_without_cell), len(df_temp))
    resPD = pd.DataFrame(columns = ['Departure', 'Arrival'] + [i for i in range(7)])
    town_dict = {
        'from_country': "",
        'from_city': "",
        'from_code': "",
        'to_country': "",
        'to_city': "",
        'to_code': ""
    }

    for i in range(len(df_temp)):
        if df_temp[i].keys().shape[0] == 2:

            df = pd.DataFrame(df_temp[i])
            text = df.keys()[0]
            word_list = text.partition(',')
            if len(word_list) == 3:
                town_dict['from_city'] = word_list[0].strip()
                town_dict['from_country'] = word_list[2].strip()
                town_dict['from_code'] = df.keys()[1].strip()

            text = df.iloc[0, 0]
            word_list = text.partition(',')
            if len(word_list) == 3:
                town_dict['to_city'] = word_list[0].strip()
                town_dict['to_country'] = word_list[2].strip()
                town_dict['to_code'] = df.iloc[0, 1].strip()

            df_table_without_cell[i] = df_table_without_cell[i].drop(index=[0, 1, 2, 3]).dropna()
            if df_table_without_cell[i].shape[0] > 0:
                resPD = pd.concat([resPD, add_code(df_table_without_cell[i], town_dict['from_code'], town_dict['to_code'])], ignore_index=True, axis=0)
        else:
            df_table_without_cell[i] = df_table_without_cell[i].dropna()
            if df_table_without_cell[i].shape[0] > 0 :
                resPD = pd.concat(
                    [resPD, add_code(df_table_without_cell[i], town_dict['from_code'], town_dict['to_code'])], ignore_index=True, axis=0)

    resPD.to_csv(file_name)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])