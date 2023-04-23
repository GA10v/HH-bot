import logging

import sentry_sdk
from core.config import settings
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.utils import BadDsn


def init_sentry():
    try:
        sentry_sdk.init(dsn=settings.logging.SENTRY_DSN, integrations=[AioHttpIntegration()])
    except BadDsn:
        logger = logging.getLogger('AioHttp')
        logger.warning('Start without Sentry!')
