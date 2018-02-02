import config
import json
from math import radians, sin, cos, acos
import sys

def print_invited_customers():
    customer_data = read_file(config.CUSTOMER_LIST)

    invites = get_invited_customers(customer_data)

    for customer in invites:
        print('user_id: {0}, name: {1}'.format(customer['user_id'], customer['name']))

def get_invited_customers(customer_data):
    '''
    Returns invited customers based on those who are located within the max distance of the
    Intercom office location
    :param customer_data:
    :return: invited_customers
    '''

    invited_customers=[]
    for customer in customer_data:
        if(calculate_distance((customer['latitude'], customer['longitude'])) < config.MAX_DISTANCE):
            invited_customers.append(customer)

    invited_customers.sort(key=lambda customer: customer['user_id'])

    return invited_customers

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

def read_file(file_name):
    customer_data = []

    try:
        with open(file_name) as json_file:
            for line in json_file:
                customer_data.append(parse_json(line))

    except FileNotFoundError as e:
        print('ERROR: {0} {1}'.format(e.strerror, e.filename))
        sys.exit()

    return customer_data

def convert_to_radians(location):
    return (radians(location[0]), radians(location[1]))

def calculate_distance(customer_location):
    '''
    Calculates Great-Circle distance between customer location and the Intercom office location
    using formula as specified in https://en.wikipedia.org/wiki/Great-circle_distance
    :param customer:
    :return: distance
    '''

    office_coords = convert_to_radians(config.DUBLIN_OFFICE_LOCATION)
    customer_coords = convert_to_radians(customer_location)

    abs_difference_longitude = abs(office_coords[1] - customer_coords[1])
    central_angle = acos(sin(office_coords[0]) * sin(customer_coords[0]) + cos(office_coords[0]) *
                         cos(customer_coords[0]) * cos(abs_difference_longitude))
    distance = config.EARTH_RADIUS * central_angle

    return distance

if __name__ == '__main__':
    print_invited_customers()