import logging


class Credentials:

    def __init__(self, username=None, password=None):
        if username is not None:
            self._username = username
        if password is not None:
            self._password = password

    def get_username(self):
        if self._username:
            return self._username
        logging.error('Username was not provided but has been requested')
        raise ValueError('Username was not provided')

    def get_password(self):
        if self._password:
            return self._password
        logging.error('Password was not provided but has been requested')
        raise ValueError('Password was not provided')
