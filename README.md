# GC-API-Score
very original naming
PackHacks 2021 Project
## How to use
To get the backend working, run the following commands in powershell in the root directory

`.\venv\Scripts\activate`

**Note:** if the above didn't work, try running the line below and try again.

`Set-ExecutionPolicy Unrestricted -scope process`

Finally, start flask.

`flask run`

## Current Endpoints
* /getCourses - opens an OAuth connection to be completed by the user, returns their Google Classroom classes.
* /getScoreDummy - generates random test data.