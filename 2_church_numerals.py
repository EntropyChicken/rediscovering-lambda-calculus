"""
let's see what i remember about church numerals
an integer n takes in a function and a subject, then repeatedly applies the function to the subject n times
the function 'f' should be unary, taking in and giving out the same type of thing
"""

# ZERO: apply f 0 times, but still take f as an argument because numerals take 2 arguments
ZERO = lambda f: lambda x: x 
ONE = lambda f: lambda x: f(x)
TWO = lambda f: lambda x: f(f(x))
THREE = lambda f: lambda x: f(f(f(x)))

"""
but now it's less obvious how to increment...?
of course the benefit is that i can actually just use the numeral to apply some function that many times
but wait, can't i just do this? i know that inc(numeral) is a numeral, so it must take in argments f and x 
so it starts with inc = lambda n: lambda f: lambda x:
"""

# this takes three arguments, but you can give it one numeral to get one numeral
INC = lambda n: lambda f: lambda x: n(f)(f(x)) # i wonder if n(f)(f(x)) is any different from f(n(f)(x))
# in terms of execution speed, or even structurally (different outputs...!?)

FOUR = INC(THREE)
FIVE = INC(FOUR)
assert THREE(lambda x: x+1)(0) == 3
assert FOUR(lambda x: x+1)(0) == 4
assert FIVE(lambda x: x+1)(0) == 5

# boolean algebra
TRUE = lambda a: lambda b: a
FALSE = lambda a: lambda b: b
AND = lambda bool_1: lambda bool_2: bool_1(bool_2(TRUE)(FALSE))(FALSE)
OR = lambda bool_1: lambda bool_2: bool_1(TRUE)(bool_2(TRUE)(FALSE))
NOT = lambda bool: bool(FALSE)(TRUE)

# returns true if zero, false if not
IS_ZERO = lambda num: num(lambda any_bool: FALSE)(TRUE)

"""
hmmm it'd be nice to have DEC(a), EQUAL(a)(b), or ADD(a)(b)
i can use python recursion to make ADD using DEC and EQUAL. ideally i wouldn't use python recursion
i feel like i should be able to implement DEC if i had EQUAL, and vice versa
but all of these ideas would need python recursion, which is not actual lambda calculus
oh wait, can't you multiply numeral by just calling them on each other...? or something...
actually, you can make them repeat inc in order to ADD!
that's another reason why church numerals are so nice: it's easy to use the numeral itself productively
"""

SIX = FIVE(INC)(ONE)
assert SIX(lambda x: x+1)(0) == 6

ADD = lambda num_1: lambda num_2: num_1(INC)(num_2)

SEVEN = ADD(FOUR)(THREE)
assert SEVEN(lambda x: x+1)(0) == 7
assert ADD(THREE)(FOUR)(lambda x: x+1)(0) == 7

MULTIPLY = lambda num_1: lambda num_2: num_1(ADD(num_2))(ZERO)
assert MULTIPLY(FOUR)(FIVE)(lambda x: x+1)(0) == 20
assert MULTIPLY(ZERO)(SEVEN)(lambda x: x+1)(0) == 0
assert MULTIPLY(SIX)(ZERO)(lambda x: x+1)(0) == 0

POWER = lambda base_num: lambda exponent_num: exponent_num(MULTIPLY(base_num))(ONE)
assert POWER(THREE)(FIVE)(lambda x: x+1)(0) == 243
assert POWER(ZERO)(SEVEN)(lambda x: x+1)(0) == 0
assert POWER(SIX)(ZERO)(lambda x: x+1)(0) == 1

"""
i would instinctively implement subtraction as adding a negation, but negatives don't make structural sense
there's iterative ways to start from zero and count up to near a numeral
in CS61A DeNero said that iteration is a special case of recursion
maybe there's a way to "do iterative stuff" in lambda calculus?
like maintain multiple variables while running a for loop
but really, having 'DEC' would solve a lot of problems right now, like making subtraction

i know there's an important thing called a y combinator, not to be confused with the startup accelerator
but i forget the details. i think it's for doing recursion

crazy idea: define "dummy -1" as a number that gives you zero when you increment it...?
then DEC can just be like ADD(dummy -1)(num)
but you can't really reverse-engineer any of the functions involved to actually make dummy -1

"""

