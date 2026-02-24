import argparse
import sys
import time
from colorama import Fore, Style

parser = argparse.ArgumentParser(description="Brainfuck Interpreter", epilog="Created by Wren!")
parser.add_argument("filename", help="File to interpret", type=argparse.FileType("r"))
parser.add_argument("-e", "--extra", help="Disable extra commands", action="store_false")
parser.add_argument("-i", "--infinity", help="Go infinitely high or low: 0=none, 1=high, 2=low, 3=both (default: 0)", type=int, default=0, choices=[0, 1, 2, 3])
parser.add_argument("-v", "--visual", help="Visualize the program. -(-d)elay recommended", action="store_true")
parser.add_argument("-d", "--delay", help="Place a delay between each instruction. (default: 0)", type=float, default=0)
args = parser.parse_args()
extra = args.extra

if args.infinity == 3:
    infinity = [True, True]
elif args.infinity == 2:
    infinity = [False, True]
elif args.infinity == 1:
    infinity = [True, False]
else:
    infinity = [False, False]

code = args.filename.read()

stack = [0]
pointer = 0
curOutput = ""

def build_jump_table(code: str):
    stack = []
    table = {}
    for i, ch in enumerate(code):
        if ch == "[":
            stack.append(i)
        elif ch == "]":
            if not stack:
                raise RuntimeError(f"Unmatched ] at {i}")
            start = stack.pop()
            table[start] = i
            table[i] = start
    if stack:
        raise RuntimeError(f"Unmatched [ at {stack[-1]}")
    return table

JUMPS = build_jump_table(code)

def _add():
    stack[pointer] += 1
    if stack[pointer] > 255 and not infinity[0]:
        stack[pointer] = 0

def _sub():
    stack[pointer] -= 1
    if stack[pointer] < 0 and not infinity[1]:
        stack[pointer] = 255

def _right():
    global pointer
    pointer += 1
    if pointer == len(stack):
        stack.append(0)

def _left():
    global pointer
    pointer -= 1
    if pointer < 0:
        exit("RANGE ERROR: POINTER CANNOT GO BELOW 0")

def _out(num=False):
    if not args.visual:
        if num:
            print(stack[pointer], end=" ")
        else:
            print(chr(stack[pointer]), end="")
    else:
        global curOutput
        if num:
            curOutput += str(stack[pointer])+" "
        else:
            curOutput += chr(stack[pointer])
    sys.stdout.flush()
    

def _inp(num=False):
    temp = input()
    if num:
        temp = int(temp)
    else:
        temp = ord(temp[0])
    stack[pointer] = temp

def _visualize(eye):
    aO = ""
    print("\033[H\033[J", end="")
    for a, i in enumerate(stack):
        aO += f'[{">" if pointer==a else " "}{i:03d}{"<" if pointer==a else " "}]'
        if (not a%10) and a>0:
            aO += '\n'
    aO += '\n'
    for i, char in enumerate(code):
        if eye==i:
            aO += f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{char}{Style.RESET_ALL}"
        else:
            aO += f"{char}"
    aO += '\n'
    aO += curOutput
    print(aO)
    sys.stdout.flush()
    

def read(lines):
    eye = 0
    while eye < len(lines):
        ch = lines[eye]
        if ch == "\\":
            eye += 2
            continue
        elif ch == "+":
            _add()
        elif ch == "-":
            _sub()
        elif ch == "<":
            _left()
        elif ch == ">":
            _right()
        elif ch == "[":
            if stack[pointer] == 0:
                eye = JUMPS[eye]
        elif ch == "]":
            if stack[pointer] != 0:
                eye = JUMPS[eye]
        elif ch == ".":
            _out()
        elif ch == ",":
            _inp()
        elif ch == "#" and extra:
            print(pointer, stack, eye,
                  lines[eye - 1:eye + 2])
        elif ch == "!" and extra:
            _out(True)
        elif ch == "?" and extra:
            _inp(True)
        elif ch == "_" and extra:
            time.sleep(.1)
        eye += 1
        if args.visual:
            _visualize(eye)
        time.sleep(args.delay)

st_time = time.time()
read(code)
print(f"\nFinished in {time.time()-st_time:.5f} seconds")