import requests

import os
import json
from datetime import datetime, timezone

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'),
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


def get_total_games_count(initial_url):
    initial_request = requests.get(initial_url, headers=headers)
    status_code = initial_request.status_code
    print("Total games length url status code : ", status_code)

    initial_response = initial_request.content
    initial_response_json = json.loads(initial_response)

    print(initial_response_json["totalCount"])
    return initial_response_json["totalCount"]


def get_games_json(game_url):
    request = requests.get(game_url, headers=headers)
    status_code = request.status_code
    print("Games JSON url status code : ", status_code)

    response = request.content
    response_json = json.loads(response)
    return response_json


def player_data(games):
    player_list = []
    for players in games["results"]:
        players_data = {
            "outcome_name": players["name"]["value"],
            "odds": players["odds"]
        }
        player_list.append(players_data)
    return player_list


def event_data(requested_data):
    event_name = requested_data["name"]["value"].replace('-', 'v')

    start_time_stripped = datetime.strptime(requested_data["startDate"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_start_time = start_time_stripped.strftime("%Y-%m-%d %H:%M")

    return event_name, formatted_start_time


def parse_games_json(data):
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    extracted_data = []

    for requested_data in data["fixtures"]:
        if requested_data["stage"] == "Live":
            continue

        tournament_name = requested_data["tournament"]["name"]["value"]

        event_name, formatted_start_time = event_data(requested_data)

        players_data_list = []
        for games in requested_data["games"]:
            if games["name"]["value"] == "Match Winner":
                players_data_list.extend(player_data(games))

        events = {
            "event_name": event_name,
            "start_time": formatted_start_time,
            "outcomes": players_data_list
        }

        extracted_data.append({
            "tournament_name": tournament_name,
            "last_fetched": current_time,
            "events": [events]
        })

    return extracted_data


def file_output(json_data):
    file_name = "json-data.json"
    working_dir = os.path.join(os.getcwd(), file_name)

    with open(working_dir, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def url_updater(take):
    sports_id, skip = 5, 0
    url_fstring = ("https://sports.bwin.com/cds-api/bettingoffer/fixtures?"
                   "x-bwin-accessid=NTZiMjk3OGMtNjU5Mi00NjA5LWI2MWItZmU4MDRhN2QxZmEz&lang=en&country=GB&"
                   "userCountry=GB&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&"
                   f"offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other&sportIds={sports_id}"
                   f"&tournamentIds=&competitionIds=&conferenceIds=&isPriceBoost=false&statisticsModes=None&skip={skip}"
                   f"&take={take}&sortBy=Tags")
    print(url_fstring)
    return url_fstring


if __name__ == '__main__':
    url = url_updater(0)
    games_url = url_updater(get_total_games_count(url) + 1)
    games_data = get_games_json(games_url)
    final_json = parse_games_json(games_data)
    file_output(final_json)
