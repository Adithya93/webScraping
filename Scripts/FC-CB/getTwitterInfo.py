import sys
import os
import time

def getInfoList(inlist):
    startIndex = -1
    for line in inlist:
        trueline = line
        if trueline[-1] == "\n": trueline = line[:-1]
        words = trueline.split()
        if len(words) > 0:
            if(words[0] == "Displaying" and words[-1] == "Twitter:"):
                startIndex = inlist.index(line)
    if startIndex == -1:
        return    
    endIndex = inlist.index('\n',startIndex)
    outlines = inlist[startIndex + 1:endIndex]
    return outlines


def getInfo(infile):
    myfile = open(infile)
    mylines = myfile.readlines()
    myfile.close()
    return getInfoList(mylines)

def getIDs(myInput):
    ids = []
    email = ''
    mylines = list(myInput)
    for linenum in range(len(mylines)):
        mywords = mylines[linenum].split()
        email = mywords[0]
        for index in range(1, len(mywords)):             
            if "'id'" in mywords[index]:
                number = mywords[index + 1]
                realnum = number
                if realnum[0] == "'":
                    realnum = realnum[1:-1]
                if realnum[-1] == "," or realnum[-1] == "'":
                    realnum = realnum[:-1]
                ids.append((email, int(realnum)))
    uniqueIDs = set(ids)
    idsList = list(uniqueIDs)
    return idsList

def reformat(inlist, mailsfile, idsfile):
    mails = open(mailsfile, 'w')
    ids = open(idsfile, 'w')
    for pair in inlist:
        if len(pair) > 1:
            mails.write(str(pair[0]) + '\n')
            ids.write(str(pair[1]) + '\n')
        else:
            print('Missing id for ' + str(pair[0]))
    mails.close()
    ids.close()


def run(inList):
    '''
Called by the 'execute' method of stage1.py, this method only reads Twitter information from a list
    '''
    content = getInfoList(inList)
    if content != None:
        intermediate = getIDs(content)
        mailsfile = input('Enter name of file to hold all Twitter Emails')
        idsfile = input('Enter name of file to hold all Twitter IDs')
        reformat(intermediate, mailsfile, idsfile)

  

if __name__ == "__main__":
    feed = list(sys.argv)
    os.chdir("C:\\Users\\Adithya\\Desktop\\Summer '15\\NEWCLEUS")
    if len(feed) < 2:
        alllines = []
        myfolder = input('Enter input folder name: ')
        myoutput = 'TWTemp.txt'
        myIDs = 'TWTempIDs.txt'
        mailsfile = input('Enter name of output file to hold Twitter Emails: ')
        idsfile = input('Enter name of output file to hold Twitter IDs: ')
        alllines = []
        for fil in os.listdir(myfolder):
            content = getInfo(os.getcwd() + '\\' + myfolder + '\\' + fil)
            if content != None:
                alllines += content
        finaloutput = getIDs(alllines)
        result = reformat(finaloutput, mailsfile, idsfile)
        print(finaloutput)    
                
        
