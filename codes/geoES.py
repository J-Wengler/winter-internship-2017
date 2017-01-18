#!/usr/bin/python3

import re
import argparse
from xml.dom import minidom
import urllib.request

def main():
    #Declaration of the URL of eutils of NCBI GDS
    gdsUrl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&'

    #Parsing allowed positional and optional arguments, arguments that start with -- are optional arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('term', type=str, help='the term to be searched')
    parser.add_argument('--field', type=str, help='limited the search to the specified Entrez field')
    parser.add_argument('--retmax', type=str, default=20, help='maximum number of UIDs to be returned')
    parser.add_argument('--datetype', type=str, choices=['mdat', 'pdat'], help='type of date; \'mdat\' \
                        for modification date and \'pdat\' for publication date')
    parser.add_argument('--reldate', type=str, help='returns only those items within the last n days')
    
    args = parser.parse_args()

    #Replace the space with + sign because the presence of space in the url with return error
    term = str(args.term).replace(' ', '+')
    field = str(args.field)
    retmax = str(args.retmax)
    datetype = str(args.datetype)
    reldate = str(args.reldate)

    queryUrl = gdsUrl + 'term=' + term

    #Checking if the arguments are present or not and appending them to the queryUrl if they
    #are present
    if field != None:
        queryUrl += '&field=' + field
    if retmax != None:
        queryUrl += '&retmax=' + retmax
    if datetype != None:
        queryUrl += '&datetype' + datetype
    if reldate != None:
        queryUrl += '&reldate' + reldate
    
    #Retrieving the 
    ret = urllib.request.urlopen(queryUrl)
    filename = str(ret.read())
    
    
    ptrn = r'<Id>(\d*)</Id>'
    UIDs = re.findall(ptrn, filename)

    if UIDs == []:
        print('Your search query returned no results')
    else:
        print(UIDs)

if __name__ == '__main__':
    main()
