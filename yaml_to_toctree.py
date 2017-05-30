#!/usr/bin/python
# Copyright (C) Metaswitch Networks 2016
# If license terms are provided to you in a COPYING file in the root directory
# of the source code repository by which you are accessing this code, then
# the license outlined in that COPYING file applies to your use.
# Otherwise no rights are granted except for those provided to you by
# Metaswitch Networks in a separate written agreement.

"""
This script converts a mkdocs.yml table of contents into a reStructuredText table of contents.
"""

import yaml

class BadSectionError(Exception):
    """Raised when a section doesn't contain either a filename or a list of
    headings/files for a subsection"""
    pass


section_num = 1

def print_toc_section(section, caption):
    """ data is a list of single-item dictionaries, each of which represent a
        page title and a file. Sections are represented by having the dictionary value
        be another list, rather than a filename.

        Here's some example input:

   [{'Home': 'index.md'},
    {'Clearwater Architecture': 'Clearwater_Architecture.md'},
    {'Clearwater Tour': 'Clearwater_Tour.md'},
    {'Support': 'Support.md'},
    {'Installation': [{'Installation Instructions': 'Installation_Instructions.md'},
                      {'All-in-one Images': 'All_in_one_Images.md'},
                      {'Configuring Zoiper': 'Configuring_Zoiper.md'}]},
    {'Upgrading and Modifying': [{'Upgrading Clearwater': 'Upgrading_Clearwater.md'},
                                 {'Migrating to etcd': 'Migrating_To_etcd.md'}]}]

    """
    global section_num

    # Output the rST section heading
    print """
.. _{}:

.. toctree::
   :caption: {}
   :maxdepth: 0
""".format(section_num, caption)

    # Increment the section number ready for the next section
    section_num += 1

    for item in section:
        for title, filename in item.iteritems():
            if isinstance(filename, basestring):
                # Special-case the index page, to avoid infinite recursion -
                # Sphinx looks in each of the files you list for a table of
                # contents, so it can list the subheadings, so listing this file
                # causes infinite recursion.
                # http://stackoverflow.com/questions/16123951/how-do-i-include-the-homepage-in-the-sphinx-toc.

                if filename == "index.md":
                    filename = "self"
                print "   {} <{}>".format(title, filename.replace(".md", ".rst"))
            elif isinstance(filename, list):
                # This is a subsection heading rather than a particular file, so
                # recurse into it
                print_toc_section(filename, title)
            else:
                raise BadSectionError("Section contains badly-typed information ({}, not str or list)".format(type(filename)))

    # Separate sections with a blank line
    print ""


with open('mkdocs.yml', 'r') as f:
    data = yaml.load(f)
    print_toc_section(data['pages'], "Overview")
