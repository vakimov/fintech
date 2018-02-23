# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from fintech.settings.const import *


SECRET_KEY = 'not-very-secret'


STATIC_ROOT = os.path.join(BASE_DIR, 'dist', 'static')
