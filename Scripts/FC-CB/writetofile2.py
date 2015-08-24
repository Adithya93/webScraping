'''
Utility functions for writing logs, summaries and custom HTML Documents. Contains special writing, printing and string processing methods to deal with unicode.
'''

import sys
import countUnique

def writeSafe(x,y):
    '''
Helper method to safely deal with unicode while minimizing lost characters
    '''
    try:
        y.write(x)
    except UnicodeEncodeError:
        lines = x.split('\n')
        for line in lines:
            try:
                y.write(line + '\n')
            except UnicodeEncodeError:
                words = line.split()
                for word in words:
                    try:
                        y.write(word + ' ')
                    except UnicodeEncodeError:
                        for letter in word:
                            try:
                                y.write(letter)
                            except UnicodeEncodeError:
                                print('Skipping a character')

def tryPrint(x):
    '''
Print analog of above function
    '''
    try:
        print(x)
    except UnicodeEncodeError:
        lines = x.split('\n')
        for line in lines:
            try:
                print(line + '\n')
            except UnicodeEncodeError:
                words = line.split()
                for word in words:
                    try:
                        print(word + ' ')
                    except UnicodeEncodeError:
                        for letter in word:
                            try:
                                print(letter)
                            except UnicodeEncodeError:
                                print('Skipping a character')



def fromDict(x):
    '''
Converts string form of Dictionary into list of tuples of strings to facilitate writing (to custom HTML Doc)
    '''
    if x[0] != '{':
        raise(ValueError('fromDict method only accepts string form of dictionaries, first character must be "{"'))
    items = []
    info = x[1:-1]
    pairs = info.split(', ')
    for pair in pairs:
        if ':' in pair:
            #print('Pair inside dictionary is ' + pair)

            keyStr = pair[:pair.index(':')]
            valStr = pair[pair.index(':') + 2 :]
            if keyStr[0] == "'" and keyStr[-1] == "'":
                keyStr = keyStr[1:-1]
            if valStr[0] == "'" and valStr[-1] == "'":
                valStr = valStr[1:-1]
            items.append((keyStr, valStr))
    return items


def fromList(x):
    '''
Converts string form of List into list of comma-seperated strings to facilitate writing (to custom HTML Doc)
    '''
    if x[0] != '[':
        raise(ValueError('fromList method only accepts string form of lists, first character must be "["'))
    info = x[1:-1]
    values = info.split(', ')
    items = [x[1:-1] for x in values if len(x) > 0 and x[0] == "'" and x[-1] == "'"]
    return items


