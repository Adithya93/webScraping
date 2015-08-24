import os, sys
import cbRefactored as cbr
import getLinkedIn as gLI
import getFBInfo as gFB
import getTwitterInfo as gTW
import writetofile2 as w2


CHOSEN_DIR = "C:\\Users\\Adithya\\Desktop\\Summer '15\\NEWCLEUS"
CB_KEY = cbr.cb_key

def execute(data, key = cbr.cb_key):
    if key == None:
        raise(ValueError('No valid key has been supplied. Supply key with named parameter "key = %YOUR_KEY_HERE%" or as 4th positional argument'))
    peopleList = cbr.run(data)
    gLI.run(peopleList)
    gTW.run(peopleList)
    gFB.run(peopleList)



if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) == 1:
        os.chdir(CHOSEN_DIR)
        data = input('Enter name of file with emails: ')
        while data not in os.listdir(os.getcwd()):
            data = input('File "' + data + '" does not exist in ' + os.getcwd()+ ' . Please check path and enter correct filename: ')
    elif len(feed) == 2:
        data = feed[1]
    if CB_KEY == None:
        CB_KEY = input('Clearbit Key has not been set. Please enter a valid key, without quotes: ')
    execute(data, CB_KEY)
    
        

            
        
    
    
