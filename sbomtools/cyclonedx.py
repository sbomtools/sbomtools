#!python
# Copyright (c) 2022, Cisco Systems, Inc. and/or its affiliates.
# All rights reserved.
# See accompanying LICENSE file in sbomtools distribution
"""
CycloneDX support routines
"""

import re
import sbomtools.exceptions

def cyclonedx_search(searchstr,sbom, want_json = False):
    """
    Search a CycloneDX file for components that match.  Return
    an array of component names and versions.
    """
    rets=[]
    prog=re.compile(searchstr)
    if not 'components' in sbom:
        return False # nothing to search
    for entry in sbom['components']:
        if prog.match(entry['name']):
            if want_json:
                rets.append(entry)
            else:
                rets.append({'name' : entry['name'], 'version' : entry['version']})
        elif 'hashes' in entry:
            for hash_entry in entry['hashes']:
                if prog.match(hash_entry['content']):
                    if want_json:
                        rets.append(entry)
                    else:
                        rets.append({'name' : entry['name'], 'version' : entry['version']})
                    break
    return rets

def cyclonedx_update(sbom,component_name,version,
                     supplier,email, url, sha256, sha1,
		     md5,website,overwrite,deps):
    """
    Add a component to a CycloneDX file.  Returns error if
    component exists and overwrite isn't set, if the file can't
    be written, if a dependency is required but not present.
    """

    if 'components' not in sbom:
        return False


    # create a new candidate entry
    newentry = {
        'type' : 'application',
        'name' : component_name,
        'bom-ref' : component_name,
        'version' : version
        }

    if supplier:
        if email:
            supplier = supplier + ' <' + email + '>'
        newentry['supplier']={ 'name' : supplier }
        if url:
            newentry['supplier']['url'] = url

    hashes= []
    if md5:
        hashes.append({
            'alg' : 'MD5',
            'content' : md5 })
    if sha1:
        hashes.append({
            'alg' : 'SHA-1',
            'content' : sha1 })
    if sha256:
        hashes.append({
            'alg' : 'SHA-256',
            'content' : sha256 })
    if hashes:
        newentry['hashes']=hashes
    if website:
        newentry['externalReferences'] = [ {
            'url' : website,
            'type' : 'website'
            }]


    if not deps:
        deplist=[]
    else:
        deplist = deps.copy()

    for entry in sbom['components']:
        if entry['name'] in deplist:
            deplist.remove(entry['name'])

        if entry['name'] == component_name:
            if not overwrite:
                raise sbomtools.exceptions.AlreadyExists("component_name")
            sbom['components'].remove(entry)


    if deplist != []:
        raise sbomtools.exceptions.DependencyNotMet(deplist)

    sbom['components'].append(newentry)

    # fix dependencies.
    if deps:
        newdeps = {
            'ref' : component_name,
            'dependsOn' : deps
            }
        if 'dependencies' in sbom:
            for dep_entry in sbom['dependencies']:
                if dep_entry['ref'] == component_name:
                    sbom['dependencies'].remove(dep_entry)
                    break
            sbom['dependencies'].append(newdeps)
        else:
            sbom.append( [ newdeps ] )

    return sbom


def cyclonedx_remove(sbom,component_name,recurse=False,have_recursed=False):
    """
    Remove a component from an SBOM.  Will also remove its dependency
    entries, and may recurse.
    """

    # remove our own entry

    found=False

    if not 'components' in sbom:
        raise sbomtools.exceptions.FileFormatError('components not found in CycloneDX file')


    for package in sbom['components']:
        if package['name'] == component_name:
            sbom['components'].remove(package)
            found=True
            break

    if not found:
        if not recurse or not have_recursed:
            raise sbomtools.exceptions.PackageNotFound(component_name)
        return sbom

# spot things that depend on us and remove our own dependency entry.

    packlist=[]
    if "dependencies" in sbom:
        for package in sbom['dependencies']:
            if component_name in package['dependsOn']:
                packlist.append(package['ref'])
            if component_name == package['ref']:
                sbom['dependencies'].remove(package)

    # if we aren't meant to recursively remove and there are dependencies,
    # we must return an error.

    if packlist:
        if not recurse:
            raise sbomtools.exceptions.DependencyNotMet(
                f'{component_name} dependency problem: {packlist}')
        for package in packlist:
            print(f'recursing from {component_name} to {package}')
            sbom=cyclonedx_remove(sbom,package,True,have_recursed=True)
            if not sbom:
                return False

    return sbom
