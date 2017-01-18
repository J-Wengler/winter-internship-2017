#!/usr/bin/python3

import re
import argparse
#from xml.dom import minidom
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
    
    #Retrieving the .xml file of the result
    ret = urllib.request.urlopen(queryUrl)
    filename = str(ret.read())
    
    #Using regular expression to find all of the UID in the .xml file
    ptrn = r'<Id>(\d*)</Id>'
    UIDs = re.findall(ptrn, filename)

    #Creating a list of the GDS<ID> and the title of the data sets
    eSumsUrl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id='
    sumPtrn = r'<Item Name=\"title\" Type=\"String\">(.*)</Item>\\n\\t<Item Name=\"sum'
    for UID in UIDs:
        eSumUrl = eSumsUrl + UID
        ret = urllib.request.urlopen(eSumUrl)
        filename = str(ret.read())
        summ = ''.join(re.findall(sumPtrn, filename))
        print('['+ UID + '] ' + summ)
    
    if UIDs == []:
        print('Your search query returned no results')
        return 0

    #Asking whether the user wants to download the any of the data sets or not and requesting
    #GDS<id> if the user said Yes
    option = input("Do you want to download any of the data sets listed above (Yes/No)? ").lower()

    while option != 'yes' and option != 'no':
        option = input("Please only enter either \'yes' or \'no': ")

    if option == 'yes':



        UIDInput = str(input('Please enter the ID of the data set that you want to download: '))
        print("\nHere are the available formats for the UIDs:")
        print("[1] SOFT, by DataSet\n[2] SOFT full, by DataSet\n[3] SOFT, by Platform")
        print("[4] SOFT, by Series\n[5] MINiML, by Platform\n[6] MINiML, by Series\n")
        formatInput = int(input('Please select one by entering the number: '))
    elif option == 'no':
        print('\nThank you for using the program.')
        return 0


if __name__ == '__main__':
    main()
