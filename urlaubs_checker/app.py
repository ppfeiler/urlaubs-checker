import os
import sys
from datetime import datetime

import httpx
from notify_events import Message


ACCOMMODATION_NAME: str = "Mobile Home Dog Lounge"
POSSIBLE_TIMES: list[tuple[str, str]] = [
    # 7 tage lang urlaub
    ("2026-07-12", "2026-07-19"),
    ("2026-07-19", "2026-07-26"),
    ("2026-07-26", "2026-08-02"),
    ("2026-08-02", "2026-08-09"),
    # 14 tage lang urlaub
    ("2026-07-12", "2026-07-26"),
    ("2026-07-19", "2026-08-02"),
    ("2026-07-26", "2026-08-09"),
    # test
    ("2026-05-05", "2026-05-09"),
]

NOTIFY_EVENT_SOURCE_TOKEN: str = os.environ.setdefault("NOTIFY_EVENT_SOURCE_TOKEN", "")


def run() -> None:
    if not NOTIFY_EVENT_SOURCE_TOKEN:
        print("Please set the environment variable 'NOTIFY_EVENT_SOURCE_TOKEN'")
        sys.exit(1)

    valid_times: list[tuple[str, str]] = []

    for possible_time in POSSIBLE_TIMES:
        (arrival, departure) = possible_time
        response = call_union_lido(arrival, departure)

        for free in response["free"]:
            if str(free["name"]).lower() == ACCOMMODATION_NAME.lower():
                valid_times.append(possible_time)

    if len(valid_times) == 0:
        print("No valid times found")
        return

    send_notification(valid_times)


def call_union_lido(arrival: str, departure: str):
    request_body = {
        "arrival": arrival,
        "departure": departure,
        "accommodationGroup": 2,
        "guests": [{"person": 7, "amount": 2}],
        "animals": [{"animal": 2, "amount": 2}],
    }

    request_headers = {
        "accept": "application/json",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6",
        "content-type": "application/json",
        "origin": "https://buchung.mare.unionlido.com",
        "referer": "https://buchung.mare.unionlido.com/",
    }

    response = httpx.post(
        "https://pms.unionlido.com/booking_public/v3/search",
        json=request_body,
        headers=request_headers,
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)

    search_results = {"free": [], "partial": [], "reserved": [], "unknown": []}

    response_body = response.json()
    for accommodation in response_body:
        match accommodation["status"]:
            case "free":
                search_results["free"].append(accommodation)
            case "partial":
                search_results["partial"].append(accommodation)
            case "reserved":
                search_results["reserved"].append(accommodation)
            case _:
                search_results["unknown"].append(accommodation)

    return search_results


def send_notification(valid_times: list[tuple[str, str]]) -> None:
    msg = f"<b>{ACCOMMODATION_NAME}</b> ist an folgenden Terminen verfügbar:<br>"
    for time in valid_times:
        arrival_time = datetime.strptime(time[0], "%Y-%m-%d")
        departure_time = datetime.strptime(time[1], "%Y-%m-%d")
        msg += f"- {arrival_time.strftime('%d.%m.%Y')} - {departure_time.strftime('%d.%m.%Y')} ({(departure_time - arrival_time).days} Tage)<br>"

    message = Message(
        msg,
        f"{ACCOMMODATION_NAME} verfügbar!",
        Message.PRIORITY_HIGHEST,
        Message.LEVEL_WARNING,
    )
    message.send(NOTIFY_EVENT_SOURCE_TOKEN)
