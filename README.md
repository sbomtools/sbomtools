# Welcome to sbomtools

This package contains a handful of routines to search and update SBOMs.  JSON
versions of both CycloneDX and SPDX are supported.

## Building


1. Bop the version on setup.cfg
2. python3 -m build -w
3. cd dist
4. pip3 install that file


## Usage

### sbomgrep

    % sbomgrep [-j] search-string [file [file...]]

Results are similar to grep.  If no file is specified, stdin will be used.

To search from python

    from sbomtools import sbom_search
    
    results= sbom_search(searchstr,sbom, want_json = False)

Where searchstr is a regex, sbom is a JSON format of an SBOM, and
want_json is whether you want the entire entry for each result.  Otherwise
a simple JSON array of dicts of the form
{'name' : pkgname, 'version' : version} will be returned.

The program will automatically detect the input format.


### sbomupdate

This routine updates an SBOM file by adding a single entry.  Again, it
will do this for both SPDX and CycloneDx.  For CycloneDX both the
components and refs are updated.  For SPDX, products, relationships, and
documentDescribes are updated.  N.B., SPDX takes as input dependencies by
short name.  You don't need to enter the SPDXID.

    usage: sbomupdate.py [-h] -f FILENAME -n NAME -v VERSION [-s SUPPLIER] [-e EMAIL] [-u URL]
                     [--sha256 SHA256] [--sha1 SHA1] [--md5 MD5] [-w WEBSITE]
                     [-O | --overwrite | --no-overwrite]
                     [-d DEPENDENCIES [DEPENDENCIES ...]]

Cross-dependencies are not currently supported.  However, one can add
both entries and then update each referencing one another.

### sbomrm

This routine removes one or more SBOM entries.  Once again, it is format
neutral.  Note, it tries to disentangle SPDX dependencies, and will do
so only for DEPENDENCY_OF and DEPENDS_ON.  The other relationships are TBD.

    usage: sbomrm [-h] -f FILENAME -n NAME [NAME ...]
		  [-r | --recurse | --no-recurse]

This one works with cross-dependencies, if you use -r.  Heh.

