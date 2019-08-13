import sys

if __name__ == '__main__':
    sys.path.append("src")

    from slack import (post_to_slack, get_channel_id, get_slack_credentials)
    from logics.tabelog import tabelog
    from utils import url_select

    key, url = url_select()
    method = globals().get(key)

    result_dict = method(url)

    channel_name, token = get_slack_credentials()
    channel_id = get_channel_id(channel_name, token)
    post_to_slack(channel_id, token, result_dict)
