#model.py
import secrets
import sqlite3 as sqlite
DBNAME = 'housing.db'
import plotly.plotly as py
import plotly
MAPBOX_TOKEN = secrets.MAPBOX_TOKEN


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
    SELECT h.housing, h.address, h.bed, h.bath, b.type, h.rent, h.status, p2.policy, p1.type, h.url, h.lat, h.lon 
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


init_housing()

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

lat_vals = []
lon_vals = []
text_vals = []

def maponplotly():
    global map

    for h in housing:
        # print(h[0])
        lat_vals.append(h[10])
        lon_vals.append(h[11])
        text_vals.append(h[0]+"\n"+h[1])

    data = [ dict(
            type = 'scattermapbox',
            lon = lon_vals,
            lat = lat_vals,
            text = text_vals,
            mode = 'markers',
            marker = dict(
                size = 8,
                symbol = 'star',
            ))]

    layout = dict(
            title = 'Housing on Mapbox<br>(Hover for more details)',
            autosize=True,
            showlegend = False,
            mapbox=dict(
                accesstoken=MAPBOX_TOKEN,
                bearing=0,
                center=dict(
                    lon=lon_vals[0],
                    lat=lat_vals[0]
                ),
                pitch=0,
                zoom=10,
            ),
        )



    fig = dict( data=data, layout=layout )
    div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True)

    return div
