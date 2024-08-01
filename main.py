import calendar
import requests
from functools import reduce
from datetime import datetime
import asyncio
import aiohttp

url = "https://66095c000f324a9a28832d7e.mockapi.io/users"


def parse_datetime(datetime_str: str):
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%d")
        except ValueError:
            print(f" ! Wrong date format ({datetime_str})")
            return None


def put_data(url: str, body):
    response: requests.Response
    response = requests.put(url, json=body)
    if response.status_code != 200:
        raise requests.RequestException("Unsuccessful request!")

    return response.json()


def get_data(url: str):
    response: requests.Response
    response = requests.get(url)
    if response.status_code != 200:
        raise requests.RequestException("Unsuccessful request!")

    return response.json()


async def get_data_async(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        if response.status != 200:
            raise requests.RequestException("Unsuccessful request!")
        return await response.json()


def task_1_find_user_by_name(json_data, wanted_name: str):
    print("Run task #1\n")

    for record in json_data:
        if record["name"] == wanted_name:
            print(wanted_name + "'s id = " + record["id"])
            break
    else:
        print(" ! " + wanted_name + " is not found :(")
    print("___________")


def task_2_total_state_of_n_users(json_data, n: int):
    async def get_user_by_id(session, user_id):
        try:
            return await get_data_async(session, url + "/" + str(user_id))
        except requests.RequestException:
            return None

    async def get_user_list(id_range):
        async with aiohttp.ClientSession() as session:
            tasks = [get_user_by_id(session, user_id) for user_id in id_range]
            return await asyncio.gather(*tasks)

    def get_user_state(user):
        try:
            return float(user["state"])
        except ValueError:
            print(f" ! Wrong state value ({user['state']}). Skipping user named \"{user['name']}\"")
            return 0

    print("Run task #2\n")

    id_from = 1
    id_to = n+1
    while id_to < 101:
        user_list = asyncio.run(get_user_list(range(id_from, id_to)))
        # check for None in user_list
        bad_id_count = reduce(lambda a, user: a + 1 if user is None else a, user_list, 0)
        if bad_id_count == 0:
            break
        # fetch more users instead of None-s
        id_from = id_to
        id_to = id_from + bad_id_count
    else:
        print("Cannot find enough users")
        print("___________")
        return

    total_state = reduce(lambda a, user: a + get_user_state(user), user_list, 0)

    print(f"Total state of first {n} users = {total_state:.2f}")
    print("___________")


def task_3_create_user_at_id(new_id):
    import json

    print("Run task #3\n")

    new_user = {
        "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "name": "PyDevIll",
        "avatar": "https://avatars.githubusercontent.com/u/169006885?v=4",
        "state": "10110010",
        "birth": "1987-10-16T00:48:07.777Z",
        "id": str(new_id)
    }
    response_json = put_data(url + '/' + str(new_id), new_user)
    print("Created user:")
    print(json.dumps(response_json, indent=4))

    print("___________")


def task_4_find_eldest_user(json_data):
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
    print("___________")


def task_5_find_poorest_user(json_data):
    def get_poorest(poorer, user):
        user_state = float(user["state"])
        return {"user_data": user, "state": user_state} if user_state < poorer["state"] else poorer

    print("Run task #5\n")

    poorest_user = {
        "user_data": {},
        "state": 999_999_999_999
    }

    poorest_user = reduce(get_poorest, json_data, poorest_user)

    if len(poorest_user["user_data"]) > 0:
        print("Poorest user:")
        print("\tName = " + poorest_user["user_data"]["name"])
        print(f"\tState = {poorest_user["state"]:.2f}")
    print("___________")


def task_6_count_users_by_birth_month(month, json_data):
    def is_born_at_month(user) -> bool:
        birth_date = parse_datetime(user["birth"])
        if birth_date is None:
            print(f" ! User skipped (id = {user['id']}; name = \"{user['name']}\"; birth = {user['birth']})")
            return False
        return birth_date.month == month

    print("Run task #6\n")

    result_user_list = list(filter(is_born_at_month, json_data))

    print("Users born in " + calendar.month_name[month] + ": " + str(len(result_user_list)))
    for user in result_user_list:
        print("\tName: " + user["name"])
        print("\tBorn: " + user["birth"])
        print()
    print("___________")


def main():
    data = get_data(url)

    task_1_find_user_by_name(data, "Wilson VonRueden")
    task_2_total_state_of_n_users(data, 76)
    task_3_create_user_at_id(69)
    task_4_find_eldest_user(data)
    task_5_find_poorest_user(data)
    task_6_count_users_by_birth_month(4, data)


if __name__ == "__main__":
    main()



