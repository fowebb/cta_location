"""Fetches train location data from CTA API."""
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
import pymongo
from pymongo import MongoClient
import requests
import sched
import time


def mongo_insert(train_loc_data):
    """Upsert train_loc_data into mongo."""
    client = MongoClient('localhost', 27017)
    db = client['cta']
    collection = db['train_locations']
    collection.insert(train_loc_data)


def fetch_train_locations(route_id):
    """Fetch train location data from CTA Train Tracker API.

    Given a valid CTA "L" Route ID, fetch train location data from the
    CTA Train Tracker Locations API.  For more information on the train
    locations API visit:

    http://www.transitchicago.com/developers/ttdocs/default.aspx#locations

    ------------------
    Valid Route ID's:
    ------------------
    Red = Red Line (Howard-95th - Dan Ryan)
    Blue = Blue Line (O'Hare - Forest Park)
    Brn = Brown Line (Kimball - Loop)
    G = Green Line (Harlem - Lake | Ashland/63rd - Cottage Grove)
    Org = Orange Line (Midway - Loop)
    P = Purple Line (Linden - Howard/Loop)
    Pink = Pink Line (54th/Cermak - Loop)
    Y = Yellow Line (Skokie - Howard)


    Args:
        route_id (str): CTA "L" Route ID

    Returns:
        locations (list): List of dicts with train info and locations
    """
    location_api_url = "http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=c3fb3a60af5d4980910acc149062beb9&rt={}"
    request_url = location_api_url.format(route_id)

    response = requests.get(request_url)
    if response.status_code != 200:
        print("Something went awry! Requests status code {}".format(response.status_code))

    soup = BeautifulSoup(response.text)

    timestamp = datetime.strptime(soup.find('tmst').text, "%Y%m%d %H:%M:%S")
    trains = soup.find_all('train')

    train_locations = []
    for t in trains:
        t_data = {}
        t_data['timestamp'] = timestamp
        for data in t.children:
            t_data[data.name] = str(data.string)
        train_locations.append(t_data)

    mongo_insert(train_locations)
    # return train_locations


if __name__ == '__main__':
    s = sched.scheduler(time.time, time.sleep)

    def ingest_train_locations(sc):
        """Call ingestion function."""
        current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        print "[{}] Ingesting CTA Train Locations...".format(current_time)
        fetch_train_locations("Red")
        sc.enter(60, 1, ingest_train_locations, (sc,))

    s.enter(60, 1, ingest_train_locations, (s,))
    s.run()
    # Fetch Red Line train locations
    # red_line_locations = fetch_train_locations("Red")
