dirsort: Directory classifier
=============================

:Author: Taher Shihadeh <taher@unixwars.com>
:Copyright: (C) 2010. Licensed GPL v2

This script is used to classify unsorted collections of media files

It takes the current directory -or alternatively one or more paths as
parameter- and classifies the files and directories that match a
similarity factor above a specified threshold. It works based solely
on the names of files and directories in a non-recursive manner.

Before comparing the names, it removes every component that matches
the list of regular expressions. Then, splits by the given list of
separators, removes unwanted substrings, and analyzes similarities
among the remaining pieces.

Afterwards it moves files and merges directories based on that
analysis.

.. Warning::
   It will overwrite files if they already exist in the target
   directory. Use a custom Mover class if that is not the desired
   behavior.

Usage
-----
Syntax:
    dirsort [options] paths

Options:
  -h, --help                    Show this help message and exit
  -s, --simulate                No-act. Perform simulation
  -d, --directories             Merge directories if appropriate
  -y, --yes                     Assume Yes to all queries and do not prompt
  -f FACTOR, --factor=FACTOR    Similarity threshold. By default, a minimun of 50% similarity is required before taking action
  -p PREFIX, --prefix=PREFIX    If needed, create new directories beginning with given prefix. You can specify '' or "" if you wan't to create new directories without prefix
