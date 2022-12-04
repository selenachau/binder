#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:35:41 2022
Original/inspiration from https://github.com/mbelvadi/lcc_from_isbn, Copyright 2021 Melissa Belvadi Open Source License CC-BY-NC-SA granted
Changes: used OCLC Classify portion and simplified to use an input of isbn list. Simplified ISBN cleaning as well.


http://classify.oclc.org/classify2/Classify?isbn=978157506752&summary=true
<response code="101"/> no match


http://classify.oclc.org/classify2/Classify?isbn=9789004335462&summary=true
<response code="0"/> or <response code="2"/>
   <recommendations>
      <lcc>
         <mostPopular holdings="673" nsfa="HX11.I46" sfa="HX11.I46"/>


http://classify.oclc.org/classify2/Classify?isbn=9781526109538&summary=true
<response code="4"/> need to go to a subpage

Additional options: 
    clean ISBNs with python library isbnlib
                                                                                                                          


@author: selenachau-local

parmvalue=isbns

"""

import logging
import isbnlib #https://pypi.org/project/isbnlib/
import requests #https://pypi.org/project/requests/
from requests.utils import requote_uri
import xml.dom.pulldom
import xml.dom.minidom
import xml.sax.saxutils
import pandas as pd    
from isbnlib import canonical 

UA = 'isbnlib (gzip)'
myheaders = {'User-Agent': UA}
base = 'http://classify.oclc.org/classify2/Classify?'
summaryBase = '&summary=true'
summaryInd = 'false'
logger = logging.getLogger(__name__)
global parmvalue
global parmtype
parmtype="isbn"

# OCLC Classify2 method
def get_oclc_data(parmtype, parmvalue=""):
    global lcc_value
    lcc_value = None
    try:
        nexturl = base + parmtype+"=" + requote_uri(parmvalue)+"&summary=true"
        logger.debug("OCLC URL: {} ".format(nexturl))
    except Exception as ue:
        logger.error("OCLC URL encode failed: {}".format(ue))
        return None
    else:
        try:
            r = requests.get(nexturl, headers=myheaders)
            if not r.ok:
                logger.error("OCLC Request returned http error: {}".format(r.status_code))
                return None
        except Exception as e:
            logger.error("OCLC URL request failed: {}".format(e))
            return None
        else:
            wq = r.text
        xdoc = xml.dom.minidom.parseString(wq)
    response = xdoc.getElementsByTagName('response')[0]
    respCode = response.attributes["code"].value
    if respCode == '0' or respCode == '2':
        recommendations = xdoc.getElementsByTagName('recommendations')[0]
        if recommendations:
            if len(xdoc.getElementsByTagName('lcc')) > 0:
                local_lcc = recommendations.getElementsByTagName('lcc')[0]
                if local_lcc:
                    for mostPopular in local_lcc.getElementsByTagName('mostPopular'):
                        nsfa = mostPopular.attributes["nsfa"].value
                        lcc_value = nsfa
    elif respCode == '4':
        works = xdoc.getElementsByTagName('works')[0]
        logger.debug('Works found: ' + str(len(works.getElementsByTagName('work'))))
        for work in works.getElementsByTagName('work'):
            try:
                m_wi = work.attributes["wi"].value
            except:
                continue
            else:
                try:
                    schemes = work.attributes["schemes"].value
                except:
                    continue
                if 'LCC' in schemes:
                    logger.debug(f'going to try to get lcc using wi {m_wi}')
                    lcc_value = get_oclc_data('wi',m_wi)
                    break
    elif respCode != '102':
        logger.error("OCLC reporting odd error {}, check by hand: {}".format(respCode,nexturl))
    if lcc_value:
        return lcc_value 
    else:
        return None


def validate_json(data):
    if str(data) == "":
        logger.error("validate_json: returns False because no data in passed string: {}".format(str(data)))
        return False
    return True

def fix_isbn(isbn):
    lib_isbn = isbnlib.canonical(isbn)
    if len(lib_isbn) in (10, 13):
        if len(lib_isbn) == 10:
            isgood = isbnlib.is_isbn10(lib_isbn)
        else:
            isgood = isbnlib.is_isbn13(lib_isbn)
        if isgood:
            return lib_isbn
    if len(lib_isbn) < 10:
        return None
    lib_isbn = isbnlib.get_isbnlike(isbn)
    if len(lib_isbn) < 10:
        return None
    lib_isbn = isbnlib.clean(lib_isbn)
    if len(lib_isbn) < 10:
        return None
    lib_isbn = isbnlib.get_canonical_isbn(lib_isbn)
    if len(lib_isbn) < 10:
        return None
    if not lib_isbn:
        return None
    if len(lib_isbn) in (10, 13):
        if len(lib_isbn) == 10:
            isgood = isbnlib.is_isbn10(lib_isbn)
        else:
            isgood = isbnlib.is_isbn13(lib_isbn)
    else:
        return None
    if isgood:
        return lib_isbn
    else:
        return None


# create new function to be used only if ISBNs need validation.
def clean_isbn(row):
    x = canonical(row[0])
    return get_oclc_data(parmtype, x)


df = pd.read_csv('isbns.csv', dtype="string", names=['isbn'])
df['lcc'] = df.apply(clean_isbn, axis=1)

df.to_csv('isbn-lcc.csv', encoding='utf-8', index=False)

