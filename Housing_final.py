from bs4 import BeautifulSoup
import requests
import json
import sqlite3
from secrets import google_places_key
import csv



class HouseListing:

    def __init__(self, id, name, address=None, url=None, desc=None, rent=None, status=None, pet=None, bed=None, bath=None, parking=None, lat=None, lon=None):
        self.id = str(id)
        self.name = name
        self.address = address
        self.url = url
        self.desc = desc
        self.rent = rent
        self.status = status
        self.pet = pet
        self.bed = bed
        self.bath = bath
        self.parking = parking
        self.lat = lat
        self.lon = lon

    def __str__(self):
        housing_str = str(self.id)+'\n\t'+self.name+'\n\t'+self.address+'\n\t'+self.bed+"/"+self.bath+'\n\t'+self.rent+'\n\t'+self.status+"\n\t"+self.parking+"\n\t"+self.pet
        return housing_str


CACHE_FNAME = 'housingcache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def get_unique_key(page_url):

    start_url = "/search?view=list&sort=default&per_bed=u&r%5Bmin%5D=&r%5Bmax%5D=&"
    end_url = "&search_all=1&movein-start=0&movein-end=1&o=&distance%5B132%5D=&distance%5B133%5D=&text_search="
    url = housing_url+start_url+page_url+end_url
    return url


def get_house_link(house_url):

    url = baseurl+house_url
    return url


def get_GPS_from_gplace(address):
    baseurl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    params = {"query": address, "key": google_places_key}

    return make_request_using_cache_for_gpalce(address, baseurl, params)


def make_request_using_cache_for_gpalce(query, baseurl, params):
    unique_ident = query
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        response = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(response.text)
        dumped_json_cache=json.dumps(CACHE_DICTION)
        fw=open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def make_request_using_cache(url):
    unique_ident = url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url).text
        CACHE_DICTION[unique_ident] = resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


baseurl = 'https://offcampushousing.umich.edu/'
housing_url = baseurl + '/property'
# header = {'User-Agent': 'SI_CLASS'}


def get_housing():

    page_list = []
    house_link_list = []
    house_ins_list = []
    for i in range(1, 44):
        page_url = "page="+str(i)
        page_text = make_request_using_cache(get_unique_key(page_url))
        page_soup = BeautifulSoup(page_text, 'html.parser')
        page_list.append(page_soup.find_all(class_="name"))
    # print(page_list)

    for page in page_list:
        # print(page)
        for house in page:
            # print(house)
            house_link = house.find("a")["href"]
            # print(house_link)
            house_link_list.append(house_link)
    # print(house_link_list)
    house_info_list = []
    for link in house_link_list:
        page_text = make_request_using_cache(get_house_link(link))
        page_soup = BeautifulSoup(page_text, 'html.parser')
        house_info = page_soup.find(id='main')
        house_info_list.append(house_info)

    house_id = 0
    for house in house_info_list:
        house_name = house.find(class_="title").text.strip()
        house_desc = house.find(class_="dborder-top").find("div").text
        house_address = house.find(class_="location").text
        house_url = house.find(class_="pad-sides").find(class_="btn-share")["data-short-url"]
        house_rent = house.find(class_="numbers").find_all("strong")[0].text.strip()
        house_status = house.find(class_="other-info").find("div").text.strip()
        house_bed = house.find(class_="numbers").find_all("strong")[1].text.strip()
        house_bath = house.find(class_="numbers").find_all("strong")[2].text.strip()
        house_id = house_id+1


        try:
            house_coordinate = get_GPS_from_gplace(house_address)["results"][0]['geometry']['location']
            house_lat = house_coordinate["lat"]
            house_lon = house_coordinate["lng"]
            house_pet = house.find(class_="snapshot-extras-list").find_all("li")[3].text.strip()
            house_parking = house.find(class_="snapshot-extras-list").find_all("li")[2].text.strip()

        except:
            house_lat = ""
            house_lon = ""
            house_pet = "Not listed"
            house_parking = "Not listed"

        house_inc = HouseListing(house_id, house_name, house_address, house_url, house_desc,  house_rent, house_status, house_pet, house_bed, house_bath, house_parking, house_lat, house_lon)
        # print(house_inc.__str__())
        house_ins_list.append(house_inc)
    # print(house_ins_list)
    return house_ins_list


get_housing()


outfile = open("Housing.csv","w")
outfile.write('Id,Name,Address,Bed,Bath,Rent,Status,Pet,Parking,Url\n')
for i in get_housing():
    outfile.write('{},{},{},{},{},{},{},{},{},{}\n'.format("\""+i.id+"\"","\""+i.name+"\"","\""+i.address+"\"","\""+i.bed+"\"","\""+i.bath+"\"","\""+i.rent+"\"","\""+i.status+"\"","\""+i.pet+"\"","\""+i.parking+"\"","\""+i.url+"\""))
outfile.close()

