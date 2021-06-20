#!/usr/bin/python3
from bs4 import BeautifulSoup as soap
from urllib.request import urlopen as uReq
import copy

courses = list()
message = ""

class Seats:
    def __init__(self):
        self.totalSeatsRemaining = '-1'
        self.currentlyRegistered = '-1'
        self.generalSeatsRemaining = '-1'
        self.restrictedSeatsRemaining = '-1'

class Course:
    def __init__(self, year, session, department, course, section):
        self.year = year
        self.session = session
        self.department = department
        self.course = course
        self.section = section
        self.currentSeats = Seats()
        self.previousSeats = Seats()

    def updateSeats(self):
        link  = 'https://courses.students.ubc.ca/cs/courseschedule?sesscd=' + self.session
        link += '&pname=subjarea&tname=subj-section&sessyr=' + self.year + '&course=' + self.course
        link += '&section=' + self.section + '&dept=' + self.department
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

            self.previousSeats = copy.deepcopy(self.currentSeats)
            self.currentSeats.totalSeatsRemaining      = total.strong.get_text()
            self.currentSeats.currentlyRegistered      = registered.strong.get_text()
            self.currentSeats.generalSeatsRemaining    = general.strong.get_text()
            self.currentSeats.restrictedSeatsRemaining = restricted.strong.get_text()
            global message
            message += self.year + ' ' + self.session + ' ' + self.department + ' ' + self.course + ' ' + self.section + '\n'
            #message += '\t' + total.td.get_text()      + ' ' + self.currentSeats.totalSeatsRemaining + '\n'
            #message += '\t' + registered.td.get_text() + ' ' + self.currentSeats.currentlyRegistered + '\n'
            message += '\t' + general.td.get_text()    + ' ' + self.currentSeats.generalSeatsRemaining + '\n'
            #message += '\t' + restricted.td.get_text() + ' ' + self.currentSeats.restrictedSeatsRemaining + '\n'
            message += '\n'
        except KeyboardInterrupt:
            exit(0)
        except:
            print('Something went wrong in bs4...')

def loadCourses():
    # <YEAR> <W/S> <DEPARTMENT> <COURSE> <SECTION>
    #   0      1        2          3         4
    global courses
    courses_file = open('courses.txt', 'r')
    courses = courses_file.readlines()
    courses = list(map(str.strip, courses))
    courses = list(map(str.split, courses))
    for i in range(len(courses)):
        courses[i] = Course(courses[i][0], courses[i][1], courses[i][2], courses[i][3], courses[i][4])
    courses_file.close()

def process():
    for course in courses:
        course.updateSeats()
    if 󰀂v.48-message󰀂 != message:
        󰀂v.48-message󰀂 = message 
        󰀂v.49-sms󰀂 = message 
    else:
        󰀂v.49-sms󰀂 = ""

if __name__ == "__main__":
    loadCourses()
    process()
