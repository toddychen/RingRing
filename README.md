# RingRing
RingRing is a smart meeting reminder app that continuously monitors your Google Calendar for upcoming meetings. When a meeting is about to start, it detects any online video conference links and delivers a powerful, near full-screen alert on your Mac to make sure you never miss a call.


## Python and Tk GUI toolkit 
NOTE: tested python version 3.13 and tcl-tk version 9.0.2

NOTE: For the missing configuration for tk, `brew install pyenv tcl-tk` might be helpful.

## How to use it
### Pull `credentials.json` from Google Cloud platform
TODO 
### Set up env
* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt

### Set up crontab (to run from inside venv)
Example:   
```*/5 * * * * /Users/toddy/repos/github/RingRing/venv/bin/python3 /Users/toddy/repos/github/RingRing/scripts/ringring.py```

NOTE: update path to the repo.