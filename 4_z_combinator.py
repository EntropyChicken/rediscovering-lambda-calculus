"""
ok, alright, i'll try to make the actual y combinator which i've been told allows us to directly write
me(arg1)(arg2)... instead of make_me()(arg1)(arg2)... in the body of the essence function
"""

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
META = lambda x: x(x)
MAKE_NUM_BOOL_PAIR = lambda num: lambda bool: lambda extraction_index: IS_ZERO(extraction_index)(num)(bool)
HALF = lambda num: num(lambda num_bool_pair: num_bool_pair(ONE)(MAKE_NUM_BOOL_PAIR(INC(num_bool_pair(ZERO)))(FALSE))(MAKE_NUM_BOOL_PAIR(num_bool_pair(ZERO))(TRUE)))(MAKE_NUM_BOOL_PAIR(ZERO)(FALSE))(ZERO)



"""
Y_COMBINATOR must turn an essence function into a self-recursing function
that has to be able to take the 'actual' arguments of ESSENCE

usage: Y_COMBINATOR(ESSENCE)(arg1)(arg2)...
so the thing passed in ESSENCE's first argument slot must, itself, be Y_COMBINATOR(ESSENCE)

Y_COMBINATOR(ESSENCE)(arg1)(arg2)... -> ESSENCE(Y_COMBINATOR(ESSENCE))(arg1)(arg2)
but like, the inner 'Y_COMBINATOR(ESSENCE)' cannot evaluate itself and expand until it is called from ESSENCE

OKAY okay. after hints about how y combinator is used, i finally think i know the TRICK:
you force the overall Y(F) to wait for another argument before running
that way it doesn't run eagerly
except you can just catch and feed that argument once essence starts running
so this will only work for recursive functions that have at least one argument... which is all of them
"""

Y_COMBINATOR = META(lambda me: lambda essence: essence(lambda arg_1: me(me)(essence)(arg_1)))
PARTITION_DP = Y_COMBINATOR(
    lambda me: lambda whole: lambda partition_max:
        IS_ZERO(whole)
        (lambda: ONE)
        (
            IS_ZERO(partition_max)
            (lambda: ZERO)
            (lambda: ADD
                (
                    LESS_THAN_OR_EQUALS(partition_max)(whole)
                    (lambda: me(SUBTRACT(whole)(partition_max))(partition_max))
                    (lambda: ZERO)()
                )
                (
                    me(whole)(DEC(partition_max))
                )
            )
        )
        ()
)
assert PARTITION_DP(ZERO)(ZERO)(lambda x: x+1)(0) == 1
assert PARTITION_DP(ONE)(ZERO)(lambda x: x+1)(0) == 0
assert PARTITION_DP(TEN)(ZERO)(lambda x: x+1)(0) == 0
assert PARTITION_DP(ZERO)(ONE)(lambda x: x+1)(0) == 1
assert PARTITION_DP(ZERO)(TEN)(lambda x: x+1)(0) == 1
assert PARTITION_DP(SIX)(FOUR)(lambda x: x+1)(0) == 9
assert PARTITION_DP(TEN)(TEN)(lambda x: x+1)(0) == 42
assert PARTITION_DP(TEN)(NINE)(lambda x: x+1)(0) == 41
assert PARTITION_DP(TEN)(THREE)(lambda x: x+1)(0) == 14

"""
LETS GOOOO IT WORKED!!!!
okay so THIS is OFFICIALLY Y COMBINATOR (corretion: well, it's actually z combinator...)
(it took me a couple days and a couple hints about how y combinator is used)
the final trick is actually not that crazy
it's just using the first argument as the 'call' that makes the self-expansion part run
so instead of () you need (arg_1) and it just makes sure that the actual run remembers arg_1
really, it's just making use of the fact that functions are curried
(you would need to pack arguments to tuple and unpack back to arguments if they weren't curried)
it's a 'sneaky' sort of 'clever' rather than an 'elegant' sort of 'clever'
"""

Z_COMBINATOR = (lambda x: x(x))(lambda m: lambda e: e(lambda a: m(m)(e)(a)))