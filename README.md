# Python wrappers for cheminformatics toolkits.

Installation
============

To use this you will need to install either:
   - [rdkit](https://www.rdkit.org/docs/Install.html)
   - [openeye python toolkit](https://docs.eyesopen.com/toolkits/python/quickstart-python/install.html)

into your python environment.

Then:
   - download(git clone) this source code

   - install it into your python environment:
     cd into thee root directory of this package
     ```bash
     pip install .
     ```



## Package: chem
General purpose helper classes around the [RDKit](https://www.rdkit.org/) and [openeye](https://www.eyesopen.com/) toolkits for handling molecular input files. This packages tries to abstract the toolkits away and thus provides a toolkit independent interface to dealing with molecular files and, to some extend, with molecule objects.

The underlying toolkit used can be determined with the CDDLIB_TOOLKIT enviroment
variable. It defaults to openeye, but if loading the openeye package fails it will try to fall back to the RDKit library.
   
The package is still under development but here is an example on how to get started:
```
from cddlib.chem.io import get_mol_input_stream, get_mol_output_stream

# open input and output files
# Note: output will be to stdout as only file extension is given
with get_mol_input_stream('tests/data/test_CCCO_confs.sdf') as inFile, \
     get_mol_output_stream('.sdf') as outFile:

    # loop over input molecules
    for mol in inFile:
        mol['numAtoms'] = len(mol.atoms) # set new sd tag value
        outFile.write_mol(mol)           # write to output file
```

## Package: util
Various utility modules.


License
=======
```
###############################################################################
## The MIT License
##
## SPDX short identifier: MIT
##
## Copyright 2020 Genentech Inc. South San Francisco
##
## Permission is hereby granted, free of charge, to any person obtaining a
## copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included
## in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
## OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.
###############################################################################
```

