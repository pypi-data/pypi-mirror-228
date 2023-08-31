#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from ast import keyword
import hashlib
import inspect
import json
import logging
import os
import re
import sys
import traceback
import uuid

from datetime import datetime
from functools import reduce, partial, lru_cache
from pathlib import Path

import avro
import parquet
import bs4

from neomodel import config
from neomodel import db

from neomodel import StructuredNode
from neomodel import StructuredRel

from neomodel import Relationship 
from neomodel import RelationshipFrom 
from neomodel import RelationshipTo

from neomodel import ZeroOrMore
from neomodel import ZeroOrOne
from neomodel import OneOrMore

from neomodel import ArrayProperty
from neomodel import BooleanProperty
from neomodel import DateTimeFormatProperty
from neomodel import EmailProperty
from neomodel import FloatProperty
from neomodel import IntegerProperty
from neomodel import JSONProperty
from neomodel import Property
from neomodel import RegexProperty
from neomodel import StringProperty
from neomodel import UniqueIdProperty

from neomodel.relationship_manager import RelationshipDefinition, RelationshipManager

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from neo4j.time import DateTime as neo4j_Datetime
from neo4j.spatial import WGS84Point as neo4j_Point

from socib.resource_catalog import config
from socib.resource_catalog import namespace

from socib.resource_catalog.annotations import singleton
from socib.resource_catalog.utils import is_url, is_email, format_exception

from socib.resource_catalog.models.api import ApiImpl
from socib.resource_catalog.models.api_operation import ApiOperationImpl, ApiOperationParameterImpl
from socib.resource_catalog.models.address import AddressImpl
from socib.resource_catalog.models.catalog import CatalogImpl
from socib.resource_catalog.models.concept import ConceptImpl 
from socib.resource_catalog.models.concept_scheme import ConceptSchemeImpl
from socib.resource_catalog.models.contact_point import ContactPointImpl
from socib.resource_catalog.models.dataset import DatasetImpl
from socib.resource_catalog.models.distribution import DistributionImpl
from socib.resource_catalog.models.document import DocumentImpl
from socib.resource_catalog.models.equipment import EquipmentImpl
from socib.resource_catalog.models.facility import FacilityImpl
from socib.resource_catalog.models.frequency import FrequencyImpl
from socib.resource_catalog.models.organization import OrganizationImpl
from socib.resource_catalog.models.platform import PlatformImpl
from socib.resource_catalog.models.person import PersonImpl
from socib.resource_catalog.models.program import ProgramImpl
from socib.resource_catalog.models.project import ProjectImpl
from socib.resource_catalog.models.variable import VariableImpl
from socib.resource_catalog.models.relation import RelationImpl
from socib.resource_catalog.models.resource import ResourceImpl
from socib.resource_catalog.models.spatial import SpatialImpl
from socib.resource_catalog.models.sensor import SensorImpl
from socib.resource_catalog.models.service import ServiceImpl
from socib.resource_catalog.models.software import SoftwareImpl
from socib.resource_catalog.models.software_source import SoftwareSourceImpl
from socib.resource_catalog.models.temporal import TemporalImpl
from socib.resource_catalog.models.text import TextImpl
from socib.resource_catalog.models.vcard import VcardImpl
from socib.resource_catalog.models.webservice import WebServiceImpl
from socib.resource_catalog.models.webpage import WebPageImpl
from socib.resource_catalog.models.website import WebSiteImpl

#######################################################################
## INTERNAL FUNCTIONS
#######################################################################

_NORMAL_MAP = {
    'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
    'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
    'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
    'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
    'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
    'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
    'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
    'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
    'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
    'Ñ': 'N', 'ñ': 'n',
    'Ç': 'C', 'ç': 'c',
    '§': 'S',  '³': '3', '²': '2', '¹': '1'}

_TRANS_MAP = str.maketrans(_NORMAL_MAP)


def is_primitive (obj):
    return not hasattr(obj, '__dict__')

def _parseDatetime(date_string, date_format='%Y-%m-%d %H:%M:%S', ignore_time=False):
    if date_string is None: return date_string

    for pattern in (date_format, '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%Z', '%Y-%m-%dT%H:%M:%SZ'):
        try:
            dt = datetime.strptime(date_string, pattern)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0) if ignore_time else dt
        except Exception as e: pass

    m = re.match(_parseDatetime.re_pattern, date_string)
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
_parseDatetime.re_pattern = re.compile('(?P<year>[\d]{2,4})(-|/){1}(?P<month>[\d]{2})(-|/){1}(?P<day>[\d]{2})(\w)?(?P<hour>[\d]{2})?(:)?(?P<minute>[\d]{2})?(:)?(?P<second>[\d]{2})?(?P<tz>[a-zA-Z]+)?')


#######################################################################
## INTERNAL OBJECTS
#######################################################################
_INTERNAL_BASE_UID_RAWID_CACHE = {}

class OfflineRelationship (object): 

    @property
    def data (self):
        rst = {key: getattr(self, key) for key in self.__dict__}
        return rst if 0 != len(rst)  else None

