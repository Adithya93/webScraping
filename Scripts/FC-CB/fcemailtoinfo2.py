import requests
import time
import sys
import writetofile2
import os

#fc_key = 'aad9a20f28c2668d'
#fc_key = '93882db6d6decb5d'
#fc_key = '4f08d5474b2257c0'
#fc_key = 'f25500041c784918'
fc_key = 'f5172a06ab3e8c53'
td_key = 'ae18e3ca3312d9314011b7f9afb708f2'

fc_base = 'https://api.fullcontact.com/v2/person.json?email='
fc_middle = '&apiKey='
failed = []


def extract_mails(inlist):
    out_list = []
    in_file = open(inlist)
    in_lines = in_file.readlines()
    for line in in_lines:
        realine = line
        if realine[-1] == '\n':
            realine = realine[:-1]
        myfields = realine.split('\t')
        if len(myfields) > 0:
            if myfields[-1] != ' ' and '@' in myfields[-1]:
                out_list.append(myfields[-1])
    return out_list


def info_from_mail(em):
    global save_str
    output_str = ""
    requrl = fc_base + em + fc_middle + fc_key
    result = requests.get(requrl)
    if(result.status_code == 200):
        resultjson = result.json()
        if 'socialProfiles' in list(resultjson.keys()):
            socprofs = resultjson['socialProfiles']
            for prof in socprofs:
                output_str += str(prof) + "\n"
            save_str += output_str + "\n"
            return output_str
    notice = "Request failed with the following message:\n" + str(result.content) + "\n"
    save_str += notice
    return notice

def info_from_mails(em):
    global master_string
    starttime = time.time()
    successes = 0
    failures = 0
    output = []
    mail_list = em
    if mail_list[0] == '[':
        mail_list = mail_list[1:-1]

    if type(mail_list) == str:
        mail_list = mail_list.split(', ')    
    failure_info = []
    
    output = list(map(lambda x : info_from_mail(x), mail_list))
    for index in range(len(output)):
        if output[index][:3] == "Req":
            #print("Request failed for " + mail_list[index] + "\nRefer below for details.\n" ) 
            failures += 1
            failure_info.append(mail_list[index] + ":\n" + output[index])
        else:
            successes += 1
            message = "Info for " + mail_list[index] + " :\n" + output[index] 
            print(message)
            master_string += (message)
    if failures > 0:
        failmessage = "Failed Requests:\n"         
        for failure in failure_info:
            failmessage += failure + '\n'
            #print(failure)
        print(failmessage)
        master_string += failmessage
    summarymessage = "\nSuccesses: " + str(successes) + "\n"+ "Failures: " + str(failures) + "\n" + "Success Rate: " + str(100*successes/(successes + failures)) + "%" 
    print(summarymessage)
    master_string += summarymessage
    endtime = time.time()
    timetaken = endtime - starttime
    finalmessage = "Time elapsed: " + str(timetaken) + " for " + str(len(mail_list)) + " entries\n" + "Mean time taken per e-mail: " + str(timetaken/len(mail_list)) + "\n"  
    print(finalmessage)
    master_string += finalmessage


def main(argv):
    return info_from_mails(argv)

if __name__ == "__main__":
    global master_string
    global save_str
    save_str = ''
    master_string = ''
    feed = list(sys.argv)
    os.chdir("C://Users/Adithya/Desktop/Summer '15/NEWCLEUS")
    if len(feed) < 2:
        feed = input('If you are looking up a single e-mail address, please type the e-mail address here. Otherwise, just hit enter.')
        if feed == '':
            feed = input('Enter e-mail addresses seperated by commas, or enter a list of e-mail addresses')
            if feed != '':
                info_from_mails(feed)
            else:
                mailsfile = input('Enter file name: ')
                mymaillist = extract_mails(mailsfile)
                info_from_mails(mymaillist)
                recordlist = master_string.split('\n')
                writetofile2.writeFromList(recordlist)                
        else:
            print(info_from_mail(feed))
    else:
        main(sys.argv[1])
