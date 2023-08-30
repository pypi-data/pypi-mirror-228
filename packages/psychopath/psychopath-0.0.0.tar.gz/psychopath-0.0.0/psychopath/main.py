import logging.config
import platform
from logging import getLogger, Logger

try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        import nest_asyncio

        nest_asyncio.apply()
except:
    ...

if platform.system() in {'Darwin', 'Linux'}:
    try:
        import uvloop

        uvloop.install()
    except ImportError as e:
        ...

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'standard': {'format': '%(asctime)s.%(msecs)03d [%(levelname)s] :: %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'standard', 'stream': 'ext://sys.stdout'},
        'file': {'class': 'logging.FileHandler', 'level': 'DEBUG', 'formatter': 'standard', 'filename': 'log.log', 'mode': 'a'},
    },
    'loggers': {'my_logger': {'handlers': ['console', 'file'], 'level': 'DEBUG'}}
})
logger = getLogger(list(Logger.manager.loggerDict)[-1])

...