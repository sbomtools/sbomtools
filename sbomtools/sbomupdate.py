#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Provide CLI functionality to do an SBOM add/update.
"""

import json
import argparse
import sbomtools.exceptions
from sbomtools.update import sbom_update


def cli():
    """
    Function to call CLI routines to invoke apt2sbom.
    """
    parser= argparse.ArgumentParser(description="Update SBOM with new package info")
    parser.add_argument('-f','--filename',help='file to edit',required=True)
    parser.add_argument('-n','--name', required=True,help='Component Name')
    parser.add_argument('-v','--version',required=True,help='Component Version')
    parser.add_argument('-s','--supplier',help='Supplier Name')
    parser.add_argument('-e','--email',help='Supplier EMail')
    parser.add_argument('-u','--url',help='Download URL')
    parser.add_argument('--sha256',help='SHA256 hash')
    parser.add_argument('--sha1',help='SHA1 hash')
    parser.add_argument('--md5',help='MD5 hash')
    parser.add_argument('-w','--website',help='Project Homepage')
    parser.add_argument('-O','--overwrite',
                        action='store_true',
                        help="Overwrite existing component")
    parser.add_argument('-d','--dependencies',
                        help='Names of components that this depends on',
                        nargs='+')

    args=parser.parse_args()
    try:
        return sbom_update(args.filename,args.name,args.version,
                           supplier=args.supplier,email=args.email,
                           url=args.url, sha256=args.sha256, sha1=args.sha1,
                           md5=args.md5,website=args.website,
                           overwrite=args.overwrite, deps=args.dependencies)
    except OSError as sbom_error:
        print(f'{args.filename}: ' + str(sbom_error))
        return False
    except json.decoder.JSONDecodeError as sbom_error:
        print(f'{args.filename}: JSON error: ' + str(sbom_error))
        return False
    except sbomtools.exceptions.FileFormatError as sbom_error:
        print(f'{args.filename}: File format error: ' + str(sbom_error))
        return False
    except sbomtools.exceptions.UnknownError as sbom_error:
        print(f'{args.filename}: Unknown error: ' + str(sbom_error))
        return False
