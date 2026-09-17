# the things i've made before
TRUE = lambda a: lambda b: a
FALSE = lambda a: lambda b: b
AND = lambda bool_1: lambda bool_2: bool_1(bool_2(TRUE)(FALSE))(FALSE)
OR = lambda bool_1: lambda bool_2: bool_1(TRUE)(bool_2(TRUE)(FALSE))
NOT = lambda bool: bool(FALSE)(TRUE)
IDENTITY = lambda x: x
INC = lambda n: lambda f: lambda x: n(f)(f(x))
IS_ZERO = lambda num: num(lambda any_bool: FALSE)(TRUE)
ZERO = lambda f: lambda x: x 
ONE = INC(ZERO)
TWO = INC(ONE)
THREE = INC(TWO)
FOUR = INC(THREE)
FIVE = INC(FOUR)
SIX = INC(FIVE)
SEVEN = INC(SIX)
EIGHT = INC(SEVEN)
NINE = INC(EIGHT)
TEN = INC(NINE)
ADD = lambda num_1: lambda num_2: num_1(INC)(num_2)
MULTIPLY = lambda num_1: lambda num_2: num_1(ADD(num_2))(ZERO)
POWER = lambda base_num: lambda exponent_num: exponent_num(MULTIPLY(base_num))(ONE)
IS_EVEN = lambda num: num(NOT)(TRUE)
FORCE_TRUE = lambda f: lambda x: TRUE
IS_FORCE_TRUE = lambda numlike: numlike(IDENTITY)(FALSE)
RAW_DEC = lambda num: num(lambda subnum: IS_FORCE_TRUE(subnum)(ZERO)(INC(subnum)))(FORCE_TRUE)
DEC = lambda num: IS_ZERO(num)(ZERO)(RAW_DEC(num))
SUBTRACT = lambda num_1: lambda num_2: num_2(DEC)(num_1)
LESS_THAN_OR_EQUALS = lambda num_1: lambda num_2: IS_ZERO(SUBTRACT(num_1)(num_2))
GREATER_THAN_OR_EQUALS = lambda num_1: lambda num_2: LESS_THAN_OR_EQUALS(num_2)(num_1)
EQUALS = lambda num_1: lambda num_2: AND(LESS_THAN_OR_EQUALS(num_1)(num_2))(GREATER_THAN_OR_EQUALS(num_1)(num_2))
LESS_THAN = lambda num_1: lambda num_2: AND(LESS_THAN_OR_EQUALS(num_1)(num_2))(NOT(GREATER_THAN_OR_EQUALS(num_1)(num_2)))
GREATER_THAN = lambda num_1: lambda num_2: LESS_THAN(num_2)(num_1)

"""
what do i know about y combinator?
i know that it lets us do recursion in lambda calculus
so it enables recursion without using the name of the function in its own body
it is a 'thing' so it is some sort of lambda
what do i guess about y combinator
it probably takes a function as an argument and makes it recursive, or something like that
surely the function has to call something to recurse
it can't just be the case that the function gets called infinitely many times
that would just be repetition. i'm sure y combinator can allow for tree recursion
so my guess is that we have to call some name inside our function, and this name must recurse
yeah, you can't just define a constant particular lambda expression to be called
because then it would do the same behavior regardless of depth. so it's an infinite loop...?
or maybe you can call the same lambda expression but it somehow has access to the things
in the outer call?
but first i will go with my original guess and assume that the function will be fed itself as an argument
therefore the function can just call the argument
and the job of the y combinator is to make sure the function is always fed its own argument...?

i'll first manually make a recursive function
it continually maintains versions of itself (from the original argument pass) so that it remembers what to do
"""

INFINITE_RECUR = lambda me: me(me)
# INFINITE_RECUR(INFINITE_RECUR) # hits recursion limit YAY

"""
but every call of INFINITE_RECUR(INFINITE_RECUR) had the same behavior
in order to stop at some point, i must make different behavior, perhaps by passing in an argument to track
how many times it has recursed
RECUR takes in itself and a numeral and outputs a boolean
RECUR = lambda me: lambda depth: LESS_THAN_OR_EQUALS(depth)(ZERO)(me(me)(INC(depth)))(TRUE)
print(RECUR(RECUR)(ONE)(8)(5))
"""

TOO_EAGER_RECUR = lambda me: lambda depth: LESS_THAN(depth)(FOUR)(me(me)(INC(depth)))(TRUE)
# assert TOO_EAGER_RECUR(TOO_EAGER_RECUR)(ZERO)(8)(5) == 8 # hits recursion limit... not what i hoped for

