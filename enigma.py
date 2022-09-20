# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]


# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order

    global wheel_rotate_cnt_0
    global wheel_rotate_cnt_1
    global wheel_rotate_cnt_2

    if reverse:
        pass_2 = SETTINGS["ETW"][SETTINGS["WHEELS"][2]["wire"].find(input) - wheel_rotate_cnt_2]
        pass_1 = SETTINGS["ETW"][SETTINGS["WHEELS"][1]["wire"].find(pass_2) - wheel_rotate_cnt_1]
        pass_0 = SETTINGS["ETW"][SETTINGS["WHEELS"][0]["wire"].find(pass_1) - wheel_rotate_cnt_0]
        return pass_0
    
    pass_0 = SETTINGS["WHEELS"][0]["wire"][(ord(input) - ord('A') + wheel_rotate_cnt_0) % 26]
    pass_1 = SETTINGS["WHEELS"][1]["wire"][(ord(pass_0) - ord('A') + wheel_rotate_cnt_1) % 26]
    pass_2 = SETTINGS["WHEELS"][2]["wire"][(ord(pass_1) - ord('A') + wheel_rotate_cnt_2) % 26]
    return pass_2

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

wheel_rotate_cnt_0 = 0
wheel_rotate_cnt_1 = 0
wheel_rotate_cnt_2 = 0
# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    turn_0 = SETTINGS["WHEELS"][0]["turn"]
    turn_1 = SETTINGS["WHEELS"][1]["turn"]
    turn_2 = SETTINGS["WHEELS"][2]["turn"]

    global wheel_rotate_cnt_0
    global wheel_rotate_cnt_1
    global wheel_rotate_cnt_2

    if wheel_rotate_cnt_0 == turn_0:
        if wheel_rotate_cnt_1 == turn_1:
            wheel_rotate_cnt_2 = (wheel_rotate_cnt_2 + 1) % 26
        wheel_rotate_cnt_1 = (wheel_rotate_cnt_1 + 1) % 26
    wheel_rotate_cnt_0 = (wheel_rotate_cnt_0 + 1) % 26
        

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')