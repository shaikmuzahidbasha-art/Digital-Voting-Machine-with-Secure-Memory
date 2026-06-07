# Digital Voting Machine with Secure Memory

## Project Overview

This project implements a Secure Electronic Voting Machine (EVM) using ESP32 and MicroPython. The system allows users to cast votes for multiple candidates using push buttons, stores vote data securely in ESP32 flash memory, displays results on an LCD, and includes debouncing logic to prevent false voting.

This project was developed as part of the Digital Electronics & VLSI Internship program.

---

## Features

* State machine based vote counting logic
* Secure vote storage using ESP32 Flash Memory (JSON)
* LCD display for vote confirmation and results
* Debouncing logic for tactile switches
* RGB LED status indication
* Buzzer feedback for user interaction
* Invalid multiple-button press detection
* Protected reset functionality with long-press security

---

## Project Requirements Covered

| Requirement                                        | Implementation                                          |
| -------------------------------------------------- | ------------------------------------------------------- |
| Design state machines for vote counting logic      | Implemented using IDLE, VOTE, RESULT and RESET states   |
| Secure data storage using EEPROM/Flash integration | Votes stored in ESP32 Flash Memory using JSON           |
| Display results on LCD or 7-segment display        | 16x2 I2C LCD Display used                               |
| Implement debouncing logic for tactile switches    | Button release detection and debounce delay implemented |

---

## Hardware Components

* ESP32 DevKit V1
* 16x2 I2C LCD Display
* Push Buttons
* RGB LED
* Buzzer
* Breadboard
* Jumper Wires

---

## Software Tools

* MicroPython
* Wokwi Simulator
* GitHub

---

## Wokwi Simulation

Simulation Link:

https://wokwi.com/projects/464929365270426625

---

## Project Structure
```
text
Digital-Voting-Machine-with-Secure-Memory
│
├── Source_Code
│   ├── main.py
│   ├── diagram.json
│   ├── lcd_api.py
│   └── i2c_lcd.py
│
├── Screenshots
│
├── README.md
├── requirements.txt
├── .gitignore
```

---

## Working Principle

1. System initializes and loads previously stored votes from flash memory.
2. User presses a candidate button to cast a vote.
3. Vote is securely stored in ESP32 flash memory.
4. LCD displays vote confirmation.
5. RGB LED and buzzer provide feedback.
6. Result button displays vote count and winner.
7. Reset button requires a long press for security.

---

## Future Enhancements

* Biometric voter authentication
* RFID-based voter identification
* Cloud vote synchronization
* Encrypted vote storage
* Web dashboard for monitoring

---

## Author

MUZAHID BASHA SHAIK

Digital Electronics & VLSI Intern
