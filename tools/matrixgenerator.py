from enum import Enum
import os

"""
    Copyright 2019 Marcel Hillesheim
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

"""
author: Marcel Hillesheim with modifications by Frank Adams to add Teensy 4.1 & 2.0++

input:
txt file in same folder with the fpc pins pair of the key in the order of the array keys
output:
matrix column and row teensy pin order
AND
key matrix
AND
modifier key matrix

Description:
https://www.instructables.com/id/How-to-Make-a-USB-Laptop-Keyboard-Controller/

little tool to help creating a matrix for a teensy usb-keyboard

its not pretty but functional :d
"""

# lc
con_pin_lc = [23, 0, 22, 1, 24, 2, 21, 3, 25, 4, 20, 5, 19, 6, 18, 7, 17, 8, 16, 9, 15, 10, 14, 11, 26, 12]
# 3.2
con_pin_v3_2 = [23, 0, 22, 1, 21, 2, 20, 3, 19, 4, 18, 5, 17, 6, 24, 7, 25, 8, 33, 9, 26, 10, 27, 11, 28, 12, 32,
                31, 30, 29, 16, 15, 14, 13]
# 4.0
con_pin_v4 = [23, 0, 22, 1, 21, 2, 20, 3, 19, 4, 18, 5, 17, 6, 29, 7, 31, 8, 33, 9, 32, 10, 30, 11, 28, 12, 27, 26,
              25, 24, 16, 15, 14, 13]
# 4.1
con_pin_v4_1 = [23, 0, 22, 1, 21, 2, 20, 3, 19, 4, 18, 5, 17, 6, 16, 7, 15, 8, 14, 9, 10, 11, 12, 24, 25, 26, 27, 28, 
              29, 30, 31, 32, 33, 41]
# 2.0++
con_pin_v2_pp = [27, 26, 0, 25, 1, 24, 2, 23, 3, 22, 4, 21, 5, 20, 28, 19, 7, 18, 8, 9, 38, 10, 39, 11, 40, 12, 41, 13, 
              42, 14, 43, 15, 44, 16, 45, 17]
teensy_devices = [('LC', con_pin_lc), ('3.2', con_pin_v3_2), ('4.0', con_pin_v4), ('4.1', con_pin_v4_1), ('2.0++', con_pin_v2_pp)]

separator = "-----------------------------------------------------\n"


class KeyType(Enum):
    KEY = 1
    MODIFIER = 2
    FN = 3
    # for all-one matrix
    ONE = 4


class Key:
    is_assigned = False

    def __init__(self, label, modifier_value, pin1, pin2):
        self.label = label
        self.pin1 = pin1
        self.pin2 = pin2
        self.type = KeyType.KEY
        # generate key type from label
        for key_type in KeyType:
            if label.startswith(key_type.name):
                self.type = key_type
        # check if user set the key type
        for key_type in KeyType:
            if modifier_value == key_type.name:
                self.type = key_type


def generate_matrix(path, con_pin):
    file = open(path)
    content = file.readlines()

    keys = []

    # result list for input pins
    input_pins = []
    # result list for output pins
    output_pins = []

    content = [x.strip() for x in content]

    # read in file and store values line by line into key objects
    for line in content:
        line = line.split()
        if len(line) >= 3:
            keys.append(Key(line[0], line[1], int(line[-1]), int(line[-2])))
    # initialize matrix creator by finding common pins of control key
    temporary = [keys[0].pin1, keys[1].pin1, keys[0].pin2, keys[1].pin2]
    # determine if there is a common pin
    for pin in temporary:
        if temporary.count(pin) == 2:
            output_pins.append(pin)

    # if no common pin found ask user for initial input
    if not output_pins:
        output_pins.append(int(input("NO common pin found for CTRL key. Please enter an output pin: ")))

    print("initial output pin: {}".format(output_pins[0]))
    # iterate until no new output pins or input pins get found
    found = True
    while found:
        found = False
        for key in keys:
            # if not already assigned
            if not key.is_assigned:
                # set partner pin to the opposite array e.g. pin1 output pin -> pin2 input pin
                if key.pin1 in output_pins:
                    input_pins.append(key.pin2)
                    key.is_assigned = True
                    found = True
                elif key.pin1 in input_pins:
                    output_pins.append(key.pin2)
                    key.is_assigned = True
                    found = True
                elif key.pin2 in output_pins:
                    input_pins.append(key.pin1)
                    key.is_assigned = True
                    found = True
                elif key.pin2 in input_pins:
                    output_pins.append(key.pin1)
                    key.is_assigned = True
                    found = True

    input_pins = list(set(input_pins))
    output_pins = list(set(output_pins))
    input_pins.sort()
    output_pins.sort()
    # Output results
    print(separator + "Results:\n" + separator)
    # print FPC pins
    print("FPC PINS:")
    print("\n" + str(len(input_pins)) + " input pins:")
    print(input_pins)
    print("\n" + str(len(output_pins)) + " output pins:")
    print(output_pins)
    print(separator + "TEENSY PINS (these have to be copied to the Teensy code):")
    # translate FPC pins to TEENSY pins using the con_pin array
    print("\n" + str(len(input_pins)) + " input pins:")
    print(list(map(lambda x: con_pin[x - 1], input_pins)))
    print("\n" + str(len(output_pins)) + " output pins:")
    print(list(map(lambda x: con_pin[x - 1], output_pins)))
    print(separator + "Copy these matrices into the Teensy USB Controller code\n")
    # create the different matrices for every key type
    for key_type in KeyType:
        matrix = separator + key_type.name + "\n" + separator + "{\n"
        # rows
        for output_pin in output_pins:
            key_row = ""
            # columns
            for input_pin in input_pins:
                # default key value
                key_label = "0"
                if key_type == KeyType.ONE:
                    key_label = "1"
                # search for key that matches with row and column pin
                for key in keys:
                    if (((key.pin1 == input_pin) | (key.pin2 == input_pin)) & (
                            (key.pin1 == output_pin) | (key.pin2 == output_pin))):
                        if key.type == key_type:
                            key_label = key.label
                key_row = key_row + key_label + ","
            matrix = matrix + "{" + key_row[:-1] + "},\n"
        matrix = matrix[:-1] + "\n}"
        print(matrix)
    print(separator + "Finished")


if __name__ == "__main__":
    default_file_names = ["Keyboard_with_number_pad.txt", "Keyboard_without_number_pad.txt"]
    file_suggestions = []

    for file_name in os.listdir():
        if file_name.endswith('.txt'):
            if file_name in default_file_names:
                file_suggestions.insert(0, file_name)
            else:
                file_suggestions.append(file_name)
    max_length = max(len(file_name) for file_name in file_suggestions)
    print('{:^6s} {:^{max_length}s}'.format('index', 'file name', max_length=max_length))
    for i, suggestion in enumerate(file_suggestions):
        print('{:^6s} {:^{max_length}s}'.format(str(i + 1), suggestion, max_length=max_length))
    while True:
        user_input = input(
            separator + 'Enter the index number of the *.txt file you want.\nOR: enter your own filepath:\n')
        if os.path.exists(user_input):
            path = user_input
            break
        elif user_input.isdigit():
            path = file_suggestions[int(user_input) - 1]
            break
        else:
            print('Couldn\'t handle input. Please try again.')

    print(separator)
    print('{:^6s} {:^12s}'.format('index', 'teensy device'))
    for i, teensy_device in enumerate(teensy_devices):
        print('{:^6s} {:^12s}'.format(str(i + 1), teensy_device[0]))

    while True:
        user_input = input(
            separator + 'The pin layout is different for each teensy version.\n'
                        'Please enter the index number of your teensy version:\n')
        # TODO custom pin layout
        if user_input.isdigit():
            con_pin = teensy_devices[int(user_input) - 1][1]
            break
        else:
            print('Couldn\'t handle input. Please try again.')
    while True:
        generate_matrix(path, con_pin)
        user_input_repeat = input('Do you want to rerun with {} and teensy {} (y/n) as input?'.format(path, teensy_devices[
            int(user_input) - 1][0]))
        if user_input_repeat.lower() in ['n', 'no']:
            break
