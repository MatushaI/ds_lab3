import pandas as pd
import os

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

list = os.listdir('excel_csv/')
table = pd.DataFrame(columns=boarding_pass_columns)

for path in list:
    if path.endswith('.DS_Store'): continue
    df = pd.read_csv('excel_csv/' + path)
    table = pd.concat([table, df], ignore_index=True, axis=0)

table.to_csv('YourBoardingPassDotAero.csv')