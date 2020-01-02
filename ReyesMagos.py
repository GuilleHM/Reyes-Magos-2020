#!/usr/bin/env python3

"""
This script takes a predefined static "ASCII Art" file (ReyesMagos.txt) that represents how
Three Wise Men followed the Star of Bethlehem across the desert and uses asynchronous
cooperative multitasking for applying dynamism to the resulting image via blinking lights emulation.
To that purpose, a special "meaning" has been stablished for some symbols included in the file.
"""

# Needed packages load
import asyncio
import random
import os

# Function for coloring each predefined symbol in the "ASCII Art" image
def colored_dot(color):
    # dic for choosing the color
    switcher = {
        'yellow': f'\033[93m\u25CF\033[0m',
        'red': f'\033[91m\u25CF\033[0m',
        'green': f'\033[92m\u25CF\033[0m',
        'blue': f'\033[94m\u25CF\033[0m'
    }
    # in "camels lights" case, lights colors will randomly change on each position
    if color == 'camel':
        return random.choice([f'\033[91m\u25CF\033[0m', f'\033[92m\u25CF\033[0m',
                              f'\033[93m\u25CF\033[0m', f'\033[94m\u25CF\033[0m'])
    # other "lights" will have always same color
    else:
        return switcher.get(color)

# Function for switching on/off each light
# Uses async with / await for cooperative multitasking
async def lights(color, indexes):
    off = True
    while True:
        for idx in indexes:
            template[idx] = colored_dot(color) if off else ' '
        async with mutex:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(''.join(template))
        off = not off
        await asyncio.sleep(random.uniform(2, 5))

# Needed variables initialization
template = list(open('ReyesMagos.txt').read().rstrip())  # file content into a list
mutex = asyncio.Lock()  # lock for inter-tasks coordination
symbols = ['y', 'r', 'g', 'b', '^']  # symbols for denoting different color lights
symbols_positions = [[] for i in range(5)]  # list of list of positions for each symbol

# Symbols positions populated into respective lists
for i, c in enumerate(template):
    if c in symbols:
        symbols_positions[symbols.index(c)].append(i)
        template[i] = ''

# Entry point
async def main():
    # Initial screen cleaning
    os.system('cls' if os.name == 'nt' else 'clear')
    # A "light" function is launched for each symbol. They operate coordinately
    # getting so a final blinking effect.
    await asyncio.gather(
        lights('yellow', symbols_positions[0]),
        lights('red', symbols_positions[1]),
        lights('green', symbols_positions[2]),
        lights('blue', symbols_positions[3]),
        lights('camel', symbols_positions[4])
    )

if __name__ == '__main__':
    asyncio.run(main())
