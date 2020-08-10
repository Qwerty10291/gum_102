from edu import parser

for i in parser('4717116286', 'UBK3'):
    print(i)
    for day in i.values():
        print(day)