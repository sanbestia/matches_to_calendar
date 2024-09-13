from datetime import datetime, timezone

import pytz

from Match import Match

import requests
import json


def get_next_matches(team_id: str, team_name: str, sport: str, time_zone: str) -> list[Match]:
    print(f"* Looking for games featuring {team_name}:\n")

    headers: dict[str, str] = {
        "X-RapidAPI-Key": "3f3cbf5db7msh03db9b62179412fp12c91bjsnd280512fdf8a",
        "X-RapidAPI-Host": "allsportsapi2.p.rapidapi.com"
    }

    next_games: list[Match] = []

    events: list = []

    read_next_page: bool = True
    page: int = 0
    while read_next_page:
        url = (f"https://allsportsapi2.p.rapidapi.com/api/"
               f"{sport + '/' if sport != 'football' else ""}"
               f"team/"
               f"{team_id}/"
               f"{'events' if sport == 'tennis' else 'matches'}/"
               f"next/"
               f"{page}")

        try:
            request = requests.get(url, headers=headers)

        except (TimeoutError, ConnectionError) as e:
            print("Couldn't communicate with sports API")
            print(e)
            return []

        if page == 0 and not request.text:
            print("No upcoming games found\n")
            return []

        request_dict = json.loads(request.text)

        if "events" not in request_dict:
            print(f"Request Error: 'events' key not found in\n"
                  f"{request_dict}")
            return []

        events += request_dict["events"]

        read_next_page = request_dict['hasNextPage']
        page += 1

    print("Got data:")
    for event in events:
        date_time = datetime.fromtimestamp(event['startTimestamp'], tz=timezone.utc)
        date_time = date_time.astimezone(pytz.timezone(time_zone))
        round_info = event.get('roundInfo')
        if round_info and 'name' not in round_info:
            round_info['name'] = f'Round {round_info['round']}'
        game = Match(
            side_one=event['homeTeam']['name'],
            side_two=event['awayTeam']['name'],
            tournament=event['season']['name'],
            stage=round_info['name'] if round_info else event['tournament']['name'],
            game_id=event['id'],
            sport=sport,
            start_time=date_time
        )

        print(game, time_zone)
        next_games.append(game)

    print()
    return next_games


def main():
    pass


if __name__ == '__main__':
    main()
