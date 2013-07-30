"""This module contains service definions for Badgr.co.

Service classes should take three strings (first, second, color) and set three
attributes (first, second, and color).

    first - the first path part => the first word on the badge
    second - the second path part => the second word on the badge
    color - a color name, the background behind the second word on the badge

"""
from urllib import quote, urlopen

from aspen import json
from badgr.colors import RED, YELLOW, YELLOWGREEN, GREEN, LIGHTGRAY


class Generic(object):

    def __init__(self, first, second, color):
        self.first = first
        self.second = second
        self.color = color


class Coveralls(object):

    def __init__(self, first, second, color):
        self.first = "coverage"
        url = "https://coveralls.io/repos/%s/badge.png?branch=master"
        fp = urlopen(url % second)
        try:
            # We get a redirect to an S3 URL.
            score = fp.url.split('_')[1].split('.')[0]
            self.second = score + '%'

            as_number = int(score)
            if as_number < 80:
                self.color = RED
            elif as_number < 90:
                self.color = YELLOW
            else:
                self.color = GREEN
        except (IndexError, ValueError):
            self.second = 'n/a'
            self.color = LIGHTGRAY


class Gittip(object):

    def __init__(self, first, second, color):
        self.first = "tips"
        fp = urlopen("https://www.gittip.com/%s/public.json" % second)
        receiving = float(json.loads(fp.read())['receiving'])
        self.second = "$%d / week" % receiving
        if receiving == 0:
            self.color = RED
        elif receiving < 10:
            self.color = YELLOW
        elif receiving < 100:
            self.color = YELLOWGREEN
        else:
            self.color = GREEN


class TravisCI(object):

    def __init__(self, first, second, color):
        self.first = "build"

        url = 'https://api.travis-ci.org/repos?slug=%s' % quote(second)
        fp = urlopen(url)
        repos = json.loads(fp.read())
        if repos:
            status = repos[0].get('last_build_status', 'n/a')
        else:
            status = 'n/a'

        self.second = { 0: 'passing'
                      , 1: 'failing'
                      , None: 'pending'
                      , 'n/a': 'n/a'
                       }.get(status, 'n/a')

        self.color = { 'failing': RED
                     , 'passing': GREEN
                     , 'pending': YELLOW
                      }.get(self.second, LIGHTGRAY)


services = {}
services['coveralls'] = Coveralls
services['gittip'] = Gittip
services['travis-ci'] = TravisCI

def get(first):
    return services.get(first, Generic)
