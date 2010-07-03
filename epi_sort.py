#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (C) 2010, Taher Shihadeh <taher@unixwars.com>
# Licensed: GPL v2

"""
The script works based only on names of files and directories in a
non-recursive manner.

It takes a path as parameter and tries to determine if the names of
the contents look alike.

It removes separator characters, numbers and file extensions prior to
the comparison.
"""

import os
import sys
import string
from operator import itemgetter

FAST = False # Change this to skip file-to-file comparisons
SEP  = '_-+~.·:;·()[]¡!¿?<>'

def main (path):
    lst1    = os.listdir (path)
    lst2    = lst1
    len_lst = len(lst1)
    count   = 0.0
    results = []

    for x in lst1:
        for y in lst2:
            if x==y:
                continue
            x_dir = os.path.isdir(x)
            y_dir = os.path.isdir(y)

            if FAST and not (x_dir or y_dir):
                continue

            result = {'A': (x, x_dir), 'B': (y, y_dir)}

            str1, str2 = x, y
            if not x_dir:
                str1,_ = os.path.splitext (x)
            if not y_dir:
                str2,_ = os.path.splitext (y)

            result['factor'] = compare (str1,str2)
            results.append(result)

        lst2.remove(x)
        count += 1
        print >> sys.stderr, '%.2f%% done\r' %(min(100.00,(count / len_lst)*200)),

    print >> sys.stderr, ''
    show(results)

def split (str1):
    trans = string.maketrans(SEP, ' '*len(SEP))
    return str1.translate(trans).split()

def clean (lst):
    assert type(lst) == list
    return filter(lambda x: not x.isdigit(), lst)

def compare (str1, str2):
    """Return similarity factor as percentage"""
    aux1 = clean (split (str1.lower()))
    aux2 = clean (split (str2.lower()))

    set_or  = set(aux1) | set(aux2)
    set_and = set(aux1) & set(aux2)

    return (float(len(set_and)) / float(len(set_or)))*100

def show (results):
    """Show most similar last"""
    for x in sorted(results, key=itemgetter('factor')):
        a,b = x['A'],x['B']
        if not b[1] and a[1]:
            a,b = b,a
        print '%.2f %s \t --> %s' %(x['factor'], a[0], b[0])

if __name__=='__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        path = os.getcwd()

    main (path)
