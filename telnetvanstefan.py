__author__ = 'SyntaxTerror'

import socket
import sys
from _thread import *
import ctypes
import sqlite3
import os
import subprocess
# Import smtplib for the actual sending function
import smtplib

# Prepare actual message

def sendMail():
    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % ("GoM - Gehandicapte ongevallen monitor", ", ".join("testwerknemer@gmail.com"), "!!NOODOPROEP!!", "Er is een noodoproep vanuit kamer: "+str(huisnummer))


    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP_SSL('smtp.gmail.com:465')

    s.login('rakesh.wmv@gmail.com', 'chickentikkamasala')
    s.sendmail('rakesh.wmv@gmail.com', 'testwerknemer@gmail.com', message)
    s.quit()


db = sqlite3.connect('kamerdatabase.db')
db.row_factory = lambda cursor, row: row[0]
c = db.cursor()
iplijst = '''SELECT ip_adres FROM woning'''
huislijst = '''SELECT huisnummer FROM woning'''
huis_nummer_lijst = c.execute(huislijst).fetchall()
trusted_ip = c.execute(iplijst).fetchall()

print(trusted_ip)

# Zorg ervoor dat je telnet client/server aan staat in de Windows Features!!!

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # AF_INET = connection type

print(s)

host = ''
port = 5555


try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))           # Dit print de error voor het binden van de socket aan de poort

s.listen(50)             # Dit is de queue (hoeveel mensen kunnen connecten)



print("Waiting for a connection")


def threaded_client(conn):          # Dit is de functie voor client connectie
    #conn.send(str.encode("HALLO GEEF ME JE CREDITCARD INFO!!"))   # Het moet geENCODE worden want je SEND. Voor RECIEVE is DECODE
    message = ''
    while True:
        data = conn.recv(2048)      # Buffer rate van de data

        message = message+data.decode('utf-8')
        for string in data.decode('utf-8'):
            if string == '\n':
                reply = "Server output: "+message
                message = ''
                conn.sendall(str.encode(reply))

            reply = "Server output: "+data.decode('utf-8'+"\n")     # We recoden want we ontvangen

            if not data:
                break

    conn.close()

while True:

    conn, addr = s.accept()
    data = conn.recv(2048)
    print('Connected to: '+addr[0]+':'+str(addr[1]))
    if addr[0] in trusted_ip:
        for i in range(0, len(trusted_ip)):
            if addr[0] == trusted_ip[i]:
                huisnummer = huis_nummer_lijst[i]
                print(huisnummer)
                sendMail()
        print("Vertrouwde connectie")
        ctypes.windll.user32.MessageBoxW(0, "Er is een noodoproep gekomen vanaf ip: "+addr[0], "Noodoproep!", 1)        # Dit maakt een pop-up windows met de noodmelding en de lokactie van de melding
        p = subprocess.Popen(["C:/Program Files (x86)/Mozilla Firefox/firefox.exe", "index.html"])
    else:
        conn.close()

    start_new_thread(threaded_client, (conn,))