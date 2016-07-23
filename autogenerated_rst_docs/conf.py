# -*- coding: utf-8 -*-
#
# Project Clearwater documentation build configuration file, created by
# sphinx-quickstart on Wed Mar  2 23:24:44 2016.

import sys
import os

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Project Clearwater'
copyright = u'2016, Metaswitch Networks'
author = u'Metaswitch Networks'

# The short X.Y version.
version = u'1.0'
# The full version, including alpha/beta/rc tags.
release = u'1.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# Output file base name for HTML help builder.
htmlhelp_basename = 'ProjectClearwaterdoc'

# The readthedocs code updates the html_context variable, setting
# display_github to True. As we don't want to display the "Edit on Github"
# link, we create a subclass of dict that always sets display_github back to
# False after being updated.
class NoGithubDict(dict):
    def update(self, other_dict):
        dict.update(self, other_dict)
        self['display_github'] = False

html_context = NoGithubDict()

