
from APNSWrapper import *
import binascii

s = "7d32d782919071c350e43c3d8f56196928edb5a0721d767ab7f452938d9230e7"
     

deviceToken = binascii.unhexlify(s)

# create wrapper
wrapper = APNSNotificationWrapper('/root/test/tea/cert.pem', True)

# create message
message = APNSNotification()
message.token(deviceToken)
message.alert("alert")
message.badge(5)
message.sound()

# add message to tuple and send it to APNS server
wrapper.append(message)
wrapper.notify()

print "after send"
