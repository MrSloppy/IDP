import sqlite3

iptablelijst = ["145.89.157.66", "145.89.107.238", "145.89.104.76", "145.89.252.147", "192.168.178.29",
                "145.89.220.55", "145.89.220.55", "192.168.42.3", "145.89.105.233", "145.89.118.176"]


db = sqlite3.connect('kamerdatabase.db')
c = db.cursor()
alarm = 0

db.commit()

try:
    c.execute('''CREATE TABLE woning(
    huisnummer tinyint(2),
    ip_adres int(30),
    alarm int(1)
    )''')
    db.commit()
except:
    pass

try:
    for i in range(0, len(iptablelijst)):
        c.execute('''INSERT INTO woning(huisnummer, ip_adres, alarm) VALUES(?, ?, ?)''', (i, iptablelijst[i], alarm))
        db.commit()
except:
    pass

db.close()