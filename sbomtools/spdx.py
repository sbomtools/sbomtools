#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution
"""
SPDX support routines
"""

import re
import sbomtools.exceptions

def spdx_search(searchstr,sbom, want_json = False):
    """
    Return array of names and versions for matching entries in SPDX
    JSON file.
    """

    if not 'packages' in sbom:
        return False
    rets=[]
    prog=re.compile(searchstr)
    for entry in sbom['packages']:
        if prog.match(entry['name']):
            if want_json:
                rets.append(entry)
            else:
                rets.append({'name': entry['name'], 'version': entry['versionInfo']})
        if 'checksums' in entry:
            for hash_entry in entry['checksums']:
                if prog.match(hash_entry['checksumValue']):
                    if want_json:
                        rets.append(entry)
                    else:
                        rets.append({'name': entry['name'], 'version': entry['versionInfo']})
    return rets

def spdx_update(sbom,component_name,version,
                     supplier,email, url, sha256, sha1,
		     md5,website,overwrite,deps):
    """
    Update SPDX file.
    """

    if 'packages' not in sbom:
        raise sbomtools.exceptions.FileFormatError("packages not found in SPDX file")

    # create a new candidate entry
    newentry = {
        'name' : component_name,
        'SPDXID' : "SPDXRef-sbomupdate." + component_name,
        'versionInfo' : version,
        'filesAnalyzed' : False,
        }

    if supplier and email:
        newentry['supplier'] : f'Organization: {supplier} <{email}>'
    if url:
        newentry['downloadLocation'] = url
    else:
        newentry['downloadLocation'] = "http://spdx.org/rdf/terms#noassertion"
    hashes= []
    if md5:
        hashes.append({
            'algorithm' : 'MD5',
            'checksumValue' : md5 })
    if sha1:
        hashes.append({
            'algorithm' : 'SHA1',
            'checksumValue' : sha1 })
    if sha256:
        hashes.append({
            'algorithm' : 'SHA256',
            'checksumvalue' : sha256 })
    if hashes:
        newentry['checksums']=hashes
    if website:
        newentry['homepage'] = website
    newentry["licenseConcluded"] = "NOASSERTION"
    newentry["licenseDeclared"] = "NOASSERTION"
    newentry["copyrightText"] = "NOASSERTION"

    if not deps:
        deplist=[] # if none provided, assume consistency.
    else:
        deplist = deps.copy()



# we will preserve the old SPDX ID if we find it so that
# dependencies on this package don't break.  We can do this
# because we own the file and the namesapce at this point.

    newdeps = []
    for entry in sbom['packages']:
        if entry['name'] == component_name:
            if not overwrite:
                raise sbomtools.exceptions.AlreadyExists(component_name)
            newentry['SPDXID'] = entry['SPDXID']
            sbom['packages'].remove(entry)

        if entry['name'] in deplist:
            newdeps.append(entry['SPDXID'])
            deplist.remove(entry['name'])

    sbom['packages'].append(newentry)

    # whack documentDescribes

    if not newentry['SPDXID'] in sbom['documentDescribes']:
        sbom['documentDescribes'].append(newentry['SPDXID'])

    # check for unmet dependencies

    if deps and deplist != []:
        raise sbomtools.exceptions.DependencyNotMet(f'{component_name}: {deps}')

    if deps:
        # remove old entries if dependencies are being updated.
        for entry in sbom['relationships']:
            if entry['relationshipType'] =='DEPENDENCY_OF':
                if entry['relatedSpdxElement'] == newentry['SPDXID']:
                    sbom['relationships'].remove(entry)
            elif entry['relationshipType'] == 'DEPENDS_ON':
                if entry['spdxElementId'] == newentry['SPDXID']:
                    sbom['relationships'].remove(entry)

        # add new entries
        for dep_entry in newdeps:
            sbom['relationships'].append( {
                'spdxElementId' : newentry['SPDXID'],
                'relationshipType' : 'DEPENDS_ON',
                'relatedSpdxElement' : dep_entry
                })

    return sbom


def spdx_remove(sbom,component_name,recurse,have_recursed=False):
    """
    Remove a component from an SBOM.  Will also remove its dependency
    entries, and may recurse.
    """
    # remove our own entry

    found=False

    if not 'packages' in sbom:
        raise sbomtools.exceptions.FileFormatError('components not found in CycloneDX file')

    for package in sbom['packages']:
        if component_name in (package['name'], package['SPDXID']):
            spdxid=package['SPDXID']
            sbom['packages'].remove(package)
            found=True
            break

    if not found:
        if not recurse or not have_recursed:
            raise sbomtools.exceptions.PackageNotFound(component_name)
        return sbom

    packlist=[]

    # SPDX is a pain in the ass with relationships because it supports
    # quite a few.  Submit a PR if you want to handle more.  This would
    # be easier in python 3.10 with match and case, but here we are in
    # an earlier version.  Should be refactored later.

    if "relationships" in sbom:
        for rel in sbom['relationships']:
            if rel['relationshipType'] == 'DEPENDENCY_OF':
                if rel['spdxElementId'] == spdxid:
                    packlist.append(rel['relatedSpdxElement'])
                if component_name == rel['relatedSpdxElement']:
                    sbom['relationships'].remove(rel)
            elif rel['relationshipType'] == 'DEPENDS_ON':
                if rel['relatedSpdxElement'] == spdxid:
                    packlist.append(rel['spdxElementId'])
                if component_name == rel['spdxElementId']:
                    sbom['relationships'].remove(rel)

    if packlist:
        if not recurse:
            raise sbomtools.exceptions.DependencyNotMet(
                f'{component_name} dependency problem: {packlist}')
        for package in packlist:
            print(f'recursing from {component_name} to {package}')
            sbom=spdx_remove(sbom,package,True,have_recursed=True)
            if not sbom:
                return False
    return sbom
