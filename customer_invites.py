import config
import json
from math import radians, sin, cos, acos
import logging
import sys

def invited_customers():
    customer_data = read_file()
    invites=[]
    for customer in customer_data:
        if(calculate_distance(customer) < config.MAX_DISTANCE):
            invites.append(customer)

    invites.sort(key=lambda customer: customer['user_id'])

    for customer in invites:
        print(customer)

def parse_json(json_data):
    try:
        customer_json = json.loads(json_data)
        customer_json['latitude'] = float(customer_json['latitude'])
        customer_json['longitude'] = float(customer_json['longitude'])
    except json.decoder.JSONDecodeError as e:
        print('ERROR: JSON decoding has failed - {0} - {1}'.format(json_data, e.args))
        sys.exit()
    except KeyError as e:
        print('ERROR: Missing Key - {}'.format(e))
        sys.exit()
    except Exception as e:
        print('ERROR: {}'.format(e))
        sys.exit()
    return customer_json

def read_file():
    customer_data = []
    try:
        with open(config.CUSTOMER_LIST) as json_file:
            for line in json_file:
                customer_data.append(parse_json(line))
    except FileNotFoundError as e:
        print('ERROR: {0} {1}'.format(e.strerror, e.filename))
        sys.exit()
    return customer_data

def convert_to_radians(location):
    return (radians(location[0]), radians(location[1]))

def calculate_distance(customer):
    office_coords = convert_to_radians(config.DUBLIN_OFFICE_LOCATION)
    customer_coords = convert_to_radians((customer['latitude'], customer['longitude']))

    # Great-circle distance https://en.wikipedia.org/wiki/Great-circle_distance
    abs_difference_longitude = abs(office_coords[1] - customer_coords[1])
    central_angle = acos(sin(office_coords[0]) * sin(customer_coords[0]) + cos(office_coords[0]) *
                         cos(customer_coords[0]) * cos(abs_difference_longitude))
    distance = config.EARTH_RADIUS * central_angle

    return distance

if __name__ == '__main__':
    invited_customers()