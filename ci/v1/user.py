"""
Python  API for the user service.
"""

# Standard library modules

# Installed packages
import requests


class User():
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, lname, email, fname):
        r = requests.post(
            self._url,
            json={'lname': lname,
                  'email': email,
                  'fname': fname, },
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['user_id']

    def update(self, u_id, lname, email, fname):
        r = requests.put(
            self._url + u_id,
            json={'lname': lname,
                  'email': email,
                  'fname': fname, },
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()

    def get(self, u_id):
        r = requests.get(
            self._url + u_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['lname'], item['email'], item['fname']

    def delete(self, u_id):
        requests.delete(
            self._url + u_id,
            headers={'Authorization': self._auth}
        )