"""
i think this would work if it weren't for that fact that python eagerly evaluates arguments
reduction order matters
it's basically expanding out the "infinite recursiveness" lopo before it actually runs the code
somehow i have to make it not have the recursion in the argument itself?
wait, i've never tried calling a created lambda function in the middle of an expression
maybe that can help for this or for something else...?

i finally have an idea:
i won't make it choose between values, but choose between functions to be called immediately!
this is using the idea of calling a newly made lambda function in one breath
"""

NOT_EAGER_RECUR = lambda me: lambda depth: LESS_THAN(depth)(FOUR)(lambda: me(me)(INC(depth)))(lambda: TRUE)()
assert NOT_EAGER_RECUR(NOT_EAGER_RECUR)(ZERO)(8)(5) == 8 # NICE!! this actually finishes and works

# (itself, numeral)->(numeral).
FACTORIAL_RECUR = lambda me: lambda num: IS_ZERO(num)(lambda: ONE)(lambda: MULTIPLY(num)(me(me)(DEC(num))))()
assert FACTORIAL_RECUR(FACTORIAL_RECUR)(THREE)(lambda x: x+1)(0) == 6 # IT WORKS!!
assert FACTORIAL_RECUR(FACTORIAL_RECUR)(FIVE)(lambda x: x+1)(0) == 120
assert FACTORIAL_RECUR(FACTORIAL_RECUR)(ZERO)(lambda x: x+1)(0) == 1
assert FACTORIAL_RECUR(FACTORIAL_RECUR)(ONE)(lambda x: x+1)(0) == 1

"""
what if i want (numeral)->(numeral)
i'll roll out FACTORIAL = lambda num: FACTORIAL_RECUR(FACTORIAL_RECUR)(num)
but that's more concicsely FACTORIAL lambda num: (lambda x: x(x))(FACTORIAL_RECUR)(num)
"""

FACTORIAL = lambda num: (lambda x: x(x))(lambda me: lambda cur_num: IS_ZERO(cur_num)(lambda: ONE)(lambda: MULTIPLY(cur_num)(me(me)(DEC(cur_num))))())(num)
assert FACTORIAL(FOUR)(lambda x: x+1)(0) == 24
assert FACTORIAL(SIX)(lambda x: x+1)(0) == 720
# assert FACTORIAL(SEVEN)(lambda x: x+1)(0) == 5040 # too much recursion :( mostly from INC calls

"""
okay maybe FACTORIAL_RECUR is the "core essence" of factorial,
which describes its branching to base case vs. main case,
and specifies what its base case and main cases are,
and therefore needs a "me" argument to be able to indicate where/how it should call itself
my guess is that the y combinator is just something that turns a "core essence" object like FACTORIAL_RECUR
into a callable one like FACTORIAL
i'm curious about arity, though. is y combinator something only for a particular kind of recursive function,
of a particular arity and return type arity?
at least i can make something that turns FACTORIAL_RECUR into FACTORIAL,
generalizable to anything that should be a unary function with a fixed output and input type
"""

RECURSION_POLISHER = lambda func_recur: lambda num: (lambda x: x(x))(func_recur)(num)
# a better verison i discovered later on: RECURSION_POLISHER = lambda func_recur: func_recur(func_recur)
assert RECURSION_POLISHER(FACTORIAL_RECUR)(FOUR)(lambda x: x+1)(0) == 24
assert RECURSION_POLISHER(FACTORIAL_RECUR)(SIX)(lambda x: x+1)(0) == 720
assert RECURSION_POLISHER(FACTORIAL_RECUR)(ZERO)(lambda x: x+1)(0) == 1
assert RECURSION_POLISHER(FACTORIAL_RECUR)(ONE)(lambda x: x+1)(0) == 1

# FIBONACCI(ZERO) -> ZERO, FIBONACCI(ONE) -> ONE, FIBONACCI(TWO) -> ONE, ...
FIBONACCI = RECURSION_POLISHER(lambda me: lambda num: LESS_THAN_OR_EQUALS(num)(ONE)(lambda: num)(lambda: ADD(me(me)(DEC(num)))(me(me)(DEC(DEC(num)))))())
assert FIBONACCI(ZERO)(lambda x: x+1)(0) == 0
assert FIBONACCI(ONE)(lambda x: x+1)(0) == 1
assert FIBONACCI(TWO)(lambda x: x+1)(0) == 1
assert FIBONACCI(THREE)(lambda x: x+1)(0) == 2
assert FIBONACCI(FOUR)(lambda x: x+1)(0) == 3
assert FIBONACCI(FIVE)(lambda x: x+1)(0) == 5
# this is the furthest it can go before hitting recursion depth limit
assert FIBONACCI(ADD(TEN)(SIX))(lambda x: x+1)(0) == 987

