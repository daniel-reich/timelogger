Push time tracked with [Klokki Slim](https://apps.apple.com/us/app/klokki-slim-time-tracking/id1459795140?mt=12) app to Jira

### Setup
- get [Klokki Slim](https://apps.apple.com/us/app/klokki-slim-time-tracking/id1459795140?mt=12) from app store
- `cp .env.example .env`
- Fill out .env file with jira email, jira api token, and local filepath to sqlite database files used by Klokki Slim
- `./build.sh`

### Using Klokki: 
- Only tasks colored red in Klokki Slim will be posted to Jira
- When posting to Jira, the app looks at the first word in the task name for the Jira issue number. Valid names in Klokki should look like: `PEX-123` or `PEX-123 Description of task` 

### To log time:
- `./logtime.sh [yyyy-mm-dd]`
- If no date is passed in, it will default to today
- Posting to jira is idempotent, you can run this script multiple times without re-posting time.
- A summary of work logged in Klokki and whether it was posted to Jira will be printed to the terminal
![image](https://user-images.githubusercontent.com/23177232/123829368-a3006f80-d8bf-11eb-98cc-8f2eff63d882.png)



This script was set up for klokki but could be modified to include other time tracking apps. A dev docker container is also included here for running/developing locally without worrying about python environment setup.
