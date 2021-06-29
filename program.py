from klokki_data_repo import KlokkiDataRepo
from datetime import datetime, timedelta
from jira_service import JiraService
from terminal_helper import TerminalHelper
from terminal_helper import bcolors
import sys
import pdb

# Get the day we want to pull data for
# Defaults to today
day = ''
if (len(sys.argv) > 1):
    try:
        day = datetime.strptime(str(sys.argv[1]), '%Y-%m-%d')
    except ValueError:
        print('First arg is date for script to be run. yyyy-mm-dd')
        sys.exit()
else:
    day = datetime.now() - timedelta(hours=6)

# Get klokki time data from local files
repo = KlokkiDataRepo()
data = repo.get_time_log_for_day(day.year, day.month, day.day)

# Post Jira tracked tasks to Jira
jira_service = JiraService()
results = jira_service.try_post_time(data)

# Define keys/headers of result data to print out
keys = ['issue', 'started', 'duration', 'status']
terminal = TerminalHelper()

# Reformat time so its more readable
for entry in results:
    entry['started'] = entry['started'].strftime('%I:%M')
    hours, remainder = divmod(entry['timeSpentSeconds'], 3600)
    minutes, seconds = divmod(remainder, 60)
    entry['duration'] = f'{int(hours)}h {int(minutes)}m'

# Define coloring rules for printout summary
def color_rule(item):
    if item['status'] == 'Posted':
        return bcolors.OKGREEN
    elif item['status'] == 'Already posted':
        return bcolors.OKBLUE
    elif item['status'] == 'NA':
        return bcolors.OKCYAN
    else:
        return bcolors.WARNING
# Print    
terminal.print_list_of_dicts_as_graph(keys, results, color_rule)



