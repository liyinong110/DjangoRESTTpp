import uuid

ADMIN = "admin"
CINEMA = "cinema"
VIEWER = "viewer"


def generate_token(prefix):

    token = uuid.uuid4().hex

    return prefix + token


def generate_admin_token():

    return generate_token(ADMIN)


def generate_cinema_token():

    return generate_token(CINEMA)


def generate_viewer_token():

    return generate_token(VIEWER)
