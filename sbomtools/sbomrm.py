#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Provide CLI functionality to remove an entry from an SBOM.
"""

import argparse
from sbomtools.remove import remove_sbom
import sbomtools.exceptions

def cli():
    """
    Function to call CLI routines to invoke apt2sbom.
    """
    parser= argparse.ArgumentParser(description="Update SBOM with new package info")
    parser.add_argument('-f','--filename',help='file to edit',required=True)
    parser.add_argument('-n','--name', required=True,help='Component Name',nargs='+')
    parser.add_argument('-r','--recurse',
                        help='Remove anything that depends on this entry as well',
                        action=argparse.BooleanOptionalAction)
    args=parser.parse_args()
    for pkgname in args.name:
        try:
            remove_sbom(args.filename,pkgname,args.recurse)
        except sbomtools.exceptions.PackageNotFound as sbom_error:
            print(f'{pkgname} not found in {args.filename}')
        except sbomtools.exceptions.DependencyNotMet as sbom_error:
            print(str(sbom_error))
