#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Provide CLI functionality for sbomgrep
"""

import argparse
import json
from sys import stderr,stdin
from sbomtools.grep import sbom_grep

def print_json_results(args):
    """
    print JSON results of a search.
    """

    if args.files == []:
        results=sbom_grep('stdin',stdin,args.searchstr[0])
        if results:
            print(json.dumps(results))
        return

    results=[]
    for filename in args.files:
        try:
            with open(filename,'r',encoding='utf8') as s_fp:
                output=sbom_grep(filename,s_fp,args.searchstr[0],args.json)
                if output:
                    results.extend(output)
        except OSError as file_except:
            stderr.write(f'{filename}: ' + str(file_except) + '\n')
            return
        except json.decoder.JSONDecodeError as j_error:
            stderr.write(f'{filename}: JSON error: ' + str(j_error) + '\n')
            return

    print(json.dumps(results))
    return

def pretty_print_results(args):
    """
    Main program to process sbomgrep
    """

    if args.files == []:
        results=sbom_grep('stdin',stdin,args.searchstr[0])
        if results:
            print(results)
        return

    results=''
    for filename in args.files:
        try:
            with open(filename,'r',encoding='utf8') as s_fp:
                output=sbom_grep(filename,s_fp,args.searchstr[0],args.json)
                if output:
                    results= results+output
        except OSError as file_except:
            stderr.write(f'{filename}: ' + str(file_except) + '\n')
            return
    print(results,end='')
    return

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
    if args.json:
        print_json_results(args)
    else:
        pretty_print_results(args)
