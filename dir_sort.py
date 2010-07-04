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
the list of regular expressions. Then, splits by the given list of
separators. Then removes unwanted substrings. And then it analyzes
similarities among the remaining pieces.

It then moves files and merges directories based on that
analysis.

WARNING: it will overwrite files if they already exist in the target
directory. Use a custom Mover class if that is not the desired
behavior.
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

REGEXES     = ['\[.*?\]' , '\(.*?\)',# strings in brackets or parens
               's\d{1,2}[ex]\d{1,2}',# episode numbers
               '\d{3,4}x\d{3,4}',    # video resolutions
               '\d+',                # numbers
               ]
SEP         = """ _-+~.·:;·()[]¡!¿?<>"'`""" # word boundaries
STRINGS     = ['dvd', 'bdrip', 'dvdrip', 'xvid', 'divx', 'x264',
               'h264', 'aac', 'mp3', 'ova', 'hdtv', 'vtv', 'notv',
               '2hd', 'hd', '720p' '1080p', 'lol', 'fqm', 'oav',
               'episode', 'season', 'volume', 'vol', 'volumen',
               'extra','episodio', 'temporada'] # lowercase


class Sorter:
    """Class to sort according to similarity factor"""
    def __init__ (self, options, paths, regexes=REGEXES, sep=SEP, strings=STRINGS):
        self.options = options
        self.paths   = paths
        self.regex   = '|'.join(regexes)
        self.trans   = string.maketrans (sep, ' '*len(sep))
        self.del_set = set([s.lower() for s in strings])
        self.entries = self.__get_entries ()
        self.results = []
        self.__run()

    def __call__ (self):
        return self.results

    def __get_entries (self):
        entries = []
        for path in self.paths:
            listdir = os.listdir (path)

            for x in listdir:
                is_dir = os.path.isdir (os.path.join(path, x))
                entries.append ({'path':path, 'dir': is_dir, 'name':x})
        return entries

    def __process_entry (self, entry):
        """Cleanup and divide entry's name down to comparable components"""
        tmp   = entry['name'].lower()

        if entry['dir'] == False:
            tmp, _ = os.path.splitext (tmp)

        # Remove regex matches, split, and disregard unwanted strings
        tmp = re.sub (self.regex, ' ', tmp)
        tmp = tmp.translate(self.trans).split()
        keep = set(tmp).difference(self.del_set)

        return filter(None, keep)

    def __compare (self, entry1, entry2):
        """Return similarity factor as percentage"""
        aux1    = self.__process_entry (entry1)
        aux2    = self.__process_entry (entry2)
        set_or  = set(aux1) | set(aux2)
        set_and = set(aux1) & set(aux2)
        return (float(len(set_and)) / float(len(set_or)))*100

    def __run (self):
        entries = self.entries
        total   = float(len(entries))
        count   = 0

        for x in self.entries:
            for y in entries:
                if x == y:
                    continue # Don't compare with itself
                elif self.options.prefix == None and all((not x['dir'], not y['dir'])):
                    continue # Skip file-file comparison if possible
                elif self.options.dirs == False and all((x['dir'],y['dir'])):
                    continue # Skip dir-dir comparison if possible

                result = {'x':x, 'y':y, 'factor': self.__compare (x,y) }
                self.results.append(result)

            entries.remove(x)# No need to compare it on both lists
            count += 1
            print >> sys.stderr, '\rAnalyzing.. %.2f%%' %(min(100.00,(count/total)*200)),

        print >> sys.stderr, ''
        self.results = sorted(self.results, key=operator.itemgetter('factor'), reverse=True)


class Mover:
    """Class to move files/dirs according to similarity factor"""
    def __init__ (self, sorter):
        self.options  = sorter.options
        self.entries  = sorter.entries
        self.results  = sorter.results
        self.used_src = []
        self.log      = []
        self.__run()

    def __run (self):
        threshold = self.options.factor
        for result in self.results:
            x,y,factor = result['x'],result['y'],result['factor']

            if factor < threshold:
                break
            if   all([x['dir'], y['dir']]):
                self.merge_dirs (x,y,factor)
            elif any([x['dir'], y['dir']]):
                self.move_file (x,y,factor)
            else:
                self.make_dirs()

    def __call__ (self):
        return self.report()

    def report (self):
        for src,dst,status in self.log:
            src_str  = '%s%s' %(os.path.join(src['path'],src['name']), ['',os.path.sep][src['dir']])
            dst_str  = '%s%s' %(os.path.join(dst['path'],dst['name']), ['',os.path.sep][dst['dir']])
            print '%s\t%s --> %s'%(['Error','OK'][status], src_str, dst_str)

    def register_operation (self, x, y, status):
        assert not x in self.used_src, 'Source already processed'

        self.used_src.append(x)
        self.log.append ((x,y,status))

    def move_file (self, x, y, factor):
        assert not all([x['dir'], y['dir']])

        if x['dir']:
            x,y = y,x

        if x in self.used_src:
            return

        src = os.path.join (x['path'], x['name'])
        dst = os.path.join (y['path'], y['name'])

        if not self.confirm (x, y, factor):
            return

        status = False
        if not self.options.demo:
            try:
                shutil.move (src, dst)
                status = True
            except:
                pass

        self.register_operation (x,y,status)

    def merge_dirs (self, x, y, factpr):
        assert all([x['dir'], y['dir']])

        if x in self.used_src:
            return

        assert False, 'Unimplemented'
        
        
        self.register_operation (x,y,status)


    def make_dirs (self):
        assert False, 'Unimplemented'
        
        
        self.register_operation (x,y,status)


    def confirm (self, src, dst, factor):
        if factor < self.options.factor:
            value, opt = False, 'y/N'
        else:
            value, opt = True, 'Y/n'

        if self.options.ask:
            src_str  = '%s%s' %(os.path.join(src['path'],src['name']), ['',os.path.sep][src['dir']])
            dst_str  = '%s%s' %(os.path.join(dst['path'],dst['name']), ['',os.path.sep][dst['dir']])
            question = '[%.2f%%] %s --> %s\nConfirm? [%s] ' %(factor, src_str, dst_str, opt)

            while True:
                answer = raw_input (question)
                if answer.lower() == 'y':
                    value = True
                    break
                elif answer.lower() == 'n':
                    value = False
                    break
                elif answer == '':
                    break

        return value


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
    mover  = Mover (sorter)
    mover.report()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ''
