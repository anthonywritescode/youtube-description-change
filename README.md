youtube-description-change
==========================

- set up an api key using [google's cloud console]
- you will also need an oauth application
    - I used "Web Application" with a callback of
      "https://localhost:5000/callback"
    - you don't actually need to have a webapp running
    - I used the `https://www.googleapis.com/auth/youtube.force-ssl` scope
- you need to get an oauth token, we won't bother with refresh, etc.
    - download the creds that the console gives you and save them as `goog.json`
    - to do that, run `get_oauth.py` (it will spit out a link, click that)
    - then paste the resulting redirect url (`https://localhost:5000/...`) into
      `get_oauth.py` and run it again, it should give you a bearer token.
- take both the api key and bearer token and make a `config.json` with this
  format: `{"key": ..., "token": ...}`
- finally, run `python -m change_descriptions`

[google's cloud console]: https://console.cloud.google.com/
