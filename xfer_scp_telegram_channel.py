# -*- coding: utf-8 -*-

"""
xfer_scp_telegram_channel: broadcast to a telegram channel when xfer_scp registered files download successfully

Settings:
    * plugins.var.python.xfer_scp_pushbullet.api_key: your API key for telegram bot
    * plugins.var.python.xfer_scp_pushbullet.channel_id: the ID for the channel/group/user you wish to broadcast to (see telgram docs for more details)

Commands:
    * none

Requires:
    * requests (pip install requests)

Version: 0.0.1
Author: Grant Bacon <btnarg@gmail.com>
License: GPL3
Date: 08 Aug 2016
"""

import_ok = True

try:
    import weechat
    from requests import get
    from requests.exceptions import Timeout, ConnectionError, HTTPError, TooManyRedirects, RequestException
    import re
    from urllib import urlencode, quote_plus
except:
    print("You must run this script within Weechat!")
    print("http://www.weechat.org")
    import_ok = False

#####
# Registration constants
#####
SCRIPT_NAME = "xfer_scp_telegram_channel"
SCRIPT_AUTHOR = "Grant Bacon <btnarg@gmail.com>"
SCRIPT_VERSION = "0.0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Notify a telegram channel of a successful send from xfer_scp"

####

TELEGRAM_API_URL = "https://api.telegram.org/bot"
API_KEY_KEY = "api_key"
CHANNEL_TAG = "channel_id"
MUTE = "mute"

is_muted = False
bot_url = ""
channel_tag = ""
api_key = ""

def handle_error(e):
    weechat.prnt('', SCRIPT_NAME + ": [ERROR] ")
    return weechat.WEECHAT_RC_ERROR

def xfer_scp_telegram_channel_init():
    global is_muted, channel_tag, api_key
    api_key = weechat.config_get_plugin(API_KEY_KEY)
    channel_tag = weechat.config_get_plugin(CHANNEL_TAG)
    is_muted = is_on(weechat.config_get_plugin(MUTE))
    if api_key and channel_tag:
        global bot_url
        bot_url = TELEGRAM_API_URL + api_key + "/"
    else:
        # throw exception, invalid api_key or missing api_key
        # or just show some kind of error in weechat duh
        # TODO
        bot_url = ""

    return weechat.WEECHAT_RC_OK

def xfer_scp_telegram_channel_config_changed_cb(data, option, value):
    xfer_scp_telegram_channel_init()

    return weechat.WEECHAT_RC_OK

def is_on(value):
    if value is "on":
        return True
    else:
        return False

def pre(msg):
    return "<pre>" + msg + "</pre>"

def message_channel(message):
    safe_message = pre(quote_plus(message))
    global bot_url, channel_tag
    url = bot_url + "sendMessage"
    url += "?" + urlencode({'chat_id': channel_tag, 'text': safe_message, 'parse_mode' : 'html'})

    try:
        get(url)
    except RequestException as e:
        handle_error(e)

def xfer_scp_success_signal_cb(data, signal, signal_data):
    global bot_url, is_muted
    if bot_url != "" and not is_muted:
        message_channel(signal_data)
        return weechat.WEECHAT_RC_OK
    else:
        return weechat.WEECHAT_RC_ERROR


#### Register, begin
if __name__ == "__main__" and import_ok:
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
        if not weechat.config_is_set_plugin(API_KEY_KEY):
            weechat.config_set_plugin(API_KEY_KEY, "")

        if not weechat.config_is_set_plugin(CHANNEL_TAG):
            weechat.config_set_plugin(CHANNEL_TAG, "")

        if not weechat.config_is_set_plugin(MUTE):
            weechat.config_set_plugin(MUTE, "off")

        weechat.hook_signal("xfer_scp_success", 'xfer_scp_success_signal_cb', '')
        weechat.hook_config("plugins.var.python." + SCRIPT_NAME + ".*", "xfer_scp_telegram_channel_config_changed_cb", "")
        xfer_scp_telegram_channel_init()
