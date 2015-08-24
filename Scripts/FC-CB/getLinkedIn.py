import sys
import os


def getInfoList(inlist):
    testlines = list(inlist)
    startIndex = -1
    for line in testlines:
        trueline = line
        if trueline[-1] == "\n": trueline = line[:-1]
        words = trueline.split()
        if len(words) > 0:
            if(words[0] == "Displaying" and words[-1] == "LinkedIn:"):
                startIndex = testlines.index(line)
    if startIndex == -1:
        return None   
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
        if len(mywords) == 0:
            continue
        email = mywords[0]     
        for index in range(1, len(mywords)):
            if 'linkedin.com' in mywords[index]:
                word = mywords[index]
                prof = word[word.index('.com/') + len('.com/'):]
                while len(prof) > 0 and prof[-1] != "'":
                    prof = prof[:-1]
                print('Outside while loop, value of prof is ' + prof)
                prof = prof[:-1]
                print(prof)
                if email not in emails:
                    emails.append(email)
                    ids.append(prof)
            elif "'handle'" in mywords[index]:
                number = mywords[index + 1]
                realnum = number
                while len(realnum) > 0 and realnum[-1] != "'":
                    realnum = realnum[:-1]
                realnum = realnum[1:-1]
                if email not in emails:
                    emails.append(email)
                    ids.append(realnum)
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
Called by the 'execute' method of stage1.py, this method only reads LinkedIn information from a list
    '''
    content = getInfoList(inList)
    if content != None:
        intermediate = getIDs(content)   
        mailsfile = input('Enter name of file to hold all LinkedIn Emails')
        idsfile = input('Enter name of file to hold all LinkedIn IDs')
        reformat(intermediate, mailsfile, idsfile)

    
if __name__ == "__main__":
    feed = list(sys.argv)
    os.chdir("C:\\Users\\Adithya\\Desktop\\Summer '15\\NEWCLEUS")
    if len(feed) < 2:
        alllines = []
        myfolder = input('Enter input folder name: ')
        mailsfile = input('Enter name of file to hold all LinkedIn Emails')
        idsfile = input('Enter name of file to hold all LinkedIn IDs')
        for fil in os.listdir(myfolder):
            content = getInfo(os.getcwd() + '\\' + myfolder + '\\' + fil)
            if content != None:
                alllines += content
        finaloutput = getIDs(alllines)
        reformat(finaloutput, mailsfile,idsfile)
