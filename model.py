#model.py
import secrets
import sqlite3 as sqlite
DBNAME = 'housing.db'
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
MAPBOX_TOKEN = secrets.MAPBOX_TOKEN


def init_housing():

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


def get_housing(sortby="name", sortorder="desc", bed="", bath="", buildingtype="", pet="", parking="", search="", status=""):
    global housing

    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    filter_list = []
    search_list = []

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

    if status == "Available":
        filter_list.append("h.status LIKE '%{}%'".format("Available Now"))

    if sortby == 'name':
        order_statement = "ORDER BY h.housing "

    else:
        order_statement = "ORDER BY h.rent "

    if sortorder == "asc":
        order_statement += "ASC"
    else:
        order_statement += "DESC"

    if search != "":
        search_list.append("h.housing LIKE '%{}%'".format(search))
        search_list.append("h.address LIKE '%{}%'".format(search))

    if len(filter_list) != 0:
        filter_statement = 'Where '
        if len(filter_list) == 1:
            filter_statement += filter_list[0]

        if len(filter_list) > 1:
            filter_statement += 'and '.join(filter_list)

    elif len(search_list) != 0:
        filter_statement = 'Where '
        if len(search_list) == 1:
            filter_statement += search_list[0]

        if len(search_list) > 1:
            filter_statement += 'or '.join(search_list)
    else:
        filter_statement = ""

    final_statement = init_housing()+''+filter_statement+''+order_statement

    # print(final_statement)
    # print(filter_list)
    # print(search_list)
    housing = cur.execute(final_statement).fetchall()


    # print(housing)

    return housing


def maponplotly(result):

    if len(result) > 0:

        lat_vals = []
        lon_vals = []
        text_vals = []

        for h in result:
            lat_vals.append(h[10])
            lon_vals.append(h[11])
            text_vals.append(h[0]+"</br>"+h[1]+"</br>"+'$'+str(h[5]))

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
                    zoom=10,
                ),
            )

        fig = dict( data=data, layout=layout )
        div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True)

        return div


def graph(result):

    Apartment_num = 0
    House_num = 0
    Townhouse_num = 0
    Room_num = 0
    Duplex_num=0

    for h in result:

        if h[4] == "Apartment":
            Apartment_num = Apartment_num+1

        if h[4] == "House":
            House_num = House_num+1

        if h[4] == "Townhouse":
            Townhouse_num = Townhouse_num+1

        if h[4] == "Duplex":
            Duplex_num = Duplex_num+1

        if h[4] == "Room":
            Room_num = Room_num+1

    labels = ['Apartment','House','Townhouse','Duplex','Room']
    values = [Apartment_num,House_num,Townhouse_num, Duplex_num, Room_num]
    trace = go.Pie(labels=labels, values=values)

    div = plotly.offline.plot([trace], show_link=False, output_type="div", include_plotlyjs=True)



    return div


def bar(result):

    Apartment =[]
    House =[]
    Townhouse =[]
    Room =[]
    Duplex =[]

    for h in result:

        if h[5] != "Call for Pricing":

            if h[4]=="Apartment":
                Apartment.append(int(str(h[5]).replace(',','')))

            if h[4]=="House":
                House.append(int(str(h[5]).replace(',','')))

            if h[4]=="Townhouse":
                Townhouse.append(int(str(h[5]).replace(',','')))

            if h[4]=="Duplex":
                Duplex.append(int(str(h[5]).replace(',','')))

            if h[4]=="Room":
                Room.append(int(str(h[5]).replace(',','')))

    if len(Apartment) != 0:
        Apartment_num = sum(Apartment)/len(Apartment)
    else:
        Apartment_num = 0

    if len(House) != 0:

        House_num = sum(House)/len(House)
    else:
        House_num = 0

    if len(Townhouse) != 0:
        Townhouse_num = sum(Townhouse)/len(Townhouse)
    else:
        Townhouse_num = 0

    if len(Duplex) != 0:
        Duplex_num = sum(Duplex)/len(Duplex)
    else:
        Duplex_num = 0

    if len(Room) != 0:
        Room_num = sum(Room)/len(Room)
    else:
        Room_num = 0

    data = [go.Bar(
            x=['Apartment', 'House', 'Townhouse', 'Duplex', 'Room'],
            y=[Apartment_num, House_num, Townhouse_num, Duplex_num, Room_num]
    )]

    div = plotly.offline.plot(data, show_link=False, output_type="div", include_plotlyjs=True)

    return div
