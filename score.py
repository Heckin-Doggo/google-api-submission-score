from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
COURSE_SCOPE = "https://www.googleapis.com/auth/classroom.courses.readonly"
STUDENT_SCOPES = ["https://www.googleapis.com/auth/classroom.coursework.me.readonly", COURSE_SCOPE]
TEACHER_SCOPES = ["https://www.googleapis.com/auth/classroom.coursework.students.readonly", COURSE_SCOPE]


def get_token():
    # default variable
    creds = None

    # determine if teacher or student
    # TODO: make this work with a single call to the python file.
    # e.g. `python score.py --teacher`
    choice_made = False
    while not choice_made:
        choice = input("Are you a [T]eacher or a [S]tudent?").strip().lower()
        if choice[0] == "t":
            scopes = TEACHER_SCOPES
            choice_made = True
        elif choice[0] == "s":
            scopes = STUDENT_SCOPES
            choice_made = True
        else:
            print("Not recognized, please try again.")

    # get the token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds




def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    creds = get_token()

    service = build('classroom', 'v1', credentials=creds)

    # Sample Code: Get 10 Courses from the user.
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

    # Get Submissions #
    # Code remains untested, proceed with caution.

    submissions = []
    page_token = None

    while True:
        coursework = service.courses().courseWork()
        response = coursework.studentSubmissions().list(
            pageToken=page_token,
            courseId=302549246247,
            userId='me').execute()
        submissions.extend(response.get('studentSubmissions', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break

    if not submissions:
        print('No student submissions found.')
    else:
        print('Student Submissions:')
        for submission in submissions:
            print("%s was submitted at %s" %
                  (submission.get('id'),
                   submission.get('creationTime')))

    # TODO: Delete token on exit.






if __name__ == '__main__':
    main()