#! python3
# iitg-auto-auth.py - Automatically authenticate with agnigarh server

import requests
import sys
import getpass
import os


class Account:
    # Attributes
    #   1. username
    #   2. password
    #   3. default?
    pass

data = {
    '4Tredir': "https://agnigarh.iitg.ac.in:1442/login?",
    'magic': "",
}

try:
    data['username'] = os.environ['IITG_USERNAME']
except KeyError as e:
    print("IITG_USERNAME environment variable is not set.")
    data['username'] = input("Username: ")

try:
    data['password'] = os.environ['IITG_PASSWORD']
except KeyError as e:
    print("IITG_PASSWORD environment variable is not set.")
    data['password'] = getpass.getpass()


class AgnigarhHandler:
    ''' Interface to make requests to the IITG login server.

    Keyword arguments:
    None

    Returns:
    Instance of self

    '''

    def __init__(self):
        self.base_url = "https://agnigarh.iitg.ac.in:1442/"
        self.login_url = self.base_url + "login??"
        self.keepalive_url = self.base_url + "keepalive?"
        self.logout_url = self.base_url + "logout??"

        self.curr_session = requests.Session()
        self.custom_headers = {
            'Host': 'agnigarh.iitg.ac.in:1442',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        # self.curr_session.headers = self.custom_headers
        self.curr_session.verify = "./iitg_ac_in.crt"
        # self.curr_session.max_redirects = 0
    
    def get_logout(self):
        url_used = self.logout_url
        resp = self.curr_session.get(url_used, allow_redirects=False)
        if resp.ok:
            return True
        else:
            raise AssertionError("Could not logout. Server responded with status code {} to URL {}.".format(resp.status_code, url_used))

    def get_login(self):
        pass

    def get_keep_alive(self, magic):
        pass

    def post_base_url(self, data):
        pass



if __name__ == "__main__":
    print('Data for POST request:', data)
    net = AgnigarhHandler()
    net.get_logout()