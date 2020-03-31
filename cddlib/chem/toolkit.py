''' Module defining the toolkit in use.
Created on Feb 13, 2019

@author: albertgo
'''
import os

# determine toolkit to be used when loading o molecules
TOOLKIT = os.environ.get("CDDLIB_TOOLKIT",None)
if not TOOLKIT:
    # default is openeye but try falling back on rdkit if oe is not available
    try:
        import openeye.oechem
        TOOLKIT = "openeye" 
    except ModuleNotFoundError:
        TOOLKIT = "rdkit"
