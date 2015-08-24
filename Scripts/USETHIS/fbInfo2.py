import os, sys, re
from bs4 import BeautifulSoup as bs
from lxml import html, etree
from datetime import date
import writetofile2 as w2

# Can be extracted directly from DOM
SIMPLE_FIELD = ('USERNAME', 'span', {'id':'fb-timeline-cover-name'}) 


def tryRead(x):
    try:
        f = open(x)
        data = f.read()
    except UnicodeDecodeError:
        with open(x, encoding = 'ascii', mode = 'r') as f:
            data = f.read()
    f.close()
    return data

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
            
# Takes a list of elements with css of 'div._50f3', which corresponds to the sidebar at top left of FB page with person's biographic info
def scrapeSideBar(sideBar):
  fields = [['Location','Lives in','Unknown'], ['Hometown', 'From', 'Unknown'], ['Friends', 'friends', 'Unknown'], ['Married', 'Married', 'Unknown'], ['Followers', 'Followed by', 'Unknown']]
  education = ['Education', 'Studied', 'Unknown', 'Unknown']
  work = ['Job', 'Company', 'at', '', '']
  sideText = [tryStr(tryText(i)) for i in sideBar]
  for partnum in range(len(sideText)):
    info = sideText[partnum]
    for field in fields:
      if field[1] in info:
        if field[1] == 'Married':
          field[2] = 'Yes'
        else:
          words = info.split()
          queryEnd = field[1].split()[-1]       
          if queryEnd in words:
            if field[1] == 'friends':
              result = words[words.index(queryEnd) - 1]
              if len(result) < 6:
                if ',' in result:
                  result = result[:result.index(',')] + result[result.index(',') + 1 :]
                field[2] = result
            elif field[1] == 'Followed by':
              field[2] = re.findall('\d+', info)[0]
            else:
              field[2] = " ".join(words[words.index(queryEnd) + 1 : ])
    words = info.split()
    if 'Studied' in info:
      if 'at' in words:
        atindex = words.index('at')
        school = " ".join(words[atindex + 1:])
        education[3] = school
      else:
        atindex = len(words)
      education[2] = " ".join(words[words.index('Studied') + 1 : atindex])
    elif 'at' in words:
      job = " ".join(words[:words.index('at')])
      comp = " ".join(words[words.index('at') + 1 :])
      if job != 'Works':
        work[3] =  job
      work[4] = comp    
  return (fields, education, work)

def getDates(person):
  dates = person.findAll('span', {'class':'fsm fwn fcg'})
  datetexts = [i.text for i in dates]
  events = [['Graduation', 'Graduated', 'Unknown'], ['Age', 'Born', 'Unknown'], ['Schooling Years', 'Attended from', 'Unknown'] ]
  for line in datetexts:
    for event in events:
      if event[1] in line:
        if event[0] == 'Graduation':
          event[2] = re.findall(r'\d+', line)[0]
        elif event[0] == 'Age':
          nums = re.findall(r'\d+', line)
          if len(nums) > 1:
            event[2] = nums[-1]
        else:
          (start, end) =  tuple(re.findall(r'\d+', line)[-2:])
          event[2] = start + ' - ' + end
  return events

def getGender(person):
  genderHint = person.find('span', {'class':'addFriendText'})
  genderText = tryStr(tryText(genderHint))
  if genderText == 'Unknown':
    return genderText
  if ' him ' in genderText:
    return 'Male'
  elif ' her ' in genderText or ' she ' in genderText:
    return 'Female'
  else:
    return 'Unknown'

