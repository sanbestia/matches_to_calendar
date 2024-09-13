#!/usr/bin/env python

import subprocess
import sys


# packages_to_install = {
#     'google-api-python-client',
#     'google-auth-oauthlib',
#     'google-auth-httplib2',
#     'pytz',
#     'tzlocal'
# }
#
#
# for package in packages_to_install:
#     subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


from check_calendar_tokens import check_calendar_tokens
from calendar_methods import update_events
from get_next_matches import get_next_matches
from get_ids import get_ids
from time_keeper import wait
import time
import datetime
from tzlocal import get_localzone

SEARCHES = {
    "Carlos Alcaraz": {
        "id": "275923",
        "sport": "tennis",
        "calendar": "2f6c5ac6edbf3fa0ff6fa234ec6b37dff78b64a2a1ea4162bf8bf7f284417f14@group.calendar.google.com"
    },
    "Argentina - Football National Team": {
        "id": "4819",
        "sport": "football",
        "calendar": "c3d4b2ce891f8038024590fb245c8e3c8227b9b49a10bc0407b29db52c4780d8@group.calendar.google.com"
    },
    "Argentina - Football U23 National Team": {
        "id": "24246",
        "sport": "football",
        "calendar": "c3d4b2ce891f8038024590fb245c8e3c8227b9b49a10bc0407b29db52c4780d8@group.calendar.google.com"
    },
    "San Antonio Spurs": {
        "id": "3429",
        "sport": "basketball",
        "calendar": "0f28ddb0e94b2b91bf79d57308609cd3554ec9b6e09c9dc726e04294ce5d5b99@group.calendar.google.com"
    },
    "Dallas Mavericks": {
        "id": "3411",
        "sport": "basketball",
        "calendar": "0f28ddb0e94b2b91bf79d57308609cd3554ec9b6e09c9dc726e04294ce5d5b99@group.calendar.google.com"
    },
    "T1": {
        "id": "364366",
        "sport": "esport",
        "calendar": "fb4bc7a499fc0fc2aa64d7c50cd5bb10b2fd797cbd64bf4e50bbad283ac3561c@group.calendar.google.com"
    },
    "Argentina - Tennis National Team": {
        "id": "14441",
        "sport": "tennis",
        "calendar": "c3d4b2ce891f8038024590fb245c8e3c8227b9b49a10bc0407b29db52c4780d8@group.calendar.google.com"
    },
    "France - Basketball National Team": {
        "id": "6248",
        "sport": "basketball",
        "calendar": "0f28ddb0e94b2b91bf79d57308609cd3554ec9b6e09c9dc726e04294ce5d5b99@group.calendar.google.com"
    },
    "Argentina - Basketball National Team": {
        "id": "6124",
        "sport": "basketball",
        "calendar": "c3d4b2ce891f8038024590fb245c8e3c8227b9b49a10bc0407b29db52c4780d8@group.calendar.google.com"
    },
    "USA - Basketball National Team": {
        "id": "6141",
        "sport": "basketball",
        "calendar": "0f28ddb0e94b2b91bf79d57308609cd3554ec9b6e09c9dc726e04294ce5d5b99@group.calendar.google.com"
    }
}


def main() -> None:
    tz = get_localzone()

    # check validity of stored tokens
    # if not present, create token file
    creds = check_calendar_tokens()

    # Create new calendar if non-existent
    # calendar = new_calendar(creds)
    # print(calendar['id'])

    refresh_rate = 240
    print()

    # Main loop
    while True:
        # Get game schedule for selected player(s)/team(s)
        for name, data_dict in SEARCHES.items():
            data = get_next_matches(team_id=data_dict["id"], team_name=name, sport=data_dict["sport"],
                                    time_zone=str(tz))
            if data:
                update_events(
                    creds=creds,
                    calendar_id=data_dict["calendar"],
                    game_list=data,
                    time_zone=str(tz)
                )
            print("--------------------------------------------------\n")

        # Wait some time to update again
        now = datetime.datetime.now(tz=tz)
        deadline = now + datetime.timedelta(minutes=refresh_rate)
        print(f"{now.hour:02}:{now.minute:02} - "
              f"Next update in {refresh_rate} minute{'' if refresh_rate == 1 else 's'}"
              f" (@ {deadline.hour:02}:{deadline.minute:02})")
        wait(deadline, tz)
        print("\n-----------------------------------------------------------------------------\n")


if __name__ == "__main__":
    main()
