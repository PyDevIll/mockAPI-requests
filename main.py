import requests
import json


def get_data(url: str):
    response: requests.Response

    response = requests.get(url)
    if response.status_code != 200:
        raise requests.RequestException("Unsuccessful request!")

    return response.json()


def task_1_find_user_by_name(json_data, wanted_name: str):
    print("Run task #1\n")
    for record in json_data:
        if record["name"] == wanted_name:
            print(wanted_name + "'s id = " + record["id"])
            break
    else:
        print(wanted_name + " is not found :(")

    print()


def task_2_total_state_of_n_users(json_data, n: int):
    print("Run task #2\n")
    total_state = 0

    if n <= len(json_data):
        for i in range(n):
            record = json_data[i]
            try:
                state_value = float(record["state"])
            except ValueError:
                print(f"Wrong state value ({record["state"]})")
                return

            total_state += state_value
        print(f"Total state of first {n} users = {total_state:.2f}")
    else:
        print("Too much user count specified")

    print()


def main():
    data = get_data("https://66095c000f324a9a28832d7e.mockapi.io/users")

    task_1_find_user_by_name(data, "Wilson VonRueden")
    task_2_total_state_of_n_users(data, 76)


if __name__ == "__main__":
    main()



