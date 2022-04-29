import requests
from requests.structures import CaseInsensitiveDict


def check_bank(i: str):
    i = i.replace("-", "")

    url = f"https://lookup.binlist.net/{i}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    data = resp.json()
    # print(data)
    return data["bank"]["name"]


# check_bank("5469-0500-1088-2189")