class OfflineRelationshipManager (object):

    def __init__ (self, name):
        logging.debug("[OfflineRelationshipManager::__init__] entering method")
        self.name = name
        self.related = []

    def connect (self, node, properties=None):
        logging.debug("[OfflineRelationshipManager::connect] entering method")
        for i in range(len(self.related)):
            r = self.related[i]
            if self.name not in ("alias", "related") and r[0].uid == node.uid: del self.related[i]
        else:
            properties = {k:v for k,v in properties.items()} if properties is not None else properties
        self.related.append((node, properties))
        return None

    def replace (self, node, properties=None):
        logging.debug("[OfflineRelationshipManager::replace] entering method")
        self.related.clear()
        self.connect(node, properties=properties)
        return None

    def relationship (self, node):
        logging.debug("[OfflineRelationshipManager::relationship] entering method")
        o = None
        for r in self.related:
            if r[0].uid == node.uid:
                o = OfflineRelationship()
                p = r[1] if r[1] is not None else {}
                for k,v in p.items(): setattr(o, k, v) 
        return o

    def all_relationships (self, node):
        logging.debug("[OfflineRelationshipManager::all_relationships] entering method")
        a = []
        for r in self.related:
            if r[0].uid == node.uid:
                o = OfflineRelationship()
                p = r[1] if r[1] is not None else {}
                for k,v in p.items(): setattr(o, k, v)
                a.append(o)
        return a

    def reconnect (self, old_node, new_node):
        logging.debug("[OfflineRelationshipManager::reconnect] entering method")
        for i in range(len(self.related)):
            r = self.related[i]
            if r[0].uid == old_node.uid: 
                properties = r[1]
                del self.related[i]
                self.connect(new_node, properties=properties)
        return None

    def disconnect (self, node):
        logging.debug("[OfflineRelationshipManager::disconnect] entering method")
        for i in range(len(self.related)):
            r = self.related[i]
            if r[0].uid == node.uid: del self.related[i]
        return None

    def disconnect_all (self):
        logging.debug("[OfflineRelationshipManager::disconnect_all] entering method")
        self.related[i].clear()
        return None

    def is_connected (self, node):
        logging.debug("[OfflineRelationshipManager::is_connected] entering method")
        for i in range(len(self.related)):
            r = self.related[i]
            if r[0].uid == node.uid: return True
        return False

    def all (self):
        logging.debug("[OfflineRelationshipManager::all] entering method")
        return [r[0] for r in self.related]

    def get (self, **kwargs):
        logging.debug("[OfflineRelationshipManager::get] entering method")
        return None

    def get_or_none (self, **kwargs):
        logging.debug("[OfflineRelationshipManager::get_or_none] entering method")
        return None

    def filter (self, **kwargs):
        logging.debug("[OfflineRelationshipManager::filter] entering method")
        return None

    def order_by (self, *props):
        logging.debug("[OfflineRelationshipManager::order_by] entering method")
        return None

    def exclude (self, **kwargs):
        logging.debug("[OfflineRelationshipManager::exclude] entering method")
        return None

    def single (self):
        logging.debug("[OfflineRelationshipManager::single] entering method")
        return None

    def match (self, **kwargs):
        logging.debug("[OfflineRelationshipManager::match] entering method")
        return None

    def _new_traversal(self):
        logging.debug("[OfflineRelationshipManager::_new_traversal] entering method")
        return None
    
    def __iter__ (self):
        logging.debug("[OfflineRelationshipManager::__iter__] entering method")
        rst = []; [rst.append(r[0].uid if r[0].uid not in rst else None) for r in self.related]
        return iter([self.related[i][0] for i in range(len(rst)) if rst[i] is not None])

    def __len__ (self):
        logging.debug("[OfflineRelationshipManager::__len__] entering method")
        return len(self.related)

    def __bool__ (self):
        logging.debug("[OfflineRelationshipManager::__bool__] entering method")
        return len(self.related) > 0

    def __nonzero__ (self):
        logging.debug("[OfflineRelationshipManager::__nonzero__] entering method")
        return len(self.related) > 0

    def __contains__ (self, obj):
        logging.debug("[OfflineRelationshipManager::__contains__] entering method")
        return None

@singleton
class AliasResolver (object):

    def __init__ (self):
        logging.debug("[AliasRelationship::__init__] entering method")
        self.cache = {}

    def resolve (self, cls, alias, also_return_rid=False):
        if alias is None: return None

        for a in alias: 
            if a in self.cache: return self.cache[a]

        alias = ["'{}'".format(a) for a in alias]
        query = "MATCH (n:{label})-[r:ALIAS]-(n) WHERE r.uri in [{alias}] RETURN DISTINCT n.uid, n.rid".format(label=cls.__label__, alias=','.join(alias))
        rst = db.cypher_query(query, {})
        
        if 0 == len(rst[0]):
            return None
        elif 1 == len(rst[0]):
            for a in alias: self.cache[a] = rst[0][0]
            return rst[0][0][0],rst[0][0][1] if also_return_rid else rst[0][0]
        else:
            raise ModelException("[AliasResolver::resolve] Found more that 'only one' entity for alias [{}+]".format(cls.__name__, ','.join(alias)))

#######################################################################
## BASE EXCEPTIONS
#######################################################################
class BaseException (Exception): pass
class ModelException (BaseException): pass

#######################################################################
## BASE
#######################################################################
class MyStructuredRel (StructuredRel):
    updated = DateTimeFormatProperty(format="%Y-%m-%dT%H:%M:%S")
    visited = DateTimeFormatProperty(format="%Y-%m-%dT%H:%M:%S", default=lambda: datetime.now())
    sources = ArrayProperty(StringProperty(), required=True)

class AliasRelationship (StructuredRel):
    uri = StringProperty(required=True)
    scheme = StringProperty()

    def pre_save (self):
        logging.debug("[AliasRelationship::pre_save] entering method")

        if self.uri is None:  
            raise ValueError("[AliasRelationship::pre_save] '{}' missing uri".format(self.uri))
        elif not is_url(self.uri) and not is_email(self.uri):  
            raise ValueError("[AliasRelationship::pre_save] '{}' is not a valid uri".format(self.uri)) 

    def post_save (self):
        logging.debug("[AliasRelationship::post_save] entering method")

class RelatedRelationship (StructuredRel):
    type = StringProperty(required=True)

    def pre_save (self):
        logging.debug("[RelatedRelationship::pre_save] entering method")
        self.type = "UNKNOWN" if self.type is None else self.type

    def post_save (self):
        logging.debug("[RelatedRelationship::post_save] entering method")

