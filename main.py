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
import time
import datetime
from tzlocal import get_localzone


def main() -> None:
    tz: str = str(get_localzone())

    # check validity of stored tokens
    # if not present, create token file
    creds = check_calendar_tokens()

    # Create new calendar if non-existent
    # calendar = new_calendar(creds)
    # print(calendar['id'])

    side_id_dict: dict[str, dict[str, str]] = get_ids()

    print(side_id_dict)

    calendar_id: str = input("Enter calendar id: ")

    refresh_rate: int = int(input("Input minutes between updates:\n"))
    print()

    # Main loop
    while True:
        # Get game schedule for selected player(s)/team(s)
        for side_id, side_data in side_id_dict.items():
            data = get_next_matches(team_id=side_id, team_name=side_data["name"], sport=side_data["sport"],
                                    time_zone=tz)
            if data:
                update_events(
                    creds=creds,
                    calendar_id=calendar_id,
                    game_list=data,
                    time_zone=tz
                )

        # Wait some time to update again
        now: Datetime = datetime.datetime.now()
        next_update: Datetime = now + datetime.timedelta(minutes=refresh_rate)
        print(f"{now.hour:02}:{now.minute:02} - "
              f"Next update in {refresh_rate} minute{'' if refresh_rate == 1 else 's'}"
              f" ({next_update.hour:02}:{next_update.minute:02})")
        print("--------------------------------------------------")
        time.sleep(refresh_rate * 60)


if __name__ == "__main__":
    main()
