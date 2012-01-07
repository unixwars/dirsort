Directory sorter
================

This script is used to classify unsorted collections
of media files

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

WARNING: it will overwrite files if they already exist in the target
directory. Use a custom Mover class if that is not the desired
behavior.

Usage
-----
Syntax:
    dirsort [options] paths

Options:
  -h, --help            show this help message and exit
  -s, --simulate        No-act. Perform simulation
  -d, --directories     Merge directories if appropriate
  -y, --yes             Assume Yes to all queries and do not prompt
  -f FACTOR, --factor=FACTOR
                        Similarity threshold. By default, a minimun of 50%
                        similarity is required before taking action
  -p PREFIX, --prefix=PREFIX
                        If needed, create new directories beginning with given
                        prefix. You can specify '' or "" if you wan't to
                        create new directories without prefix

Algorithm
---------
The algorithm is as simple as it gets, but gets good results whatsoever.

0) sort:
	take lowercase basename
	remove extensions and regex matches
	substitute all separators, and split
	calculate similarity factor = number of common parts / number of sum of the parts
	sort by factor

1) simple_move:
	when factor (dir-dir) >= threshold:
	     merge
	     register moved_dir, and threshold

	when factor (dir-file) >= threshold:
	     move file
	     register moved_file, and threshold

2) for remaining files:
        when factor (file-file) >= threshold:
	     if both in sets:
	        skip
	     elif one in set:
	        add other to same set
	     else:
	        add files to new set

   generate dir_name:
   	    clean shortest name on the set
	    split

	    for p in pieces:
	    	if p.lower() in intersect:
		dirname += p
	    dirname = '_'.join(dirname)
