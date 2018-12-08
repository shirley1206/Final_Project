#model.py
import csv
import sqlite3
import sqlite3 as sqlite
DBNAME = 'housing.db'

housing = []


def init_housing():
    global housing
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()

    # option =

    filter_statement = ''

    #
    # if 'sellcountry=' in option:
    #     value = option.split("=")[1]
    #     filter_statement = 'Where c1.Alpha2='
    #     filter_statement += '"{}"'.format(value)
    #
    # elif 'sourcecountry=' in option:
    #     value = option.split("=")[1]
    #     filter_statement = 'Where c2.Alpha2='
    #     filter_statement += '"{}"'.format(value)
    #
    # elif 'sellregion=' in option:
    #     value = option.split("=")[1]
    #     filter_statement = 'Where c1.Region='
    #     filter_statement += '"{}"'.format(value)
    #
    # elif 'sourceregion=' in option:
    #     value = option.split("=")[1]
    #     filter_statement = 'Where c2.Region='
    #     filter_statement += '"{}"'.format(value)
    #
    order_statement = ''
    # if 'cocoa' in words:
    #     order_statement = 'ORDER BY b.CocoaPercent DESC'
    #
    # else:
    #     order_statement = 'ORDER BY b.rating DESC'

    base_statement = '''
    SELECT h.housing, h.address, h.bed, h.bath, b.type, h.rent, h.status, p2.policy, p1.type, h.url 
    from Housing as h
    JOIN BuildingType as b
    on b.ID = h.BuildingTypeId
    JOIN Parking as p1
    on p1.ID = h.ParkingId
    JOIN Pet as p2
    on p2.ID = h.petpolicyid
    '''

    final_statement = base_statement+filter_statement+' '+order_statement
    # print(final_statement)
    housing = cur.execute(final_statement).fetchall()


def get_housing(sortby='bed', sortorder='desc'):

    if sortby == 'bed':
        sortcol = 2
    elif sortby == 'bath':
        sortcol = 3
    elif sortby == 'rent':
        sortcol = 5
    else:
        sortcol = 0

    rev = (sortorder == 'desc')
    sorted_list = sorted(housing, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list



