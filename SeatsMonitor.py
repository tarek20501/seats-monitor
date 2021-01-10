from bs4 import BeautifulSoup as soap
from urllib.request import urlopen as uReq
from datetime import datetime
import time
import os
from notify_run import Notify

def move(y, x):
    print("\033[%d;%dH" % (y, x))

def getCourseInfo(year, session, dep, course, section):
    link  = 'https://courses.students.ubc.ca/cs/courseschedule?sesscd=' + session
    link += '&pname=subjarea&tname=subj-section&sessyr=' + year + '&course=' + course
    link += '&section=' + section + '&dept=' + dep
    try:
        uClient = uReq(link, None, 5.0)
        page_html = uClient.read()
        uClient.close()
        page_soap = soap(page_html, 'html.parser')

        SeatSum = list(page_soap.body.children)[5]
        SeatSum = list(SeatSum.children)[34]
        SeatSum = list(SeatSum.children)[27]

        total = list(SeatSum)[3]
        registered = list(SeatSum)[5]
        general = list(SeatSum)[7]
        restricted = list(SeatSum)[9]

        dateTimeObj = datetime.now()
        print(year + ' ' + session + ' ' + dep + ' ' + course + ' ' + section + '                     ')
        print('    ' + total.td.get_text() + ' ' + total.strong.get_text() + '          ')
        print('    ' + registered.td.get_text() + ' ' + registered.strong.get_text() + '           ')
        print('    ' + general.td.get_text() + ' ' + general.strong.get_text() + '        ')
        print('    ' + restricted.td.get_text() + ' ' + restricted.strong.get_text() + '    ')
        print('[' + dateTimeObj.strftime('%T') + ']' + '                                ')
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

courses_file = open('courses.txt', 'r')
courses = courses_file.readlines()
courses_file.close()

notify = ' '
while (notify != 'y' and notify != 'n'):
    notify = input('Do you want notifications? (y or n) ')

if notify == 'y':
    prevInfo = [[0,0,0,0]] * len(courses)
os.system('clear')
while True:
    move(0,0)
    i = 0
    for course in courses:
        course = course.strip()
        course = course.split(' ')
        currInfo = getCourseInfo(course[0], course[1], course[2], course[3], course[4])
        if currInfo[0] == -1:
            i += 1
            continue
        if notify == 'y':
            compare(course, currInfo, prevInfo[i])
            prevInfo[i] = currInfo
        i += 1
        print('                                        ')
        time.sleep(1)
