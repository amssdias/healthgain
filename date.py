import datetime

tday = datetime.date.today()
print(tday)

tdelta = datetime.timedelta(days=1)

print(tdelta)

print( tday - tdelta)