class Base (StructuredNode): 
    __abstract_node__ = True

    uid = StringProperty(required=True, unique_index=True)
    rid = StringProperty(unique_index=True)

    name = StringProperty(index=True)
    description = StringProperty(index=True)
    keywords = StringProperty(index=True)
    url = StringProperty() #todo change to RegexProperty with url pattern (include more than http protocol)

    created = DateTimeFormatProperty(format="%Y-%m-%dT%H:%M:%S")
    modified = DateTimeFormatProperty(format="%Y-%m-%dT%H:%M:%S")

    updated = DateTimeFormatProperty(format="%Y-%m-%dT%H:%M:%S")
    visited = DateTimeFormatProperty(format="%Y-%m-%dT%H:%M:%S", default=lambda: datetime.now())

    active = BooleanProperty(default=True)
    status = StringProperty()
    version = StringProperty()
    type =  StringProperty()
    family =  StringProperty()

    permission = StringProperty(default=config.DEFAULT_PERMISSION)
    visibility = StringProperty(default=config.DEFAULT_VISIBILITY)

    sources = ArrayProperty(StringProperty(), required=True)
    categories = ArrayProperty(StringProperty())
    identifiers = ArrayProperty(StringProperty())

    alias = RelationshipTo("Base", "ALIAS", model=AliasRelationship)
    parent = RelationshipTo("Base", "PARENT", cardinality=ZeroOrOne)
    related = RelationshipTo("Base", "RELATED", model=RelatedRelationship)
    subject_of = RelationshipTo("Base", "IS_SUBJECT_OF")

    concepts = RelationshipTo("Concept", "HAS_CONCEPT")
    spatials =  RelationshipTo("Spatial", "HAS_SPATIAL")
    temporals = RelationshipTo("Temporal", "HAS_TEMPORAL")
    
    def __init__ (self, **kwargs): 
        logging.debug("[Base::__init__] entering method")
        StructuredNode.__init__(self, **kwargs)

        for k,v in kwargs.items(): setattr(self, k, v)
        self.uid = str(uuid.uuid4()) if self.uid is None else self.uid

        self._first_born = False
        self._current_mode_offline = config.MODEL_MODE_OFFLINE
        self._current_hash = None
        
    def __getattribute__ (self, name):
        attr = StructuredNode.__getattribute__(self, name)

        if config.MODEL_MODE_OFFLINE and isinstance(attr, RelationshipManager):
            return getattr(self, "_offline_{}".format(name))

        return attr

    def __eq__ (self, other):
        return str(self) == str(other)

    def __str__ (self):
        return self.serialize(include_relationships=False, avoid_offline_restriction=True)

    def __prepare__ (self):
        self.rid = _INTERNAL_BASE_UID_RAWID_CACHE.get(self.uid) if self.rid is None else self.rid
        self.permission = config.DEFAULT_PERMISSION if self.permission is None else self.permission
        self.visibility = config.DEFAULT_VISIBILITY if self.visibility is None else self.visibility
        try: 
            my_keywords = ''
            if isinstance(self.keywords, list):
                for k in self.keywords:
                    if isinstance(k, dict) and 'keywords' in k:
                        my_keywords = ','.join(k["keywords"])
                    else:
                         my_keywords = "{}{}{}".format(
                             my_keywords,
                             ', ' if 0 != len(my_keywords) else '',
                             k
                         )
            else:
                my_keywords = self.keywords
        except Exception as e: 
            keywords = ''
        finally: 
            self.keywords = my_keywords

        self.updated = self.visited.replace(hour=0, minute=0, second=0, microsecond=0)
        #self.visited = self.visited.replace(hour=0, minute=0, second=0, microsecond=0)

        self.url = self.url.replace('//', '/').replace(':/', '://') if self.url is not None else self.url

        if self.sources is not None: self.sources = [str(s) for s in self.sources]

        if self.name is not None:
            self.name = bs4.BeautifulSoup(self.name, features="html5lib").get_text() if self.name is not None else self.name
            self.name = self.name.translate(_TRANS_MAP) if hasattr(self.name, 'maketrans') else self.name
        if self.description is not None:
            self.description = bs4.BeautifulSoup(self.description, features="html5lib").get_text(strip=True) if self.description is not None else self.description
            self.description = self.description.translate(_TRANS_MAP) if hasattr(self.description, 'maketrans') else self.description
        if self.keywords is not None:
            self.keywords = bs4.BeautifulSoup(self.keywords, features="html5lib").get_text(strip=True) if self.description is not None else self.description
            self.keywords = self.keywords.translate(_TRANS_MAP) if hasattr(self.keywords, 'maketrans') else self.keywords

        self.categories = [c.lower() for c in self.categories if c is not None and '' != c.strip()] if self.categories is not None else self.categories

        properties = [p for p in dir(self) if hasattr(self.__class__, p) and isinstance(getattr(self.__class__, p), Property)]
        for key in properties: 
            value = getattr(self, key)
            if value is None: continue
            if isinstance(value, str):
                value = value.replace("'", "\'")
                value = value.strip()
                value = value if '' != value else None
                setattr(self, key, value)

    @classmethod
    def has_property(cls, name):
        properties = [p for p in dir(cls) if isinstance(getattr(cls, p), Property) and name == p]
        return len(properties) > 0

    @classmethod
    def has_relationship(cls, name):
        relationships = [r for r in dir(cls) if hasattr(cls, r) and isinstance(getattr(cls, r), RelationshipDefinition) and name == r]
        return len(relationships) > 0

    def hash (self):
        payload = self.serialize(include_relationships=False, avoid_offline_restriction=True, exclude_set=["visited", "updated"])
        return hashlib.sha1(payload.encode("utf-8")).hexdigest()

    def dump (self, path=os.getcwd()):
        logging.debug("[Base::dump] entering method")
        with open("{}{}{}.json".format(path, os.sep, self.uid.split('/')[-1]), "w") as f: json.dump(self.serialize(return_as_string=False), fp=f, indent=4, sort_keys=True)

    def properties (self, include_empty=False):
        properties = [p for p in dir(self) if hasattr(self.__class__, p) and isinstance(getattr(self.__class__, p), Property)]
        properties = [p for p in properties if include_empty or getattr(self, p, None) is not None]
        return properties

    def relationships (self, include_empty=False):
        relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
        if not include_empty: 
            relationships = [r for r in relationships if 0 != len(getattr(self, r, []))]
        return relationships

    def set_attribute_for_all(self, name=None, value=None, replace=True, append=False):
        if name is None: return
        
        current = getattr(self, name, None)
        if current is None:
            setattr(self, name, value)
        elif replace:
            setattr(self, name, value)
        elif append:
            current = current if isinstance(current, list) else [current]
            if isinstance(value, list):
                current.extend(value)
            else:
                current.append(value) 
            lst=[]; lst = [c for c in current if c not in lst]
            setattr(self, name, lst)
        else:
            pass
        
        
        relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
        for relationship in relationships:
            try:
                nodes = getattr(self, relationship); nodes = [] if nodes is None else nodes
                for node in nodes:
                    node.set_attribute_for_all(name=name, value=value, replace=replace, append=append)
            except Exception as e:
                print(e)

    def save (self):
        logging.debug("[Base::save] entering method")

        if not config.MODEL_MODE_OFFLINE:
            with db.transaction:
                self.register_unsaved_nodes()
                self.transform_to_online()
                StructuredNode.save(self)
            with db.transaction:
                self.fix_multiple_labels()
        else:
            logging.warning("[Base::save] not allowed in 'offline' mode")
        return self

    def delete (self):
        logging.debug("[Base::delete] entering method")

        if not config.MODEL_MODE_OFFLINE:
            with db.transaction:
                self.register_unsaved_nodes()
                self.transform_to_online()
                rst = StructuredNode.delete(self)
            return rst
        else:
            logging.warning("[Base::delete] not allowed in 'offline' mode")
            return False

    def refresh (self):
        logging.debug("[Base::refresh] entering method")

        if not config.MODEL_MODE_OFFLINE:
            StructuredNode.refresh(self)
        else:
            logging.warning("[Base::refresh] not allowed in 'offline' mode")

    def cypher (self, query, params=None):
        logging.debug("[Base::refresh] entering method")

        if not config.MODEL_MODE_OFFLINE:
            return StructuredNode.cypher(self, query, params=params)
        else:
            logging.warning("[Base::cypher] not allowed in 'offline' mode")
        return None

    def execute_transaction (self, query, params={}):
        logging.debug("[Base::execute_transaction] entering method")
        data = None
        db.begin()
        try:
            data = db.cypher_query(query, params)
            db.commit()
        except Exception as e:
            db.rollback()
        return data

    def pre_save (self):
        logging.debug("[Base::pre_save] entering method")

        #KLUDGE: specific for harvesting and offline to online + alias resolution issues
        if hasattr(self, "_z_alias"):
            uid,rid = AliasResolver.instance().resolve(self.__class__, getattr(self, "_z_alias"), also_return_rid=True)
            if uid is not None: self.uid = uid
            if rid is not None: self.rid = uid

        self.__prepare__()
        if hasattr(self, "prepare"): getattr(self, "prepare")()

        is_valid = getattr(self, "validate")() if hasattr(self, "validate") else True
        if not is_valid:
            raise ValueError("[Base::pre_save] {0}.{1}() attempted on deleted node".format(self.__class__.__name__, "save"))

        self.merge (self.__class__.nodes.get_or_none(uid=self.uid))

    def post_save (self):
        logging.debug("[Base::post_save] entering method")
        self.__current_hash = self.hash()

    def pre_delete (self):
        logging.debug("[Base::pre_delete] entering method")

        self.__prepare__()
        if hasattr(self, "prepare"): getattr(self, "prepare")()

        is_valid = getattr(self, "validate")() if hasattr(self, "validate") else True
        if not is_valid:
            raise ValueError("[Base::pre_delete] {0}.{1}() attempted on deleted node".format(self.__class__.__name__, "delete"))

    def post_delete (self):
        logging.debug("[Base::post_delete] entering method")

    def post_create (self):
        logging.debug("[Base::post_create] entering method")

    def get_related (self):
        logging.debug("[Base::get_related] entering method")
        rst = []
        for r in [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]:
            e = getattr(self, r)
            if hasattr(e, "related"):
                for a in getattr(self, r).related:
                    rst.append(a[0].uid)
                    rst.extend(a[0].get_related())
            else:
                logging.debug("[Base::get_related] only has sense in offline mode")
        return list(dict.fromkeys(rst)) if len(rst) else rst

    @property
    def first_born (self):
        return self._first_born
    @first_born.setter
    def first_born (self, value):
        self._first_born = bool(value)

    @property
    def scaffold (self):
        s = self.__class__()
        s.uid = self.uid
        s.rid = self.rid

        properties = [p for p in dir(self) if hasattr(self.__class__, p) and isinstance(getattr(self.__class__, p), Property)]
        properties = [p for p in properties if getattr(self.__class__, p).required]
        for p in properties: setattr(s, p, getattr(self, p))

        if hasattr(self, "id"): s.id = self.id
        return s

    @property
    def node (self):
        s = self.__class__()
        s.uid = self.uid
        s.rid = self.rid

        properties = [p for p in dir(self) if hasattr(self.__class__, p) and isinstance(getattr(self.__class__, p), Property)]
        for p in properties: setattr(s, p, getattr(self, p))

        if hasattr(self, "id"): s.id = self.id
        return s

    @property
    def isDirty (self): 
        return self.__current_hash != self.hash()

    @property
    def currentModelOffline (self): 
        return self._current_mode_offline

    @property
    def currentRID (self):
        return self.rid if self.rid is not None else _INTERNAL_BASE_UID_RAWID_CACHE.get(self.uid)

    @classmethod
    def getDirectMode (cls):
        return config.MODEL_DIRECT_MODE
    
    @classmethod
    def setModelOffline (cls, value): 
        config.MODEL_MODE_OFFLINE = True if value else False
    @classmethod
    def getModelOffline (cls): 
        return config.MODEL_MODE_OFFLINE
    
    @classmethod
    def getBaseClass (cls):
        logging.debug("[Base::getBaseClass] entering method")

        rst = cls.__name__
        for cls in inspect.getmro(cls):
            if cls.__name__ == "Base": break
            rst = cls.__name__
        return rst

    @classmethod
    def buildURI (cls, *args):
        args = [str(a) for a in args]
        args = [a.strip() for a in args]

        uid = ":".join(args)
        uid = uid.upper()
        uid = uid if isinstance(uid, str) else str(uid)

        scope = cls.getBaseClass().lower()
        uri = "{domain}/{scope}/{id}".format(domain=config.MODEL_SETTING_UID_DOMAIN, scope=scope, id=hashlib.sha1(uid.encode("utf-8")).hexdigest())

        if config.MODEL_SETTING_SAVE_RAWID: _INTERNAL_BASE_UID_RAWID_CACHE[uri] = uid
        
        return uri

    @classmethod
    def buildRID (cls, *args):
        args = [str(a) for a in args]
        args = [a.strip() for a in args]

        uid = ":".join(args)
        uid = uid.upper()
        uid = uid if isinstance(uid, str) else str(uid)

        return uid

    @classmethod        
    def buildSourceURI (cls, source, *args):
        source = [str(s) for s in source]
        source = [s.strip() for s in source]
        source = '/'.join(source)

        args = [str(a) for a in args]
        args = [a.strip() for a in args]

        uid = ":".join(args)
        uid = uid.upper()
        uid = uid if isinstance(uid, str) else str(uid)
        
        scope = cls.getBaseClass().lower()
        uri = "{domain}/{scope}/{source}/{id}".format(domain=config.MODEL_SETTING_UID_DOMAIN, scope=scope, source=source, id=hashlib.sha1(uid.encode("utf-8")).hexdigest())
        
        return uri

    @classmethod
    def findUIDByAlias (cls, alias=None):
        return AliasResolver.instance.resolve(cls, alias, also_return_rid=False)
        
    @staticmethod
    def extractResourceClassFromSerialized (data):
        data = json.loads(data) 
        rst = getattr(sys.modules[__name__], data["@type"])
        return  rst

    @staticmethod
    def registerUnsavedNode (node, value=None):
        if not hasattr(node, "id"): 
            if value is None:
                rst = StructuredNode.save(node.node)
                node.id = rst.id
            else:
                node.id = value
        return node.id

