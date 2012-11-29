#Rogers Cisco network monitor
import urllib
import urllib2
import cookielib

#Set connection parameters
routerPostPage = "http://192.168.0.1/goform/Docsis_system"
routerDHCPPage = "http://192.168.0.1/DHCPClientTable.asp"

values = urllib.urlencode({'password_login' : 'login_password',
          'username_login' : 'login_username'})

users = [
	[ "User",
		[
			["Device", "MA:CA:DD:RE:SS:00"]
		]
	]
]

def formatMacAddress(mac):
	mac = mac.upper()
	return mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]


#Create a CookieJar
cj = cookielib.CookieJar()

print "Logging In...."

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.open(routerPostPage, values)

print "Getting logged in devices...\n\n"
resp = opener.open(routerDHCPPage)
rawHTML = resp.read()


rawlines = rawHTML.splitlines()
data = []

for line in rawlines:
	if( "<OPTION value" in line):
		record = line.split("&nbsp;")
		size = len(record)
		record[size-9] = record[size-9][len(record[size-9])-12:]
		record = filter(None, record)
		record[0] = formatMacAddress(record[0])
		record.append('')
		data.append(record)

#Translate
for record in data:
	for user in users:
		for device in user[1]:
			if(record[0] == device[1]):
				print user[0] + " logged in on " + device[0] + " at " + record[1]
				record[len(record)-1] = 'X'

for record in data:
	if(record[len(record)-1] != 'X'):
		print "Unknown Device On Network at " + record[1] + " with Mac Address " + record[0] + "!!"



