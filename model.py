#model.py
import secrets
import sqlite3 as sqlite
DBNAME = 'housing.db'
import plotly.plotly as py
import plotly
MAPBOX_TOKEN = secrets.MAPBOX_TOKEN


def init_housing():
    global housing

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
    return base_statement


def get_housing(sortby="name", sortorder="desc", bed="", bath="", buildingtype="", pet="", parking=""):
    global housing

    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    filter_list = []

    if bed == "Studio":
        filter_list.append('h.bed="{}"'.format(bed))
    elif bed != "":
        filter_list.append('h.bed={} '.format(bed))
    
    if bath != "":
        filter_list.append('h.bath={} '.format(bath))

    if buildingtype != "":
        filter_list.append('h.buildingtypeid={} '.format(buildingtype))

    if pet != "":
        filter_list.append('h.petpolicyid={} '.format(pet))

    if parking != "":
        filter_list.append('h.parkingid={} '.format(parking))

    if sortby == 'name':
        order_statement = "ORDER BY h.housing "

    else:
        order_statement = "ORDER BY h.rent "

    if sortorder == "asc":
        order_statement += "ASC"
    else:
        order_statement += "DESC"

    if len(filter_list) != 0:
        filter_statement = 'Where '
        if len(filter_list) == 1:
            filter_statement += filter_list[0]

        if len(filter_list) > 1:
            filter_statement += 'and '.join(filter_list)
    else:
        filter_statement = ""

    try:
        final_statement = init_housing()+''+filter_statement+''+order_statement
    except:
        final_statement = init_housing()+''+order_statement

    print(final_statement)
    housing = cur.execute(final_statement).fetchall()

    return housing



lat_vals = []
lon_vals = []
text_vals = []

def maponplotly():

    if housing:
        for h in housing:
            lat_vals.append(h[10])
            lon_vals.append(h[11])
            text_vals.append(h[0]+"\n"+h[1])

        max_lat = max(lat_vals)
        min_lat = min(lat_vals)
        max_lon = max(lon_vals)
        min_lon = min(lon_vals)

        center_lat = (max_lat+min_lat) / 2
        center_lon = (max_lon+min_lon) / 2

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
                        lon=center_lon,
                        lat=center_lat
                    ),
                    pitch=0,
                    zoom=12,
                ),
            )

        fig = dict( data=data, layout=layout )
        div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True)

        return div

