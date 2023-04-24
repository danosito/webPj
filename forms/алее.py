i='3'*6+'4'*75
while '35' in i or '355' in i or '3444' in i:
    if '35' in i:
        i = i.replace('35','4',1)
    else:
        if '355' in i:
            i = i.replace('355','4',1)
        else:
            i = i.replace('3444','4',1)
print(i)