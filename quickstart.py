from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students']

# 'https://www.googleapis.com/auth/classroom.courses.readonly'

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API (comment this portion out when creating assignments)
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            print(course['name'])
            print(course.get('id'))


    ########### Assignment Creation ###########

    # use scope https://www.googleapis.com/auth/classroom.coursework.students
    course_id = 301301107341        # insert your own course id here

    coursework = {
        'title': 'Ant colonies',
        'description': '''Read the article about ant colonies
                          and complete the quiz.''',
        'materials': [
            {'link': {'url': 'http://example.com/ant-colonies'}},
            {'link': {'url': 'http://example.com/ant-quiz'}}
        ],
        'workType': 'ASSIGNMENT',
        'state': 'PUBLISHED',
        'dueDate': ""
    }
    coursework = service.courses().courseWork().create(
        courseId=course_id, body=coursework).execute()
    print('Assignment created with ID {%s}' % coursework.get('id'))



    ########### Course Creation ###########

    # use scope https://www.googleapis.com/auth/classroom.courses
    course = {
        'name': 'Chem',
        'section': 'Period 2',
        'descriptionHeading': 'Welcome to 10th Grade Biology',
        'description': """We'll be learning about about the
                     structure of living creatures from a
                     combination of textbooks, guest lectures,
                     and lab work. Expect to be excited!""",
        'room': '301',
        'ownerId': 'me',
        'courseState': 'PROVISIONED'
    }
    course = service.courses().create(body=course).execute()
    print('Course created: %s %s' % (course.get('name'), course.get('id')))


if __name__ == '__main__':
    main()