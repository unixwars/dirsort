#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (C) 2010, Taher Shihadeh <taher@unixwars.com>
# Licensed: GPL v2.        http://unixwars.com

"""
Directory sorter: This script is used to classify assorted collections
of media files.

It takes the current directory -or alternatively one or more paths as
parameter- and classifies the files and directories that are similar
that match a similarity factor above a specified threshold. It works
based solely only on the names of files and directories in a
non-recursive manner.

Before comparing the names, it removes every component that matches
the predefined list of regular expressions.
"""

import operator
import optparse
import os
import re
import shutil
import string
import sys

__author__  = 'Taher Shihadeh <taher@unixwars.com>'
__version__ = '1.0'
USAGE       = '%prog [options] paths'
EPILOG      = 'Report bugs to taher@unixwars.com'

SEP         = '_-+~.·:;·()[]¡!¿?<>'
REGEXES     = ['\[.*?\]', '\(.*?\)', '\d{3,4}x\d{3}',
               's\d{1,2}[ex]{1,2}', '\d+', 'dvd', 'bdrip', 'dvdrip',
               'xvid', 'divx', 'x264', 'h264', 'aac', 'mp3', 'ova',
               'oav', 'episode', 'season', 'episodio', 'temporada']


class Sorter:
    """Class to sort according to similarity factor"""
    def __init__ (self, options, paths, sep=SEP, regexes=REGEXES):
        self.options = options
        self.paths   = paths
        self.regexes = regexes
        self.trans   = string.maketrans (sep, ' '*len(sep))
        self.entries = self.__get_entries ()
        self.results = []
        self.run()

    def __get_entries (self):
        entries = []
        for path in self.paths:
            listdir = os.listdir (path)

            for x in listdir:
                is_dir = os.path.isdir (os.path.join(path, x))
                entries.append ({'path':path, 'dir', is_dir, 'name':x})
        return entries

    def __process_entry (self, entry):
        """Cleanup and divide entry's name down to comparable  components"""
        tmp   = self.__cleanup (entry)
        lst   = tmp.translate(self.trans).split()
        return filter(None, lst)

    def __cleanup_str (self, entry):
        tmp   = entry['name'].lower()

        if entry['dir'] == False:
            tmp, _ = os.path.splitext (tmp)

            
            
            
            
            
            
        #stuff with re self.regexes

        return tmp

    def compare (self, entry1, entry2):
        """Return similarity factor as percentage"""
        aux1    = self.__process_entry (entry1)
        aux2    = self.__process_entry (entry2)
        set_or  = set(aux1) | set(aux2)
        set_and = set(aux1) & set(aux2)
        return (float(len(set_and)) / float(len(set_or)))*100

    def run (self):
        entries = self.entries
        total   = float(len(entries))
        count   = 0

        for x in self.entries:
            for y in entries:
                if x == y:
                    continue # Don't compare with itself
                elif self.options.prefix == None and not (x['dir'] or y['dir']):
                    continue # Skip file-file comparison if possible
                elif self.options.dirs == False and (x['dir'] and y['dir']):
                    continue # Skip dir-dir comparison if possible

                result = {'x':x, 'y':y, 'factor': self.compare (x,y) }
                self.results.append(result)

            entries.remove(x)# No need to compare it on both lists
            count += 1
            print >> sys.stderr, 'Analyzing.. %.2f%%\r' %(min(100.00,(count/total)*200)),

        print >> sys.stderr, ''
        self.results = sorted(self.results, key=operator.itemgetter('factor'), reverse=True)


class Mover:
    """Class to move files/dirs according to similarity factor"""
    def __init __(self, sorter):
        self.options = sorter.options
        self.entries = sorter.entries
        self.results = sorter.results
        self.run()

    def run (self):
        threshold = self.options.factor
        for result in self.results:
            x,y,factor = result['x'],result['y'],result['factor']

            if factor < treshold:
                break

            if   all([x['dir'], y['dir']]):
                if not options.ask:
                    pass
                
                
            elif any([x['dir'], y['dir']]):
                if not options.ask:
                    pass
                
                
            else:
                self.make_dirs()

    def merge_dirs (self, x, y):
        pass
    
    def move_files (self, x, y):
        assert not all([x['dir'], y['dir']])

        if x['dir']:
            x,y = y,x

        src = os.path.join (x['path'], x['name'])
        dst = os.path.join (y['path'], y['name'])
        return shutil.move (src, dst)
    
    def make_dirs (self):
        pass
    

def main():
    parser = optparse.OptionParser (USAGE, epilog=EPILOG)
    parser.add_option("-s", "--simulate",
                      action="store_true", dest="demo", default=False,
                      help="No-act. Perform simulation")
    parser.add_option("-d", "--directories",
                      action="store_true", dest="dirs", default=False,
                      help="Merge directories if appropriate")
    parser.add_option("-y", "--yes",
                      action="store_false", dest="ask",  default=True,
                      help="Assume Yes to all queries and do not prompt")
    parser.add_option("-f", "--factor", type="float",  dest="factor", default=50.0,
                      help="Similarity threshold. By default, a minimun of 50% similarity is required before taking action")
    parser.add_option("-p", "--prefix", dest="prefix", default=None,
                      help="If needed, create new directories beginning with given prefix. You can specify '' or \"\" if you wan't to create new directories without prefix")

    (options, args) = parser.parse_args()

    for arg in args:
        if not os.path.isdir (arg):
            print >> sys.stderr, 'Argument "%s" is not a directory.'%(arg)
            sys.exit(1)

    if args == []:
        args.append (os.getcwd())

    sorter = Sorter (options, args)
    Mover (sorter)


if __name__ == "__main__":
    main()
