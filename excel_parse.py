import  pandas as pd
import os

list = os.listdir('excel_files/')

boarding_pass_columns = [
    'Flight',
    'Name',
    'Sex',
    'Departure',
    'Arrival',
    'Date',
    'Time',
    'PNR',  # код бронирования
    'ETicket',
    'LP',  # Программа лояльности
    'LP Number',
    'Class'
]


pass_ser = pd.Series(index=boarding_pass_columns, dtype=object)

for path in list:
    boarding_pass_table = pd.DataFrame(columns=boarding_pass_columns)
    df = pd.read_excel('excel_files/' + path, sheet_name=None, header=None, usecols='A:H', nrows=13)
    print(path)
    for bp in df:
        pass_ser['Flight'] = df[bp].iloc[4][0]
        pass_ser['Name'] = df[bp].iloc[2][1]
        pass_ser['Sex'] = df[bp].iloc[2][1]
        pass_ser['Departure'] = df[bp].iloc[6][3]
        pass_ser['Arrival'] = df[bp].iloc[6][7]
        pass_ser['Date'] = df[bp].iloc[8][0]
        pass_ser['Time'] = df[bp].iloc[8][2]
        pass_ser['PNR'] = df[bp].iloc[12][1]
        pass_ser['ETicket'] = df[bp].iloc[12][4]
        pass_ser['Class'] = df[bp].iloc[2][7]

        if str(df[bp].iloc[2][5]) == 'nan' :
            pass_ser['LP'] = None
            pass_ser['LP Number'] = 0
        else :
            lp = df[bp].iloc[2][5].split()
            pass_ser['LP'] = lp[0]
            pass_ser['LP Number'] = lp[1]
        boarding_pass_table.loc[len(boarding_pass_table)] = pass_ser

    boarding_pass_table.to_csv('excel_csv/' + path[:-5] + '.csv', index=False)