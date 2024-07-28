# Odds Scraper
## Overview
This Python script is designed for scraping sports betting data from the Bwin website. It utilizes the requests library to fetch data from the Bwin API and extracts information about upcoming sports events, including tournament names, event names, start times, and betting odds.

## Results

This is currently being ran on a RaspberryPi Model 4 every

0 */2 * * *

(once every second hour)

The outputted JSON can be found here:

[Nate's Dropbox](https://www.dropbox.com/scl/fo/envwkbmx6rqeq82ri3le4/h?rlkey=2skc2ny1poimq793x4squxp4j&dl=0)

## Script Structure

### Imported Libraries

requests: Used for making HTTP requests to the Bwin API.

os: Provides a way to interact with the operating system, used for file handling.

json: Used for reading and writing JSON data.

datetime and timezone: Used for handling date and time information.

### Functions:

get_total_games_count: Retrieves the total count of upcoming games.

get_games_json: Fetches JSON data for the specified number of current games.

parse_games_json: Parses the fetched JSON data and extracts relevant information.

player_data: Helps extract player-related data from the response JSON.

event_data: Helps extract event-related data from the response JSON.

file_output: Writes the extracted data to a JSON file.

url_updater: Is a small helper function that updates the URL with the specified parameters.

## Main Execution:

Constructs the initial API URL and fetches JSON data.

Parses the JSON data and extracts relevant information.

Writes the extracted data to a JSON file in the current working directory.


Note:

Bwin have an API available with where an access_id and token can be obtained by becoming an affiliate.
This can be found here: [BWin API Docs](https://sportsapi.bwin.com/articles/getinvolved.html)