def getInfo(person):
  ## Gather Information

  # Username
  username = tryStr(tryText(person.find(SIMPLE_FIELD[1], SIMPLE_FIELD[2])))    

  # Gender
  gender = getGender(person)
    
  # Sidebar Information
  sideBar = person.findAll('div', {'class':'_50f3'})
  summary = scrapeSideBar(sideBar)
  fields = summary[0]
  edu = summary[1]
  work = summary[2]

  # Dates
  dates = getDates(person)

  # Interests
  interests = {'Music':0, 'Sports':0, 'Movies':0}
  hisInterests = person.findAll('div', {'role':'article'})
  hisIntText = '\n'.join([x.text for x in hisInterests])
  for key in interests:
    if key in hisIntText:
      found = re.findall(r'\d+', hisIntText[hisIntText.index(key) + len(key) + 3 : ])
      if len(found) > 0:
        val = tryStr(found[0])
    else:
      #val = '0'
      val = 0
    interests[key] = val
  reverse_interests = {}
  for key, val in interests.items():
    reverse_interests[val] = key
  if max(interests.values()) == 0:
    main_interest = 'Unknown'
  else:
    main_interest = reverse_interests[max(reverse_interests)]

  # Date of Last Post
  postDates = person.findAll('abbr', {'class':'_5ptz'})
  numDays = 'Unknown'
  if len(postDates) > 0 :
    MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    lastPostDate = postDates[0]
    postDateText = tryStr(tryText(lastPostDate))
    dateWords = postDateText.split()

    print dateWords

    
    if 'hrs' in dateWords:
      numDays = 0
    elif len(dateWords) == 1:
      print 'Only 1 word: ' + str(dateWords) + ' assuming 15 for the day'
      month = dateWords[0]
      if month in MONTHS:
        monthNum = MONTHS.index(month) + 1
        dayNum = 15
        numDays = (date.today() - date(date.today().year, monthNum, dayNum)).days
        print 'Number of days from ' + postDateText + ' to today: ' + str(numDays)

    elif len(dateWords) == 2:
      month = dateWords[0]
      if month in MONTHS:
        monthNum = MONTHS.index(month) + 1
        dayNum = int(dateWords[1])
        try:
          numDays = (date.today() - date(date.today().year, monthNum, dayNum)).days
        except ValueError:
          print 'Something wrong with the day and month combination: ' + MONTHS[monthNum - 1] + ', ' + str(dayNum) + '. Substituting 15 for day.'
          numDays = (date.today() - date(dayNum, monthNum, 15)).days
    elif len(dateWords) == 3:
      month = dateWords[0]
      if month in MONTHS:
        monthNum = MONTHS.index(month) + 1
        dayNum = int(dateWords[1][:-1])
        yearNum = int(dateWords[2])
        numDays = (date.today() - date(yearNum, monthNum, dayNum)).days
    elif 'at' in dateWords:
      print '"at" Detected! dateWords is ' + str(dateWords)
      monthNum = MONTHS.index(dateWords[0]) + 1
      dayNum = int(dateWords[1])
      numDays = (date.today() - date(date.today().year, monthNum, dayNum)).days
      print str(numDays) + ' from ' + postDateText + ' to today'
            
      

  else :
    postDateText = 'Unknown'
    numDays = 'Unknown'
    

  ## Format Information
  data = 'Email : ' + person.get('id') + '\n'
  custom = '<p id = "Email">' + person.get('id') + '</p>'
  data += SIMPLE_FIELD[0] + ' : ' + username + '\n'
  custom += '<p id = "' + SIMPLE_FIELD[0] + '">' + username + '</p>'
  data += 'Gender : ' + gender + '\n'
  custom += '<p id = "Gender">' + gender + '</p>'
  for field in fields:
    data += field[0] + ' : ' + field[2] + '\n'
    custom += '<p id = "' + field[0].replace(' ', '') + '">' + field[2] + '</p>'
  data += edu[0] + ' : ' + edu[2] + '\n' + 'Schools : ' + edu[3] + '\n'
  custom += '<p id = "' + edu[0] + '">' + edu[2] + '</p>' + '<p id = "Schools">' + edu[3] + '</p>'
  data += work[0] + ' : ' + work[3] + '\n' + work[1] + ' : ' + work[4] + '\n'
  custom += '<p id = "' + work[0] + '">' + work[3] + '</p>' + '<p id = "' + work[1] + '">' + work[4] + '</p>'
  for event in dates:
    data += event[0] + ' : ' + event[2] + '\n'
    custom += '<p id = "' + event[0].replace(' ', '') + '">' + event[2] + '</p>'
  # Interests
  for key in interests:
    data += key + ' : ' + str(interests[key]) + '\n'
    custom += '<p id = "' + key + '">' + str(interests[key]) + '</p>'  
  # Main Interest
  data += 'Main Interest : ' + main_interest + '\n'
  custom += '<p id = "MainInterest">' + main_interest + '</p>'
  # Date of Last Post & No.of Days from Last Post
  data += 'Last Post Date : ' + postDateText + '\n'
  custom += '<p id = "LastPostDate">' + postDateText + '</p>'
  data += 'Days Since Last Post as of ' + str(date.today()) + ' : ' + str(numDays) + '\n'
  custom += '<p id = "DaysSinceLastPost">' + str(numDays) + '</p>' 
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
    newdoc.write('<div class = "INFO">')
    result = getInfo(person)
    personInfo = result[0]
    personDiv = result[1]
    #output.write(personInfo)
    w2.writeSafe(personInfo, output)
    w2.writeSafe(personDiv, newdoc)

    #newdoc.write(personDiv)
    output.write('END OF PERSON\n\n')
    newdoc.write('</div>')
  output.write('END OF FILE\n\n')
  newdoc.write('</html>')
  output.close()


if __name__ == "__main__":
  feed = list(sys.argv)
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
    #doc = open(infile)
    #docstr = doc.read()
    #doc.close()
    docstr = tryRead(infile)
    getAll(docstr, outfile, newpage)
