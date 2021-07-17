from __future__ import annotations

import argparse
import difflib
import json
import urllib.parse
import urllib.request
from typing import NamedTuple

PLAYLIST_ID = 'UU46xhU1EH7aywEgvA9syS3w'
DESCRIPTION_BLURB = '''\
==========

twitch: https://twitch.tv/anthonywritescode
dicsord: https://discord.gg/xDKGPaW
twitter: https://twitter.com/codewithanthony
github: https://github.com/asottile
stream github: https://github.com/anthonywritescode

I won't ask for subscriptions / likes / comments in videos but it really helps the channel.  If you have any suggestions or things you'd like to see please comment below!
'''  # noqa: E501


class Wideo(NamedTuple):
    wideo_id: str
    title: str
    description: str


def list_wideos(*, api_key: str) -> list[Wideo]:
    base = 'https://www.googleapis.com/youtube/v3/playlistItems'
    params = {
        'part': 'snippet',
        'playlistId': PLAYLIST_ID,
        'key': api_key,
        'maxResults': 50,
    }

    ret = []

    while True:
        url = f'{base}?{urllib.parse.urlencode(params)}'
        resp = urllib.request.urlopen(url)
        json_resp = json.load(resp)
        ret.extend(json_resp['items'])
        next_page_token = json_resp.get('nextPageToken')
        if next_page_token:
            params['pageToken'] = next_page_token
        else:
            break

    return [
        Wideo(
            wideo_id=wideo['snippet']['resourceId']['videoId'],
            title=wideo['snippet']['title'],
            description=wideo['snippet']['description'],
        )
        for wideo in ret
    ]


def get_wideo_category(wideo_id: str, *, api_key: str) -> str:
    resp = urllib.request.urlopen(
        f'https://www.googleapis.com/youtube/v3/videos?'
        f'part=snippet&id={wideo_id}&key={api_key}',
    )
    json_resp = json.load(resp)
    wideo, = json_resp['items']
    return wideo['snippet']['categoryId']


def get_tokens() -> tuple[str, str]:
    with open('config.json') as f:
        contents = json.load(f)
    return contents['key'], contents['token']


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    api_key, token = get_tokens()

    wideos = list_wideos(api_key=api_key)

    for wideo in wideos:
        description = wideo.description
        # for some reason: mixed newlines, normalize before fixing
        description = orig_description = '\n'.join(description.splitlines())

        begin, _, _ = description.rpartition('==========\n')
        description = f'{begin}{DESCRIPTION_BLURB}'.rstrip()

        if description != orig_description:
            title = wideo.title
            a = orig_description.splitlines(True)
            b = description.splitlines(True)
            diff = difflib.unified_diff(
                a,
                b,
                fromfile=f'a/{title}',
                tofile=f'b/{title}',
            )
            for line in diff:
                print(line, end='')

            if not args.dry_run:
                category = get_wideo_category(wideo.wideo_id, api_key=api_key)

                body = {
                    'id': wideo.wideo_id,
                    'snippet': {
                        'categoryId': category,
                        'title': wideo.title,
                        'description': description,
                    },
                }
                req = urllib.request.Request(
                    'https://youtube.googleapis.com/youtube/v3/videos?'
                    'part=snippet',
                    method='PUT',
                    data=json.dumps(body).encode(),
                    headers={
                        'Authorization': f'Bearer {token}',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                )
                urllib.request.urlopen(req)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
