import requests

norbert = "http://152.94.160.198/rw/panel/ctrlstate"
auth = requests.auth.HTTPDigestAuth( "Default User" ,"robotics" )
# make an get - request
response = requests.get( norbert , auth = auth )
print(response.status_code) # an integer
print(response.text) # a string
# the response may be returned in JSON format
response = requests.get( norbert + " ? json =1 " , auth = auth )
print (response.text)
