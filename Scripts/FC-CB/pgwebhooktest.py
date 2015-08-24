import requests
import time
import sys
import writetofile

pg_key = 'LmLyAF2lBD6XtbCNzcNJEixPYmaTZwef'
pg_base = 'https://api.peoplegraph.io/v2/lookup?email='
pg_middle = '&webhookUrl='
pg_webhook = 'http://stripe.ra102.ultrahook.com'
pg_end = '&apiKey='
failed = []
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
    global failed
    output_str = ""
    requrl = pg_base + em + pg_middle + pg_webhook + pg_end + pg_key
    try:
        result = requests.get(requrl)
        if(result.status_code == 200):
            resultjson = result.json()
            for key in resultjson.keys():
                output_str += str(key) + " : " + str(resultjson[key]) + "\n"
                save_str += str(key) + " : " + str(resultjson[key]) + "\n"
                return output_str
        elif(result.status_code == 202):
            message = "Pending...Results will be posted to webhook " + pg_webhook + " when available\n"
            output_str += message
            save_str += message
            pending.append(em)
            return output_str
        else:
            notice = "Request failed with the following message:\n" + str(result.content) + "\n"
            failed.append(em)
            save_str += notice
            return notice
    except requests.exceptions.HTTPError:
        errormsg = "Either the limit has been reached for PeopleGraph API's free trial, or the e-mail address was totally invalid :/\nSee for yourself. The e-mail passed in was: " + em
        print(errormsg)
        save_str += errormsg
        return("Query was not processed.")       

def info_from_mails(em):
    global master_string
    starttime = time.time()
    successes = 0
    failures = 0
    waiting = 0
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
        if output[index][:3] == "Req":
            #print("Request failed for " + mail_list[index] + "\nRefer below for details.\n" ) 
            failures += 1
            failure_info.append(mail_list[index] + ":\n" + output[index])
        elif output[index][:4] == "Pend":
            waiting += 1
            message = "Waiting on " + mail_list[index] + "\n"
            print(message)
            master_string += message
        else:
            successes += 1
            message = "Info for " + mail_list[index] + " :\n" + output[index] 
            print(message)
            master_string += (message)
    if failures > 0:
        failmessage = "The following requests failed\n"         
        for failure in failure_info:
            failmessage += failure + '\n'
            #print(failure)
        print(failmessage)
        master_string += failmessage
        
    summarymessage = "\nPeopleGraph Successes: " + str(successes) + "\n"+ "PeopleGraph Failures: " + str(failures) + "\n" + "PeopleGraph Success Rate: " + str(100*successes/(len(mail_list))) + "%" 
    print(summarymessage)
    master_string += summarymessage
    endtime = time.time()
    timetaken = endtime - starttime
    finalmessage = "Time elapsed: " + str(timetaken) + " for " + str(len(mail_list)) + " entries\n" + "Mean time taken by PeopleGraph per e-mail: " + str(timetaken/len(mail_list)) + "\n"  
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
                writetofile.writeFromList(recordlist)                
        else:
            print(info_from_mail(feed))
    else:
        main(sys.argv[1])
