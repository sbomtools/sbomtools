#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution
"""
Routines to search SBOMs.
"""

import json
from sbomtools.constants import FORMAT_CDX,FORMAT_SPDX
from sbomtools.cyclonedx import cyclonedx_search
from sbomtools.spdx import spdx_search

def sbom_grep(search_fp,searchstr, want_json = True,want_wild=True):
    """
    takes as input a filename, file pointer, search string, and
    whether to produce JSON output.
    """
    sbom=json.loads(search_fp.read())

    if want_wild:
        searchstr= '.*' + searchstr
    else:
        searchstr= searchstr + '$'
    if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
        (state,res)= (FORMAT_CDX,cyclonedx_search(searchstr,sbom,want_json))
    if 'spdxVersion' in sbom:
        (state,res)= (FORMAT_SPDX,spdx_search(searchstr,sbom,want_json))
    if not res:
        return (False, [])

    return (state,res)
