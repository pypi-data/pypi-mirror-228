#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import inspect
import json
import logging
import os
import re
import sys
import types

import requests

import orcid

from socib.resource_catalog.annotations import singleton
from socib.resource_catalog.utils import dict_to_dict_lowercase

__all__ = []

#######################################################################
## NAMESPACE
#######################################################################
class Namespace(str):

    def __init__(self, namespace):
        self._namespace = namespace.upper()

    def qname(self, name):
        value = None
        if name is not None: 
            value = "{}:{}".format(self._namespace, str(name)) 
        return value

    def __getattr__(self, name):
        if name.startswith("_"): 
            raise AttributeError
        else:
            return self.qname(name)

    def __str__(self):
        return self._namespace.upper()

    def __repr__(self):
        return self._namespace.upper()


#######################################################################
## ROR NAMESPACE
#######################################################################
class RORNamespace(Namespace):
    def __init__ (self, namespace):
        logging.debug("[RORNamespace::__init__] entering method")
        Namespace.__init__(self, namespace)
    
    def extractMetadata (self, rorID, proxies=None):
        data = None
        try:
            m = re.match(self.extractMetadata._ROR_API_PATTERN, rorID) 
            if m:
                rorID = m.group("ID") if m else rorID
            else:
                m = re.match(self.extractMetadata._ROR_URL_PATTERN, rorID)
                rorID = m.group("ID") if m else rorID 

            url = self.extractMetadata._ROR_API_GET_URL.format(id=rorID)
            response = requests.get(url, verify=False, allow_redirects=True, proxies=proxies)
            
            if requests.codes.ok == response.status_code:
                data = response.json()
                data = dict_to_dict_lowercase(data)
                data["aliases"] = [data["id"]] #warning overwrite existing 'aliases' property, previous information is lost!!!
                for k,v in self.extractMetadata._ROR_ORG_REFERENCES.items():
                    if k in data["external_ids"]:
                        data["external_ids"][k]["all"] = data["external_ids"][k]["all"] if isinstance(data["external_ids"][k]["all"], list) else [data["external_ids"][k]["all"]]
                        data["aliases"].extend([v.format(id=i) for i in data["external_ids"][k]["all"]])
        except Exception as e: 
            pass
        return data
    
    extractMetadata._ROR_URL_PATTERN = re.compile(r"https://ror.org/(?P<ID>[\w]+)")
    extractMetadata._ROR_API_PATTERN = re.compile(r"http(s)?://api.ror.org/organizations/(?P<ID>[\w]+)")
    extractMetadata._ROR_API_GET_URL = "https://api.ror.org/organizations/{id}"
    extractMetadata._ROR_ORG_REFERENCES = {
        "ror": "https://ror.org/{id}",
        "isni": "http://isni.org/isni/{id}",
        "wikidata": "https://www.wikidata.org/wiki/{id}",
        "fundref": "https://api.crossref.org/funders/{id}",
        "grid": "https://grid.ac/institutes/{id}",
    }

    def findByName (self, name, proxies=None):
        rorID = None
        try:
            url = self.findByName._ROR_API_SEARCH_URL.format(name=name, proxies=proxies)
            response = requests.get(url)
            
            if requests.codes.ok == response.status_code:
                data = response.json()
                if 1 == data["number_of_results"]: rorID = data["items"][0]["id"]
        except Exception as e:
            pass
        return rorID
    findByName._ROR_API_SEARCH_URL = "https://api.ror.org/organizations?query={name}"

#######################################################################
## ORCID NAMESPACE
#######################################################################
class ORCIDNamespace(Namespace):

    def __init__ (self, namespace):
        logging.debug("[ORCIDNamespace::__init__] entering method")
        Namespace.__init__(self, namespace)
        self.client = None
    
    def connect (self, key, secret):
        self.client = orcid.PublicAPI(key, secret)

    def resolve (self, terms, proxies=None):
        logging.debug("[ORCIDResolver:resolve] entering method")
        if terms is None: return None
        if self.client is None: return None
            
        query_terms = []
        for t in terms if isinstance(terms, list) else [terms]:
            
            if isinstance(t, dict):
                for key in t:
                    if "given-names" == key: query_terms.append('given-names: "{}"'.format(t[key]))
                    if "family-name" == key: query_terms.append('family-name: "{}"'.format(t[key]))
                    if "email" == key: query_terms.append('email: "{}"'.format(t[key]))
            elif isinstance(t, str) and re.match(self.resolve._re_pattern_email, t):
                query_terms.append('email: "{}"'.format(terms))
            elif isinstance(t, str): 
                query_terms.append('"{}"'.format(terms))
        else:
            if 0 == len(query_terms): return None
        
        try:
            query = " AND ".join(query_terms)
            if query in self.resolve._cache: return self.resolve._cache[query]

            rst = self.client.search(query)

            if 1 == len(rst["result"]): 
                self.resolve._cache[query] = rst['result'][0]['orcid-identifier']['uri']
                logging.debug("[ORCIDResolver:resolve] Found ORCID profile({}): {}".format(query, rst['result'][0]['orcid-identifier']['uri']))
                return rst['result'][0]['orcid-identifier']['uri']
        except Exception as e:
            logging.debug("[ORCIDResolver:resolve] something wrong with query({})".format(query))
        return None
    resolve._cache = {}
    resolve._re_pattern_email = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    
    def buildResolveTerm (self, given_name=None, family_name=None, email=None):
        rst = {}
        if given_name is not None: rst["given-names"] = given_name
        if family_name is not None: rst["family-name"] = family_name
        if email is not None: rst["email"] = email
        return rst


