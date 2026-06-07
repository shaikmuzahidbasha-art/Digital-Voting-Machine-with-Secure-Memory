# =========================================================
# DIGITAL VOTING MACHINE WITH SECURE MEMORY USING ESP32
# =========================================================
# Features Implemented:
#
# 1. Design state machines for vote counting logic
# 2. Secure data storage using EEPROM/flash integration
# 3. Display results on LCD display
# 4. Implement debouncing logic for tactile switches
#
# =========================================================

from machine import Pin, I2C, PWM
import time
import json

# =========================================================
# LCD INTERFACE
# Requirement:
# "Display results on LCD or 7-segment display"
# =========================================================

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
addr = 0x27

BACKLIGHT = 0x08
ENABLE = 0x04

def lcd_write(data):
    i2c.writeto(addr, bytes([data | BACKLIGHT]))

def lcd_toggle(data):
    lcd_write(data | ENABLE)
    time.sleep_us(500)
    lcd_write(data & ~ENABLE)
    time.sleep_us(500)

def lcd_send(data, mode=0):

    high = (data & 0xF0) | mode
    low = ((data << 4) & 0xF0) | mode

    lcd_write(high)
    lcd_toggle(high)

    lcd_write(low)
    lcd_toggle(low)

def lcd_cmd(cmd):
    lcd_send(cmd, 0)

def lcd_data(data):
    lcd_send(data, 1)

def lcd_init():

    time.sleep(0.05)

    lcd_cmd(0x33)
    lcd_cmd(0x32)
    lcd_cmd(0x28)
    lcd_cmd(0x0C)
    lcd_cmd(0x06)
    lcd_cmd(0x01)

def lcd_clear():
    lcd_cmd(0x01)
    time.sleep(0.01)

def lcd_move(col, row):

    if row == 0:
        lcd_cmd(0x80 + col)
    else:
        lcd_cmd(0xC0 + col)

def lcd_puts(text):

    for c in text:
        lcd_data(ord(c))

# =========================================================
# BUTTON INPUTS
# Tactile switches for voting
# =========================================================

btnA = Pin(14, Pin.IN, Pin.PULL_UP)
btnB = Pin(27, Pin.IN, Pin.PULL_UP)
btnC = Pin(26, Pin.IN, Pin.PULL_UP)

btnResult = Pin(25, Pin.IN, Pin.PULL_UP)
btnReset = Pin(33, Pin.IN, Pin.PULL_UP)

# =========================================================
# RGB STATUS LED
# =========================================================

red = Pin(4, Pin.OUT)
green = Pin(2, Pin.OUT)
blue = Pin(15, Pin.OUT)

def rgb_off():
    red.value(0)
    green.value(0)
    blue.value(0)

def show_green():
    red.value(0)
    green.value(1)
    blue.value(0)

def show_red():
    red.value(1)
    green.value(0)
    blue.value(0)

def show_blue():
    red.value(0)
    green.value(0)
    blue.value(1)

# =========================================================
# BUZZER
# =========================================================

buzzer = PWM(Pin(18))
buzzer.duty(0)

def tone(freq, duration):

    buzzer.freq(freq)
    buzzer.duty(512)

    time.sleep(duration)

    buzzer.duty(0)

def vote_sound():
    tone(1200, 0.08)

def result_sound():
    tone(1000, 0.1)
    tone(1200, 0.1)

def reset_sound():
    tone(400, 0.2)

# =========================================================
# SECURE DATA STORAGE USING FLASH MEMORY
#
# Requirement:
# "Secure data storage using EEPROM/flash integration"
#
# Votes are stored inside ESP32 flash memory using JSON
# file storage.
# =========================================================

voteA = 0
voteB = 0
voteC = 0

def save_votes():

    data = {
        "A": voteA,
        "B": voteB,
        "C": voteC
    }

    with open("votes.json", "w") as f:
        json.dump(data, f)

def load_votes():

    global voteA, voteB, voteC

    try:

        with open("votes.json", "r") as f:

            data = json.load(f)

            voteA = data["A"]
            voteB = data["B"]
            voteC = data["C"]

    except:

        voteA = 0
        voteB = 0
        voteC = 0

