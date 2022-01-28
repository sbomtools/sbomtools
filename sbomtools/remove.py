#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.
"""
Route to remove to appropriate handler, either SPDX or CycloneDX.
"""

import json
import sbomtools.exceptions
from sbomtools.cyclonedx import cyclonedx_remove
from sbomtools.spdx import spdx_remove

def sbom_rm(filename,component_name,recurse):
    """
    Dispatch routine.  Open file, figure out if it's SPDX or CycloneDX,
    and then dispatch.
    """

    with open(filename,'r',encoding='utf-8') as sbom_fp:
        sbom=json.load(sbom_fp)

    if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
        sbom= cyclonedx_remove(sbom,component_name,recurse)
    elif 'spdxVersion' in sbom:
        sbom= spdx_remove(sbom,component_name,recurse)
    else:
        raise sbomtools.exceptions.FileFormatError("Unrecognized Format")

    if not sbom:
        raise sbomtools.exceptions.UnknownError("Something went wrong")

#    Write out the file

    with open(filename,'w',encoding='utf-8') as sbom_fp:
        sbom_fp.write(json.dumps(sbom))

    return True
