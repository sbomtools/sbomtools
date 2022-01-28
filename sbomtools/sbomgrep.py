#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in apt2sbom distribution.
"""
Provide CLI functionality for sbomgrep
"""

import argparse
from sys import stderr,stdin
from sbomtools.search import do_search

def cli():
    """
    Function to call CLI routines to invoke apt2sbom.
    """
    parser= argparse.ArgumentParser(description="search SBOM for packages")
    parser.add_argument('-j','--json', action=argparse.BooleanOptionalAction,
                        help="Output JSON results")
    parser.add_argument('searchstr',nargs=1)
    parser.add_argument('files',nargs='*')

    args=parser.parse_args()
    return main(args)


def main(args):
    """
    Main program to process sbomgrep
    """

    if args.files == []:
        results=do_search('stdin',stdin,args.searchstr[0])
        if results:
            print(results)
    else:
        results=''
        for filename in args.files:
            try:
                with open(filename,'r',encoding='utf8') as s_fp:
                    output=do_search(filename,s_fp,args.searchstr[0],args.json)
                    if output:
                        results=results+output
            except OSError as file_except:
                stderr.write(f'{filename}: ' + str(file_except) + '\n')
                return
        if results:
            print(results)
        return
