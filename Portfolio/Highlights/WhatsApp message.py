import pywhatkit

contact = input('Enter a contact number:  ')
message = input('Enter a message to send to '+contact+' : ')
hours = int(input('Enter time to send message(hours): '))
minutes = int(input('Enter time to send message(minutes): '))

pywhatkit.sendwhatmsg(contact, message, hours, minutes)

#Message to: +44 7867 305652
#Reminder to give the cards at coaching, give 2 each and then 3 to best performers
#Time 5:00