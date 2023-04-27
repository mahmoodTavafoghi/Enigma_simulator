# Enigma Simulator(M3 or I or Wehrmacht Enigma)
# This program was written by Mahmood Tavafoghi on Spring 1402
# mahmood.tavafoghi@gmail.com
import sys
import string


def C2I(cc):
    return string.ascii_uppercase.index(cc)
# -----------------------


def I2C(ii):
    return string.ascii_uppercase[ii]
# -----------------------


def is_upercase_char(c):
    if string.ascii_uppercase.find(c) != -1:
        return True
    else:
        return False
# -----------------------

# Rotor-Class----


class Rotor:
    def __init__(self, Rotor_number, Ring=0, Grund=0):

        self.Grund = Grund
        self.Ring = Ring
        rt = open("rotors/"+Rotor_number+".rot", "r")
        self.Rotor_Map = list(map(C2I, (rt.readline().strip())))
        self.notches = list(map(C2I, rt.readline().strip()))
        # print(self.Rotor_Map)
# Rotor-setup----
        for i in range(26):
            self.Rotor_Map[i] = (self.Rotor_Map[i]+self.Ring) % 26

        for i in range(self.Ring):
            self.Rotor_Map.insert(0, self.Rotor_Map.pop())

        for i in range(self.Grund):
            self.Rotor_Map.append(self.Rotor_Map.pop(0))
        # print(self.Rotor_Map)

# Methods-----
    def advance(self):
        self.Rotor_Map.append(self.Rotor_Map.pop(0))
        self.Grund += 1
# -----------------------

    def cipher_first(self, p):
        return (self.Rotor_Map[p]-self.Grund+26) % 26
# -----------------------

    def cipher_second(self, q):
        return self.Rotor_Map.index((q + self.Grund) % 26)
# ------------------------


class PlugBoard:
    def __init__(self, Steckers):
        self.Plug_Board_map = list(range(26))

        if len(Steckers) == 0:
            return
        Steckers = Steckers.split(":")

        for i in range(len(Steckers)):
            self.Plug_Board_map[C2I(Steckers[i][0])] = C2I(Steckers[i][1])
            self.Plug_Board_map[C2I(Steckers[i][1])] = C2I(Steckers[i][0])
# ----------------------

    def cipher(self, w):
        return self.Plug_Board_map[w]
# ---------------------


class Enigma:

    def __init__(self, ukw="B", left="I", middle="II", right="III",
                 st="AB:CD:EF:GH:IJ", ring="AAA", grund="AAA", debug=False):

        self.Rotor_Left = Rotor(left, C2I(ring[0]), C2I(grund[0]))

        self.Rotor_Middle = Rotor(middle, C2I(ring[1]), C2I(grund[1]))

        self.Rotor_Right = Rotor(right, C2I(ring[2]), C2I(grund[2]))

        self.Reflector = Rotor(ukw, 0, 0)

        self.PlugBoard = PlugBoard(st)

        self.debug = debug

        self.number = 0
# ------------------------

    def Rotors_Advance(self):
        self.number += 1
        if self.Rotor_Middle.Grund in self.Rotor_Middle.notches:
            self.Rotor_Right.advance()
            self.Rotor_Middle.advance()
            self.Rotor_Left.advance()

        elif self.Rotor_Right.Grund in self.Rotor_Right.notches:
            self.Rotor_Right.advance()
            self.Rotor_Middle.advance()
        else:
            self.Rotor_Right.advance()
# -------------------------

    def Encode(self, c):
        c = C2I(c)
        self.Rotors_Advance()

        if self.debug:
            print('{:0=3}'.format(self.number), '--->', I2C(self.Rotor_Left.Grund % 26) +
                  I2C(self.Rotor_Middle.Grund % 26)+I2C(self.Rotor_Right.Grund % 26), end='----->')

        if self.debug:
            print(I2C(c), end=' ------> ')
        c = self.PlugBoard.cipher(c)

        if self.debug:
            print(I2C(c), end=' --> ')
        c = self.Rotor_Right.cipher_first(c)

        if self.debug:
            print(I2C(c), end=' --> ')
        c = self.Rotor_Middle.cipher_first(c)

        if self.debug:
            print(I2C(c), end=' --> ')
        c = self.Rotor_Left.cipher_first(c)

        if self.debug:
            print(I2C(c), end=' --> ')
        c = self.Reflector.cipher_first(c)

        if self.debug:
            print(I2C(c), end=' --> ')
        c = self.Rotor_Left.cipher_second(c)

        if self.debug:
            print(I2C(c), end=' --> ')
        c = self.Rotor_Middle.cipher_second(c)

        if self.debug:
            print(I2C(c), end=' --> ')
        c = self.Rotor_Right.cipher_second(c)

        if self.debug:
            print(I2C(c), end=' -----> ')
        c = self.PlugBoard.cipher(c)

        if self.debug:
            print(I2C(c))

        return I2C(c)
# -----------------------------
# -------DRIVE CODE-------------


if len(sys.argv) < 8:
    print(
        "\n\nEnigma M3 Simulator...\nplease Enter correct syntax as follows:\npython Enigma_mt_M3.py UKW LEFT MIDDLE RIGHT PLUGBOARD RING GRUND [Debug]\nExample :\npython Enigma_M3_mt.py B II IV III AC:YX:HR:QW:NM TGF WSW DEBUG < test.txt")

    sys.exit(0)
else:
    UKW = sys.argv[1].upper()
    LEFT = sys.argv[2].upper()
    MIDDLE = sys.argv[3].upper()
    RIGHT = sys.argv[4].upper()
    PLUGBOARD = sys.argv[5].upper()
    RING = sys.argv[6].upper()
    GRUND = sys.argv[7].upper()
    if len(sys.argv) > 8:
        DEBUG = True
    else:
        DEBUG = False


input_text = sys.stdin.readlines()
Enigma_machine = Enigma(UKW, LEFT, MIDDLE, RIGHT,
                        PLUGBOARD, RING, GRUND, DEBUG)
output_text = ""
# global number

if DEBUG:
    print('\nDEBUG MODE IS ON!\n')
    print('Reflector used                         == ', UKW)
    print('Wheel order (Walzenlage)               == ', LEFT, MIDDLE, RIGHT)
    print('Ring settings (Ringstellung)           == ', RING)
    print('Starting position(Grundstellung)       == ', GRUND)
    print('Plug connections (Steckerverbindungen) == ', PLUGBOARD)
    print('No.     Grund   INPUT  PB     R1    R2    R3   UKW    R3    R2    R1     PB   OUTPUT')

for line in input_text:
    input_characters = line.upper()
    for w in input_characters:
        if w == '-':
            temp = Enigma_machine.Encode('X')
            output_text += '-'
            continue
        if not is_upercase_char(w):
            continue
        output_text += Enigma_machine.Encode(w)


print(output_text)
