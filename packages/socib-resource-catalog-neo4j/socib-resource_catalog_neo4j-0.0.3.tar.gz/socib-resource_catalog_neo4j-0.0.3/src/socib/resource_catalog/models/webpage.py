#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import hashlib
import inspect
import json
import logging
import os
import pkg_resources
import re
import sys
import traceback
import uuid

from datetime import datetime
from functools import reduce, partial, lru_cache
from pathlib import Path
from validator_collection import checkers, errors

from neomodel import config
from neomodel import db

from neomodel import StructuredNode
from neomodel import StructuredRel
from neomodel import Relationship, RelationshipFrom, RelationshipTo

from neomodel import ArrayProperty
from neomodel import BooleanProperty
from neomodel import DateTimeFormatProperty
from neomodel import EmailProperty
from neomodel import FloatProperty
from neomodel import IntegerProperty
from neomodel import JSONProperty
from neomodel import RegexProperty
from neomodel import StringProperty
from neomodel import UniqueIdProperty

#######################################################################
## WEBPAGE (implementation)
#######################################################################
class WebPageImpl (object): 

    language = StringProperty() 
    mimetype = StringProperty()

    def __init__ (self):
        logging.debug("[WebPageImpl::__init__] entering method")

