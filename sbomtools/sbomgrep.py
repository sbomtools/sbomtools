#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Provide CLI functionality for sbomgrep
"""

import argparse
import json
from sys import stdin
from sbomtools.constants import FORMAT_NONE
from sbomtools.grep import sbom_grep

def print_json_results(args):
    """
    print JSON results of a search.
    """

    if args.files == []:
        (state,results)=sbom_grep('stdin',stdin,args.searchstr[0])
        if results:
            print(json.dumps(results))
        return

    results=[]
    sbom_type=FORMAT_NONE
    for filename in args.files:
        try:
            with open(filename,'r',encoding='utf8') as s_fp:
                (state,output)=sbom_grep(s_fp,args.searchstr[0],args.json)
                if sbom_type not in ( state, FORMAT_NONE ):
                    print(f'{filename}: mixed SBOM types in JSON')
                    return
                sbom_type=state
                if output:
                    results.extend(output)
        except OSError as file_except:
            print(f'{filename}: ' + str(file_except) + '\n')
            return
        except json.decoder.JSONDecodeError as j_error:
            print(f'{filename}: JSON error: ' + str(j_error) + '\n')
            return

    print(json.dumps(results))
    return

def pretty_print_results(args):
    """
    Main program to process sbomgrep
    """

    if args.files == []:
        results=sbom_grep(stdin,args.searchstr[0])[1]
        if results:
            print(f'stdin: {results["name"]} version {results["version"]}\n')
        return

    results=''
    for filename in args.files:
        try:
            with open(filename,'r',encoding='utf8') as s_fp:
                output=sbom_grep(s_fp,args.searchstr[0],args.json)[1]
                for entry in output:
                    results=results + f'{filename}: {entry["name"]} ' + \
                        f'version {entry["version"]}\n'
        except OSError as file_except:
            print(f'{filename}: ' + str(file_except) + '\n')
            return
    print(results,end='')
    return

def cli():
    """
    Function to call CLI routines to invoke sbomgrep.
    """
    parser= argparse.ArgumentParser(description="search SBOM for packages")
    parser.add_argument('-j','--json', action='store_true',
                        help="Output JSON results")
    parser.add_argument('searchstr',nargs=1)
    parser.add_argument('files',nargs='*')

    args=parser.parse_args()
    if args.json:
        print_json_results(args)
    else:
        pretty_print_results(args)
