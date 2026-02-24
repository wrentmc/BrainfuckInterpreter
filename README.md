# BrainfuckInterpreter
My interpretation of a [brainfuck](https://en.wikipedia.org/wiki/Brainfuck) interpreter
# Usage
* Run `main.py` with arguments (underline indicates shorthand):
  * \<filename\> (required): File to interpret
  * <ins>e</ins>xtra: Disable extra commands (extra commands are enabled by default)
  * <ins>i</ins>nfinity: Allow numbers to go infinitely high or low: 0=none, 1=high, 2=low, 3=both (default: 0)
    * By default, numbers wrap around from 255<->0

# Text2BF
`text2bf.py` is a primitive program to create a BF file to print something. In the file, `text_to_translate` can be changed arbitrarily. The desired filename should be passed into the program via STDIN.
# Brainfuck guide
Brainfuck is an esoteric language that has very few characters. In most interpreters, it is eight-bit with 2^16 stacked cells.
The default commands are:
Symbol | Usage
---|---
| + | Increment cell
| - | Decrement cell
| < | Move pointer left
| > | Move pointer right
| [ | Begin loop
| ] | End loop (break if currently selected cell is 0)
| . | Output cell as ASCII
| , | Take ASCII input as integer

I have taken it upon myself to add more characters:

Symbol | Usage
---|---
| # | Output pointer, stack, eye (file input pointer), surrounding instructions, and current loops (this is mostly for debug)
| ! | Output cell as integer
| ? | Take integer input
| _ | Delay by 100ms
