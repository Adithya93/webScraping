import sys
import countUnique

def writeFromList(finalist):
    if type(finalist) == str:
        finalist = finalist.split('\n')
        #print(len(finalist))
    lilist = []
    twitlist = []
    fblist = []    
    filetitle = input('Choose a name for the log file')
    logfile = open(filetitle, 'w')
    for line in finalist:
        try:
            logfile.write(line + '\n')
        except UnicodeEncodeError:
            print('Hey! Some unencodable characters were encountered! This is ' + str(logfile.tell()) +' bytes into the file. The following line will have missing characters in the log:')
            print(line)
            for char in line:
                try:
                    logfile.write(char)
                except UnicodeEncodeError:
                    continue            
    logfile.close()
    sumtitle = input('Choose a name for the summary file')
    sumfile = open(sumtitle, 'w')
    sumfile.write('General information:\n')
    checkfile = open(filetitle)
    bigstrlower = checkfile.read().lower()
    checkfile.close()

    uniques = countUnique.numUnique(bigstrlower)
    #licount = bigstrlower.count('linkedin')
    #twitcount = bigstrlower.count('twitter')
    #fbcount = bigstrlower.count('facebook')
    licount = uniques['linkedin']
    twitcount = uniques['twitter']
    fbcount = uniques['facebook']

    sumfile.write('Appearances of "LinkedIn: "' + str(licount) + "\n")
    sumfile.write('Appearances of "Twitter: "' + str(twitcount) + "\n")
    sumfile.write('Appearances of "Facebook: "' + str(fbcount) + "\n")    
    mylines = bigstrlower.split('\n')
    for line in mylines:
        if 'linkedin' in line:
            lilist.append(line)
        if 'twitter' in line:
            twitlist.append(line)
        if 'facebook' in line:
            fblist.append(line)
    sumfile.write('Displaying information relevant to LinkedIn:\n')
    for line in lilist:
        sumfile.write(line + '\n')
    sumfile.write('\n')
    sumfile.write('Displaying information relevant to Twitter:\n')
    for line in twitlist:
        sumfile.write(line + '\n')
    sumfile.write('\n')
    sumfile.write('Displaying information relevant to Facebook:\n')
    for line in fblist:
        sumfile.write(line + '\n')
    sumfile.write('\n')
    sumfile.write('End Of Report\n')
    bitswritten = sumfile.tell()
    sumfile.close()
    return bitswritten

def writeOuput(inputfile):
    lilist = []
    twitlist = []
    fblist = []    
    #filetitle = input('Choose a name for the log file')
    #logfile = open(filetitle, 'w')
    #for line in finalist:
    #    logfile.write(line + '\n')
    #logfile.close()
    sumtitle = input('Choose a name for the summary file')
    sumfile = open(sumtitle, 'w')
    sumfile.write('General information:\n')
    checkfile = open(inputfile)
    bigstrlower = checkfile.read().lower()
    checkfile.close()
    licount = bigstrlower.count('linkedin')
    twitcount = bigstrlower.count('twitter')
    fbcount = bigstrlower.count('facebook')
    sumfile.write('Appearances of "LinkedIn: "' + str(licount) + "\n")
    sumfile.write('Appearances of "Twitter: "' + str(twitcount) + "\n")
    sumfile.write('Appearances of "Facebook: "' + str(fbcount) + "\n")    
    mylines = bigstrlower.split('\n')
    for line in mylines:
        if 'linkedin' in line:
            lilist.append(line)
        elif 'twitter' in line:
            twitlist.append(line)
        elif 'facebook' in line:
            fblist.append(line)
    sumfile.write('Displaying information relevant to LinkedIn:\n')
    for line in lilist:
        sumfile.write(line + '\n')
    sumfile.write('\n')
    sumfile.write('Displaying information relevant to Twitter:\n')
    for line in twitlist:
        sumfile.write(line + '\n')
    sumfile.write('\n')
    sumfile.write('Displaying information relevant to Facebook:\n')
    for line in fblist:
        sumfile.write(line + '\n')
    sumfile.write('\n')
    sumfile.write('End Of Report\n')
    bitswritten = sumfile.tell()
    sumfile.close()
    return bitswritten



if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) < 2:
        inarg = input('If reading from a file, enter file name. Otherwise, just hit enter for now.')
        if inarg != '':
            numwritten = writeOutput(inarg)
            print(numwritten)
        else:
            inlist = input('Enter the input with lines separated by the newline character')
            writeFromList(inlist)
    else:
        writeOutput(feed[1])

