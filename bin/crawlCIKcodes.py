import pickle as pk
def crawlCIKcodes(filename):
    """
    Takes in the CIK code list from: https://www.sec.gov/Archives/edgar/full-index/<YYYY>/QTR<1,2,3,4>/master.gz
    Extract the .gz file, and remove all the lines above the code list
    The file is renamed to : CIK_YYYY_<QTR Digit>.txt, example: CIK_2018_1.txt

    INPUT: filename of the file as described above
    OUTPUT: dictionary of CIK codes
    NOTE: maintains a CIK code list, appends new CIK items with each new file
          filename for dict pickle: cikcodes2name.pk and ciknames2code.pk
    """
    lines = open(filename, 'r').readlines()
    try:
        with open('../data/SEC_data/cikcodes2name.pk', 'rb') as f:
            cikcodes2name = pk.load(f)
    except:
        cikcodes2name = {}

    try:
        with open('../data/SEC_data/ciknames2code.pk', 'rb') as f:
            ciknames2code = pk.load(f)
    except:
        ciknames2code = {}

    for line in lines:
        k = line.split('|')
        ciknames2code[k[1]] = k[0]
        cikcodes2name[k[0]] = k[1]

    with open('../data/SEC_data/cikcodes2name.pk', 'wb') as handle:
        pk.dump(cikcodes2name, handle, protocol=pk.HIGHEST_PROTOCOL)

    with open('../data/SEC_data/ciknames2code.pk', 'wb') as handle:
        pk.dump(ciknames2code, handle, protocol=pk.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    filename = '../data/SEC_Data/CIK_2018_1.txt'
    crawlCIKcodes(filename)
