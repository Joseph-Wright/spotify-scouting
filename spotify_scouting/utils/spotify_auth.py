from spotipy import SpotifyOAuth
from spotipy.oauth2 import SpotifyStateError


class CustomAuth(SpotifyOAuth):
    def __init__(self, *args, **kwargs):
        super(CustomAuth, self).__init__(*args, **kwargs)

    def process_auth_response(self, response_url):
        state, code = SpotifyOAuth.parse_auth_response_url(response_url)
        if self.state is not None and self.state != state:
            raise SpotifyStateError(self.state, state)
        self.get_access_token(code=code)
        return "/"

    