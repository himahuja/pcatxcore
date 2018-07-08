import pickle as pk
def crawlCIKcodes(filename):
    """
    Takes in the CIK code list from: https://www.sec.gov/Archives/edgar/full-index/<YYYY>/QTR<1,2,3,4>/master.gz
    Extract the .gz file, and remove all the lines above the code list

    INPUT: filename of the file as described above
    OUTPUT: dictionary of CIK codes
    NOTE: maintains a CIK code list, appends new CIK items with each new file
          filename for dict pickle: cikcodes2name.pk and ciknames2code.pk
    """
    lines = open(filename, 'r').readlines()
    try:
        with open('../data//{}.pk'.format(search_query), 'wb') as handle:
            pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)

    cikcodes2name = {}
    for line in lines:
        k = line.split('|')
        cikcodes2name[k[0]] = k[1]


if __name__ == '__main__':
    filename = '../data/SEC_Data/CIK_2018_1.txt'
    crawlCIKcodes(filename)
