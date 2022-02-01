# Welcome to sbomtools

**WARNING**

This package is early in development.  May cause warts or indigestion.
Save your work.  Interfaces subject to change without notice.

This package contains a handful of routines to search and update SBOMs.  JSON
versions of both CycloneDX and SPDX are supported.

## Building


1. Bop the version on setup.cfg
2. python3 -m build -w
3. cd dist
4. pip3 install that file


## Usage

### sbomls

    usage: sbomls [-h] [-j] [-1] -f FILENAME [components ...]

Where-
 - -j produces JSON entries that match.  The JSON will be of the
   appropriate form for a component for CycloneDX or a package
   for SPDX.
 - -1 produces a single entry per line.  Otherwise, a tabbed list
   is produced a'la ls(1).
 - -f is the filename of the SBOM to use.  Format is automatically
   detected.
 - one or more components may optionally be named.  Wildcards are
   permitted.
   
Returns a list of matching components (or all).

### sbomgrep

    % sbomgrep [-j] search-string [file [file...]]

Results are similar to grep.  If no file is specified, stdin will be used.

To search from python

    from sbomtools import sbom_grep

    from sbom tools import sbom_grep
    results= sbom_grep(filename, searchstr,file_pointer, want_json = True)

Where
 - filename is nothing more than a strong for search results.  This is done simply
   to emulate grep behavior fro pretty printing.
 - searchstr is a regex, sbom is a JSON format of an SBOM, and
 - file_pointer is the successful result of open() or sys.stdin
 - want_json is whether you want the entire entry for each result.


The function will automatically detect the input format.

results is either a printable string of results or (sbom_type,jsonstring)
where SBOM type is either sbomtools.FORMAT_CDX or sbomtools.FORMAT_SPDX.


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

To call from python:

    from sbomtools import sbom_update
    sbom_update(filename,component_name,version, supplier, email
    		url, sha256, sha1, md5, website, overwrite=False, deps)

Where

 - filename is the name of the SBOM file to update (stdin is not acceptable)
 - component_name is the name of the component to add/update
 - supplier is the descriptive name of the supplier
 - email is the email of the supplier
 - sha256, sha1, md5 are respective hashes
 - website is the homepage of the package
 - overwrite is a flag to indicate whether to overwrite an existing entry
 - deps is an array of dependencies to be added for this package.
 
### sbomrm

This routine removes one or more SBOM entries.  Once again, it is format
neutral.  Note, it tries to disentangle SPDX dependencies, and will do
so only for DEPENDENCY_OF and DEPENDS_ON.  The other relationships are TBD.

    usage: sbomrm [-h] -f FILENAME [-r | --recurse | --no-recurse]
                   NAME [NAME ...]

This one works with cross-dependencies, if you use -r.  Heh.

To call from python:

    from sbomtools import sbom_rm

    sbom_rm(filename, component_name, recurse)

Where
 - filename is the name of the SBOM file to act on
 - component_name is the name of the component to remove
 - recurse says to remove those packages that are dependent on this component

The following exceptions are defined:

 - PackageNotFound: you tried to edit/remove a package that wasn't present.
 - DependencyNotMet: you tried to remove something that had a dependency
   		     and you didn't use -r.
 - AlreadyExists: you tried to add an entry that already exists, and you
                  didn't use -O
 - FileFormatError: there is something wrong with the JSON or the SBOM.
 - UnknownError: Something weird happened.  Open an Issue ;-(
