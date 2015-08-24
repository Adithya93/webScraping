'''
Module that accepts name of file with emails as input, returning 4 outputs:
1) Logfile, 2) PEOPLE Summary, 3) COMPANIES Summary and 4) COMPANIES Custom HTML Doc
'''
import requests
import clearbit
import time
import sys
import writetofile2 as w2
import ssl

cb_key = '45f4a98a763d6880893006eeaa4df5a8'
clearbit.key = cb_key
pending = []
omitted = []

# Globals for recovering information in the event of unhandled exceptions/server crashes
master_string = ''
save_str = ''

def extract_mails(inlist):
    '''
Takes in string represnting name of emails file, returns a Python list of emails
    '''
    out_list = []
    in_file = open(inlist)
    in_lines = in_file.readlines()
    in_file.close()
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
    '''
Makes request to Clearbit PersonCompany Combined API for a single email, returning response string with custom formatting and
adding response to global variable for backup recovery purpose
    '''
    global save_str
    output_str = ""
    inp = em
    if inp[0] == "'":
        inp = inp[1:-1]
    if clearbit.key == None:
        clearbit.key = cb_key
    try:
        result = clearbit.person_company.PersonCompany.find(email = inp)
        #result = clearbit.Person.find(email=inp)
    except requests.exceptions.HTTPError:
        errormsg = "Either the limit has been reached for Clearbit API's free trial, or the e-mail address was totally invalid :/\nSee for yourself. The e-mail passed in was: " + inp + '\n'
        w2.tryPrint(errormsg)
        save_str += errormsg
        omitted.append(inp)
        return("Query was not processed.")
    except (ssl.SSLEOFError, requests.packages.urllib3.exceptions.SSLError, requests.exceptions.SSLError):
        errormsg = 'SSLEOFError encountered for ' + inp + '\n' 
        w2.tryPrint(errormsg)
        save_str += errormsg
        omitted.append(inp)
        return("Query was not processed.")
    except:
        errormsg = 'Unknown error with ' + inp + '\n'
        w2.tryPrint(errormsg)
        save_str += errormsg
        omitted.append(inp)
        return('Query was not processed.')
    if result != None:
        if 'pending' in result.keys() and em not in pending:
            pending.append(inp)
            pendmessage = "Waiting on " + inp + "\n"
            save_str += pendmessage
            return pendmessage        
        if em in pending:
            pending.remove(em)
        if 'person' in result:
            output_str += 'PERSON' + '\n'
            person = result['person']
            if person != None:
                for key in person:
                    if key == 'id':
                        continue
                    val = person[key]
                    if val != None:
                        if type(val) == dict:
                            if None not in val.values():
                                output_str += str(key) + " : " + str(val) + "\n"
                        else:
                            output_str += str(key) + " : " + str(val) + "\n"

        if 'company' in result:
            output_str += 'COMPANY' + '\n'
            company = result['company']
            if company != None:
                for key in company:
                    if key == 'id':
                        continue
                    val = company[key]
                    #if val != None:
                        #if type(val) == dict:
                            #if None not in val.values():
                            #    output_str += str(key) + ' : ' + str(val) + '\n'
                            #output_str += str(key) + ' : ' + str(val) + '\n'
                        #else:
                        #    output_str += str(key) + ' : ' + str(val) + '\n'
                        #output_str += str(key) + ' : ' + str(val) + '\n'
                    output_str += str(key) + ' : ' + str(val) + '\n'

        save_str += output_str + '\n'
        return output_str
    else:
        if em in pending:
            pending.remove(em)
        notice = "Request failed for " + em + "\n"
        save_str += notice
        return notice

def info_from_mails(em):
    '''
Plural version of info_from_mail function which accepts list of emails and compiles responses for all emails. Also saves responses and custom messages
to global variables for backup recovery and meta data analysis purposes.
    '''
    global master_string
    starttime = time.time()
    successes = 0
    waiting = 0
    failures = 0
    left_out = 0
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
    excluded_mails = []

    #output = list(map(lambda x : info_from_mail(x), mail_list))
    output = []
    for mail in mail_list:
        #try:
        #    output.append(info_from_mail(mail))
        output.append(info_from_mail(mail))
        #except:
        #    print('Unknown error processing ' + mail)
        #    left_out += 1
        #    excluded_mails.append(mail)

    for index in range(len(output)):
        if output[index][:5] == "Query":
            left_out += 1
        if output[index][:3] == "Req":
            failures += 1
            failure_info.append(mail_list[index] + ":\n" + output[index])

        elif output[index][:4] == "Wait":
            waiting += 1

        else:            
            goodmessage = "Info for " + mail_list[index] + " :\n" + output[index] + "\n" 
            master_string += goodmessage
            successes += 1

    if waiting > 0:
        pendingmessage = "Please follow up ASAP on these pending requests:\n"
        for mail in pending:
            pendingmessage += mail + "\n"
        pendingmessage += "\n"
        w2.tryPrint(pendingmessage)
        master_string += pendingmessage

    if failures > 0:
        failmessage = "Failed Requests:\n" 
        for failure in failure_info:
            failmessage += failure + "\n"
        w2.tryPrint(failmessage)
        master_string += failmessage

    if left_out > 0:
        wastemessage = "Unprocessed emails:\n"
        for waste in excluded_mails:
            wastemessage += waste + '\n'
        wastemessage += '\n'
        w2.tryPrint(wastemessage)
        master_string += wastemessage
    
    summarymessage = "\nSuccesses: " + str(successes) + "\nPending: " + str(waiting) + "\n" + "Failures: " + str(failures) + "\n" + "Success Rate: " + str(100*successes/(len(mail_list))) + "%\n" 
    endtime = time.time()
    timetaken = endtime - starttime
    summarymessage += "Time elapsed: " + str(timetaken) + " for " + str(len(mail_list)) + " entries\n"
    summarymessage += "Mean time taken per e-mail: " + str(timetaken/len(mail_list)) + "\n"
    summarymessage += "Queries omitted: " + str(left_out) + "\n"
    w2.tryPrint(summarymessage)
    master_string += summarymessage    

    if waiting > 0:
        follow_up = input("Do you wish to follow up on the " + str(waiting) + " pending cases now?")
        if follow_up.lower() == 'y':
            info_from_mails(pending)

def run(infile):
    mymaillist = extract_mails(infile)
    info_from_mails(mymaillist)
    recordlist = master_string.split('\n')
    result = w2.writeFromList(recordlist)
    peopleList = result[0]
    compList = result[1]
    w2.makeCompPage(compList)
    return peopleList


if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) < 2:
        infile = input('Enter file name: ')
    elif len(feed) == 2:
        infile = sys.argv[1]
    else:
        raise ValueError('Wrong number of arguments. Enter filename only.')
    run(infile)
