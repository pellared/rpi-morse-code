#!/usr/bin/python3

import gpiozero
import time
from enum import Enum

Morse = Enum("Morse", "SHORT LONG NEW_LETTER NEW_WORD")

MorseToSound = {
    Morse.SHORT : (1, 1),
    Morse.LONG : (3, 1),
    Morse.NEW_LETTER : (0, 2),
    Morse.NEW_WORD : (0, 6)
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
    led = gpiozero.LED(17) 
    led.on() # light when app is running

    active_buzzer = gpiozero.Buzzer(20)

    button1 = gpiozero.Button(26)
    button2 = gpiozero.Button(19)
    button3 = gpiozero.Button(13)
    button4 = gpiozero.Button(6)
    button5 = gpiozero.Button(5)
    button6 = gpiozero.Button(22)
    button7 = gpiozero.Button(27)

    running = True
    def close():
        nonlocal running
        print("closing...")
        running = False
    button7.when_pressed = close

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
        while running and message:
            morse_code = message.pop(0)
            send_code(morse_code)
    
    def send_code(code):
        hi, lo = MorseToSound[code]
        if hi > 0:
            active_buzzer.on()
            time.sleep(0.1 * hi)
        active_buzzer.off()
        time.sleep(0.1 * lo)

    button1.when_pressed = write_short
    button2.when_pressed = write_long
    button3.when_pressed = write_new_letter
    button4.when_pressed = write_new_word
    button5.when_pressed = clear_message
    button6.when_pressed = send_message

    while running:
       s = input('--> ')
       send_code(Morse.LONG)

if __name__ == "__main__":
    main()
