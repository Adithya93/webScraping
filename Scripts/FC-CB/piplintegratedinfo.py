import requests
import sys

'''
Initialize an empty master list to gather output data
Open a file name based on string from command line/console and save it
readlines from that file --> list with each index corresponding to a person
for each string entry in list:
    take substring of that entry excluding \n character
    split this substring with \t as delimiter to obtain list of fields for that person
    pass this list into makeurl method to obtain a valid string url 
    make request to pipl for this url
    obtain info and format it
    add formatted info to master list
return formatted list
'''

reqbase = 'https://api.pipl.com/search/v4/?'
prefixes = {'First Name' : 'first_name=', 'Last Name' : 'last_name=', 'email' : 'email=', 'city' : 'city='}
prefixlist = ['First Name', 'Last Name', 'email', 'city']
sep = '&'
access = 'key=sample_key'

names = []
def getinputs(somefile):
    myfile = open(somefile)
    mylines = myfile.readlines()
    return mylines

def makeurl(fields):
    base = reqbase
    #myfields = list(fields)
    #del(myfields[2])
    if len(fields) == 4:
        for index in range(len(fields)):
            myindex = index
            if index == 2:
                myindex = 3
            elif index == 3:
                myindex = 2
            if fields[index] != '' and fields[index] != ' ':
                #print("Index no. " + str(index) + ", " + fields[index] + " is not blank")
                base += prefixes[prefixlist[myindex]] + fields[index] + sep
    base += access
    return base


def makereqs(peoplelist):
    req_list = []
    for person in peoplelist:
        if person[-1] == "\n":
            valid = person[:-1]
        else:
            valid = person
        fields = valid.split('\t')
        name = fields[0] + " " + fields[1]
        names.append(name)
        del(fields[2])
        #print(fields)
        requrl = makeurl(fields)
        req_list.append(requrl)
    #print("List coming out of makereqs is\n")
    #for el in req_list:
    #    print(el)
    return req_list

def prepare(filename):
    thelines = getinputs(filename)
    #print(thelines)
    return makereqs(thelines)


def launch(reqlist):

    #input_list = prepare()
    #for guy in reqlist:
    #    print(guy)

    output_list = []
    for reqnum in range(len(reqlist)):
        try:
            myreq = requests.get(reqlist[reqnum])
            myjson = myreq.json()
            if myreq.status_code != 200:
                print('Request failed for ' + names[reqnum] + " with the following error message\n" + myjson['error'])
                continue
            if 'possible_persons' in list(myjson.keys()):             
                mypersons = myjson['possible_persons']
                for pers_index in range(len(mypersons)):
                    current = mypersons[pers_index]
                    pers_info = {}
                    if 'jobs' in current:
                        his_jobs = current['jobs']
                        jobs_disp = []
                        for job in his_jobs:
                            if type(job) == list:
                                for real_job in job:
                                    if type(real_job) == dict:
                                        if 'display' in list(real_job.keys()):
                                            jobs_disp.append(real_job['display'])
                            elif type(job) == dict:
                                if 'display' in list(job.keys()):
                                    jobs_disp.append(job['display'])
                        pers_info['Jobs'] = jobs_disp
                    if 'user_ids' in current:
                        his_ids = current['user_ids']
                        out_ids = []
                        for eachid in his_ids:
                            if type(eachid) == dict:
                                if 'content' in list(eachid.keys()):
                                    out_ids.append(eachid['content'])
                        pers_info['User IDs'] = out_ids
                    #if fields[3] == ' ':
                    cities = []
                    if 'addresses' in current:
                        places = current['addresses']
                        for place in places:
                            if type(place) == dict:
                                if 'city' in list(place.keys()):
                                    cities.append(place['city'])
                        pers_info['cities'] = cities
                output_list.append(pers_info)

            elif 'person' in list(myjson.keys()):
                current = myjson['person']
                pers_info = {}
                if 'jobs' in current:
                    his_jobs = current['jobs']
                    jobs_disp = []
                    for job in his_jobs:
                        if type(job) == list:
                            for real_job in job:
                                if type(real_job) == dict:
                                    if 'display' in list(real_job.keys()):
                                        jobs_disp.append(real_job['display'])
                        elif type(job) == dict:
                            if 'display' in list(job.keys()):
                                jobs_disp.append(job['display'])
                    pers_info['Jobs'] = jobs_disp
                if 'user_ids' in current:
                    his_ids = current['user_ids']
                    out_ids = []
                    for eachid in his_ids:
                        if type(eachid) == dict:
                            if 'content' in list(eachid.keys()):
                                out_ids.append(eachid['content'])
                    pers_info['User IDs'] = out_ids
                #if fields[3] == ' ':
                
                if 'addresses' in current:
                    cities = []
                    places = current['addresses']
                    for place in places:
                        if type(place) == dict:
                            if 'city' in list(place.keys()):
                                cities.append(place['city'])
                    pers_info['cities'] = cities
                output_list.append(pers_info)

            else:
                print('Skipping ' + req + ' as no valid content was returned')
                continue
        except urllib.error.HTTPError:
            output_list.append('API Threw a HTTP 401 Unauthorized Error!')

    return output_list

#def main(argv):
#    getinputs(argv)

if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) < 2:
        in_file = input('Enter file name (absolute path if not in Machine Learning directory): ')
        mylist = prepare(in_file)
        #print("Length of my list is " + str(len(mylist)))
        #print("My list is:\n")
        #for el in mylist:
        #    print(el)
        outlist = launch(mylist)

        #print("Length of output list : " + str(len(outlist)))
        
        for index in range(len(outlist)):
            print("Info for " + names[index] + ":\n" + str(outlist[index]))
