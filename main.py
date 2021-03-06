#!/usr/bin/python3

import gpiozero
import time
from enum import Enum

class Pi:
    led = gpiozero.LED(17) 
    active_buzzer = gpiozero.Buzzer(20)
    button1 = gpiozero.Button(26)
    button2 = gpiozero.Button(19)
    button3 = gpiozero.Button(13)
    button4 = gpiozero.Button(6)
    button5 = gpiozero.Button(5)
    button6 = gpiozero.Button(22)
    button7 = gpiozero.Button(27)

SHORT_IN_SECONDS = 0.1

Morse = Enum("Morse", "SHORT LONG NEW_LETTER NEW_WORD EXTEND_LETTER_TO_WORD")

MorseToSound = {
    Morse.SHORT : (1, 1),
    Morse.LONG : (3, 1),
    Morse.NEW_LETTER : (0, 2),
    Morse.NEW_WORD : (0, 6),
    Morse.EXTEND_LETTER_TO_WORD : (0, 4)
}

CharToMorse = {
    "a" : [ Morse.SHORT, Morse.LONG ],
    "b" : [ Morse.LONG, Morse.SHORT, Morse.SHORT, Morse.SHORT ],
    "c" : [ Morse.LONG, Morse.SHORT, Morse.LONG, Morse.SHORT ],
    "d" : [ Morse.LONG, Morse.SHORT, Morse.SHORT ],
    "e" : [ Morse.SHORT ],
    "f" : [ Morse.SHORT, Morse.SHORT, Morse.LONG, Morse.SHORT ],
    "g" : [ Morse.LONG, Morse.LONG, Morse.SHORT ],
    "h" : [ Morse.SHORT, Morse.SHORT, Morse.SHORT, Morse.SHORT ],
    "i" : [ Morse.SHORT, Morse.SHORT ],
    "j" : [ Morse.SHORT, Morse.LONG, Morse.LONG, Morse.LONG ],
    "k" : [ Morse.LONG, Morse.SHORT, Morse.LONG ],
    "l" : [ Morse.SHORT, Morse.LONG, Morse.SHORT, Morse.SHORT ],
    "m" : [ Morse.LONG, Morse.LONG ],
    "n" : [ Morse.LONG, Morse.SHORT ],
    "o" : [ Morse.LONG, Morse.LONG, Morse.LONG ],
    "p" : [ Morse.SHORT, Morse.LONG, Morse.LONG, Morse.SHORT ],
    "q" : [ Morse.LONG, Morse.LONG, Morse.SHORT, Morse.LONG ],
    "r" : [ Morse.SHORT, Morse.LONG, Morse.SHORT ],
    "s" : [ Morse.SHORT, Morse.SHORT, Morse.SHORT ],
    "t" : [ Morse.LONG ],
    "u" : [ Morse.SHORT, Morse.SHORT, Morse.LONG ],
    "v" : [ Morse.SHORT, Morse.SHORT, Morse.SHORT, Morse.LONG ],
    "w" : [ Morse.SHORT, Morse.LONG, Morse.LONG ],
    "x" : [ Morse.LONG, Morse.SHORT, Morse.SHORT, Morse.LONG ],
    "y" : [ Morse.LONG, Morse.SHORT, Morse.LONG, Morse.LONG ],
    "z" : [ Morse.LONG, Morse.LONG, Morse.SHORT, Morse.SHORT ]
}

def main():
    running = True
    Pi.led.on() # light when app is running
    def close():
        nonlocal running
        print("closing...")
        running = False
    Pi.button7.when_pressed = close

    message = []
    def write_short():
        message.append(Morse.SHORT)
    def write_long():
        message.append(Morse.LONG)
    def write_new_letter():
        message.append(Morse.NEW_LETTER)
    def write_new_word():
        message.append(Morse.NEW_WORD)
    def clear_message():
        message.clear()
    def send_message():
        send_morse(message)

    Pi.button1.when_pressed = write_short
    Pi.button2.when_pressed = write_long
    Pi.button3.when_pressed = write_new_letter
    Pi.button4.when_pressed = write_new_word
    Pi.button5.when_pressed = clear_message
    Pi.button6.when_pressed = send_message

    while running:
        s = input('--> ')
        m = to_morse(s)
        send_morse(m)

def send_morse(morse):
    while morse:
        morse_code = morse.pop(0)
        send_code(morse_code)

def send_code(code):
    hi, lo = MorseToSound[code]
    if hi > 0:
        Pi.active_buzzer.on()
        time.sleep(SHORT_IN_SECONDS * hi)
    Pi.active_buzzer.off()
    time.sleep(SHORT_IN_SECONDS * lo)

def to_morse(s):
    result = []
    for c in s:
        if c.isspace():
            result.append(Morse.EXTEND_LETTER_TO_WORD)
        else:
            c = c.lower()
            if c in CharToMorse:
                result.extend(CharToMorse[c].copy())
                result.append(Morse.NEW_LETTER)
    return result

if __name__ == "__main__":
    main()
