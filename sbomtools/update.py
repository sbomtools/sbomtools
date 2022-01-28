#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution.

"""
Routines to call update an SBOM
"""

import json
import sbomtools.exceptions
from sbomtools.cyclonedx import cyclonedx_update
from sbomtools.spdx import spdx_update

def sbom_update(filename,component_name,version,
                supplier,email, url, sha256, sha1,
		md5,website,overwrite,deps):
    """
    Dispatch routine.  Open file, figure out if it's SPDX or CycloneDX,
    and then dispatch.
    """

    with open(filename,'r',encoding='utf-8') as sbom_fp:
        sbom=json.load(sbom_fp)

    if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
        sbom= cyclonedx_update(sbom,component_name,version,
                                supplier,email, url, sha256, sha1,
		                md5,website,overwrite,deps)
    elif 'spdxVersion' in sbom:
        sbom= spdx_update(sbom,component_name,version,
                           supplier,email, url, sha256, sha1,
		           md5,website,overwrite,deps)

    else:
        raise sbomtools.exceptions.FileFormatError('unrecognized format')

    if not sbom:
        raise sbomtools.exceptions.UnknownError("failed to update")

    with open(filename,'w',encoding='utf-8') as sbom_fp:
        sbom_fp.write(json.dumps(sbom))
    return True
