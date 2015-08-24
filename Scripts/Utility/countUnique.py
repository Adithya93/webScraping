import sys

def numUnique(infile):
    results = {'linkedin': 0, 'twitter': 0, 'facebook': 0}
    if type(infile) == list:
        mylines = list(infile)
    elif type(infile) == str:
        mylines = infile.split('\n')
    else:
        myfile = open(infile)
        mylines = myfile.readlines()
        myfile.close()
    for line in mylines:
        for soc in list(results.keys()):
            if soc in line.lower():
                results[soc] += 1
    for soc in results:
        print(soc + ": " + str(results[soc]))
    return results

    