#######################################################################
## NAMESPACE MANAGER
#######################################################################
@singleton
class NamespaceManager():
    def registerNamespace (self, namespace): 
        logging.debug("[NamespaceManager::registerNamespace] entering method")

        if isinstance(namespace, Namespace):
            my_module = sys.modules[__name__]
            name = str(namespace).replace('-', '_').upper()
            my_module.__all__.append(name)
            setattr(my_module, name, namespace)
        else:
            logging.warning("[NamespaceManager::registerNamespace] namespace must be an instance of Namespace")

    def getNamespace (self, name):
        name = str(name).replace('-', '_').upper()
        my_module = sys.modules[__name__]
        if name in my_module.__all__:
            return getattr(my_module, name)
        else:
            return None

#######################################################################
## BUILT_IN NAMESPACES
#######################################################################
## GENERAL NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("socib"))   
from socib.resource_catalog.namespace import SOCIB

NamespaceManager.instance().registerNamespace(Namespace("nemosina"))    #socib:nemosina (not binded resources)
from socib.resource_catalog.namespace import NEMOSINA 

NamespaceManager.instance().registerNamespace(Namespace("wikidata"))    
from socib.resource_catalog.namespace import WIKIDATA 

## PEOPLE NAMESPACES
NamespaceManager.instance().registerNamespace(ORCIDNamespace("orcid"))    
from socib.resource_catalog.namespace import ORCID 

NamespaceManager.instance().registerNamespace(Namespace("researchgate"))    
from socib.resource_catalog.namespace import RESEARCHGATE 

NamespaceManager.instance().registerNamespace(RORNamespace("ror"))
from socib.resource_catalog.namespace import ROR

NamespaceManager.instance().registerNamespace(Namespace("isni"))
from socib.resource_catalog.namespace import ISNI

NamespaceManager.instance().registerNamespace(Namespace("grid"))
from socib.resource_catalog.namespace import GRID

## PROJECT NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("edmerp"))  #seadatanet:edmerp 
from socib.resource_catalog.namespace import EDMERP

## ORGANIZATION NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("edmo"))    #seadatanet:edmo 
from socib.resource_catalog.namespace import EDMO

## DATASET NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("edmed"))   #seadatanet:edmed (
from socib.resource_catalog.namespace import EDMED

## PLATFORM NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("edios"))   #seadatanet:edios 
from socib.resource_catalog.namespace import EDIOS

## PLATFORM NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("wmo"))   #seadatanet:edios 
from socib.resource_catalog.namespace import WMO

NamespaceManager.instance().registerNamespace(Namespace("coriolis"))   #seadatanet:edios 
from socib.resource_catalog.namespace import CORIOLIS

NamespaceManager.instance().registerNamespace(Namespace("ices"))   #seadatanet:edios 
from socib.resource_catalog.namespace import ICES

## CRUISE NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("csr"))     #seadatanet:csr (cruise)
from socib.resource_catalog.namespace import CSR

## DOCUMENT NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("doi"))     #datacite:doi 
from socib.resource_catalog.namespace import DOI

NamespaceManager.instance().registerNamespace(Namespace("crossref"))     #datacite:doi 
from socib.resource_catalog.namespace import CROSSREF

NamespaceManager.instance().registerNamespace(Namespace("obps"))     #datacite:doi 
from socib.resource_catalog.namespace import OBPS

NamespaceManager.instance().registerNamespace(Namespace("oceandocs"))     #datacite:doi 
from socib.resource_catalog.namespace import OCEANDOCS

NamespaceManager.instance().registerNamespace(Namespace("ramadda"))     #datacite:doi 
from socib.resource_catalog.namespace import RAMADDA

## SOFTWARE NAMESPACES
NamespaceManager.instance().registerNamespace(Namespace("github"))     #datacite:doi 
from socib.resource_catalog.namespace import GITHUB


