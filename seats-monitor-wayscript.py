from bs4 import BeautifulSoup as soap
from urllib.request import urlopen as uReq

courses = list()
message = ""

class Course:
    def __init__(self, year, session, department, course, section):
        self.year = year
        self.session = session
        self.department = department
        self.course = course
        self.section = section

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
            # .td.get_text():text .strong.get_text():number
            global message
            message += self.department + ' ' + self.course + ' ' + self.section + ': ' + general.strong.get_text() + '\n'
        except Exception as e:
            message += str(e) + '\n'

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

def notify():
    if variables["message"] != message:
        variables["message"] = message 
        variables["sms"] = message 
    else:
        variables["sms"] = ""

def process():
    for course in courses:
        course.updateSeats()

if __name__ == "__main__":
    loadCourses()
    process()
    notify()
