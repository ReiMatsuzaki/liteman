#!/bin/python -u
import os
expanduser = os.path.expanduser
import re

bib_in_list_default = [expanduser("~/Documents/library.bib")]
#cite_list = ["Varandas2009", "Gritsenko2016", "Oana2007", "Oana2009"]

journal_dict = {"Chemical Physics":"Chem.Phys",
                "Journal of Chemical Physics": "J.Chem.Phys.",
                "The Journal of Chemical Physics": "J.Chem.Phys.",                
                "The Journal of chemical physics": "J.Chem.Phys.",
                "Physical review letters": "Phys.Rev.Lett.",
                "Physical Review Letters": "Phys.Rev.Lett.",
                "Physical Review A - Atomic, Molecular, and Optical Physics": "Phys.Rev.A",
                "Journal of Physics B: Atomic and Molecular Physics": "J.Phys.B",
                "Phys. Chem. Chem. Phys.": "Phys. Chem. Chem. Phys."}

re_journal = re.compile("^journal = \{(.*)\},")

def process(fi, line, fo):
    while line:
        if(line == "}\n"):
            break
        find_journal = re_journal.search(line)
        if(find_journal):
            orig = find_journal.group(1)
            line = "journal = {" + journal_dict[orig] + "},\n"
        fo.write(line)
        line = fi.readline()
    fo.write("}\n")
    
def run_liteman(cite_list, bib_out, bib_in_list=bib_in_list_default):
    fo = open(bib_out, "w")
    for bib_in in bib_in_list:
        fi = open(bib_in,  "r")
        line = fi.readline()
        while line:
            if(line.find("@article")>-1):
                for c in cite_list:
                    if(line.find(c)>-1):
                        process(fi, line, fo)
            line = fi.readline()
