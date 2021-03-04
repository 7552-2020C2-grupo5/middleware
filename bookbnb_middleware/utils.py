import os
from bookbnb_middleware.constants import BOOKBNB_TOKEN


def get_sv_auth_headers():
    return {"BookBNBAuthorization": os.getenv(BOOKBNB_TOKEN.upper(), "_")}
