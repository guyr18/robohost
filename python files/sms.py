from twilio.rest import Client

account_sid = 'AC222d9accf4275e0a382642ca769af586' 
auth_token = '[3e478e164fad246b1b7144e4dbb0eb75]' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create(to='+19199854106')
 
print(message.sid)
