import jwt

from django.conf import settings
from django.core.cache import cache

import time


def get_centrifugo_data(user_id):
    ws_url = settings.CENTRIFUGO_WS_URL
    secret = settings.CENTRIFUGO_SECRET
    token = jwt.encode(
        {
            'sub': str(user_id),
            'exp': int(time.time()) + 10 * 60
        },
        secret, algorithm="HS256"
    )

    return {'centrifugo': {'token': token, 'url': ws_url}}


def get_top_lists():
    top_users = cache.get('top_users')
    top_tags = cache.get('top_tags')

    return {
        'best_members': top_users,
        'popular_tags': top_tags,
    }
