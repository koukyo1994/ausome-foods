import json
import time

import urllib.request
import urllib.parse

import constants as C

from typing import Optional, Tuple, Dict


def get_channel_id(channel_name: str, token: str) -> Optional[str]:
    api_url = urllib.parse.urljoin(C.SLACK_HOST, C.CHANNEL_LIST)
    api_url = api_url + "?token=" + token

    with urllib.request.urlopen(api_url) as res:
        result = json.load(res)
        time.sleep(1)

    if not result["ok"]:
        return None

    channels = result["channels"]
    for c in channels:
        if c["name"] == channel_name:
            channel_id = c["id"]
            break
    else:
        channel_id = None

    return channel_id


def get_slack_credentials() -> Tuple[str, str]:
    with open(C.CREDENTIALS) as f:
        credentials = json.load(f)

    channel_name = credentials["channel"]
    token = credentials["token"]
    return channel_name, token


def post_to_slack(channel_id: str, token: str, img_profiles: Dict[str, str]):
    api_url = urllib.parse.urljoin(C.SLACK_HOST, C.POST)

    post_json = {
        "channel":
        channel_id,
        "text":
        f"レストラン: {img_profiles['rst_name']}({img_profiles['rst_url']})",
        "username":
        "ausome-foods",
        "icon_url":
        C.ICON_URL,
        "attachments": [{
            "fields": [{
                "title": img_profiles["img_name"],
                "value": img_profiles["img_url"]
            }],
            "image_url":
            img_profiles["img_url"]
        }]
    }
    json_data = json.dumps(post_json).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    method = "POST"
    req = urllib.request.Request(
        api_url, data=json_data, headers=headers, method=method)
    with urllib.request.urlopen(req) as res:
        json.load(res)


if __name__ == '__main__':
    print(globals())
