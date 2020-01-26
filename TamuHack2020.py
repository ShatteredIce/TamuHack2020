import requests
import json
from flask import Flask, render_template, request
import HospitalSearcher as hs

# returns the index of the minimum duration given a list of durations in the form x days y hours z minutes
def compareTimes(durations):
    converted_times = []
    for duration in durations:
        total_minutes = 0
        temp = 0
        token_list = duration.split()
        for token in token_list:
            if token.isnumeric():
                temp = int(token)
            elif token == "days" or token == "day":
                total_minutes += temp * 1440
                temp = 0
            elif token == "hours" or token == "hour":
                total_minutes += temp * 60
                temp = 0
            elif token == "mins" or token == "min":
                total_minutes += temp
                temp = 0
            else:
                print("Error: unknown unit " + token + " encountered.")
        converted_times.append(total_minutes)
    return converted_times.index(min(converted_times))


# returns the formatted url to be queried
def format_url(origin, destinations, key):
    dst_string = ""
    for dst in destinations:
        if dst != destinations[0]:
            dst_string += "|"
        dst_string += dst
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" \
          + origin + "&destinations=" + dst_string + "&key=" + key
    print(url)
    return url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def getvalue():
    # get data from website form
    st_addr = request.form['usr_addr']
    city = request.form['usr_city']
    suburb = request.form['usr_suburb']
    state = request.form['usr_state']
    condition = request.form['usr_con']

    start_addr = st_addr + ", " + city + " " + state
    dest_addr = []

    # collect addresses of hospitals
    hospitals = hs.getPossibleLocs(condition, state, city, suburb)
    if len(hospitals) == 0:
        return render_template('index.html', results="No results found.")

    for line in hospitals:
        dest_addr.append(" ".join(line[3:6]))
    print(dest_addr)

    # read api key from local file
    kfile = open("key.txt","r")
    key = kfile.read()
    kfile.close()

    url = format_url(start_addr, dest_addr, key)
    res = requests.get(url)
    data = res.json()

    print(data)
    print("Starting address: ", data['origin_addresses'])
    print("Destination addresses: ", data['destination_addresses'])

    # Extract duration and distance data from json query
    distances = []
    durations = []
    travel_data = data['rows'][0]['elements']
    for i in range(0, len(travel_data)):
        try:
            distances.append(travel_data[i]['distance']['text'])
            durations.append(travel_data[i]['duration']['text'])
        except KeyError:
            return render_template('index.html', results=data['destination_addresses'][i] + ".")


    print("Distances", distances)
    print("Durations", durations)
    min_t_index = compareTimes(durations)

    result_str = "Results for " + condition + " around " + start_addr + ":\n \
    Closest destination is " + data['destination_addresses'][min_t_index] + " which is " + distances[min_t_index] + \
                 " and " + durations[min_t_index] + " away."

    print("\nClosest destination is", data['destination_addresses'][min_t_index], "which is", distances[min_t_index], "and", durations[min_t_index], "away.")

    return render_template('index.html', results=result_str)


if __name__ == '__main__':
    app.run(debug=True)

# dest_addr = []
# input_line = "placeholder"
# print("Enter destination addresses one line at a time, enter blank line to exit")
# input_line = input("Enter destination address (hit enter to exit): ")
# while input_line != "":
#    dest_addr.append(input_line)
#    input_line = input("Enter destination address (hit enter to exit): ")
#
#
# url = format_url(start_addr, dest_addr, key)
#
# #url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=14332 NW Falconridge Ln&destinations=Texas A&M University|Cornell University&key=AIzaSyAYT6ulXlSRx5RVOVFN0GMcirSCkCKlRfo"
#
#
# res = requests.get(url)
# data = res.json()
#
# #data = {'destination_addresses': ['Portland, OR, USA', 'Houston, TX, USA', '800 George Bush Dr, College Station, TX 77840, USA'], 'origin_addresses': ['8211 Triple Crown, Boerne, TX 78015, USA'], 'rows': [{'elements': [{'distance': {'text': '3,297 km', 'value': 3297348}, 'duration': {'text': '1 day 7 hours', 'value': 112590}, 'status': 'OK'}, {'distance': {'text': '356 km', 'value': 356262}, 'duration': {'text': '3 hours 21 mins', 'value': 12043}, 'status': 'OK'}, {'distance': {'text': '294 km', 'value': 294044}, 'duration': {'text': '3 hours 7 mins', 'value': 11208}, 'status': 'OK'}]}], 'status': 'OK'}
#
# print(data)
# print("Starting address: ", data['origin_addresses'])
# print("Destination addresses: ", data['destination_addresses'])
#
# # Extract duration and distance data from json query
# distances = []
# durations = []
# travel_data = data['rows'][0]['elements']
# for i in range(0, len(travel_data)):
#     try:
#         distances.append(travel_data[i]['distance']['text'])
#         durations.append(travel_data[i]['duration']['text'])
#     except KeyError:
#         print("Cannot find route to", data['destination_addresses'][i] + ".")
#         exit()
#
#
# print("Distances", distances)
# print("Durations", durations)
# min_t_index = compareTimes(durations)
# print("\nClosest destination is", data['destination_addresses'][min_t_index], "which is", distances[min_t_index], "and", durations[min_t_index], "away.")




