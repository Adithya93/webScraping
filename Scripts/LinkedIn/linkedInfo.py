import os, sys
from bs4 import BeautifulSoup as bs
from lxml import html, etree

# Can be extracted directly from DOM
SIMPLE_FIELDS = [('FULL NAME', 'span', {'class':'full-name'}),('TITLE', 'p', {'class':'title'}), ('LOCATION', 'span', {'class':'locality'}), ('INDUSTRY', 'dd', {'class':'industry'}),
          ('CURRENT COMPANY', 'a', {'name' : 'company'})]
# Require Further Processing 
COMPLEX_FIELDS = ['CONNECTIONS', 'PAST COMPANIES', 'JOB TITLES', 'JOB DATES', 'EXPERIENCE', 'EDUCATION LEVEL', 'EDUCATIONAL INSTITUTION', 'SKILLS', 'GROUPS', 'GROUP NAMES', 'GROUP SIZES']

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
    ### Gather Information

    ## Simple Information
    simple_info = []
    for field in SIMPLE_FIELDS:
        simple_info.append(tryStr(tryText(person.find(field[1], field[2]))))    

    ## Complex Information    
    complex_info = []    
    # Connections
    constr = tryStr(tryText(person.find('div', {'class':'member-connections'})))
    conval = constr
    if conval != "Unknown":
        conval = conval[:conval.index('con')]
        if '+' in conval:
            conval = conval[:-1]
    complex_info.append(conval)
    
    # Past companies
    prevComps = person.find('tr', {'id':'overview-summary-past'})
    if prevComps != None:
        prevs = prevComps.find('ol')
        prevTexts = tryStr(tryText(prevs))        
    else:
        prevTexts = "Unknown"
    complex_info.append(prevTexts)


    # All Jobs
    jobTitles = person.findAll('a', {'name':'title'})
    jobTexts = [title.text for title in jobTitles]
    jobStr = '; '.join([tryStr(text) for text in jobTexts])
    if jobStr == '':
        jobStr = 'Unknown'
    complex_info.append(jobStr)

    # Job Dates
    jobDates = person.findAll('span', {'class':'experience-date-locale'})
    dateTexts = [date.text for date in jobDates]
    #dateStr = ', '.join([tryStr(text) for text in dateTexts])
    dateWords = [text.split() for text in dateTexts]
    dateStr = ''
    for text in dateWords:
        for word in text:
            dateStr += tryStr(word) + ' '
        dateStr += '; '
    if dateStr == '':
        dateStr = 'Unknown'
    complex_info.append(dateStr)

    # Experience
    exTexts = person.findAll('p', {'class':'description summary-field-show-more'})
    exWords = map(lambda x : tryStr(tryText(x)), exTexts)
    exStr = " ".join(exWords)
    ex = exStr.replace('\n', ' ')
    complex_info.append(ex)

    # Education Level & Educational Institutions
    edu = person.findAll('div', {'class':'education'})
    if edu != []:
        eduHeads = map(lambda x : x.find('header'), edu)
        eduIns = map(lambda x : x.find('h4'), eduHeads)
        eduLevels = map(lambda x : x.find('h5'), eduHeads)
        eduInsStr = "; ".join(map(lambda x : tryStr(tryText(x)), eduIns))
        eduLevelsStr = "; ".join(map(lambda x : tryStr(tryText(x)), eduLevels))
    else:
        eduLevelsStr = "Unknown"
        eduInsStr = "Unknown"
    complex_info.append(eduLevelsStr)
    complex_info.append(eduInsStr)

    # Skills
    skills = person.findAll('a', {'class':'endorse-item-name-text'})
    skillsList = map(lambda x : tryStr(tryText(x)), skills)
    skillsStr = ", ".join(skillsList)
    complex_info.append(skillsStr)

    # Groups, Group Names & Group Sizes
    groups = person.find('div', {'id':'groups'})
    if groups != None:
        numGroups = groups.get('data-total-num-groups')
        complex_info.append(numGroups)
        groupNames = groups.findAll('strong')
        groupNameTexts = [tryStr(tryText(name)) for name in groupNames]
        groupNameStr = "; ".join(groupNameTexts)
        complex_info.append(groupNameStr)
        groupSizes = groups.findAll('p', {'class':'groups-stats'})
        groupSizesStr = [tryStr(tryText(x)) for x  in groupSizes]
        groupSizeNums = [x.split()[0] for x in groupSizesStr]
        realNums = ''
        for size in groupSizeNums:
            if ',' in size:
                realNums += size[:size.index(',')] + size[size.index(',') + 1: ] + '; '
        complex_info.append(realNums)
    else:
        complex_info += ['Unknown','Unknown','Unknown']

    # Following Companies -- Not Available from DOM?

    ## Format Information
    email = person.get('id')
    data = "Email : " + email + "\n"
    custom = '<p id = "' + 'EMAIL' + '">' + email + '</p>' 
    for fieldnum in range(len(SIMPLE_FIELDS)):
        data += SIMPLE_FIELDS[fieldnum][0] + " : " + simple_info[fieldnum] + "\n"
        custom += '<p id = "' + SIMPLE_FIELDS[fieldnum][0].replace(' ', '') + '">' + simple_info[fieldnum] + '</p>'
    for num in range(len(COMPLEX_FIELDS)):
        data += COMPLEX_FIELDS[num] + " : " + complex_info[num] + "\n"
        custom += '<p id = "' + COMPLEX_FIELDS[num].replace(' ', '') + '">' + complex_info[num] + '</p>'

    return (data, custom)


def getAll(doc, out, new):
    soup = bs(doc)
    people = soup.findAll('div', {'class':'INFO'})
    print str(len(people)) + " people detected"
    output = open(out, 'w')
    newdoc = open(new, 'w')
    output.write("Information for " + str(len(people)) + " people:\n\n")
    newdoc.write('<html>')
    for person in people:
        output.write('START OF PERSON:\n')
        newdoc.write('<div class = "INFO">')# id = "' + person.get('id') + '">')
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