#######################################################################
## MERGER
#######################################################################
class Merger (object):

    def __init__ (self):
        logging.debug("[Merger::__init__] entering method")

    def merge (self, node, includes=None, excludes=None):
        logging.debug("[Merger::merge] entering method")

        if node is None:
            pass
        elif isinstance(node,StructuredNode):

            properties = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), Property)]
            for key in properties:
                if includes is not None and key not in includes: continue
                if excludes is not None and key in excludes: continue

                val = getattr(self, key)
                other = getattr(node, key)
                setattr(self, key, self.mergePolicy(key, val, other))
            else:
                if self.uid == node.uid and hasattr(node, "id"): self.id = node.id

            relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
            for key in relationships:
                if includes is not None and key not in includes: continue
                if excludes is not None and key in excludes: continue

        elif isinstance(node, dict):

            properties_map = {"id": "gid", "uid": "@id"}
            properties = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), Property)]
            for key in properties:
                val = getattr(self, key)
                other = node.get(properties_map.get(key, key))
                self.mergePolicy(key, val, other)
            else:
                if val.uid == other.uid and hasattr(other, "id"): val.id = other.id
                if val.uid == other.uid: val.rid = other.rid

            relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
            for key in relationships:
                if includes is not None and key not in includes: continue
                if excludes is not None and key in excludes: continue

                for node in getattr(self, key):
                    logging.debug("[Merger::merge] todo merge relationship '{}:{}'".format(key, node.uid))

        else:
            raise ValueError("[Base::merge] node must be a instance of StructuredNode or dict")

    def mergePolicy (self, key, value, other):
        logging.debug("[Merger::mergePolicy] entering method")
        if value is None and other is None: return value

        if key in ("uid", "rid", "visited", "updated"): return value

        if key in ("created", "modified"):
            value = other if value is None else value
            other = value if other is None else other

            which = True if "created" == key and value > other else False
            which = True if "modified" == key and value < other else which
            return other if which else value

        if isinstance(value, ArrayProperty):
            value = [] if value is None else value
            value = [str(v) for v in value]
            other = [] if other is None else other
            other = [str(v) for v in other]

            other.extend([v for v in value if v not in other])
            value = []; [value.append(o) for o in other if o not in value]
            return value

        if isinstance(value, JSONProperty):
            logging.warning("[Merger::mergePolicy] TODO JSONProperty logic")
        if isinstance(value, EmailProperty):
            logging.warning("[Merger::mergePolicy] TODO EmailProperty logic")
        if isinstance(value, RegexProperty):
            logging.warning("[Merger::mergePolicy] TODO RegexProperty logic")
        if isinstance(value, UniqueIdProperty):
            logging.warning("[Merger::mergePolicy] TODO UniqueIdProperty logic")
        
        return value if value is not None else other
