import pandas as pd
import readline
import re

file = open("Sirena-export-fixed.tab", "r")
file.readline()
num = 0

data_cols = [
    'FullName',
    'BirthDate',
    'DepartDate',
    'DepartTime',
    'ArrivalDate',
    'ArrivalTime',
    'Flight',
    'From',
    'To',
    'E-Ticket',
    'Document',
    'Meal',
    'Class',
    'LoyaltyP',
    'Service'
]

pass_ser = pd.Series(index=data_cols, dtype=object)

reg = re.compile(r'(?P<fullname>[а-яёА-ЯЁ]+\s(?:[а-яёА-ЯЁ])*\s?[а-яёА-ЯЁ]+)\s+(?P<birthdate>\d{4}-\d{2}-\d{2}|N/A)\s+' +
                 r'(?P<departdate>\d{4}-\d{2}-\d{2})\s+(?P<departtime>\d{2}:\d{2})\s+' +
                 r'(?P<arrivaldate>\d{4}-\d{2}-\d{2})\s+(?P<arrivaltime>\d{2}:\d{2})\s+' +
                 r'(?P<flight>\w{6})(?P<sh>YES|NO)\s+(?P<from>[a-zA-Z]{3})\s+(?P<to>[a-zA-Z]{3})\s+' +
                 r'(?P<code>\w{6})(?P<eticket>\d+)\s+(?P<document>\d{4}\s\d{6}|\d{2}\s\d{7})\s+(?:N/A)\s+' +
                 r'(?P<meal>\w{4})?\s+(?P<class>[A-Z])\s+\w{4,10}(?:\s+(?:(?:Travel with infant)|(?:Assistance Required))?[\w#]?\s+' +
                 r'(?:FF#(?P<loyalty>\w{2}\s\d+))?(?:\s+(?P<service>[\w.]{3,}))|\s*)'
                 )

tables = []

while True:
    name = file.readline()
    if not name: break

    if num % 5000 == 0 :
        tables.append(pd.DataFrame(columns=data_cols))

    reg_str = re.search(string=name.strip(), pattern=reg)
    pass_ser['FullName'] = reg_str.group('fullname')
    pass_ser['BirthDate'] = reg_str.group('birthdate')
    pass_ser['DepartDate'] = reg_str.group('departdate')
    pass_ser['DepartTime'] = reg_str.group('departtime')
    pass_ser['ArrivalDate'] = reg_str.group('arrivaldate')
    pass_ser['ArrivalTime'] = reg_str.group('arrivaltime')
    pass_ser['Flight'] = reg_str.group('flight')
    pass_ser['From'] = reg_str.group('from')
    pass_ser['To'] = reg_str.group('to')
    pass_ser['E-Ticket'] = reg_str.group('eticket')
    pass_ser['Document'] = reg_str.group('document')
    pass_ser['Meal'] = reg_str.group('meal')
    pass_ser['Class'] = reg_str.group('class')
    pass_ser['LoyaltyP'] = reg_str.group('loyalty')
    pass_ser['Service'] = reg_str.group('service')

    tables[-1].loc[len(tables[-1])] = pass_ser
    num = num + 1

table = pd.DataFrame(columns=data_cols)
for i in tables :
    table = pd.concat([table, i], axis=0, ignore_index=True)

table.to_csv("Sirena-export-fixed.csv")

file.close()