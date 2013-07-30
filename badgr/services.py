"""This module contains service definions for Badgr.co.

Service classes should take three strings (first, second, bg) and set three
attributes (first, second, and bg).

    first - the first path part => the first word on the badge
    second - the second path part => the second word on the badge
    bg - an RGB color definition, the background behind the second word on the
        badge

"""
from urllib import quote, urlopen

from badgr.colors import RED, YELLOW, GREEN, LIGHT_GREY
from aspen import json


class Generic(object):

    def __init__(self, first, second, bg):
        self.first = first
        self.second = second
        self.bg = bg


class Coveralls(object):

    def __init__(self, first, second, bg):
        self.first = "coverage"
        url = "https://coveralls.io/repos/%s/badge.png?branch=master"
        fp = urlopen(url % second)
        try:
            # We get a redirect to an S3 URL.
            score = fp.url.split('_')[1].split('.')[0]
            self.second = score + '%'

            as_number = int(score)
            if as_number < 80:
                self.bg = RED
            elif as_number < 90:
                self.bg = YELLOW
            else:
                self.bg = GREEN
        except (IndexError, ValueError):
            self.second = 'n/a'
            self.bg = LIGHT_GREY


class Gittip(object):

    def __init__(self, first, second, bg):
        self.first = "tips"
        fp = urlopen("https://www.gittip.com/%s/public.json" % second)
        receiving = json.loads(fp.read())['receiving']
        self.second = "$%d / week" % float(receiving)
        self.bg = (42, 143, 121)  # Gittip green! :)


class TravisCI(object):

    def __init__(self, first, second, bg):
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

        self.bg = { 'failing': RED
                  , 'passing': GREEN
                  , 'pending': YELLOW
                   }.get(self.second, LIGHT_GREY)


services = {}
services['coveralls'] = Coveralls
services['gittip'] = Gittip
services['travis-ci'] = TravisCI

def get(first):
    return services.get(first, Generic)