#######################################################################
## SERIALIZER
#######################################################################
class Serializer (object):

    def __init__ (self):
        logging.debug("[Serializer::__init__] entering method")

    def serialize (self, return_as_string=True, include_relationships=True, avoid_offline_restriction=False, exclude_set=None):
        def _process_serialize_item (i):
            r = None
            if isinstance(i, StructuredNode):
                r = i.serialize(return_as_string=False, include_relationships=include_relationships)
            elif isinstance(i, ArrayProperty):
                r = i.serialize(return_as_string=False, include_relationships=include_relationships)
            elif isinstance(i, JSONProperty):
                r = i.serialize(return_as_string=False, include_relationships=include_relationships)
            elif isinstance(i, dict):
                r = {k:_process_serialize_item(v) for k,v in i.items()}
            elif isinstance(i, list):
                r = [_process_serialize_item(v) for v in i]
            elif isinstance(val, datetime):
                r = i.strftime("%Y-%m-%dT%H:%M:%S")
            elif is_primitive(i):
                r = i
            elif isinstance(i, namespace.Namespace):
                r = str(i)
            elif inspect.ismethod(i):
                logging.warning("[Serializer::serialize] {} is method ({})".format(key, key, self.__class__.__name__))
            else:
                logging.warning("[Serializer::serialize] not know how to process '{}'({})".format(key, type(i)))
            return r

        logging.debug("[Serializer::serialize] entering method")
        #if not config.MODEL_MODE_OFFLINE and not avoid_offline_restriction: raise Exception("serialization is only allowed in 'OFFLINE' mode")

        self.rid = _INTERNAL_BASE_UID_RAWID_CACHE.get(self.uid) if self.rid is None else self.rid
        rst = {"@id": str(self.uid), "@type": self.getBaseClass(), "rid": self.rid}
        if hasattr(self, "id"): rst["gid"] = self.id

        properties = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), Property)]
        for key in properties:
            if key in ("uid", "rid"): continue
            if exclude_set is not None and key in exclude_set: continue

            val = getattr(self, key)
            if val is None: continue
            rst[key] = _process_serialize_item(val)

        if include_relationships:
            relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
            for key in relationships:
                if exclude_set is not None and key in exclude_set: continue

                val = []
                for node,prp in getattr(self, "_offline_{}".format(key)).related:
                    rel = _process_serialize_item(node)
                    if prp is not None:
                        prp = {k:v for k,v in prp.items()}
                        if "id" in prp: 
                            prp["gid"] = prp["id"]; del prp["id"]
                        rel["@metadata"] = prp
                    val.append(rel)
                if len(val): rst[key] = val
        return json.dumps(rst, sort_keys=True) if return_as_string else rst

    @classmethod
    def deserialize (cls, data, force_deserialize_class=False):
        def _process_deserialize_datetime (s):
            try:
                dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S") if s is not None else s
            except Exception as e: 
                dt = None
            return dt

        def _process_deserialize_item (u,i):
            r = None
            if isinstance(i, dict):
                if "@type" in i:
                    r = cls.deserialize(i)
                    if "@metadata" in i: setattr(r, "_metadata", i["@metadata"])
                else:
                    r = {k:_process_deserialize_item(u,v) for k,v in i.items()}
            elif isinstance(i, list):
                r = [_process_deserialize_item(u,v) for v in i]
            elif isinstance(i, str):
                r = _process_deserialize_datetime(i)
                r = i if r is None else r
            elif is_primitive(i):
                r = i
            else:
                logging.warning("[Serializer::serialize] not know how to process '{}'({})".format(key, type(i)))
            return r

        logging.debug("[Serializer::deserialize] entering method")
        #if not config.MODEL_MODE_OFFLINE: raise Exception("deserialization is only allowed in 'OFFLINE' mode")

        data = json.loads(data) if not isinstance(data, dict) else data
        type = data.get("@type")
        uid = data.get("@id")

        gid = data.get("gid")
        
        module = sys.modules[__name__]
        cls = reduce(lambda a,b: a or (b[1] if type == b[0] else None), inspect.getmembers(module, inspect.isclass), None) if not force_deserialize_class else cls
        if cls is None:
            logging.warning("[Serializer::deserialize] not found model for type '{}'".format(type)); 
            return None
        
        logging.debug("[Serializer::deserialize] processing {} ({})".format(type, uid))

        my_self = cls()
        my_self.uid = uid
        my_self.rid = data.get("rid")

        if gid: my_self.id = gid

        for key,val in data.items():
            try:
                if key in ("@id", "@type", "@metadata", "uid", "rid", "gid"): continue
                val = _process_deserialize_item(uid, val)
                rel = getattr(my_self, "_offline_{}".format(key), None)
                if rel is not None:
                    for itm in val:
                        prp = getattr(itm, "_metadata", None)
                        if prp is not None:
                            if "gid" in prp:
                                prp["id"] = prp["gid"]; del prp["gid"]
                        rel.connect(itm, properties=prp)

                        #KLUDGE: specific for harvesting and offline to online + alias resolution issues
                        if "alias" == key and prp is not None:
                            if not hasattr(my_self, "_z_alias"): setattr(my_self, "_z_alias", [])
                            getattr(my_self, "_z_alias").append(prp["uri"])
                else:
                    setattr(my_self, key, val)
            except Exception as e: 
                logging.warning("[Serializer::deserialize] deserializartion process fails '{}'".format(e))
                print(format_exception(e))
                return None

        return my_self
    
    def toJSON (self):
        logging.debug("[Serializer::toJSON] entering method")
        return self.serialize()
    
    @staticmethod
    def fromJSON (data):
        logging.debug("[Serializer::fromJSON] entering method")
        what = Base.extractResourceClassFromSerialized(data)
        return what.deserialize(data)

    def toAVRO (self):
        logging.debug("[Serializer::toAVRO] entering method")
        logging.warn("[Serializer::toAVRO] not implemented.")
        return None
    
    @staticmethod
    def fromAVRO (data):
        logging.debug("[Serializer::fromAVRO] entering method")
        logging.warn("[Serializer::fromAVRO] not implemented.")
        return None

    def toPARQUET (self):
        logging.debug("[Serializer::toPARQUET] entering method")
        logging.warn("[Serializer::toPARQUET] not implemented.")
        return None
    
    @staticmethod
    def fromPARQUET (self):
        logging.debug("[Serializer::fromPARQUET] entering method")
        logging.warn("[Serializer::fromPARQUET] not implemented.")
        return None

    def toTURTLE (self):
        logging.debug("[Serializer::toTURTLE] entering method")
        logging.warn("[Serializer::toTURTLE] not implemented.")
        return None
    
    @staticmethod
    def fromTURTLE (self):
        logging.debug("[Serializer::fromTURTLE] entering method")
        logging.warn("[Serializer::fromTURTLE] not implemented.")
        return None

    def toJSONLD (self):
        logging.debug("[Serializer::toTURTLE] entering method")
        logging.warn("[Serializer::toJSONLD] not implemented.")
        return None
    
    @staticmethod
    def fromJSONLD (self):
        logging.debug("[Serializer::fromtoTURTLE] entering method")
        logging.warn("[Serializer::fromJSONLD] not implemented.")
        return None

