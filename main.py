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


def main():
    data = get_data("https://66095c000f324a9a28832d7e.mockapi.io/users")

    task_1_find_user_by_name(data, "Wilson VonRueden")


if __name__ == "__main__":
    main()