def writeFromList(finalist):
    '''
Called by cbemailtoinfo2.py in creating log file and summary file for PEOPLE and COMPANIES
    '''
    if type(finalist) != list:
        raise TypeError('Only lists should be fed into the writeFromList method')
    finalstr = '\n'.join(finalist)
    lilist = []
    twitlist = []
    fblist = []

    peopleList = []
    compList = []    
    
    filetitle = input('Choose a name for the log file')
    logfile = open(filetitle, 'w')
    writeSafe(finalstr, logfile)
    logfile.close()
    sumtitle = input('Choose a name for the PEOPLE summary file: ')

    comptitle = input('Choose a name for the COMPANIES summary file: ')

    sumfile = open(sumtitle, 'w')

    compfile = open(comptitle, 'w')

    sumfile.write('General Information:\n')

    compfile.write('General Information:\n')
    
    checkfile = open(filetitle)
    bigstrlower = checkfile.read().lower()
    checkfile.close()

    uniques = countUnique.numUnique(bigstrlower)
    licount = uniques['linkedin']
    twitcount = uniques['twitter']
    fbcount = uniques['facebook']

    sumfile.write('Total Appearances of LinkedIn: ' + str(licount) + "\n")
    sumfile.write('Total Appearances of Twitter: ' + str(twitcount) + "\n")
    sumfile.write('Total Appearances of Facebook: ' + str(fbcount) + "\n")    
    mylines = bigstrlower.split('\n')
    index = 0
    email = ''
    compInfo = ''

    peopleLIs = 0
    peopleFBs = 0
    peopleTWs = 0

    compLIs = 0
    compFBs = 0
    compTWs = 0

    person_mode = True
    
    while index < len(mylines):
        line = mylines[index]

        if 'info for ' in line:
            words = line.split()
            email = words[-2]

        if line == 'person':
            person_mode = True

        if line == 'company':
            compInfo = email + '\n' + '\n'.join(mylines[index + 1 : mylines.index('', index)])
            if compInfo != email + '\n':
                compList.append(compInfo + '\n')
                person_mode = False               

        if line == '':
            email = ''
            compInfo = ''
    
        if 'linkedin' in line:
            if person_mode:
                peopleLIs += 1
                lilist.append(email + ' : ' + line)
            else:
                compLIs += 1
            
        if 'twitter' in line:
            if person_mode:
                peopleTWs += 1
                twitlist.append(email + ' : ' + line)
            else:
                compTWs += 1
            
        if 'facebook' in line:
            if person_mode:
                peopleFBs += 1
                fblist.append(email + ' : ' + line)
            else:
                compFBs += 1

        index += 1

    sumfile.write('PEOPLE Appearances of LinkedIn: ' + str(peopleLIs) + '\n')
    sumfile.write('PEOPLE Appearances of Twitter: ' + str(peopleTWs) + '\n')
    sumfile.write('PEOPLE Appearances of Facebook: ' + str(peopleFBs) + '\n\n')
    
    liHeader = 'Displaying information relevant to LinkedIn:\n'
    sumfile.write(liHeader)
    peopleList.append(liHeader)

    liContent = '\n'.join(lilist) + '\n' 
    writeSafe(liContent + '\n', sumfile)
    peopleList += lilist
    peopleList.append('\n')


    twHeader = 'Displaying information relevant to Twitter:\n'
    sumfile.write(twHeader)
    peopleList.append(twHeader)

    twContent = '\n'.join(twitlist) + '\n'
    writeSafe(twContent + '\n', sumfile)
    peopleList += twitlist
    peopleList.append('\n')

    fbHeader = 'Displaying information relevant to Facebook:\n'
    sumfile.write(fbHeader)
    peopleList.append(fbHeader)

    fbContent = '\n'.join(fblist) + '\n'
    writeSafe(fbContent + '\n', sumfile)
    peopleList += fblist
    peopleList.append('\n')

    compfile.write('Displaying information for COMPANIES:\n')
    compfile.write('COMPANY Appearances of LinkedIn: ' + str(compLIs) + '\n')
    compfile.write('COMPANY Appearances of Twitter: ' + str(compTWs) + '\n')
    compfile.write('COMPANY Appearances of Facebook: ' + str(compFBs) + '\n\n')
    compfile.write('\n\n')
    writeSafe('\n'.join(compList), compfile)

    sumfile.write('End Of PEOPLE Report\n')
    pplBitsWritten = sumfile.tell()
    sumfile.close()

    compfile.write('End Of COMPANIES Report\n')
    compBitsWritten = compfile.tell()
    compfile.close()

    #return pplBitsWritten + compBitsWritten
    return (peopleList, compList)

def makeCompPage(complist):
    pageName = input('Choose name of custom HTML Document for Companies Info: ')
    page = open(pageName, 'w')
    #prefix = 'COMPANY_'
    page.write('<html>')
    for comp in complist:
        thisComp = comp.split('\n')
        email = thisComp[0]
        #writeSafe('<div id = "Email">' + email + '">', page)
        page.write('<div class = "COMPANY">')
        writeSafe('<p id = "Email">' + email + '</p>', page)

        for line in thisComp[1:]:
            words = line.split()
            if len(words) == 0:
                continue
            field = words[0]
            value = ' '.join(words[2:])
            if value[0] == '{' and value[-1] == '}':
                info = fromDict(value)
                for pair in info:
                    writeSafe('<p id = "' + field + '_' + pair[0] + '">' + pair[1] + '</p>', page)
            elif value[0] == '[' and value[-1] == ']':
                info = fromList(value)
                writeSafe('<p id = "' + field + '">' + ', '.join(info) + '</p>', page)
            else:
                writeSafe('<p id = "' + field + '">' + value + '</p>', page)
        page.write('</div>')
    page.write('</html>')
    page.close()


'''
DEPRECATED
def run():
    return


if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) < 2:
        inarg = input('If reading from a file, enter file name. Otherwise, just hit enter for now.')
        if inarg != '':
            numwritten = writeOutput(inarg)
            #print(numwritten)
        else:
            inlist = input('Enter the input with lines separated by the newline character')
            complist = writeFromList(inlist)
            makeCompPage(complist)
            
    else:
        writeOutput(feed[1])
'''
