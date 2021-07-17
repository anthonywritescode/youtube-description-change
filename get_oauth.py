from __future__ import annotations

import google_auth_oauthlib.flow

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'goog.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
)

flow.redirect_uri = 'https://localhost:5000/callback'
authorization_url, state = flow.authorization_url(
    access_type='offline',
    state='watwatwatawtawt',
    include_granted_scopes='true',
)

print(authorization_url)

# fill out url here
flow.fetch_token(authorization_response='')

print(flow.credentials.token)
