#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in apt2sbom distribution
"""
Routines to search SBOMs.
"""

import json
from sys import stderr
from sbomtools.cyclonedx import cyclonedx_search
from sbomtools.spdx import spdx_search

def sbom_search(searchstr,sbom, want_json = False):
    """
    figure out which format the sbom is and then call the appropriate
    search routine.  searchstr is a regex expression. sbom is dict.
    want_json indicates what format should be returned.
    """

    if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
        return cyclonedx_search(searchstr,sbom,want_json)
    if 'spdxVersion' in sbom:
        return spdx_search(searchstr,sbom,want_json)

    return False

def do_search(filename,search_fp,searchstr, want_json = False):
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

    res=sbom_search(searchstr,sbom,want_json)
    if not res:
        return False

    output=''
    outjson=[]

    for entry in res:
        if want_json:
            outjson.append(entry)
        else:
            output=output + f'{filename}: {entry["name"]} version {entry["version"]}\n'
    if want_json and outjson:
        output = json.dumps(outjson)
    return output
