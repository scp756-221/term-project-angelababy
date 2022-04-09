"""
Python  API for the user service.
"""

# Standard library modules

# Installed packages
import requests


class User():
    """Python API for the user service(s1).

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the user service.
    auth: string
        Authorization code to pass to the user service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, lname, email, fname):
        """Create a user with lname, email, fname.

        Parameters
        ----------
        lname: string
            The last name of the user.
        email: string
            The email of the user.
        fname: string
            The first name of the user.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by s1.
            The string is the UUID of this user in the user database.
        """
        r = requests.post(
            self._url,
            json={'lname': lname,
                  'email': email,
                  'fname': fname, },
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['user_id']

    def update(self, u_id, lname, email, fname):
        """Update a user with lname, email, fname.

        Parameters
        ----------
        u_id: string
            The UUID of this user in the user database.
        lname: string
            The last name of the user.
        email: string
            The email of the user.
        fname: string
            The first name of the user.

        Returns
        -------
        (number)
            The number is the HTTP status code returned by s1.
        """
        r = requests.put(
            self._url + u_id,
            json={'lname': lname,
                  'email': email,
                  'fname': fname, },
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def get(self, u_id):
        """Get a user's last name, email, first name.

        Parameters
        ----------
        u_id: string
            The UUID of this user in the user database.

        Returns
        -------
        status, lname, email, fname

        status: number
            The HTTP status code returned by s1.
        lname: If status is 200, the last name of the user.
          If status is not 200, None.
        email: If status is 200, the email of the user.
          If status is not 200, None.
        fname: If status is 200, the first name of the user.
          If status is not 200, None.
        """
        r = requests.get(
            self._url + u_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['lname'], item['email'], item['fname']

    def delete(self, u_id):
        """Delete a user.

        Parameters
        ----------
        u_id: string
            The UUID of this user in the user database.

        Returns
        -------
        Does not return anything. The user delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + u_id,
            headers={'Authorization': self._auth}
        )