# =========================================================
# DEBOUNCING LOGIC
#
# Requirement:
# "Implement debouncing logic for tactile switches"
#
# This prevents multiple vote registrations caused by
# switch bouncing.
# =========================================================

def wait_release(btn):

    while btn.value() == 0:
        time.sleep(0.05)

# =========================================================
# LCD MESSAGE HELPER
# =========================================================

def message(line1, line2=""):

    lcd_clear()

    lcd_move(0, 0)
    lcd_puts(line1)

    lcd_move(0, 1)
    lcd_puts(line2)

# =========================================================
# INVALID MULTI BUTTON PRESS DETECTION
# =========================================================

def invalid_vote():

    show_red()

    message("Invalid Vote", "Try Again")

    tone(300, 0.3)

    time.sleep(1)

    rgb_off()

# =========================================================
# INITIALIZATION
# =========================================================

lcd_init()

load_votes()

message("Secure EVM", "Ready to Vote")

show_blue()

time.sleep(2)

# =========================================================
# STATE MACHINE FOR VOTE COUNTING LOGIC
#
# Requirement:
# "Design state machines for vote counting logic"
#
# States:
#
# 1. IDLE STATE
# 2. VOTE STATE
# 3. RESULT STATE
# 4. RESET STATE
#
# =========================================================

while True:

    # =====================================================
    # IDLE STATE
    # Waiting for user input
    # =====================================================

    pressed = 0

    if btnA.value() == 0:
        pressed += 1

    if btnB.value() == 0:
        pressed += 1

    if btnC.value() == 0:
        pressed += 1

    # =====================================================
    # INVALID STATE
    # Multiple buttons pressed simultaneously
    # =====================================================

    if pressed > 1:

        invalid_vote()

        wait_release(btnA)
        wait_release(btnB)
        wait_release(btnC)

    # =====================================================
    # VOTE STATE : Candidate A
    # =====================================================

    elif btnA.value() == 0:

        voteA += 1

        save_votes()

        show_green()

        vote_sound()

        message("Vote Recorded", "Candidate A")

        wait_release(btnA)

        rgb_off()

    # =====================================================
    # VOTE STATE : Candidate B
    # =====================================================

    elif btnB.value() == 0:

        voteB += 1

        save_votes()

        show_green()

        vote_sound()

        message("Vote Recorded", "Candidate B")

        wait_release(btnB)

        rgb_off()

    # =====================================================
    # VOTE STATE : Candidate C
    # =====================================================

    elif btnC.value() == 0:

        voteC += 1

        save_votes()

        show_green()

        vote_sound()

        message("Vote Recorded", "Candidate C")

        wait_release(btnC)

        rgb_off()

    # =====================================================
    # RESULT STATE
    # =====================================================

    elif btnResult.value() == 0:

        total = voteA + voteB + voteC

        show_blue()

        message("Counting Votes", "")

        time.sleep(1)

        lcd_clear()

        lcd_puts(f"A:{voteA} B:{voteB}")

        lcd_move(0, 1)

        lcd_puts(f"C:{voteC}")

        time.sleep(3)

        lcd_clear()

        lcd_puts(f"Total:{total}")

        time.sleep(2)

        if voteA > voteB and voteA > voteC:

            message("Winner", "Candidate A")

        elif voteB > voteA and voteB > voteC:

            message("Winner", "Candidate B")

        elif voteC > voteA and voteC > voteB:

            message("Winner", "Candidate C")

        else:

            message("Result", "Tie")

        result_sound()

        wait_release(btnResult)

        rgb_off()

    # =====================================================
    # RESET STATE
    # Long press reset protection for security
    # =====================================================

    elif btnReset.value() == 0:

        message("Hold Reset", "3 Seconds")

        start = time.time()

        while btnReset.value() == 0:

            if time.time() - start >= 3:

                voteA = 0
                voteB = 0
                voteC = 0

                save_votes()

                show_red()

                reset_sound()

                message("System Reset", "Completed")

                time.sleep(2)

                rgb_off()

                break

    time.sleep(0.05)
