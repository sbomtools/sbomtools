#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Provide CLI functionality to remove an entry from an SBOM.
"""

import json
import argparse
from sbomtools.remove import sbom_rm
import sbomtools.exceptions

def cli():
    """
    Function to call CLI routines to invoke apt2sbom.
    """
    parser= argparse.ArgumentParser(description="Update SBOM with new package info")
    parser.add_argument('-f','--filename',help='file to edit',required=True)
    parser.add_argument('-r','--recurse',
                        help='Remove anything that depends on this entry as well',
                        action='store_true')
    parser.add_argument('name',help='Component Name',nargs='+')
    args=parser.parse_args()
    for pkgname in args.name:
        try:
            sbom_rm(args.filename,pkgname,args.recurse)
        except sbomtools.exceptions.PackageNotFound:
            print(f'{pkgname} not found in {args.filename}')
        except sbomtools.exceptions.FileFormatError as sbom_error:
            print(str(sbom_error))
        except sbomtools.exceptions.UnknownError as sbom_error:
            print(str(sbom_error))
        except sbomtools.exceptions.DependencyNotMet as sbom_error:
            print(f'{pkgname}: dependency error: ' + str(sbom_error))
        except OSError as os_e:
            print(f'{args.filename}: ' + str(os_e))
        except json.decoder.JSONDecodeError as j_error:
            print(f'{args.filename}: JSON error: ' + str(j_error))