"""
what recursive functions have a different arity than just (numeral)->(numeral)?
maybe a division operator
(numeral, numeral) -> (numeral)
"""

DIVIDE = RECURSION_POLISHER(lambda me: lambda num_1: lambda num_2: GREATER_THAN_OR_EQUALS(num_1)(num_2)(lambda: INC(me(me)(SUBTRACT(num_1)(num_2))(num_2)))(lambda: ZERO)())
assert DIVIDE(ZERO)(THREE)(lambda x: x+1)(0) == 0
assert DIVIDE(ONE)(THREE)(lambda x: x+1)(0) == 0
assert DIVIDE(TWO)(THREE)(lambda x: x+1)(0) == 0
assert DIVIDE(THREE)(THREE)(lambda x: x+1)(0) == 1
assert DIVIDE(FOUR)(THREE)(lambda x: x+1)(0) == 1
assert DIVIDE(FIVE)(THREE)(lambda x: x+1)(0) == 1
assert DIVIDE(SIX)(THREE)(lambda x: x+1)(0) == 2
assert DIVIDE(SEVEN)(THREE)(lambda x: x+1)(0) == 2
assert DIVIDE(TEN)(THREE)(lambda x: x+1)(0) == 3
assert DIVIDE(SEVEN)(EIGHT)(lambda x: x+1)(0) == 0
assert DIVIDE(TEN)(FIVE)(lambda x: x+1)(0) == 2

MODULO = RECURSION_POLISHER(lambda me: lambda num_1: lambda num_2: GREATER_THAN_OR_EQUALS(num_1)(num_2)(lambda: me(me)(SUBTRACT(num_1)(num_2))(num_2))(lambda: num_1)())
assert MODULO(ZERO)(THREE)(lambda x: x+1)(0) == 0
assert MODULO(ONE)(THREE)(lambda x: x+1)(0) == 1
assert MODULO(TWO)(THREE)(lambda x: x+1)(0) == 2
assert MODULO(THREE)(THREE)(lambda x: x+1)(0) == 0
assert MODULO(FOUR)(THREE)(lambda x: x+1)(0) == 1
assert MODULO(FIVE)(THREE)(lambda x: x+1)(0) == 2
assert MODULO(SIX)(THREE)(lambda x: x+1)(0) == 0
assert MODULO(SEVEN)(THREE)(lambda x: x+1)(0) == 1
assert MODULO(TEN)(THREE)(lambda x: x+1)(0) == 1
assert MODULO(SEVEN)(EIGHT)(lambda x: x+1)(0) == 7
assert MODULO(TEN)(FIVE)(lambda x: x+1)(0) == 0

"""
wait, that's crazy. RECURSION_POLISHER even works for (numeral, numeral) -> (numeral)
maybe it works for any arity. it probably does actually:

RECURSION_POLISHER = lambda func_recur: lambda num: (lambda x: x(x))(func_recur)(num)
is just the same as:
RECURSION_POLISHER = lambda func_recur: func_recur(func_recur)

so actually nevermind i don't think RECURSION_POLISHER is anything computationally meaningful
it's certainly not y combinator. i think.
well, i have achieved recursion without y combinator. idk what y combinator is, then
"""

# to make a quick halver, i'd like to store a number and pair together
# (so i can inc only half the time by toggling the bool part)
# a num bool pair is a thing where if you pass in zero as the argument, you get the number
# and if you pass in one as the argument, you get the bool
MAKE_NUM_BOOL_PAIR = lambda num: lambda bool: lambda extraction_index: IS_ZERO(extraction_index)(num)(bool)

HALF = lambda num: num(lambda num_bool_pair: num_bool_pair(ONE)(MAKE_NUM_BOOL_PAIR(INC(num_bool_pair(ZERO)))(FALSE))(MAKE_NUM_BOOL_PAIR(num_bool_pair(ZERO))(TRUE)))(MAKE_NUM_BOOL_PAIR(ZERO)(FALSE))(ZERO)
assert HALF(TWO)(lambda x: x+1)(0) == 1
assert HALF(THREE)(lambda x: x+1)(0) == 1
assert HALF(FOUR)(lambda x: x+1)(0) == 2
assert HALF(FIVE)(lambda x: x+1)(0) == 2
assert HALF(SIX)(lambda x: x+1)(0) == 3
assert HALF(SEVEN)(lambda x: x+1)(0) == 3

