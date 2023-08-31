from Furious.Version import __version__

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication

import math
import pathlib
import platform
import functools

APP = functools.partial(QApplication.instance)

APPLICATION_NAME = 'Furious'
APPLICATION_VERSION = __version__
APPLICATION_MACOS_SIGNATURE = 'com.Furious'
APPLICATION_ABOUT_PAGE = 'https://github.com/LorenEteval/Furious/'
APPLICATION_REPO_OWNER_NAME = 'LorenEteval'
APPLICATION_REPO_NAME = 'Furious'

ORGANIZATION_NAME = 'Furious'
ORGANIZATION_DOMAIN = 'Furious.GUI'

PLATFORM = platform.system()

LOCAL_SERVER_NAME = '891ad49d-8996-43cb-820c-d9baf42a04de'

GOLDEN_RATIO = (math.sqrt(5) - 1) / 2

SYSTEM_LANGUAGE = QtCore.QLocale().name()[:2].upper()

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / APPLICATION_NAME / 'Data'
CRASH_LOG_DIR = ROOT_DIR / APPLICATION_NAME / 'CrashLog'

PROXY_SERVER_BYPASS = (
    'localhost;*.local;127.*;10.*;172.16.*;172.17.*;'
    '172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;'
    '172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*'
)

TOR_FAQ_URL = 'https://support.torproject.org/faq/'
TOR_FAQ_LABEL = f'Tor FAQ: <a href=\"{TOR_FAQ_URL}\">{TOR_FAQ_URL}</a>'

# Avoid standard Tor port in case of running Tor services
DEFAULT_TOR_SOCKS_PORT = 9048
DEFAULT_TOR_HTTPS_PORT = 9047


class Color:
    LIGHT_RED_ = '#FF7276'
    LIGHT_BLUE = '#43ACED'
