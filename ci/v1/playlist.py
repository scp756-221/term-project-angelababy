"""
Python  API for the playlist service.
"""

# Standard library modules

# Installed packages
import requests


class PlayList():
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, playListName, songs):
        r = requests.post(
            self._url,
            json={'PlayListName': playListName,
                  'Songs': songs, },
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['playlist_id']

    def get(self, pl_id):
        r = requests.get(
            self._url + pl_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None
        item = r.json()['Items'][0]
        return r.status_code, item["PlayListName"], item["Songs"]

    def add(self, pl_id, m_id):
        r = requests.put(
            self._url + 'add_song_to_list/' + pl_id,
            json={'music_id': m_id},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def delete_song(self, pl_id, m_id):
        r = requests.put(
            self._url + 'delete_song_from_list/' + pl_id,
            json={'music_id': m_id},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def delete(self, pl_id):
        requests.delete(
            self._url + pl_id,
            headers={'Authorization': self._auth}
        )
