import os


BASE_URL = os.environ.get(
    "LOCATIESERVER_URL", "https://api.pdok.nl/bzk/locatieserver/search/v3_1/"
)
