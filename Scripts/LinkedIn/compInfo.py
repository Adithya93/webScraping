import os, sys, re
from bs4 import BeautifulSoup as bs
from lxml import html, etree


def tryText(info):
    try:
        result = info.text
    except AttributeError:
        result = 'Unknown'
    return result

def tryStr(info):
    try:
        result = str(info)
    except UnicodeEncodeError:
        result = ""
        for letter in result:
            try:
                result += str(letter)
            except UnicodeEncodeError:
                print "Unicode Encountered! Marked with asterisk"
                result += "*"
    return result


def getInfo(person):
    # Obtain Info
    email = person.get('id')
    name = tryStr(tryText(person.find('span', {'dir':'ltr'})))
    industry = tryStr(tryText(person.find('p', {'class':'industry'})))
    size = tryStr(tryText(person.find('p', {'class':'company-size'})))
    if size != 'Unknown':
        words = size.split()
        num = words[0]
        if ',' in num:
            num = num.replace(',', '')
        if '+' in num:
            num = num[:-1]
    else:
        num = 'Unknown'
    numFollows = 'Unknown'
    followers = person.find('p', {'class':'followers-count'})
    if followers != None:
        followStr = tryStr(tryText(followers.find('strong')))
        if followStr != 'Unknown':
            folloWords = followStr.split()
            numFollows = folloWords[0]
            if ',' in numFollows:
                numFollows = numFollows.replace(',','')
            if '+' in numFollows:
                numFollows = numFollows[:-1]

    # Format Info
    data = 'Email : ' + email + '\n' + 'Name : ' + name + '\n' + 'Industry: ' + industry + '\n' + 'Size: ' + num + '\n' + 'Followers: ' + numFollows + '\n'
    custom = '<p id = "Email">' + email + '</p>' + '<p id = "Name">' + name + '</p>' + '<p id = "Industry">' + industry + '</p>' + '<p id = "Size">' + num + '</p>' + '<p id = "Followers">' + numFollows + '</p>' 
    return(data,custom)    


def getAll(doc, out, new):
    soup = bs(doc)
    people = soup.findAll('div', {'class':'INFO'})
    print str(len(people)) + " companies detected"
    output = open(out, 'w')
    newdoc = open(new, 'w')
    output.write("Information for " + str(len(people)) + " people:\n\n")
    newdoc.write('<html>')
    for person in people:
        output.write('START OF COMPANY:\n')
        newdoc.write('<div class = "INFO">')
        result = getInfo(person)
        personInfo = result[0]
        personDiv = result[1]
        output.write(personInfo)
        newdoc.write(personDiv)
        output.write('END OF PERSON\n\n')
        newdoc.write('</div>')
    output.write('END OF FILE\n\n')
    newdoc.write('</html>')
    output.close()


if __name__ == "__main__":
    feed = list(sys.argv)
    os.chdir("C:\\Users\Adithya\Desktop\Summer '15\NEWCLEUS")
    if len(feed) == 3:
        infile = feed[1]
        outfile = feed[2]
    else:
        if len(feed) == 2:
            infile = feed[1]
        elif len(feed) == 1:
            infile = input('Enter name of input file: ')
        outfile = input('Enter name of output file: ')
    newpage = input('Enter name of custom HTML document: ')
    doc = open(infile)
    docstr = doc.read()
    doc.close()
    getAll(docstr, outfile, newpage)
