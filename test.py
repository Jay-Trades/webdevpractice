#Jay Chen
#14733030
#Worked alone with the help of google and some comments on slack

def read_file(file):    #empty space killer
    '''reads files and removes empty spaces and return lines as a list in c'''
    text = []
    for line in open(file):
        text.append(line.strip())       #reads the line and strips white space and new line on both sides and appends to text[]
    c= []
    for line in text:
        if line != '':              #reads the line and appends to c[] if it is not empty ''
            c.append(line)          
    return c
    
def get_name(file):
    ''' gets the first file of the resume and looks to see if the name is capitalized, if so return name'''

    with open(file) as f:           #opens file as f and closes automatically
        name = f.readline().strip()     #reads the first line and strips white space and new line on both sides
        if name == '':
            return 'No Name'
        if name[0].isupper():           # checks if the first letter is upper
            return name
        else:
            raise RuntimeError('First letter of the name has to be capitalize')     #prints the following runtimeerror


def get_email(file):
    '''opens a file and strips/appends it to a list line by line. Then looks for the '@' symbol to find the email. If it ends in .edu or .com and has no numbers then returns'''
    with open(file) as f:    
        text = []
        for line in f:
            text.append(line.strip())       #reads the line and strips white space and new line on both sides and appends to text[]
        email = None
        for line in text:   
            if '@' in line and line[-4:] == '.edu' or line[-4:] == '.com':      #if @ is in the line and it ends in .edu or .com we set email = that line.
                email = line
        if email is None:
            return ''       #if email is none we return a empty string
        idx = email.index('@')
        if email[idx+1].isupper():
            return ''
        for character in email:
            if character.isdigit():     #iterates through the string and checks if each character is a digit. If it is print a statement
                print('this is an invalid email')
                return ''
        return email

def detect_courses(file):
    '''opens a file and strip/appends it line by line to a list. Then appends to another list if the line is not empty. 
    After we check if 'Courses' is in line and then looks for the next 
    letter after 'Courses'. Then returns courses starting from that first letter'''

    c = read_file(file)
    for line in c:
        if 'Courses' in line:       #looks if Courses is in the line in list C
            courses = line[7:]      #if it is set var courses beginning from index 7 because we don't want to iterate through 'Courses'
            for letter in courses:  #iterate through new var courses to see where the actually courses names start by finding first letter
                if letter.isalpha():
                    idx = courses.find(letter)  #index that first beginning spot and break
                    break
    courses = courses[idx:]     #returns courses from that spot indexed 
    return(courses)

  
    
def detect_project(file):
    '''reads file through read_file function and searches for 'Projects' and indexs that line. After searches for 10 dashes. 
    If found then index that line. Project will be the slice of those 2 indexs'''

    c = read_file(file)
    projects = []
    projectIdx = None
    for line in c:              #iterates lines in c to look for 'Project' string. Index that line when found
        if 'Projects' in line:
            projectIdx = c.index(line)
        if '-------------' in line:         #iterates lines in c to look for 10 dahses string. Index that line when found
            dashIdx = c.index(line)
    if projectIdx == None:
        return 'no projects'
    projects = c[projectIdx+1:dashIdx]      #projects are inbetween these two indexs so slice the list c and return
    return(projects)
        
def surround_block(tag, text):
    '''surround text block with user defined tags'''
    return('<' + tag + '>' + text + '</' + tag + '>')     #concatenates 3 strings


def html(template, taggedfile, htmlresume):
    '''opens given files. Reads file1 the HTML template. Appends that to a list removes last 2 lines. Appends file2 to the end of the list then adds back the removed 2 lines. 
    after it joins the list back into a string and writes it to file3'''

    text = []
    for line in open(template):     #opens file and appends line
        text.append(line)
    end = text[-2:]                 #stores end 2 lines 
    text = text[0:-2]               #stores rest of the lines in template

    for l in open(taggedfile):      #opens taggedfile(resume with html added) and appends lines to var text.
        text.append(l)

    for n in end:                   #appends last two lines to var text
        text.append(n)
    
    resume = open(htmlresume, 'w')  #opens htmlresume in write mode
    textwrite = ' '.join(text)      #joins the elements of list text with a space to form a long string
    resume.write(textwrite)         #writes it to htmlresume
        

def create_email_link(email_address):
    '''with an email address parameter. Looks for the '@' symbol and splits email address at '@'. then inserts [aT] in between the 2 elements and joins elemntes backtogether'''
    list = []
    if '@' in email_address:
        list = email_address.split('@')     #searches for @ and splits it on @
        list.insert(1, '[aT]')              #insert [aT] in between the 2 split elements
        list.append('</a>')
        email = ''.join(list)               #joins the elements back together
    else:
        email = email_address + '</a>'
    print('<a href=\"mailto:'+ email_address +'\">'+ email) 
    return '<a href=\"mailto:'+ email_address +'\">'+ email     #returns the tag with original email address and changed email address to prevent spam
   
def wrap_basic_info_write(resumeTxt, writefile):
    '''wraps name, email in proper html tags with surround_block function and concatenating strings adds newline for format'''
    email = get_email(resumeTxt)            #gets email with function
    taggedEmail = 'Email:'+ create_email_link(email)        #adds Email: tag in front of html email link
    name = get_name(resumeTxt)              #gets name with function
    htmlName = surround_block('h1', name)   #adds tags to name
    htmlEmail = surround_block('p', taggedEmail)    #adds tags to email
    htmlNameEmail = htmlName + '\n' + htmlEmail + '\n'  #concatenate email and name with newlines in between
    taggedNameEmail = surround_block('div', htmlNameEmail)  #adds tags to concatenated string
    taggedNameEmail = '<div id=\"page-wrap\">\n' + taggedNameEmail  #concatenate more tags to string
    f = open(writefile, 'w')    #opens file for write 
    f.write(taggedNameEmail)    
    f.close()           

def wrap_project_write(resumeTxt, writefile):
    '''wraps projects in proper html tags. Uses detect_project to find project as a list'''
    data = detect_project(resumeTxt)    #finds the projects and returns as list
    surroundedProjects = []
    title = '<h2> Project </h2> \n' #title as string
    
    for line in data:   
        surroundedProjects.append(surround_block('li', line) + '\n')    #appends each string after it gets wrapped in tags and concatenated with newline
    taggedProjects = ' '.join(surroundedProjects)                       #join the project list with a space
    surroundedProjects = surround_block('ul', taggedProjects)           #wraps the project string in ul tags
    surroundedProjects = title + surroundedProjects                     #concatenates titel with project
    surroundedProjects = surround_block('div', surroundedProjects)      #wraps it again div tags
    f = open(writefile, 'a')    #opens file in append mode
    f.write(surroundedProjects) #writes the final string with tags to file
    f.close

def wrap_courses_write(resumeTxt, writefile):
    '''uses detect_courses function to return courses and addes it to courses title and wraps it in tags using surround_block then writes it to file'''

    data = detect_courses(resumeTxt)        #gets courses and stores it in var data
    title = '\n<h3>Courses</h3>\n'          #the title with tags
    courses = title + surround_block('span', data)  #adds span tag to courses a
    courses = surround_block('div', courses)        #surrounds courses in another div tag
    f = open(writefile, 'a')                #opens file in append and writes to it
    f.write(courses)
    f.close()


def main():
    wrap_basic_info_write('resumetest.txt','htmltest.py')
    wrap_project_write('resumetest.txt', 'htmltest.py')
    wrap_courses_write('resumetest.txt', 'htmltest.py')
    html('resume_template.html', 'htmltest.py', 'test.html')


if __name__ == '__main__':
    main()