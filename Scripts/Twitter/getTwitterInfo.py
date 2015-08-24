import sys
import os

def getInfo(infile):
    myfile = open(infile)
    mylines = myfile.readlines()
    myfile.close()
    testlines = list(mylines)
    startIndex = -1
    for line in testlines:
        trueline = line
        if trueline[-1] == "\n": trueline = line[:-1]
        words = trueline.split()
        if len(words) > 0:
            if(words[0] == "Displaying" and words[-1] == "Twitter:"):
                startIndex = testlines.index(line)
    if startIndex == -1:
        return    
    endIndex = testlines.index('\n',startIndex)
    outlines = testlines[startIndex + 1:endIndex]
    return outlines

def getIDs(infile, outfile):
    ids = []
    myfile = open(infile)
    output = open(outfile, 'w')
    mylines = myfile.readlines()
    myfile.close()
    for linenum in range(1, len(mylines)):
        mywords = mylines[linenum].split()
        for index in range(len(mywords)):
            if "'id'" in mywords[index]:
                number = mywords[index + 1]
                realnum = number
                if realnum[0] == "'":
                    realnum = realnum[1:-1]
                if realnum[-1] == "," or realnum[-1] == "'":
                    realnum = realnum[:-1]
                ids.append(int(realnum))
    uniqueIDs = set(ids)
    for line in uniqueIDs:
        output.write(str(line) + '\n')
    output.close()
    return ids


if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) < 2:
        alllines = []
        myfolder = input('Enter input folder name: ')
        myoutput = input('Enter name of output file with all Twitter Info: ')
        myIDs = input('Enter name of file to hold all IDs: ')
        os.chdir("C:\\Users\\Adithya\\Desktop\\Summer '15\\Machine Learning")
        for file in os.listdir(myfolder):
            content = getInfo(file)
            if content != None:
                alllines += getInfo(file)
        alldata = open(myoutput, 'w')
        for line in alllines:
            alldata.write(line)
        alldata.close()
        finaloutput = getIDs(myoutput, myIDs)         
        print(finaloutput)    
                
        
