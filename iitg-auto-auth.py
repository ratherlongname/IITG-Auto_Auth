#! python3
# iitg-auto-auth.py - Automatically authenticate with agnigarh server

import requests
import sys
import getpass
import os
from config import config
from urllib3.util.retry import Retry
import urllib3

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
        self.base_url = config['base_url']
        self.login_url = config['login_url']
        self.keepalive_url = config['keepalive_url']
        self.logout_url = config['logout_url']

        self.curr_session = requests.Session()

        if config['custom_headers']:
            self.custom_headers = config[config['custom_headers']]
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
        #except urllib3.exceptions.MaxRetryError as e:
        #    print(e)
        #except requests.exceptions.RequestException as e:
        #    print(e)
        #except ConnectionError:
        #    pass
            # TODO: write to log and exit
        #except requests.exceptions.HTTPError:
        #    pass
            # TODO: write to log and exit
        #except TimeoutError:
        #    pass
            # TODO: write to log and exit
        #except:
        #    pass
            # TODO: write to log and exit
        except Exception as e:
            print(e)
        else:
            return True
            # raise AssertionError("Could not logout. Server responded with status code {} to URL {}.".format(resp.status_code, url_used))

    def get_login(self):
        pass
        # self.curr_session.get()

    def get_keep_alive(self, magic):
        pass

    def post_base_url(self, data):
        pass


if __name__ == "__main__":
    net = AgnigarhHandler()
    net.get_logout()