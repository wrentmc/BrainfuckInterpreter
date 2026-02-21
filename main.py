import argparse
import sys
import time

parser = argparse.ArgumentParser(description="Brainfuck Interpreter", epilog="Created by Wren!")
parser.add_argument("filename", help="File to interpret", type=argparse.FileType("r"))
parser.add_argument("-e", "--extra", help="Disable extra commands", action="store_false")
parser.add_argument("-i", "--infinity", help="Go infinitely high or low: 0=none, 1=high, 2=low, 3=both (default: 0)", type=int, default=0, choices=[0, 1, 2, 3])
args = parser.parse_args()
filename = args.filename.name
extra = args.extra
if args.infinity == 3: #Infinity = [high, low]
    infinity = [True, True]
elif args.infinity == 2:
    infinity = [False, True]
elif args.infinity == 1:
    infinity = [True, False]
else:
    infinity = [False, False]
with open(filename, "r") as file:
    code = file.read()
stack = [0]
pointer = 0
loops = []

def _add():
    global stack
    stack[pointer] += 1
    if stack[pointer] > 255 and not infinity[0]:
        stack[pointer] = 0

def _sub():
    global stack
    stack[pointer] -= 1
    if stack[pointer] < 0 and not infinity[1]:
        stack[pointer] = 255

def _right():
    global pointer
    pointer+=1
    if pointer==len(stack):
        stack.append(0)

def _left():
    global pointer
    pointer-=1
    if pointer<0:
        exit("RANGE ERROR: POINTER CANNOT GO BELOW 0")

def _sloop(i):
    global loops
    loops.append(i)

def _eloop(i):
    global loops
    if len(loops) == 0:
        return i
    if stack[pointer] == 0:
        loops.pop()
        return i
    else:
        return loops[-1]

def _out(num=False):
    if num:
        print(stack[pointer], end=" ")
    else:
        print(chr(stack[pointer]), end="")
    sys.stdout.flush()

def _inp(num=False):
    global stack
    temp = input()
    if num:
        temp = int(temp)
    else:
        temp = ord(temp)[0]
    stack[pointer] = temp
   
def read(lines):
    eye = 0
    while eye < len(lines):
        if lines[eye-1 if eye > 0 else 0] == "\\":
            eye+=1
            continue
        if lines[eye] == "+":
            _add()
        elif lines[eye] == "-":
            _sub()
        elif lines[eye] == "<":
            _left()
        elif lines[eye] == ">":
            _right()
        elif lines[eye] == "[":
            _sloop(eye)
        elif lines[eye] == "]":
            eye = _eloop(eye)
        elif lines[eye] == ".":
            _out()
        elif lines[eye] == ",":
            _inp()
        elif lines[eye] == "#" and extra:
            print(pointer, stack, eye, lines[eye-1:eye+2], loops)
        elif lines[eye] == "!" and extra:
            _out(True)
        elif lines[eye] == "?" and extra:
            _inp(True)
        elif lines[eye] == "_" and extra:
            time.sleep(.1)
        eye+=1

read(code)