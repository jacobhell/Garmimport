import json as j
import os
import re
from datetime import datetime
from datetime import timedelta

class Activity:
    def __init__(self, url, name, type, time, distance, duration):
        self.url = url
        self.name = name
        self.type = type
        self.time = time
        self.distance = distance
        self.duration = duration        
    
def meters_to_miles(meters):
    return meters * 0.000621371
    
def get_activity(file):
    json_contents = j.loads(file.read())
    url = 'https://connect.garmin.com/modern/activity/%d' % json_contents['activityId']
    name = json_contents['activityName']
    type = json_contents['activityTypeDTO']['typeKey']
    time = datetime.strptime(json_contents['summaryDTO']['startTimeLocal'], '%Y-%m-%dT%H:%M:%S.%f')
    try:
        distance = '%.2f' % meters_to_miles(json_contents['summaryDTO']['distance'])
    except:
        distance = ''
    duration = timedelta(seconds=json_contents['summaryDTO']['duration'])
    
    return Activity(url, name, type, time, distance, duration)
    
def create_md(activity):
    template = '''+++

author = "Jacob Hell"
title = "{activityName} {activityTime}"
date = "{activityDate}"
tags = [
    "activity", "{activityType}"
]

+++

<!--more-->

|Field  |Value  |
|--- | --- |
|**Start Time**|{activityTime}|
|**Distance**|{activityDistance} miles|
|**Duration**|{activityDuration}|

{activityUrl}'''

    out = template.format(activityName=re.sub('"', '\\"', activity.name), 
    activityTime=activity.time, 
    activityDate=activity.time, 
    activityType=activity.type, 
    activityDistance=activity.distance, 
    activityDuration=activity.duration,
    activityUrl=activity.url) 
    
    file_name = re.sub('\\W', '', '{} {}.md'.format(activity.name, activity.time))
    absolute_file = 'content/activities/{}.md'.format(file_name)
    print('writing {}'.format(absolute_file))
    file = open(absolute_file, 'w')
    file.write(out)
    file.close()
    


for filename in os.listdir('activities/'):
    if 'summary.json' in filename:
        file = open('activities/' + filename)
        activity = get_activity(file)
        create_md(activity)