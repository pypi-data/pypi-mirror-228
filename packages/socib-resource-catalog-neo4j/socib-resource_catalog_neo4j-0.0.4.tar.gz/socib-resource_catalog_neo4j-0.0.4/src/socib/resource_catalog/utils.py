#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import hashlib
import json
import logging
import os
import re
import sys
import traceback

import validators as checker

from datetime import datetime, timedelta
from functools import partial, reduce
from pathlib import Path

##########################################################
## PUBLIC FUNCTIONS
##########################################################
def format_exception (e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str

def format_email( email):
    email = email.replace(" at ", "@")
    email = email.replace(" ", "")
    return email

def is_primitive (obj):
    return not hasattr(obj, '__dict__')

def is_url (value):
    try: 
        return checker.url(value)
    except checker.ValidationFailure as e: pass
    return False

def is_email (value):
    try: 
        return checker.email(value)
    except checker.ValidationFailure as e: pass
    return False

def parse_datetime (date_string, date_format='%Y-%m-%d %H:%M:%S', ignore_time=False):
    if date_string is None: return date_string

    date_string = date_string.strftime('%Y-%m-%d %H:%M:%S') if isinstance(date_string, datetime) else date_string

    for pattern in (date_format, '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%Z', '%Y-%m-%dT%H:%M:%SZ'):
        try:
            dt = datetime.strptime(date_string, pattern)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0) if ignore_time else dt
        except Exception as e: pass
        
    m = re.match(parse_datetime.re_pattern, date_string)
    if m is not None:
        year = int(m.group("year"))
        month = int(m.group("month"))
        day = int(m.group("day"))

        hour = int(m.group("hour")) if m.group("hour") is not None and not ignore_time else 0 
        minute = int(m.group("minute")) if m.group("minute") is not None and not ignore_time else 0 
        second = int(m.group("second")) if m.group("second") is not None and not ignore_time else 0
        
        timezone = m.group("tz")
        
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    logging.warning("[parseDatetime] Error parsing datetime ({}) with format '{}'".format(date_string, date_format))
    return None
parse_datetime.re_pattern = re.compile('(?P<year>[\d]{2,4})(-|/){1}(?P<month>[\d]{2})(-|/){1}(?P<day>[\d]{2})(\w)?(?P<hour>[\d]{2})?(:)?(?P<minute>[\d]{2})?(:)?(?P<second>[\d]{2})?(?P<tz>[a-zA-Z]+)?')

def round_time (date_time, roundToSeconds=24*60*60):
    if date_time == None : date_time = datetime.now()
    seconds = (date_time.replace(tzinfo=None) - date_time.min).seconds
    rounding = (seconds+roundToSeconds/2) // roundToSeconds * roundToSeconds
    return date_time + timedelta(0,rounding-seconds,-date_time.microsecond)

def camelcase_to_snakecase (value, sep='_'):
    return ''.join([sep+c.lower() if c.isupper() else c for c in value]).lstrip(sep)

def snakecase_to_camelcase (value, sep='_'):
    return ''.join(word.title() for word in value.split(sep))

def is_sha1 (str_value, return_sha1_string=False):
    match = re.match(is_sha1.re_sha1, str_value)
    return hashlib.sha1(str_value.encode("utf-8")).hexdigest() if return_sha1_string else (match is not None)
is_sha1.re_sha1 = re.compile(r'\b[0-9a-f]{40}\b')

def purge_empty_keys_in_dict (value):
    if not isinstance(value, dict): return value

    my_dict = {}
    for k,v in value.items():
        if isinstance(v, dict):
            my_dict[k.lower()] = dict_to_dict_lowercase(v)
        elif isinstance(v, list):
            my_dict[k.lower()] = []
            for l in v:
                if isinstance(l, dict):
                    my_dict[k.lower()].append(dict_to_dict_lowercase(l))
                elif isinstance(l,str) and l.strip() == '':
                    pass
                else:
                    my_dict[k.lower()].append(l)
        elif isinstance(v,str) and v.strip() == '':
            pass
        else:
            my_dict[k.lower()] = v
    return my_dict

def dict_to_dict_lowercase (value):
    if not isinstance(value, dict): return value

    my_dict = {}
    for k,v in value.items():
        if isinstance(v, dict):
            my_dict[k.lower()] = dict_to_dict_lowercase(v)
        elif isinstance(v, list):
            my_dict[k.lower()] = []
            for l in v:
                if isinstance(l, dict):
                    my_dict[k.lower()].append(dict_to_dict_lowercase(l))
                else:
                    my_dict[k.lower()].append(l)
        else:
            my_dict[k.lower()] = v
    return my_dict


# def tokenize_name(name, remove_punctuation=True, min_terms=-1, left_coincidences=1, hash_token=True):
#         rst = None
#         if name is None or not isinstance(name,str): return None

#         if 0 < min_terms:
#             tokens = [n for n in name.split(' ')]
#             if remove_punctuation: tokens = [re.sub(r"[\W]+","", t) for t in tokens]
#             tokens = [t.strip().lower() for t in tokens if "" != t.strip()]

#             if min_terms < len(tokens):
#                 rst = []
#                 for r in range(min(min_terms,len(tokens)),len(tokens)+1):
#                     for t in itertools.combinations(tokens, r):
#                         is_valid = True
#                         for i in range(left_coincidences):
#                             is_valid = is_valid and (t[i] == tokens[i])
                        
#                         if is_valid:
#                             candidate = ''.join(t)
#                             if hash_token:
#                                 rst.append(hashlib.sha1(candidate.encode("utf-8")).hexdigest())
#                             else:
#                                 rst.append(candidate.encode("utf-8")) 
#             else:
#                 return tokenize_name(name, remove_punctuation=remove_punctuation)
#         else:
#             if remove_punctuation:
#                 _name = re.sub(r"[\W]+","", name)
#             _name  = _name.strip().lower()
#             if re.match(r"[\w]*,[\w]*", _name):
#                 _name = ' '.join(reversed(_name.split(',')))

#             if hash_token:
#                 rst = [hashlib.sha1(_name.encode("utf-8")).hexdigest()]
#             else:
#                 rst = [_name.encode("utf-8")]
 
#         return rst[0] if -1 == min_terms and len(rst) > 0 else rst

# def countWordOcurrences(string, word):
#     if string is None or word is None: return 0
#     rst = len(re.findall(word, string))
    # return rst

# def url_exists(url):
#     response = requests.get(url)
#     return response.status_code == 200

# def detect_lang(string):
#     if not isinstance(string, str): return None
#     return langdetect.detect(string)

# def geolocate(country=None, locality=None):
#     try:
#         if country is not None: 
#             query = country
#             query = "{},{}".format(locality, country) if locality is not None else query
#             if query in geolocate.cache:
#                 rst = geolocate.cache[query]
#             else:
#                 rst = geolocate.locator.geocode(query)
#                 geolocate.cache[query] = rst
#             return (rst.latitude, rst.longitude)
#     except Exception as e: pass
#     return None
# geolocate.cache = {}
# geolocate.locator = Nominatim(user_agent="jerico-s3.wp7.5")
