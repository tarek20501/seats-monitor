from bs4 import BeautifulSoup as soap
from urllib.request import urlopen as uReq
from datetime import datetime
import time
from notify_run import Notify

class Seats:
    def __init__(self):
        self.totalSeatsRemaining = -1
        self.currentlyRegistered = -1
        self.generalSeatsRemaining = -1
        self.restrictedSeatsRemaining = -1

class Course:
    def __init__(self, year, session, department, course, section):
        self.year = year
        self.session = session
        self.department = department
        self.course = course
        self.section = section
        self.currentSeats = Seats()
        self.previousSeats = Seats()

def getCourseInfo(year, session, dep, course, section):
    link  = 'https://courses.students.ubc.ca/cs/courseschedule?sesscd=' + session
    link += '&pname=subjarea&tname=subj-section&sessyr=' + year + '&course=' + course
    link += '&section=' + section + '&dept=' + dep
    try:
        uClient = uReq(link, None, 5.0)
        page_html = uClient.read()
        uClient.close()
        page_soap = soap(page_html, 'html.parser')
        
        SeatSum = page_soap.body.find(class_="'table").find_all('tr')
        total      = SeatSum[0]
        registered = SeatSum[1]
        general    = SeatSum[2]
        restricted = SeatSum[3]

        dateTimeObj = datetime.now()
        print(year + ' ' + session + ' ' + dep + ' ' + course + ' ' + section)
        print('\t' + total.td.get_text() + ' ' + total.strong.get_text())
        print('\t' + registered.td.get_text() + ' ' + registered.strong.get_text())
        print('\t' + general.td.get_text() + ' ' + general.strong.get_text())
        print('\t' + restricted.td.get_text() + ' ' + restricted.strong.get_text())
        print('[' + dateTimeObj.strftime('%T') + ']')
    except:
        print('Something went wrong in bs4...')
        return [-1]
    
    return [total.strong.get_text(), registered.strong.get_text(), general.strong.get_text(), restricted.strong.get_text()]

def compare(course, curr, prev):
        notify = Notify()
        if (curr[2] != prev[2]):
            message = course[2] + ' ' + course[3] + ': \n'
            # message += 'Total Seats Remaining: ' + str(prev[0]) + ' -> ' + str(curr[0]) + '\n'
            # message += 'Currently Registered:' + str(prev[1]) + ' -> ' + str(curr[1]) + '\n'
            message += 'General Seats Remaining: ' + str(prev[2]) + ' -> ' + str(curr[2]) + '\n'
            # message += 'Restricted Seats Remaining*: ' + str(prev[3]) + ' -> ' + str(curr[3]) + '\n'
            notify.send(message)            

courses = list()

def addCourse():
    # TODO
    pass

def removeCourse():
    # TODO
    pass

def saveCourses():
    # TODO
    pass

def loadCourses():
    # <YEAR> <W/S> <DEPARTMENT> <COURSE> <SECTION>
    global courses
    courses_file = open('courses.txt', 'r')
    courses = courses_file.readlines()
    courses = list(map(str.strip, courses))
    # courses = list(map(str.split, courses))
    # for i in range(len(courses)):
        # courses[i] = Course(courses[i][0], courses[i][1], courses[i][2], courses[i][3], courses[i][4])
    courses_file.close()

def process(period, notify):
    if notify == 'y':
        prevInfo = [[0,0,0,0]] * len(courses)

    while True:
        i = 0
        for course in courses:
            print('--------------------------------------')
            course = course.split(' ')
            currInfo = getCourseInfo(course[0], course[1], course[2], course[3], course[4])
            if currInfo[0] == -1:
                i += 1
                continue
            if notify == 'y':
                compare(course, currInfo, prevInfo[i])
                prevInfo[i] = currInfo
            i += 1
        print('--------------------------------------')
        time.sleep(period)

if __name__ == "__main__":
    loadCourses()
    notify = ' '
    while (notify != 'y' and notify != 'n'):
        notify = input('Do you want notifications? (y or n) ')
    process(1, notify)