IS_EVEN = lambda num: num(NOT)(TRUE)
assert IS_EVEN(SIX)(True)(False)
assert not IS_EVEN(FIVE)(True)(False)

# implementation of DEC that depends on EQUALS:
# DEC = lambda num: num(lambda subnum: EQUALS(INC(subnum),num)(subnum)(INC(subnum)))(ZERO)

"""
ok here's an idea:
start at some detectable initial value that is structurally like a number but functionally unique
detect when it is the initial value (as opposed to some natural number), then set it to zero
else incremenet it
"""

IDENTITY = lambda x: x

 # kind of a pseudo-numeral thing. it's of the "numeral" type but is distinct from all numeras
FORCE_TRUE = lambda f: lambda x: TRUE
IS_FORCE_TRUE = lambda numlike: numlike(IDENTITY)(FALSE)
assert not IS_FORCE_TRUE(ONE)(True)(False)
assert IS_FORCE_TRUE(FORCE_TRUE)(True)(False)

RAW_DEC = lambda num: num(lambda subnum: IS_FORCE_TRUE(subnum)(ZERO)(INC(subnum)))(FORCE_TRUE)

# YAY the implementation of raw decrement genuinely took me a couple hours. now we can do subtract and stuff

# DEC should be guarded: it can only go down to ZERO then get stuck
DEC = lambda num: IS_ZERO(num)(ZERO)(RAW_DEC(num))
assert DEC(SIX)(lambda x: x+1)(0) == 5

SUBTRACT = lambda num_1: lambda num_2: num_2(DEC)(num_1)

LESS_THAN_OR_EQUALS = lambda num_1: lambda num_2: IS_ZERO(SUBTRACT(num_1)(num_2))
GREATER_THAN_OR_EQUALS = lambda num_1: lambda num_2: LESS_THAN_OR_EQUALS(num_2)(num_1)
EQUALS = lambda num_1: lambda num_2: AND(LESS_THAN_OR_EQUALS(num_1)(num_2))(GREATER_THAN_OR_EQUALS(num_1)(num_2))
LESS_THAN = lambda num_1: lambda num_2: AND(LESS_THAN_OR_EQUALS(num_1)(num_2))(NOT(GREATER_THAN_OR_EQUALS(num_1)(num_2)))
GREATER_THAN = lambda num_1: lambda num_2: LESS_THAN(num_2)(num_1)

assert EQUALS(ONE)(ONE)(True)(False)
assert EQUALS(ZERO)(ZERO)(True)(False)
assert EQUALS(TWO)(TWO)(True)(False)
assert not EQUALS(ONE)(ZERO)(True)(False)
assert not EQUALS(ZERO)(TWO)(True)(False)
assert not EQUALS(ZERO)(ONE)(True)(False)
assert LESS_THAN_OR_EQUALS(SIX)(SEVEN)(True)(False)
assert LESS_THAN_OR_EQUALS(ONE)(SEVEN)(True)(False)
assert LESS_THAN_OR_EQUALS(FOUR)(FOUR)(True)(False)
assert LESS_THAN_OR_EQUALS(ZERO)(ZERO)(True)(False)
assert not LESS_THAN_OR_EQUALS(SIX)(FIVE)(True)(False)
assert not LESS_THAN_OR_EQUALS(ONE)(ZERO)(True)(False)
assert LESS_THAN(SIX)(SEVEN)(True)(False)
assert LESS_THAN(ONE)(SEVEN)(True)(False)
assert not LESS_THAN(FOUR)(FOUR)(True)(False)
assert not LESS_THAN(ZERO)(ZERO)(True)(False)
assert not LESS_THAN(SIX)(FIVE)(True)(False)
assert not LESS_THAN(ONE)(ZERO)(True)(False)
assert not GREATER_THAN_OR_EQUALS(SIX)(SEVEN)(True)(False)
assert GREATER_THAN_OR_EQUALS(ZERO)(ZERO)(True)(False)
assert GREATER_THAN_OR_EQUALS(ONE)(ZERO)(True)(False)
assert not GREATER_THAN(SIX)(SEVEN)(True)(False)
assert not GREATER_THAN(ZERO)(ZERO)(True)(False)
assert GREATER_THAN(ONE)(ZERO)(True)(False)
print("PASSED!")