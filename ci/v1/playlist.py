"""
Python  API for the playlist service.
"""

# Standard library modules

# Installed packages
import requests


class PlayList():
    def __init__(self, url, auth):
        """Python API for the playlist service(s3).

        Handles the details of formatting HTTP requests and decoding
        the results.

        Parameters
        ----------
        url: string
            The URL for accessing the playlist service.
        auth: string
            Authorization code to pass to the playlist service. For many
            implementations, the code is required but its content is
            ignored.
        """
        self._url = url
        self._auth = auth

    def create(self, playListName, songs):
        """Create a playlist with playListName and songs.

        Parameters
        ----------
        playListName: string
            The name of the playlist.
        songs: list
            The list of m_id of the songs in the playlist.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by s3.
            The string is the UUID of this playlist in the playlist database.
        """
        r = requests.post(
            self._url,
            json={'PlayListName': playListName,
                  'Songs': songs, },
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['playlist_id']

    def get(self, pl_id):
        """Get a playlist's name and songs m_id.

        Parameters
        ----------
        pl_id: string
            The UUID of this playlist in the playlist database.

        Returns
        -------
        status, playListName, songs

        status: number
            The HTTP status code returned by s3.
        playListName: If status is 200, the name of the playlist.
          If status is not 200, None.
        songs: If status is 200, the list of m_id of the songs in the playlist.
          If status is not 200, None.
        """
        r = requests.get(
            self._url + pl_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None
        item = r.json()['Items'][0]
        return r.status_code, item["PlayListName"], item["Songs"]

    def add(self, pl_id, m_id):
        """Add a song with m_id to a playlist.

        Parameters
        ----------
        pl_id: string
            The UUID of this playlist in the playlist database.
        m_id: string
            The UUID of the song to be added to the playlist.

        Returns
        -------
        (number)
            The number is the HTTP status code returned by s3.
        """
        r = requests.put(
            self._url + 'add_song_to_list/' + pl_id,
            json={'music_id': m_id},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def delete_song(self, pl_id, m_id):
        """Delete a song with m_id from a playlist.

        Parameters
        ----------
        pl_id: string
            The UUID of this playlist in the playlist database.
        m_id: string
            The UUID of the song to be deleted from the playlist.

        Returns
        -------
        (number)
            The number is the HTTP status code returned by s3.
        """
        r = requests.put(
            self._url + 'delete_song_from_list/' + pl_id,
            json={'music_id': m_id},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def delete(self, pl_id):
        """Delete a playlist.

        Parameters
        ----------
        pl_id: string
            The UUID of this playlist in the playlist database.

        Returns
        -------
        Does not return anything. The playlist delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + pl_id,
            headers={'Authorization': self._auth}
        )
