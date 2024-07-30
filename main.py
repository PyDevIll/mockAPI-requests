import requests
from functools import reduce


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
        print(" ! " + wanted_name + " is not found :(")

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
                print(f" ! Wrong state value ({record["state"]})")
                return

            total_state += state_value
        print(f"Total state of first {n} users = {total_state:.2f}")
    else:
        print(" ! Too much user count specified")

    print()


def task_4_find_eldest_user(json_data):
    from datetime import datetime

    def parse_datetime(datetime_str: str):
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                return datetime.strptime(datetime_str, "%Y-%m-%d")
            except ValueError:
                print(f" ! Wrong date format ({datetime_str})")
                return None

    def get_eldest(elder, user):
        user_datetime = parse_datetime(user["birth"])
        if user_datetime is None:
            print(f" ! User skipped (id = {user['id']}; name = \"{user['name']}\"; birth = {user['birth']})")
            return elder
        return {"user_data": user, "time": user_datetime} if elder["time"] > user_datetime else elder

    print("Run task #4\n")

    eldest_user = {
        "user_data": {},
        "time": datetime.now()
    }

    eldest_user = reduce(get_eldest, json_data, eldest_user)

    if len(eldest_user["user_data"]) > 0:
        print("Eldest user:")
        print("\tName = " + eldest_user["user_data"]["name"])
        print("\tBorn = " + eldest_user["time"].strftime("%d.%m.%Y %H:%M:%S"))


def main():
    data = get_data("https://66095c000f324a9a28832d7e.mockapi.io/users")

    task_1_find_user_by_name(data, "Wilson VonRueden")
    task_2_total_state_of_n_users(data, 76)
    task_4_find_eldest_user(data)


if __name__ == "__main__":
    main()



