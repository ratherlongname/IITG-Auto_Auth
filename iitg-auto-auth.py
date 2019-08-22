#! python3
# iitg-auto-auth.py - Automatically authenticate with agnigarh server

import requests
import sys
import getpass
import os
from config import config
from urllib3.util.retry import Retry
import urllib3
import re
from time import sleep

class AgnigarhHandler:
    ''' Interface to make requests to the IITG login server.

    Keyword arguments:
    None

    Returns:
    Instance of self

    '''

    def __init__(self):
        self.base_url = config['base_url']
        self.login_url = config['login_url']
        self.keepalive_url = config['keepalive_url']
        self.logout_url = config['logout_url']

        self.curr_session = requests.Session()

        if config['custom_headers']:
            self.custom_headers = config['custom_headers']
            self.curr_session.headers = self.custom_headers

        if config['certificate_path']:
            self.curr_session.verify = config['certificate_path']
        else:
            self.curr_session.verify = False

        if config['retry_profile']:
            retry_config = config[config['retry_profile']]
            retries = Retry(total = retry_config['total'],
                            backoff_factor = retry_config['backoff_factor'],
                            status_forcelist = retry_config['status_forcelist'],
                            raise_on_status = retry_config['raise_on_status'])
        else:
            retries = Retry()
        self.curr_session.mount('https://', requests.adapters.HTTPAdapter(max_retries = retries))

    def get_logout(self):
        try:
            self.curr_session.get(self.logout_url, allow_redirects=False, timeout=10)
        except Exception as e:
            # TODO: write e to log along with info if it is caused due to client, server or this programme
            print(e)
        else:
            return True

    def get_login(self):
        try:
            resp = self.curr_session.get(self.login_url, timeout=10)
        except Exception as e:
            # TODO: write e to log along with info if it is caused due to client, server or this programme
            print(e)
        else:
            try:
                login_magic = self.extract_login_magic(resp.text)
            except AssertionError as e:
                print(e)
                raise
                # TODO: retry get_login()
            else:
                return login_magic

    def post_base_url(self, data):
        try:
            resp = self.curr_session.post(self.base_url, data=data, allow_redirects=False, timeout=10)
        except Exception as e:
            print(e)
        else:
            keepalive_magic = self.extract_keepalive_magic(resp.text)
            return keepalive_magic

    def get_keep_alive(self, magic):
        try:
            self.curr_session.get(self.keepalive_url + magic, allow_redirects=False, timeout=10)
        except Exception as e:
            # TODO: write e to log along with info if it is caused due to client, server or this programme
            print(e)
        else:
            return True
    
    def extract_keepalive_magic(self, post_text):
        pattern = re.compile('keepalive[?](?P<keepalive_magic>[a-z0-9]*)')

        match = pattern.search(post_text)
        if match:
            return match.group('keepalive_magic')
        else:
            raise AssertionError("POST did not return magic value. Response received:\n{}".format(post_text))


    def extract_login_magic(self, login_text):
        pattern = re.compile('<input type="hidden" name="magic" value="(?P<login_magic>[a-z0-9]*)">')

        match = pattern.search(login_text)
        if match:
            return match.group('login_magic')
        else:
            raise AssertionError("Login page does not contain magic value. Login page received:\n{}".format(login_text))

    def build_form_data(self, login_magic):
        data = {}
        data['4Tredir'] = config['4Tredir_url']
        data['magic'] = login_magic

        # TODO: don't read username, pw from env variables. read from file. maybe gnome keychain?
        try:
            data['username'] = os.environ['IITG_USERNAME']
            if not data['username']:
                raise KeyError
        except KeyError:
            print("IITG_USERNAME environment variable is not set")
            try:
                data['username'] = config['IITG_USERNAME']
                if not data['username']:
                    raise KeyError
            except KeyError:
                print("IITG_USERNAME not set in config.py")
                try:
                    data['username'] = input("Username: ")
                except EOFError:
                    data['username'] = ""

        try:
            data['password'] = os.environ['IITG_PASSWORD']
            if not data['password']:
                raise KeyError
        except KeyError:
            print("IITG_PASSWORD environment variable is not set")
            try:
                data['password'] = config['IITG_PASSWORD']
                if not data['password']:
                    raise KeyError
            except KeyError:
                print("IITG_PASSWORD not set in config.py")
                try:
                    data['password'] = getpass.getpass()
                except EOFError:
                    data['password'] = ""

        return data

if __name__ == "__main__":
    net = AgnigarhHandler()
    net.get_logout()
    login_magic = net.get_login()
    print("login_magic received:", login_magic)
    data = net.build_form_data(login_magic)
    print(data)
    keepalive_magic = net.post_base_url(data)
    while True:
        if net.get_keep_alive(keepalive_magic):
            print("keepalive successful!")
        sleep(500)
    