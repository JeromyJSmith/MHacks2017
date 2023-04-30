import difflib
import logging as log
from twilio.rest import Client
import config
import weather, wiki, news, help

DIFF_SENSITIVITY=0.7


def send_text(body, to_num, from_num):
    log.debug('Sending text')
    client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
    message = client.api.account.messages.create(to=to_num,
						from_=from_num,
						body=body)


def get_api_words():
    return [
        {'api': 'help', 'words': ['help', 'helpme']},
        {'api': 'weather', 'words': ['weather', 'forecast']},
        {'api': 'news', 'words': ['news', 'headlines', 'worldnews', 'updates']},
        {'api': 'wikipedia', 'words': ['wiki', 'wikipedia']}
    ]


def run_api_function(api, body):
    options = {
        'wikipedia': wiki.search,
        'news': news.getNews,
        'weather': weather.getWeather,
        'help': help.sendHelp
    }
    return options[api](body)


def has_word(string, good_words):
    return len(difflib.get_close_matches(string, good_words, 1,
                                        DIFF_SENSITIVITY)) > 0


def get_response_text(body):
    # hierarchy of responses, help at the top
    words = body.lower().split()
    api_words = get_api_words()
    chosen_api = ''
    done = False
    for api in api_words:
        for word in words:
            if has_word(word, api['words']):
                chosen_api = api['api']
                break
        if done:
           break

    if not chosen_api:
        log.error('No api found from body')
        return 'Thanks for using LifeText! Try something like any of these:\nweather Madison, WI\ntechnology news\nwikipedia Weezer\nhelp [sends an alarm text out to your listed emergency contacts]\n\nYou can also go to lifetext.us to make an account'

    log.debug(f'api found: {chosen_api}')
    if ret_string := run_api_function(chosen_api, body):
        return ret_string
