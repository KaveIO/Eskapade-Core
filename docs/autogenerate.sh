#!/bin/bash

# (re)create required directories
rm -rf autogen
mkdir -p source/_static autogen

# auto-generate code documentation
sphinx-apidoc -f -H Eskapade-Core -o autogen ../python/escore
mv autogen/modules.rst autogen/escore_index.rst
mv autogen/* source/ 

# remove auto-gen directory
rm -rf autogen
