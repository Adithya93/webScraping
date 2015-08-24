import requests
import clearbit
import time
import sys
import writetofile

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
        if len(myfields) > 0:
            if myfields[0] != ' ' and '@' in myfields[0]:
                out_list.append(myfields[0])
    return out_list


def info_from_mail(em):
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

def info_from_mails(em):
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

    output = list(map(lambda x : info_from_mail(x), mail_list))

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
        failmessage = "Failed Requests:\n" 
        for failure in failure_info:
            failmessage += failure + "\n"
        print(failmessage)
        master_string += failmessage
    summarymessage = "\nSuccesses: " + str(successes) + "\nPending: " + str(waiting) + "\n" + "Failures: " + str(failures) + "\n" + "Success Rate: " + str(100*successes/(len(mail_list))) + "%\n" 
    endtime = time.time()
    timetaken = endtime - starttime
    summarymessage += "Time elapsed: " + str(timetaken) + " for " + str(len(mail_list)) + " entries\n"
    summarymessage += "Mean time taken per e-mail: " + str(timetaken/len(mail_list)) + "\n"
    print(summarymessage)
    master_string += summarymessage    

    ## This portion is still being resolved... only works if activated after a few minutes of waiting
    if waiting > 0:
        follow_up = input("Do you wish to follow up on the " + str(waiting) + " pending cases now?")
        if follow_up.lower() == 'y':
            info_from_mails(pending)


def main(argv):
    return info_from_mails(argv)

if __name__ == "__main__":
    feed = list(sys.argv)
    global save_str
    save_str = ''
    if len(feed) < 2:
        feed = input('If you are looking up a single e-mail address, please type the e-mail address here. Otherwise, just hit enter.')
        if feed == '':
            feed = input('Enter e-mail addresses seperated by commas, or enter a list of e-mail addresses. Else if entering a filename, just hit enter for now.')
            if feed != '':
                info_from_mails(feed)
            else:
                global master_string
                master_string = ""
                mailsfile = input('Enter file name: ')
                mymaillist = extract_mails(mailsfile)
                #for line in mymaillist:
                #    print(line)
                info_from_mails(mymaillist)
                recordlist = master_string.split('\n')
                writetofile.writeFromList(recordlist)               
        else:
            print(info_from_mail(feed))
    else:
        main(sys.argv[1])
