#import urllib
import requests
import time
import sys
import writetofile
import clearbit

fc_key = 'aad9a20f28c2668d'
td_key = 'ae18e3ca3312d9314011b7f9afb708f2'

fc_base = 'https://api.fullcontact.com/v2/person.json?email='
fc_middle = '&apiKey='
#failed = []

cb_key = '89770fc52db237f17e4a7165937d8b2a'
clearbit.key = cb_key
pending = []

def extract_mails(inlist):
    out_list = []
    in_file = open(inlist)
    in_lines = in_file.readlines()
    for line in in_lines:
        realine = line
        if realine[-1] == '\n':
            realine = realine[:-1]
        myfields = realine.split('\t')
        if len(myfields) >= 4:
            if myfields[-1] != ' ' and '@' in myfields[-1]:
                out_list.append(myfields[-1])
    return out_list


def cb_info_from_mail(em):
    global save_str
    output_str = ""
    inp = em
    if inp[0] == "'":
        inp = inp[1:-1]
   # print(inp)
    if clearbit.key == None:
        clearbit.key = cb_key
    try:
        result = clearbit.Person.find(email=inp)
    except requests.exceptions.HTTPError:
        errormsg = "Either the limit has been reached for Clearbit API's free trial, or the e-mail address was totally invalid :/\nSee for yourself. The e-mail passed in was: " + inp
        print(errormsg)
        save_str += errormsg
        return("Query was not processed.")
    if result != None:
        if 'pending' in result.keys() and em not in pending:
            pending.append(inp)
            pendmessage = "Waiting on " + inp + "\n"
            save_str += pendmessage
            return pendmessage        
        if em in pending:
            pending.remove(em)
        for key in result:
            if result == 'id':
                continue
            val = result[key]
            if val != None:
                if type(val) == dict:
                    if None not in val.values():
                        output_str += str(key) + " : " + str(val) + "\n"
                else:
                    output_str += str(key) + " : " + str(val) + "\n"
        save_str += output_str
        return output_str
    else:
        if em in pending:
            pending.remove(em)
        notice = "Request failed for " + em + "\n"
        save_str += notice
        return notice

def cb_info_from_mails(em):
    global master_string
    starttime = time.time()
    successes = 0
    waiting = 0
    failures = 0
    output = []
    if type(em) == list:
        mail_list = list(em)
    elif type(em) == str:
        mail_list = em
        if mail_list[0] == '[':
            mail_list = mail_list[1:-1]
        mail_list = mail_list.split(', ')       
    else:
        print('Input is of inappropriate data type: ' + str(type(em)) + ', please enter strings or lists only.')
        return
    failure_info = []
    
    output = list(map(lambda x : cb_info_from_mail(x), mail_list))

    for index in range(len(output)):
        if output[index][:3] == "Req" or output[index][:5] == "Query":
            #badmessage = "Request failed for " + mail_list[index] + "\nRefer below for details.\n"
            #print(badmessage)
            #master_string += badmessage
            failures += 1
            failure_info.append(mail_list[index] + ":\n" + output[index])

        elif output[index][:4] == "Wait":
            #waitmessage = "Waiting on " + mail_list[index] + "\n" 
            #print(waitmessage)
            #master_string += waitmessage
            waiting += 1

        else:            
            goodmessage = "Info for " + mail_list[index] + " :\n" + output[index] + "\n" 
            print(goodmessage)        
            master_string += goodmessage
            successes += 1

    if waiting > 0:
        pendingmessage = "Please follow up ASAP on these pending requests:\n"
        for mail in pending:
            pendingmessage += mail + "\n"
        pendingmessage += "\n"
        print(pendingmessage)
        master_string += pendingmessage

    if failures > 0:
        failmessage = "Totally failed Requests:\n" 
        for failure in failure_info:
            failmessage += failure + "\n"
        print(failmessage)
        master_string += failmessage
    summarymessage = "\nClearbit Successes: " + str(successes) + "\nPending: " + str(waiting) + "\n" + "Clearbit Failures: " + str(failures) + "\n" + "Clearbit Success Rate: " + str(100*successes/(len(mail_list))) + "%\n" 
    endtime = time.time()
    timetaken = endtime - starttime
    summarymessage += "Time elapsed: " + str(timetaken) + " for " + str(len(mail_list)) + " entries\n"
    summarymessage += "Mean time taken by Clearbit per e-mail: " + str(timetaken/len(mail_list)) + "\n"
    print(summarymessage)
    master_string += summarymessage    

    ## This portion is still being resolved... only works if activated after a few minutes of waiting
    if waiting > 0:
        follow_up = input("Do you wish to follow up on the " + str(waiting) + " pending cases now?")
        if follow_up.lower() == 'y':
            cb_info_from_mails(pending)



def fc_info_from_mail(em):
    global save_str
    global failed
    output_str = ""
    requrl = fc_base + em + fc_middle + fc_key
    try:
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
        failed.append(em)
        save_str += notice
        return notice
    except requests.exceptions.HTTPError:
        errormsg = "Either the limit has been reached for FullContact API's free trial, or the e-mail address was totally invalid :/\nSee for yourself. The e-mail passed in was: " + em
        print(errormsg)
        save_str += errormsg
        return("Query was not processed.")
    
def fc_info_from_mails(em):
    global master_string
    starttime = time.time()
    successes = 0
    failures = 0
    output = []
    '''
    mail_list = em
    if mail_list[0] == '[':
        mail_list = mail_list[1:-1]

    if type(mail_list) == str:
        mail_list = mail_list.split(', ')    
    '''
    if type(em) == list:
        mail_list = list(em)
    elif type(em) == str:
        mail_list = em
        if mail_list[0] == '[':
            mail_list = mail_list[1:-1]
        mail_list = mail_list.split(', ')       
    else:
        print('Input is of inappropriate data type: ' + str(type(em)) + ', please enter strings or lists only.')
        return
    failure_info = []
    
    output = list(map(lambda x : fc_info_from_mail(x), mail_list))
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
        failmessage = "The following failed requests are forwarded to Clearbit:\n"         
        for failure in failure_info:
            failmessage += failure + '\n'
            #print(failure)
        print(failmessage)
        master_string += failmessage


        
    summarymessage = "\nFullContact Successes: " + str(successes) + "\n"+ "FullContact Failures: " + str(failures) + "\n" + "FullContact Success Rate: " + str(100*successes/(successes + failures)) + "%" 
    print(summarymessage)
    master_string += summarymessage
    endtime = time.time()
    timetaken = endtime - starttime
    finalmessage = "Time elapsed: " + str(timetaken) + " for " + str(len(mail_list)) + " entries\n" + "Mean time taken by FullContact per e-mail: " + str(timetaken/len(mail_list)) + "\n"  
    print(finalmessage)
    master_string += finalmessage




def main(argv):
    return info_from_mails(argv)

if __name__ == "__main__":
    global master_string
    global save_str
    global failed
    failed = []
    save_str = ''
    master_string = ''
    feed = list(sys.argv)
    if len(feed) < 2:
        mailsfile = input('Enter file name: ')
        mymaillist = extract_mails(mailsfile)
        fc_info_from_mails(mymaillist)
        cb_info_from_mails(failed)
        recordlist = master_string.split('\n')
        writetofile.writeFromList(recordlist)                
    else:
        main(sys.argv[1])
