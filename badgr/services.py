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


class Gittip(object):

    def __init__(self, first, second, bg):
        self.first = "Gittip"
        self.second = second
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
services['gittip'] = Gittip
services['travis-ci'] = TravisCI

def get(first):
    return services.get(first, Generic)
