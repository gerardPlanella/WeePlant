import datetime
import time

a = datetime.datetime.now()

#time.sleep(3)

#b = datetime.datetime.now()

min = datetime.datetime.now() - datetime.timedelta(seconds=10)

now = datetime.datetime.now()
ttwfnm = now - min
if (now + ttwfnm < now): ttwfnm = ttwfnm.total_seconds()
else: ttwfnm = 0

print(ttwfnm)