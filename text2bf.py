import math

# While this is the most intuitive way to do this, it is by no means the "best".
# It creates a seperate cell for each letter instead of modifying existing cells.

text_to_translate:str = "Hello, World!"

# This computes the compression of a number. This concept belongs partially to G4G
def min_factor_sum(n: int) -> tuple[int, tuple[int, int, int]]:
    best = float("inf") # "Anything is better than this"
    best_solution = (0, 0, 0)
    # We only search up to floor(2*sqrt(n)) because (a, b) just reverses after sqrt(n)
    # The +2 is due to range being end-exclusive
    # Our best pairs will be closest to sqrt(n)*2
    for a in range(1, int(2 * math.sqrt(n)) + 2):
        # Check closest product above and below n (remainders may be negative)
        b_floor = n // a 
        b_ceil = b_floor + 1
        for b in (b_floor, b_ceil):
            if b <= 0: # Zero cases are useless
                continue
            r = (n - a * b) # Get our remainder
            cost = a + b + abs(r) # Check our cost
            if cost < best:
                best = cost
                best_solution = (int(a), int(b), int(r))
    return int(best), best_solution

# This computes if it is "worth it" to compress a number
# It should always be worth it because we really shouldn't see small numbers in ASCII codes but who knows :P
# For example, the letter `a` (dec 97) should be written as >++++++++[-<++++++++++++>]+ as it is more efficient than just the + operator 97 times
def should_compress(n: int):
    # We add 7 for the requirements of a loop: brackets and pointer modification
    return n+7>=min_factor_sum(n)[0]


# First, just represent each unique character in the string in its most basic BF form

lookupTable = {}
pointer=0
basic_text = ""
for char in text_to_translate:
    if char in lookupTable.keys():
        basic_text+=("<"*(pointer-lookupTable[char]))+"."+(">"*(pointer-lookupTable[char]))+'\n'
    else:
        basic_text+=("+"*ord(char))+"\n.>\n"
        lookupTable[char]=pointer
        pointer+=1

# Next, try to simplify the file with loops. This is a function so we can run it again.
def compressMySins(basic:str):
    rep = ""
    for line in basic.split('\n'):
        # If the line isn't worth compressing just skip it
        if (not line.startswith('+')) or (not should_compress(len(line))):
            rep+=line
            # print(min_factor_sum(len(line)), len(line)+7)
        else:
            min_sum = min_factor_sum(len(line))[1]
            # All this next statement boils down to is actually making the loop. Remember: remainders may be negative!
            rep+=f">{'+'*min_sum[0]}[-<{'+'*min_sum[1]}>]<{('+'*min_sum[2]) if (min_sum[2]>0) else ('-'*abs(min_sum[2]))}"
        rep+='\n'
    return rep[:-1] # No need for that last newline

step2 = compressMySins(basic_text)

# Last, we just check to make sure we didn't overlook anything
while len(step2)>len(compressMySins(step2)):
    step2 = compressMySins(basic_text)

final_text = step2

with open(input(">")+'.bf', 'w') as file:
    file.write(final_text)