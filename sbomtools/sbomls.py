#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Similar to sbomgrep, but produce either all components or components
that match a pattern for a single file.
"""

import argparse
import json
import re
from shutil import get_terminal_size
from sbomtools.grep import sbom_grep

def call_grep(args):
    """
    call grep with appropriate fp and args
    """
    results=[]
    if args.components:
        components=args.components
    else:
        components=['.*']
    try:
        for component in components:
            with open(args.filename,'r',encoding='utf8') as s_fp:
                output=sbom_grep(s_fp,component,args.json,want_wild=False)[1]
                if output:
                    results.extend(output)
    except OSError as file_except:
        print(f'{args.filename}: ' + str(file_except) + '\n')
        return False
    except json.decoder.JSONDecodeError as j_error:
        print(f'{args.filename}: JSON error: ' + str(j_error) + '\n')
        return False
    except re.error as re_error:
        print(f'{args.filename}: regex error: ' + str(re_error))

    return results

def print_json_results(args):
    """
    print JSON results of a search.
    """

    results=call_grep(args)
    if results:
        print(json.dumps(results))

def pretty_print_results(args):
    """
    Main program to process sbomgrep
    """

    results=call_grep(args)
    if not results:
        return

    names=[d['name'] for d in results]
    names.sort()
    term_width=get_terminal_size()[0]
    line=names.pop(0)

    ntabs=1
    for name in names:
        if args.one:
            print(name)
            continue
        if len(line)+len(name) + 5*ntabs> term_width:
            print(line)
            line=name
            ntabs=1
        else:
            line=line+ f'\t{name}'
            ntabs=ntabs+1
    print(line)
    return

def cli():
    """
    Function to call CLI routines to invoke sbomls.
    """
    parser= argparse.ArgumentParser(description="search SBOM for packages")
    parser.add_argument('-j','--json', action='store_true',
                        help="Output JSON results")
    parser.add_argument('-1','--one',help="One entry per line",action='store_true')
    parser.add_argument('-f','--filename',required=True,help="SBOM file")
    parser.add_argument('components',nargs='*',help='Components to to list')
    args=parser.parse_args()
    if args.json:
        print_json_results(args)
    else:
        pretty_print_results(args)
