from PIL import Image


def construct(a):
    if len(a) < 10:
        a = a[:2] + '0' * (10 - len(a)) + a[2:]
    return a


print("IMAGE STENOGRAPHY")
print("Note: Make sure the program and\nthe image lye in the same directory.")
mode = input('Do you want to encrypt[0] data or decrypt[1]?')

name = input("Please enter the name of the image: ")
image = Image.open(name)

x, y = image.size
pixelMap = image.load()

if mode == '0':
    msg = input('Please enter the message [max length: ' + str(x * y) + ']: ').lower()
    msg = msg.replace(' ', '{').replace('.', '|').replace(',', '}').replace('?', '~')
    if len(msg) < x * y:
        msg += "{" * (x * y - len(msg))

    msgList = []
    for ch in msg:
        ch = ord(ch) - 96
        a = bin(ch)
        a = a[2:]
        if len(a) < 6:
            a = "0" * (6 - len(a)) + a
        msgList.append([a[0:2], a[2:4], a[4:6]])

    msgIte = 0
    for widIte in range(x):
        for heiIte in range(y):
            temp = list(pixelMap[widIte, heiIte])

            r = bin(temp[0])
            r = construct(r)
            r = r[:len(r) - 2]
            r += str(msgList[msgIte][0])
            r = int(r, 2)

            g = bin(temp[1])
            g = construct(g)
            g = g[:len(g) - 2]
            g += str(msgList[msgIte][1])
            g = int(g, 2)

            b = bin(temp[2])
            b = construct(b)
            b = b[:len(b) - 2]
            b += str(msgList[msgIte][2])
            b = int(b, 2)

            pixelMap[widIte, heiIte] = (r, g, b)

            msgIte += 1

    image.save(name[:len(name) - 4] + '_processed' + name[-4:])
############################################
else:
    msgList = ''

    msgIte = 0
    for widIte in range(x):
        for heiIte in range(y):
            temp = list(pixelMap[widIte, heiIte])

            r = construct(bin(temp[0]))
            r = r[-2:]

            g = construct(bin(temp[1]))
            g = g[-2:]

            b = construct(bin(temp[2]))
            b = b[-2:]

            ch = r + '' + g + '' + b
            ch = int(ch, 2) + 96
            msgList += chr(ch)

    msgList = msgList.replace('{', ' ').replace('|', '.').replace('}', ',').replace('~', '?')
    msgList.strip()

    print(msgList)
