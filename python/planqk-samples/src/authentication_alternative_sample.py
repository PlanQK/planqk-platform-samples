from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

username = "your username"
password = "your password"
client_id = "vue-frontend"
client_secret = "~"

"""
This alternative authentication requires the installation of oauthlib and requests_oauthlib
"""

# create access_token
oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
token = oauth.fetch_token(
    "https://platform.planqk.de/auth/realms/planqk/protocol/openid-connect/token",
    username=username, password=password, client_id=client_id, client_secret=client_secret
)

# get the access token from the json response
access_token = token.get('access_token')
