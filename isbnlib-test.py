#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 09:06:53 2022

@author: selenachau-local
"""

#install isbnlib from the command line

from isbnlib import canonical, is_isbn13

print("Is this isbn witih dashes valid? 978-90-04335-46-2")
is_valid = is_isbn13("978-90-04335-46-2")
out = canonical("978-90-04335-46-2")
print(is_valid,out)