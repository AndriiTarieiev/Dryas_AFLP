#!/usr/bin/env python3                  
#
# sampleStructureFile.py
# Last updated on 13 March 2013 by kjemerson
#
# This script takes a structure file and randomly samples n loci from that file for all populations.
# This script takes as input the number of fixed columns (default 2) in the structure file - those
# columns are maintained in the output file..


from optparse import OptionParser
import os
import sys
import datetime
import random
import logging
import platform

# main()
#   
def main(cmdline=None):
    parser = make_parser()
    opts, args = parser.parse_args(cmdline)

    # Check for required options

    if not opts.numFixedCols:
        parser.error("numFixedCols not given.")
    if not opts.numLoci:
        parser.error("numLoci not given.")
    if not opts.outFileName:
        parser.error("outFile not given.")
    if not opts.fileName:
        parser.error("inFile not given.")

    logging.basicConfig(filename='sampleStructure.log', level=logging.INFO,
                        format='%(message)s')

    if not os.path.isfile(opts.fileName):
        print("Error: Input Filename does not exist")
        sys.exit()

    if os.path.isfile(opts.outFileName):
        print("Error: Output File already exists.")
        sys.exit()

    # round 1: decide how many columns are in the file
    InFile = open(opts.fileName, 'r')
    numCols = len(InFile.readline().strip("\n").split("\t"))
    InFile.close()

    # generate a random list of indices to sample from the colums
    # note that it is -2 becasue you will always retain the sample name and the population name

    columns = list(range(opts.numFixedCols,numCols))
    indices = sorted(random.sample(columns, opts.numLoci))

    logging.info('------')
    logging.info('Run started on %s', datetime.datetime.now())
    logging.info('Running on: %s', ":".join(platform.uname()))
    logging.info('Running in working directory: %s', os.getcwd())
    logging.info('Input File:  %s', opts.fileName)
    logging.info('Output File: %s', opts.outFileName)
    logging.info('There are %d columns in %s', numCols, opts.fileName)
    logging.info('Using indices: %s', " ".join(str(i) for i in indices))

    # round 2: rewrite the lines of the file
    InFile = open(opts.fileName, 'r')
    OutFile = open(opts.outFileName, 'w')
    for line in InFile:
        newLine = [line.strip("\n").split("\t")[i] for i in indices]
        outString = "%s\t%s\n" % ("\t".join(line.split("\t")[0:2]), "\t".join(newLine))   
        OutFile.write(outString)
    InFile.close()
    return 0

# make_parser()
#                                                               
def make_parser(): 
    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")
    parser.add_option("-f", "--numFixedCols", help="number of fixed columns in file",
                      action="store", type="int", dest="numFixedCols")
    parser.add_option("-n", "--numLoci", help="number of loci to sample",
                      action="store", type="int", dest="numLoci") 
    parser.add_option("-i", "--inFile", help="input structure file",
                      action="store", type="string", dest="fileName")
    parser.add_option("-o", "--outFile", help="output file destination",
                      action="store", type="string", dest="outFileName")
    return parser

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
