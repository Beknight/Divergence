import smtplib

def sendEmail(msg):
#    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login("kickierkicks@gmail.com","aboveAll!1")
        server.sendEmail("kickierkicks@gmail.com", "benjamin.fan11.11@gmail.com", msg) 
        server.quit()

