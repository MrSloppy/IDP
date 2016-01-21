# Import smtplib for the actual sending function
import smtplib

# Prepare actual message

message = """\
From: %s
To: %s
Subject: %s

%s
""" % ("Rakesh Patel", ", ".join("rybrugman@gmail.com"), "Welcome to Microsoft", "I just spam sir!!")


# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP_SSL('smtp.gmail.com:465')

s.login('rakesh.wmv@gmail.com', 'chickentikkamasala')
s.sendmail('rakesh.wmv@gmail.com', 'rybrugman@gmail.com', message)
s.quit()