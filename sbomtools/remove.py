#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Route to remove to appropriate handler, either SPDX or CycloneDX.
"""

import json
from sys import stderr
from sbomtools.cyclonedx import cyclonedx_remove
from sbomtools.spdx import spdx_remove

def sbom_rm(filename,component_name,recurse):
    """
    Dispatch routine.  Open file, figure out if it's SPDX or CycloneDX,
    and then dispatch.
    """

    try:
        with open(filename,'r',encoding='utf-8') as sbom_fp:
            sbom=json.load(sbom_fp)
    except OSError as os_e:
        stderr.write(f'{filename}: ' + str(os_e))
        return False
    except json.decoder.JSONDecodeError as j_error:
        stderr.write(f'{filename}: JSON error: ' + str(j_error))
        return False

    if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
        sbom= cyclonedx_remove(sbom,component_name,recurse)
    elif 'spdxVersion' in sbom:
        sbom= spdx_remove(sbom,component_name,recurse)
    else:
        stderr.write(f'{filename}: unrecognized format.\n')
        return False

    if not sbom:
        stderr.write('Errors encountered in request.')
        return False

#    Write out the file

    try:
        with open(filename,'w',encoding='utf-8') as sbom_fp:
            sbom_fp.write(json.dumps(sbom))
    except OSError as sbom_err:
        return False

    return True