#######################################################################
## MODEL CLASSES
#######################################################################
def __constructor__(self, **kwargs):
    def _fix_model_relations ():
        for k in dir(self.__class__):
            v = getattr(self.__class__, k)
            if isinstance(v, RelationshipDefinition):
                if v.definition.get("node_class", object) is Base or "Base" == v._raw_class:
                    logging.debug("[{}:__constructor__] create -offline- relationship with attributes '{}'".format(self.__class__.__name__, v.definition["relation_type"]))
                    c = RelationshipTo  if 1 == v.definition["direction"] else RelationshipFrom
                    c = Relationship  if -1 == v.definition["direction"] else c
                    r = c(self.__class__, v.definition["relation_type"], cardinality=v.manager, model=v.definition["model"])
                    setattr(self.__class__, k, r)
                else:
                    logging.debug("[{}:__constructor__] create -offline- relationship '{}'".format(self.__class__.__name__, v.definition["relation_type"]))
                setattr(self, "_offline_{}".format(k), OfflineRelationshipManager(k))
                setattr(self.__class__, "transform_to_online", __offline_to_online__)
                setattr(self.__class__, "transform_to_offline", __online_to_offline__)
                setattr(self.__class__, "register_unsaved_nodes", __register_nodes__)
                setattr(self.__class__, "fix_multiple_labels", __fix_multiple_labels__)
                setattr(self.__class__, "direct_save",__direct__save__)
                setattr(self.__class__, "direct_delete",__direct__delete__)
                setattr(self.__class__, "direct_merge",__direct__merge__)
                setattr(self.__class__, "direct_split",__direct__split__)
                setattr(self.__class__, "direct_process_properties",__direct_process_properties__)
                setattr(self.__class__, "direct_process_relation_properties",__direct_process_relation_properties__)
                setattr(self.__class__, "direct_prepare_string",__direct_prepare_string__)
                setattr(self.__class__, "TOPIC", register_model._models[self.__class__.__name__][0])

    _fix_model_relations()

    mro = register_model._models[self.__class__.__name__]
    classes = inspect.getmro(self.__class__)
    for cls in classes[1:]:
        if not hasattr(cls, "__init__"): continue
        if cls is Base:
            setattr(cls, "__label__", self.__class__.__name__)
            cls.__init__(self, **kwargs)
        elif issubclass(cls, Serializer):
            cls.__init__(self)
        elif issubclass(cls, Merger):
            cls.__init__(self)
        elif cls.__name__ in ("StructuredNode", "NodeBase", "PropertyManager"):
            pass
        elif cls is object: 
            pass
        else:
            cls.__init__(self)

def __register_nodes__ (self, rst={}):
    def _is_non_property (k):
        rst = k not in properties 
        rst = rst and not k.startswith('_') 
        rst = rst and hasattr(self.__class__, k)
        rst = rst and not isinstance(getattr(self.__class__, k), RelationshipDefinition)
        rst = rst and k not in ("id")
        return rst

    logging.debug("[{}::register_nodes] entering method".format(self.__class__.__name__))
    if config.MODEL_MODE_OFFLINE: raise ValueError("[{}::register_nodes] not allowed in 'offline' mode")

    rst[self.uid] = Base.registerUnsavedNode(self, value=rst.get(self.uid))

    properties = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), Property)]
    non_properties = [a for a in self.__dict__ if _is_non_property(a)]
    for key in non_properties:
        logging.warning("[{}::register_nodes] found attribute '{}' not defined as properties".format(self.__class__.__name__, key))

    relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
    for key in relationships:
        relationship = getattr(self, key) 
        for node in relationship:
            if node.uid in rst:
                node.id = rst[node.uid]
            else: 
                node.register_unsaved_nodes(rst=rst)

    return rst

