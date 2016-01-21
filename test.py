__author__ = 'Timo'

iptablelijst = ["123.123", "321.321", "456.456"]
kamerlijst = ['1', '2', '3']

print(iptablelijst)
print(kamerlijst)

addr = ["456.456"]

for i in range(0, len(iptablelijst)):
    if addr[0] == iptablelijst[i]:
        kamernummer = kamerlijst[i]
        print(kamernummer)