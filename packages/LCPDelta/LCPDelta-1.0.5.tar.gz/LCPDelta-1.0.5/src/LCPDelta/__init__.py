import requests
import json
import time as pytime
from enum import Enum
from datetime import date, time, datetime
from signalrcore.hub_connection_builder import HubConnectionBuilder
import threading
from functools import partial
import calendar

from . import Enact