"""
ok an outside source said having a y combinator lets us make functions that
simply call an argument that represents themselves, like me() instead of me(me)()

well, then "me" somehow has to know about itself...?
maybe "me" is always made out of the y combinator and essence put together somehow
and the y combinator is some sort of super special function that can "recreate itself"
(or, the combination of the y combinator and some essence can recreate itself)

okay apparently the y combinator is such that Y(F) = F(Y(F))
but doesn't that imply that you call Y(F)(arg1)(arg2)...etc. to actually get functionality?
and so that becomes F(Y(F))(arg1)(arg2)...
okay the general idea is that Y(F)->F(Y(F))->F(F(Y(F)))->F(F(F(Y(F)))) so like,
if we imagine a theoretical unrolled U = F(F(F(F(F(F(F(F(F(...Y(F)...))))))))) with infinitely many Fs,
then U(arg1)(arg2)... is F(U)(arg1)(arg2)... which should do the "essence function" F
and recreate itself
but the reduction order of this recreation must not unroll too early (that'd be infinite recursion)
"""

PARTITION_DP_ESSENCE = lambda me: lambda whole: lambda partition_max: IS_ZERO(whole)(lambda: ONE)(IS_ZERO(partition_max)(lambda: ZERO)(lambda: ADD(LESS_THAN_OR_EQUALS(partition_max)(whole)(lambda: me()(SUBTRACT(whole)(partition_max))(partition_max))(lambda: ZERO)())(me()(whole)(DEC(partition_max)))))()

"""
Y_COMBINATOR = lambda essence: essence(lambda: Y_COMBINATOR(essence))
assert Y_COMBINATOR(PARTITION_DP_ESSENCE)(ZERO)(ZERO)(lambda x: x+1)(0) == 1
assert Y_COMBINATOR(PARTITION_DP_ESSENCE)(ONE)(ZERO)(lambda x: x+1)(0) == 0
assert Y_COMBINATOR(PARTITION_DP_ESSENCE)(TEN)(ZERO)(lambda x: x+1)(0) == 0
assert Y_COMBINATOR(PARTITION_DP_ESSENCE)(ZERO)(ONE)(lambda x: x+1)(0) == 1
assert Y_COMBINATOR(PARTITION_DP_ESSENCE)(ZERO)(TEN)(lambda x: x+1)(0) == 1
assert Y_COMBINATOR(PARTITION_DP_ESSENCE)(SIX)(FOUR)(lambda x: x+1)(0) == 9
1 1 1 1 1 1
1 1 1 1 2
1 1 2 2
2 2 2
1 1 1 3
1 2 3
3 3
1 1 4
2 4
that's 9 ways
so this works. we basically want to do this:
Y_COMBINATOR = lambda essence: essence(lambda: Y_COMBINATOR(essence))
except we must not use Y_COMBINATOR's name in its definition
it probably has to pass itself into itself as well
Y_COMBINATOR = lambda me: lambda essence: essence(lambda: me(essence))
Y_COMBINATOR(Y_COMBINATOR)(ESSENCE)

i'm trying to remember the old simple thing that recurs forever
THING = lambda x: x(x)
THING(THING)

THING = lambda me: lambda essence: essence(me(me)(essence))
THING(THING)(ESSENCE) becomes ESSENCE(THING(THING)(ESSENCE))
this looks pretty close
Y_COMBINATOR = THING(THING)
but we would have to return a nullary that can call Y(F) rather than Y(F) to prevent python eagerness
"""

DUPER = lambda me: lambda essence: essence(lambda: me(me)(essence))
# Y_COMBINATOR = DUPER(DUPER)
Y_COMBINATOR = (lambda x: x(x))(lambda me: lambda essence: essence(lambda: me(me)(essence)))
PARTITION_DP = Y_COMBINATOR(PARTITION_DP_ESSENCE)
assert PARTITION_DP(ZERO)(ZERO)(lambda x: x+1)(0) == 1
assert PARTITION_DP(ONE)(ZERO)(lambda x: x+1)(0) == 0
assert PARTITION_DP(TEN)(ZERO)(lambda x: x+1)(0) == 0
assert PARTITION_DP(ZERO)(ONE)(lambda x: x+1)(0) == 1
assert PARTITION_DP(ZERO)(TEN)(lambda x: x+1)(0) == 1
assert PARTITION_DP(SIX)(FOUR)(lambda x: x+1)(0) == 9

"""
yoooo it passed!!!!!
is this really it?
i think i actually made Y_COMBINATOR!
(except it has to return a nullary function in order to prevent python's eagerness)
otherwise it would be cool like this:
Y_COMBINATOR = (lambda x: x(x))(lambda me: lambda essence: essence(me(me)(essence)))
and in real lambda calculus you would use a lazy reduction order
that doesn't do me(me)(essence) first (infinite loop)

okay apparently this is an atypical variant of y combinator or of z combinator...?
but it works in python :D
"""

# note: nullary functions probably shouldn't be allowed, since this is supposed to be like untyped lambda calculus