#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution
"""
Routines to search SBOMs.
"""

import json
from sbomtools.cyclonedx import cyclonedx_search
from sbomtools.spdx import spdx_search

def sbom_grep(filename,search_fp,searchstr, want_json = True):
    """
    takes as input a filename, file pointer, search string, and
    whether to produce JSON output.  Filename is only used for
    display purposes.  Returns either pretty string or JSON.
    """
    sbom=json.loads(search_fp.read())

    if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
        res= cyclonedx_search(searchstr,sbom,want_json)
    if 'spdxVersion' in sbom:
        res= spdx_search(searchstr,sbom,want_json)
    if not res:
        return False

    output=''

    if want_json:
        return res
    for entry in res:
        output=output + f'{filename}: {entry["name"]} version {entry["version"]}\n'
    return output