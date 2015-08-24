import os, sys, lxml, collections
from bs4 import BeautifulSoup as bs
from lxml import html
from collections import OrderedDict

TARGET = ['div', {'class' : 'INFO'}]

USELESS_LINKS = set(["http://gmail.com", "https://rapportive.com/", "https://help.linkedin.com/app/answers/detail/a_id/15004",
                 "https://www.linkedin.com/legal/privacy-policy", "#", "http://maps.google.com/maps?q=Singapore"])

UNIQUE = set([])
# Helper to handle missing data
def tryInfo(source):
    try:
        val = source.text
    except AttributeError:
        val = "Unknown"
    return val

# Helper to handle non-unicode characters
def tryStr(source):
    val = tryInfo(source)
    result = ""
    if val == "Unknown":
        return val
    try:
        result = str(val)
    except UnicodeEncodeError:
        for letter in val:
            try:
                result += str(letter)
            except UnicodeEncodeError:
                print "Unicode encountered!"
                continue
    return result
    

# Uses above two helpers to return formatted information for one person
def getInfo(person):
    #fields = {'Name':'', 'Location':'', 'Email':'', 'Headline':'', 'Jobs':'', 'Companies':'', 'LinkedIn Profile':'', 'Other links':''}
    fields = OrderedDict([('Name', ''), ('Location', ''), ('Email', ''), ('Headline', ''), ('Jobs', ''), ('Companies', ''), ('LinkedIn Profile', ''), ('Other links', '')])
    
    # Get all the information
    nameInfo = person.find('h1', {'class':'name'})
    name = tryStr(nameInfo)
    fields['Name'] = name
    
    locInfo = person.find('a', {'class':'location'})
    loc = tryStr(locInfo)
    fields['Location'] = loc

    mailInfo = person.find('span', {'class':'email'})
    mail = tryStr(mailInfo)
    fields['Email'] = mail

    headInfo = person.find('li',{'class':'headline'})
    head = tryStr(headInfo)
    fields['Headline'] = head

    jobInfo = person.findAll('span', {'class':'job-title'})
    #jobsList = map(lambda x : tryInfo(x), jobInfo)
    #jobs = tryStr("; ".join(jobsList))
    jobsList = map(lambda x : tryStr(x), jobInfo)
    jobs = "; ".join(jobsList)
    fields['Jobs'] = jobs

    companies = set(person.findAll('span',{'class':'company'})) | set(person.findAll('a', 'company'))
    compList = map(lambda x : tryStr(x), list(companies))
    comps = "; ".join(compList)
    fields['Companies'] = comps

    links = person.findAll('a')
    linkList = map(lambda x : str(x.get('href')), links)
    liprof = ""
    otherlinkList = []
    lidone = False
    for link in linkList:
        if "profile/view" in link and not lidone:
            liprof = link
            lidone = True
        else:
            if link not in USELESS_LINKS:
                otherlinkList.append(link)
    otherlinkstr = "; ".join(otherlinkList)
    fields['LinkedIn Profile'] = liprof
    fields['Other links'] = otherlinkstr

    # Save LinkedIn Profiles to file
    global lidoc
    lidoc.write(mail + " : " + liprof + "\n")    
   
    # Format the information
    data = ""
    custom = ""
    for key in fields:
        data += key + " : " + fields[key] + "\n"
        custom += '<p id = "' + key.replace(' ', '') + '">' + fields[key] + '</p>'
#        if fields[key] != "Unknown" and fields[key] != "":
#            data += key + " : " + fields[key] + "\n"
#    data = "Name: " + name + "\n" + "Email: " + mail + "\n" + "Location: " + loc + "\n" + "Headline: " + head + "\n" + "Jobs: " + jobs + "\n"
#    data += "Companies: " + comps + "\n" + "LinkedIn Profile: " + liprof + "\n" + "Other links: " + otherlinkstr
#    data += "\n"
    return (data, custom)

# Uses above method to collect formatted information for all people and writes it to a file
def getAllInfo(docstr, out, new):
    soup = bs(docstr)
    people = soup.findAll(TARGET[0], TARGET[1])
    print str(len(people)) + ' detected.'
    report = open(out, 'w')
    newdoc = open(new, 'w')
    report.write('START OF REPORT\n')
    newdoc.write('<html>')
    for person in people:
        if person not in UNIQUE:
            UNIQUE.add(person)
            info = getInfo(person)
            report.write('START OF PERSON\n')
            newdoc.write('<div class = "INFO">')
            report.write(info[0])
            newdoc.write(info[1])
            report.write('END OF PERSON\n\n')
            newdoc.write('</div>')
    report.write('END OF FILE\n')
    newdoc.write('</html>')
    report.close()
    newdoc.close()
    
    
if __name__ == '__main__':
    os.chdir("C:\\Users\\Adithya\\Desktop\\Summer '15\\NEWCLEUS")
    inlist = list(sys.argv)
    if len(inlist) == 3:
        rappfile = open(inlist[1])
        outfile = inlist[2]
    else:
        
        if len(inlist) == 1 :
            filename = input('Enter input filename: ')
        elif len(inlist) == 2 :
            filename = inlist[1]
        rappfile = open(filename)
        outfile = input('Enter output filename: ')
        print('Extracting information from ' + filename + " and writing to " + outfile)

    global lidoc
    liprofiles = input('Enter name of file to hold all linkedin profile urls: ')
    newpage = input('Enter name of custom HTML file: ')
    rappstr = rappfile.read()
    rappfile.close()
    lidoc = open(liprofiles, 'w')
    getAllInfo(rappstr, outfile, newpage)
    lidoc.close()
