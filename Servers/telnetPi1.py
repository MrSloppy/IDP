__author__ = 'SyntaxTerror'

import socket
import sys
from thread import *
import ctypes
import RPi.GPIO as GPIO
import sqlite3
import os
import subprocess
GPIO.setmode(GPIO.BCM)

# Pin 21 correspondeert met 39 op het board
# Pin GPIO.OUT is nodig want
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

db = sqlite3.connect('kamerdatabase.db')
db.row_factory = lambda cursor, row: row[0]
c = db.cursor()
iplijst = '''SELECT ip_adres FROM woning'''
trusted_ip = c.execute(iplijst).fetchall()

print(trusted_ip)

try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # AF_INET = connection type
except socket.error:
        print("Failed to create socket!!")
        sys.exit(0)

print("Socket gemaakt")

print(s)

host = ''
port = 5555

iptablelijst = ["145.89.157.66", "145.89.107.238", "145.89.104.76", "145.89.252.147", "192.168.178.29",
                "145.89.254.155", "192.168.42.3", "145.89.158.209", "145.89.220.55"]

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))           # Dit print de error voor het binden van de socket aan de poort

s.listen(50)             # Dit is de queue (hoeveel mensen kunnen connecten)

print("Waiting for a connection")


def threaded_client(conn):          # Dit is de functie voor client connectie

    while True:

        data = conn.recv(2048)      # Buffer rate van de data


    conn.close()

while True:

    conn, addr = s.accept()
    data = conn.recv(2048)
    print(data.decode('utf-8'))
    print("Connected to: "+addr[0]+":"+str(addr[1]))
    if addr[0] in trusted_ip:
        print("Vertrouwde connectie")
        print(trusted_ip)
        if GPIO.input(21) == 0:
                GPIO.output(21, GPIO.HIGH)
                conn.close()

                #ctypes.windll.user32.MessageBoxW(0, "Er is een noodoproep gekomen vanaf ip: "+addr[0], "Noodoproep!", 1)        # Dit maakt een pop-up windows met de $
        else:
                GPIO.output(21, GPIO.LOW)
                conn.close()
        conn.close()
    else:
        GPIO.output(21, GPIO.LOW)
        conn.close()

    start_new_thread(threaded_client, (conn,))

GPIO.cleanup()


