# -*- coding: utf-8 -*-
from dotenv import load_dotenv

from .bot import *
from .counters import *
from .database import *
from .default_options import *

if __name__ == '__main__':
    pass
else:
    load_dotenv()
