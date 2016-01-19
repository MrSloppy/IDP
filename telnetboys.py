__author__ = 'SyntaxTerror'

import socket
import sys
from _thread import *
import ctypes
import telnetlib
import subprocess
import os

#print(os.path.exists("C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"))            # Dit checkt op VLC uberhaupt bestaat op de laptop
#p = subprocess.Popen(["C:/Program Files (x86)/VideoLAN/VLC/vlc.exe", "C:\\Users\\Timo\\Downloads\\kek.webm"])   # Dit speelt de gekozen video af



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # AF_INET = connection type

print(s)

host = ''
port = 5555

iptablelijst = ["145.89.157.66", "145.89.107.238", "145.89.104.76", "145.89.252.147", "192.168.178.29",
                "145.89.254.155", "145.89.118.72"]

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))           # Dit print de error voor het binden van de socket aan de poort

s.listen(50)             # Dit is de queue (hoeveel mensen kunnen connecten)



print("Waiting for a connection")


def threaded_client(conn):          # Dit is de functie voor client connectie

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
    if addr[0] in iptablelijst:
        print("Vertrouwde connectie")
        print(iptablelijst)
        ctypes.windll.user32.MessageBoxW(0, "Er is een noodoproep gekomen vanaf ip: "+addr[0], "Noodoproep!", 1)        # Dit maakt een pop-up windows met de noodmelding en de lokactie van de melding

    else:
        conn.close()

    start_new_thread(threaded_client, (conn,))