def __fix_multiple_labels__ (self):
    def _transverse_nodes (n):
        if n.id not in node_id: 
            node_id.append(n.id); node_class.append(n.__class__)

        relationships = [a for a in dir(n) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
        for key in relationships:
            relationship = getattr(n, "_offline_{}".format(key)) if n._current_mode_offline else  getattr(n, key) 
            for r in relationship:
                rid = "{}${}".format(r.id, r.__class__)
                if r.id not in node_id: _transverse_nodes(r)

    logging.debug("[{}::fix_multiple_labels] entering method".format(self.__class__.__name__))
    if config.MODEL_MODE_OFFLINE: raise ValueError("[{}::fix_multiple_labels] not allowed in 'offline' mode")

    node_id = []; node_class = []
    _transverse_nodes(self)

    for idx in range(len(node_id)):
        _id = node_id[idx]; _class = node_class[idx]
        node = _class()
        node.id = _id
        node.refresh()
        
        labels = [l for l in node.labels() if l != node.__label__]
        for label in labels:
            stm = "MATCH (n) WHERE id(n)={id} REMOVE n:{label}".format(id=node.id, label=label)
            self.cypher(stm)

def __offline_to_online__ (self):
    logging.debug("[{}::transform_to_online] entering method".format(self.__class__.__name__))
    
    if self._current_mode_offline:
        Base.registerUnsavedNode(self)

        relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
        for key in relationships:
            online_relationships = getattr(self, key)
            offline_relationships = getattr(self, "_offline_{}".format(key))
            for node in offline_relationships:
                
                if "alias" == key: 
                    node.id = self.id if self.uid == node.uid else Base.registerUnsavedNode(node)
                else:
                    Base.registerUnsavedNode(node)
                    node.transform_to_online()
                    
                for relation in offline_relationships.all_relationships(node):
                    if relation is not None: 
                        if isinstance(online_relationships, ZeroOrOne): 
                            online_relationships.disconnect(node)
                        properties = relation.data
                    else:
                        properties = None
                    try:
                        online_relationships.connect(node, properties)
                    except Exception as e:
                        print(format_exception(e))
            else:
                offline_relationships.related.clear()

    config.MODEL_MODE_OFFLINE = self._current_mode_offline = False    
    
def __online_to_offline__ (self):
    logging.debug("[{}::transform_to_offline] entering method".format(self.__class__.__name__))
    
    if not self._current_mode_offline:
        relationships = [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]
        for key in relationships:
            offline_relationships = getattr(self, "_offline_{}".format(key))
            offline_relationships.related.clear()
            online_relationships = getattr(self, key)
            for node in online_relationships:
                node.transform_to_offline()
                for relation in online_relationships.all_relationships(node):
                    properties = {key: getattr(self, key) for key in relation.__dict__}
                    offline_relationships.connect(node, properties)

    config.MODEL_MODE_OFFLINE = self._current_mode_offline = False

def __direct__save__ (self):
    logging.debug("[{}::__direct__save] entering method".format(self.__class__.__name__))

    if hasattr(self, "__prepare__"): 
        getattr(self, "__prepare__")()
        if hasattr(self, "prepare"): getattr(self, "prepare")()
        is_valid = getattr(self, "validate")() if hasattr(self, "validate") else True
        if not is_valid:
            logging.warning("[{}::__direct__save] TODO - handle not valid resource".format(self.__class__.__name__))
    
    ## step 0 - split nodes and relationship
    properties,relationships = self.direct_split()

    ## step 1 - get node
    query = "MATCH (n:{label}) WHERE n.uid = '{uid}' RETURN n".format(label=self.__label__, uid=self.uid)
    data = db.cypher_query(query, {})
    if 0 == len(data[0]):
        query = "MERGE (n:{label} {{uid: '{uid}', rid: '{rid}'}}) RETURN n".format(label=self.__label__, uid=self.uid, rid=self.rid)
        data = self.execute_transaction(query)
        data = data[0][0][0]; data = dict(zip(data.keys(), data.values()))
    elif 1 == len(data[0]):
        data = data[0][0][0]; data = dict(zip(data.keys(), data.values()))
    else: 
        logging.error("[{label}::__direct__save] found more than one node ({uid}, {count})".format(label=self.__label__, uid=self.uid, count=len(data[0])))
        return self
    
    ## step 2 - merge node
    properties = self.direct_merge(properties, data)

    ## step 3 - save node
    set_stm = self.direct_process_properties(properties)
    query = "MATCH (n:{label} {{uid: '{uid}'}}) SET {properties} RETURN id(n) as n".format(label=self.__label__, uid=self.uid, properties=set_stm)
    data = self.execute_transaction(query)

    ## step 3 - get relationaships
    g_r = {}
    query = """
        MATCH (n:{label})-[r]->(m) 
        WHERE n.uid = '{uid}' 
        RETURN n.uid as source,  m.uid as target, type(r) as role, labels(m) as target_type, m.rid as target_rid, properties(r) as properties"""
    query = query.format(label=self.__label__, uid=self.uid)
    data = db.cypher_query(query, {})
    for p in data[0]:
        g_r_key = "{}$&${}$&${}$&${}$&${}".format(p[0],p[1],p[2],p[3],p[4])
        if g_r_key not in g_r: g_r[g_r_key] = []
        g_r[g_r_key].append(p[5])

    n_r = {}
    for r in relationships:
        for p in relationships[r]:
            n_r_key = "{}$&${}$&${}$&${}$&${}".format(p[0],p[1],p[2],p[4],p[5])
            if n_r_key not in n_r: n_r[n_r_key] = []
            n_r[n_r_key].append(p[3])
    
    ## step 4 - merge relationships
    d_r = [r for r in g_r if r not in n_r]
    u_r = [r for r in n_r if r in g_r]

    for r in u_r:
        for k in g_r[r]: 
            #n_r[r] = g_r[r]
            logging.debug("[{}::__direct__save] TODO merge '{}'".format(self.__class__.__name__, k))

    ## step 5 - register relationships
    for r in n_r:
        if n_r[r] is None: continue

        p = r.split("$&$")
        for c in n_r[r]:
            c = {} if c is None else c
            
            r_p = []
            for k in c:
                if hasattr(self.__class__, r):
                    r_p.append((k, hasattr(self.__class__, r), c[k]))
                else:        
                    r_p.append((k, StringProperty, c[k])) 

            query = "MATCH (n:{label}) WHERE n.uid = '{uid}' RETURN n".format(label=p[3], uid=p[1])
            data = db.cypher_query(query, {})
            if 0 == len(data[0]):
                query = "MERGE (n:{label} {{uid: '{uid}', rid: '{rid}'}}) RETURN n".format(label=p[3], uid=p[1], rid=p[4])
                data = self.execute_transaction(query)

            my_properties = self.direct_process_relation_properties(r_p)
            query = """ 
                MATCH (n {{ uid: '{uid_from}' }})
                MATCH (m {{ uid: '{uid_to}' }})
                MERGE (n)-[r:{label} {{ {properties} }}]->(m) 
                RETURN id(r) as r   
            """
            query = query.format(uid_from=p[0], uid_to=p[1], label=p[2], properties=my_properties)
            data = self.execute_transaction(query)
    
    ## step 6 - register child node
    properties_minimal = ['active', 'permission', 'rid', 'sources', 'uid', 'visibility', 'visited', 'updated']

    for r in [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]:
        if getattr(self, r) is None: continue
        for a in getattr(self, r).related:
            node_current = a[0]
            properties_current = [p for p in node_current.properties() if p not in properties_minimal]
            if True or 0 != len(properties_current): 
                node_current.direct_save()
            else:
                pass
            
    return self
    
def __direct__delete__ (self):
    logging.debug("[{}::__direct__delete] entering method".format(self.__class__.__name__))

def __direct__merge__ (self, properties, data):
    logging.debug("[{}::__direct__merge] entering method".format(self.__class__.__name__))

    l = {properties[i][0]:i for i in range(len(properties))}
    for k,v in data.items():
            if k not in l:
                properties.append((k, getattr(self.__class__, k), v))
            elif "sources" == k:
                v.extend(properties[l[k]][2])
                properties[l[k]] = (k, getattr(self.__class__, k), list(set([str(n) for n in v])))
    else:
        if "updated" not in data:
            properties[l["updated"]] = ("updated", getattr(self.__class__, "updated"), datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
        if "visited" not in data:
            properties[l["visited"]] = ("visited", getattr(self.__class__, "visited"), datetime.now())
    return properties

def __direct__split__ (self):
    logging.debug("[{}::__direct__split__] entering method".format(self.__class__.__name__))
    
    properties = []
    for p in self.properties(): properties.append((p, getattr(self.__class__, p), getattr(self, p)))

    relationships = {}
    for r in [a for a in dir(self) if hasattr(self.__class__, a) and isinstance(getattr(self.__class__, a), RelationshipDefinition)]:
        if getattr(self, r) is None: continue
        for a in getattr(self, r).related:
            d = getattr(self.__class__, r).definition
            if r not in relationships: relationships[r] = []
            relationships[r].append((self.uid, a[0].uid, d["relation_type"], a[1], a[0].__label__, a[0].rid))

    return properties,relationships

def __direct_process_properties__ (self, properties):
    stms = []
    for p in properties:
        stm = None
        if isinstance(p[1], ArrayProperty):
            stm = "n.{} = [{}]".format(p[0], ','.join(["'{}'".format(s) for s in p[2]]))
        elif isinstance(p[1], BooleanProperty):
            stm = "n.{} = {}".format(p[0], "True" if p[2] else "False")
        elif isinstance(p[1], DateTimeFormatProperty):
            stm = "n.{} = {}".format(p[0], "datetime('{}')".format(str(p[2]).replace(' ', 'T')))
        elif isinstance(p[1], EmailProperty):
            stm = "n.{} = '{}'".format(p[0], p[2])
        elif isinstance(p[1], FloatProperty):
            stm = "n.{} = {}".format(p[0], p[2])
        elif isinstance(p[1], IntegerProperty):
            stm = "n.{} = {}".format(p[0], p[2])
        elif isinstance(p[1], RegexProperty):
            stm = "n.{} = '{}'".format(p[0], p[2])
        elif isinstance(p[1], StringProperty):
            stm = "n.{} = \"{}\"".format(p[0], self.direct_prepare_string(p[2]))
        elif isinstance(p[1], UniqueIdProperty):
            stm = "n.{} = \"{}\"".format(p[0], p[2])
        elif isinstance(p[1], JSONProperty):
            pass
        if stm is not None: stms.append(stm)
    stms = ', '.join(stms)
    return stms

def __direct_process_relation_properties__ (self, properties):
    stms = []
    for p in properties:
        stm = None
        if isinstance(p[1], ArrayProperty) or p[1] is ArrayProperty:
            stm = "{}: [{}]".format(p[0], ','.join(["'{}'".format(s) for s in p[2]]))
        elif isinstance(p[1], BooleanProperty) or p[1] is BooleanProperty:
            stm = "{}: {}".format(p[0], "True" if p[2] else "False")
        elif isinstance(p[1], DateTimeFormatProperty) or p[1] is DateTimeFormatProperty:
            stm = "{}: {}".format(p[0], "datetime('{}')".format(str(p[2]).replace(' ', 'T')))
        elif isinstance(p[1], EmailProperty) or p[1] is EmailProperty:
            stm = "{}: '{}'".format(p[0], p[2])
        elif isinstance(p[1], FloatProperty) or p[1] is FloatProperty:
            stm = "{}: {}".format(p[0], p[2])
        elif isinstance(p[1], IntegerProperty) or p[1] is IntegerProperty:
            stm = "{}: {}".format(p[0], p[2])
        elif isinstance(p[1], RegexProperty) or p[1] is RegexProperty:
            stm = "{}: '{}'".format(p[0], p[2])
        elif isinstance(p[1], StringProperty) or p[1] is StringProperty:
            stm = "{}: \"{}\"".format(p[0], self.direct_prepare_string(p[2]))
        elif isinstance(p[1], UniqueIdProperty) or p[1] is UniqueIdProperty:
            stm = "{}: \"{}\"".format(p[0], p[2])
        elif isinstance(p[1], JSONProperty) or p[1] is JSONProperty:
            pass
        if stm is not None: stms.append(stm)
    stms = ', '.join(stms)
    return stms

def __direct_prepare_string__ (self, value):
    if value is None: return ''
    try:
        value = str(value)
        value = value.replace('"', "'")
    except Exception as e:
        logging.warning("[{}::__direct_prepare_string__] entering method".format(self.__class__.__name__))
    return value


def register_model (name, topic, implementation, merger=Merger, serializer=Serializer):
    register_model._models[name] = (topic.upper(), implementation, merger, serializer)

    module = sys.modules[__name__]
    model = type(name,(Base, implementation, merger, serializer) ,{"__init__": __constructor__})

    setattr(module, name, model)
    module = sys.modules['.'.join(__name__.split('.')[:-1])]
    setattr(module, name, model)
    return model
register_model._models = {}

register_model("Api", "api", ApiImpl)
register_model("ApiOperation", "aop", ApiOperationImpl)
register_model("ApiOperationParameter", "app", ApiOperationParameterImpl)
register_model("Address", "add", AddressImpl)
register_model("Catalog", "cat", CatalogImpl)
register_model("Concept", "cnp", ConceptImpl)
register_model("ConceptScheme", "cns", ConceptSchemeImpl)
register_model("ContactPoint", "cpt", ContactPointImpl)
register_model("Dataset", "dat", DatasetImpl)
register_model("Distribution", "dis", DistributionImpl)
register_model("Document", "doc", DocumentImpl)
register_model("Equipment", "eqp", EquipmentImpl)
register_model("Facility", "fct", FacilityImpl)
register_model("Frequency", "frq", FrequencyImpl)
register_model("Organization", "org", OrganizationImpl)
register_model("Person", "per", PersonImpl)
register_model("Platform", "plf", PlatformImpl)
register_model("Program", "prg", ProgramImpl)
register_model("Project", "prj", ProjectImpl)
register_model("Relation", "rel", RelationImpl)
register_model("Resource", "res", ResourceImpl)
register_model("Spatial", "spt", SpatialImpl)
register_model("Sensor", "snr", SensorImpl)
register_model("Service", "srv", ServiceImpl)
register_model("Software", "sft", SoftwareImpl)
register_model("SoftwareSource", "sfs", SoftwareSourceImpl)
register_model("Temporal", "tmp", TemporalImpl)
register_model("Text", "txt", TextImpl)
register_model("Variable", "var", VariableImpl)
register_model("Vcard", "vcd", VcardImpl)
register_model("WebService", "wsr", WebServiceImpl)
register_model("WebPage", "pge", WebPageImpl)
register_model("WebSite", "ste", WebSiteImpl)
