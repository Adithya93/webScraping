import sys
import os
from getLinkedIn import reformat as r


def getInfoList(testlines):
    startIndex = -1
    for line in testlines:
        trueline = line
        if trueline[-1] == "\n": trueline = line[:-1]
        words = trueline.split()
        if len(words) > 0:
            if(words[0] == "Displaying" and words[-1] == "Facebook:"):
                startIndex = testlines.index(line)
    if startIndex == -1:
        return    
    endIndex = testlines.index('\n',startIndex)
    outlines = testlines[startIndex + 1:endIndex]
    return outlines
    

def getInfo(infile):
    myfile = open(infile)
    mylines = myfile.readlines()
    myfile.close()
    return getInfoList(mylines)


def getIDs(mylines):
    ids = []
    emails = []
    email = ''
    for linenum in range(len(mylines)):
        mywords = mylines[linenum].split()
        email = mywords[0]
        for index in range(1, len(mywords)):
            if "'id'" in mywords[index] or "'handle'" in mywords[index]:
                number = mywords[index + 1]
                realnum = number
                if realnum[0] == "'":
                    realnum = realnum[1:]
                while realnum[-1] != "'":
                    realnum = realnum[:-1]
                realnum = realnum[:-1]
                emails.append(email)
                ids.append(realnum)
                break
            elif 'facebook' in mywords[index]:
                url = mywords[index]
                if 'facebook.com/' in url:
                    realnum = url[url.index('.com/') + len('.com/'):]
                    while realnum[-1] != "'":
                        realnum = realnum[:-1]
                    realnum = realnum[:-1]
                    print(realnum)
                    if email not in emails:
                        emails.append(email)
                        print('Adding ' + email + ' to list')
                        ids.append(realnum)
                        break
    return (emails, ids)


def reformat(values, mailsfile, idsfile):
    emails = values[0]
    ids = values[1]
    if len(emails) != len(ids):
        raise ValueError('Length of Emails is not same as length of IDs! Quitting.')
    mails = open(mailsfile, 'w')
    IDs = open(idsfile, 'w')
    mails.write('["')
    IDs.write('["')
    for index in range(len(emails) - 1):
        mails.write(emails[index] + '", "')
        IDs.write(ids[index] + '", "')
    mails.write(emails[-1] + '"]')
    IDs.write(ids[-1] + '"]')
    mails.close()
    IDs.close()


def run(inList):
    '''
Called by the 'execute' method of stage1.py, this method only reads Facebook information from a list
    '''
    content = getInfoList(inList)
    if content != None:
        intermediate = getIDs(content)   
        mailsfile = input('Enter name of file to hold all Facebook Emails')
        idsfile = input('Enter name of file to hold all Facebook IDs')
        reformat(intermediate, mailsfile, idsfile)


if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) < 2:
        os.chdir("C:\\Users\\Adithya\\Desktop\\Summer '15\\NEWCLEUS")
        alllines = []
        myfolder = input('Enter input folder name: ')
        mailsfile = input('Enter name of output file to hold all FB emails: ')
        idsfile = input('Enter name of output file to hold all FB IDs: ')
        for fil in os.listdir(myfolder):
            content = getInfo(os.getcwd() + '\\' + myfolder + '\\' + fil)
            if content != None:
                alllines += content
        finaloutput = getIDs(alllines)         
        r(finaloutput, mailsfile, idsfile)
        print(finaloutput)    
