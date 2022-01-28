#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution
"""
Routines to search SBOMs.
"""

import json
from sys import stderr
from sbomtools.cyclonedx import cyclonedx_search
from sbomtools.spdx import spdx_search

def sbom_grep(filename,search_fp,searchstr, want_json = False):
    """
    takes as input a filename, file pointer, search string, and
    whether to produce JSON output.  Filename is only used for
    display purposes.  Returns either pretty string or JSON.
    """
    try:
        sbom=json.loads(search_fp.read())
    except json.decoder.JSONDecodeError as j_error:
        stderr.write(f'{filename}: JSON error: ' + str(j_error) + '\n')
        return False

    if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
        res= cyclonedx_search(searchstr,sbom,want_json)
    if 'spdxVersion' in sbom:
        res= spdx_search(searchstr,sbom,want_json)
    if not res:
        return False

    output=''
    outjson=[]

    for entry in res:
        if want_json:
            outjson.append(entry)
        else:
            output=output + f'{filename}: {entry["name"]} version {entry["version"]}'
    if want_json and outjson:
        output = json.dumps(outjson)
    return output
