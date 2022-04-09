"""

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import music
import user
import playlist


@pytest.fixture
def userv(request, user_url, auth):
    return user.User(user_url, auth)


@pytest.fixture
def username(request):
    return ('Smith', 'JamesSmith@sfu.ca', 'James')


@pytest.fixture
def new_user(request):
    return ('Johnson', 'DavidJohnson@sfu.ca', 'David')


def test_simple_run_s1(userv, username, new_user):
    trc, user_id = userv.create(username[0], username[1], username[2])
    assert trc == 200

    trc, lname, email, fname = userv.get(user_id)
    assert (trc == 200 and lname == username[0] and email == username[1]
            and fname == username[2])

    trc = userv.update(user_id, new_user[0], new_user[1], new_user[2])
    assert trc == 200

    trc, lname, email, fname = userv.get(user_id)
    assert (trc == 200 and lname == new_user[0] and email == new_user[1]
            and fname == new_user[2])

    userv.delete(user_id)
    try:
        trc = userv.get(user_id)
        # An exception would be thrown by user.py if delete() success.
        assert False
    except Exception:
        assert True
    # No status to check


@pytest.fixture
def mserv(request, music_url, auth):
    return music.Music(music_url, auth)


@pytest.fixture
def song(request):
    return ('Elvis Presley', 'Hound Dog')


def test_simple_run_s2(mserv, song):
    trc, m_id = mserv.create(song[0], song[1])
    assert trc == 200
    trc, artist, title = mserv.read(m_id)
    assert (trc == 200 and artist == song[0] and title == song[1])
    mserv.delete(m_id)
    # An exception would be thrown by music.py if delete() success.
    try:
        trc = mserv.read(m_id)
        assert False
    except Exception:
        assert True


@pytest.fixture
def plserv(request, playlist_url, auth):
    return playlist.PlayList(playlist_url, auth)


@pytest.fixture
def song2(request):
    return ('Elvis Presley', 'Jailhouse Rock')


@pytest.fixture
def myPlayList(request):
    return ('MyPlayList')


def test_simple_run_s3(mserv, plserv, song, song2, myPlayList):
    trc, m_id = mserv.create(song[0], song[1])
    trc, m2_id = mserv.create(song2[0], song2[1])
    trc, pl_id = plserv.create(myPlayList, [m_id])
    assert trc == 200

    trc, pl_name, songs = plserv.get(pl_id)
    assert (trc == 200 and pl_name == myPlayList and songs == [m_id])

    trc = plserv.add(pl_id, m2_id)
    assert trc == 200

    trc, _, songs = plserv.get(pl_id)
    assert (trc == 200 and songs == [m_id, m2_id])

    trc = plserv.delete_song(pl_id, m_id)
    assert trc == 200

    trc, _, songs = plserv.get(pl_id)
    assert (trc == 200 and songs == [m2_id])

    plserv.delete(pl_id)
    try:
        trc = plserv.get(pl_id)
        # Exception would be thrown by playlist.py if delete() success.
        assert False
    except Exception:
        assert True
