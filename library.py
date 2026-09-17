TRUE = lambda a: lambda b: a
FALSE = lambda a: lambda b: b
AND = lambda bool_1: lambda bool_2: bool_1(bool_2(TRUE)(FALSE))(FALSE)
OR = lambda bool_1: lambda bool_2: bool_1(TRUE)(bool_2(TRUE)(FALSE))
NOT = lambda bool: bool(FALSE)(TRUE)
IDENTITY = lambda x: x
NONE = IDENTITY
META = lambda x: x(x)
INC = lambda n: lambda f: lambda x: n(f)(f(x))
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
IS_ZERO = lambda num: num(lambda any_bool: FALSE)(TRUE)
ADD = lambda num_1: lambda num_2: num_1(INC)(num_2)
MULTIPLY = lambda num_1: lambda num_2: num_1(ADD(num_2))(ZERO)
POWER = lambda base_num: lambda exponent_num: exponent_num(MULTIPLY(base_num))(ONE)
IS_EVEN = lambda num: num(NOT)(TRUE)
NAN = lambda f: lambda x: FALSE
IS_NUMERAL = lambda numlike: numlike(IDENTITY)(TRUE)
DEC = lambda num: IS_ZERO(num)(ZERO)(num(lambda subnum: IS_NUMERAL(subnum)(INC(subnum))(ZERO))(NAN))
SUBTRACT = lambda num_1: lambda num_2: num_2(DEC)(num_1)
LESS_THAN_OR_EQUALS = lambda num_1: lambda num_2: IS_ZERO(SUBTRACT(num_1)(num_2))
GREATER_THAN_OR_EQUALS = lambda num_1: lambda num_2: LESS_THAN_OR_EQUALS(num_2)(num_1)
EQUALS = lambda num_1: lambda num_2: AND(LESS_THAN_OR_EQUALS(num_1)(num_2))(GREATER_THAN_OR_EQUALS(num_1)(num_2))
LESS_THAN = lambda num_1: lambda num_2: AND(LESS_THAN_OR_EQUALS(num_1)(num_2))(NOT(GREATER_THAN_OR_EQUALS(num_1)(num_2)))
GREATER_THAN = lambda num_1: lambda num_2: LESS_THAN(num_2)(num_1)
MAKE_NUM_BOOL_PAIR = lambda num: lambda bool: lambda extraction_index: IS_ZERO(extraction_index)(num)(bool)
HALF = lambda num: num(lambda num_bool_pair: num_bool_pair(ONE)(MAKE_NUM_BOOL_PAIR(INC(num_bool_pair(ZERO)))(FALSE))(MAKE_NUM_BOOL_PAIR(num_bool_pair(ZERO))(TRUE)))(MAKE_NUM_BOOL_PAIR(ZERO)(FALSE))(ZERO)
assert HALF(ZERO)(lambda x: x+1)(0) == 0
assert HALF(ONE)(lambda x: x+1)(0) == 0
assert HALF(TWO)(lambda x: x+1)(0) == 1
assert HALF(THREE)(lambda x: x+1)(0) == 1
assert HALF(FOUR)(lambda x: x+1)(0) == 2
assert HALF(FIVE)(lambda x: x+1)(0) == 2

Z_COMBINATOR = (lambda x: x(x))(lambda me: lambda essence: essence(lambda arg_1: me(me)(essence)(arg_1)))

FACTORIAL = Z_COMBINATOR(lambda me:
    lambda num:
        IS_ZERO(num)
        (lambda _: ONE)
        (lambda _: MULTIPLY(num)(me(DEC(num))))
        (NONE)
)
assert FACTORIAL(ZERO)(lambda x: x+1)(0) == 1
assert FACTORIAL(ONE)(lambda x: x+1)(0) == 1
assert FACTORIAL(FOUR)(lambda x: x+1)(0) == 24
assert FACTORIAL(FIVE)(lambda x: x+1)(0) == 120
assert FACTORIAL(SIX)(lambda x: x+1)(0) == 720

DIVIDE = Z_COMBINATOR(lambda me:
    lambda num_1: lambda num_2:
        GREATER_THAN_OR_EQUALS(num_1)(num_2)
        (lambda _: INC(me(SUBTRACT(num_1)(num_2))(num_2)))
        (lambda _: ZERO)
        (NONE)
)
assert DIVIDE(ZERO)(ONE)(lambda x: x+1)(0) == 0
assert DIVIDE(ZERO)(TEN)(lambda x: x+1)(0) == 0
assert DIVIDE(ONE)(ONE)(lambda x: x+1)(0) == 1
assert DIVIDE(SIX)(SEVEN)(lambda x: x+1)(0) == 0
assert DIVIDE(SEVEN)(SIX)(lambda x: x+1)(0) == 1
assert DIVIDE(ADD(TEN)(TEN))(ONE)(lambda x: x+1)(0) == 20
assert DIVIDE(ADD(TEN)(TEN))(FIVE)(lambda x: x+1)(0) == 4
assert DIVIDE(ADD(TEN)(TEN))(THREE)(lambda x: x+1)(0) == 6
assert DIVIDE(ADD(TEN)(TEN))(ADD(TEN)(TEN))(lambda x: x+1)(0) == 1

MODULO = Z_COMBINATOR(lambda me:
    lambda num_1: lambda num_2:
        GREATER_THAN_OR_EQUALS(num_1)(num_2)
        (lambda _: me(SUBTRACT(num_1)(num_2))(num_2))
        (lambda _: num_1)
        (NONE)
)
assert MODULO(ZERO)(ONE)(lambda x: x+1)(0) == 0
assert MODULO(ZERO)(TEN)(lambda x: x+1)(0) == 0
assert MODULO(ONE)(ONE)(lambda x: x+1)(0) == 0
assert MODULO(SIX)(SEVEN)(lambda x: x+1)(0) == 6
assert MODULO(SEVEN)(SIX)(lambda x: x+1)(0) == 1
assert MODULO(ADD(TEN)(TEN))(ONE)(lambda x: x+1)(0) == 0
assert MODULO(ADD(TEN)(TEN))(FIVE)(lambda x: x+1)(0) == 0
assert MODULO(ADD(TEN)(TEN))(THREE)(lambda x: x+1)(0) == 2
assert MODULO(ADD(TEN)(TEN))(ADD(TEN)(TEN))(lambda x: x+1)(0) == 0

FIBONACCI = Z_COMBINATOR(lambda me:
    lambda num:
        LESS_THAN_OR_EQUALS(num)(ONE)
        (lambda _: num)
        (lambda _:
            ADD
            (me(DEC(num)))
            (me(DEC(DEC(num))))
        )
        (NONE)
)
assert FIBONACCI(ZERO)(lambda x: x+1)(0) == 0
assert FIBONACCI(ONE)(lambda x: x+1)(0) == 1
assert FIBONACCI(TWO)(lambda x: x+1)(0) == 1
assert FIBONACCI(THREE)(lambda x: x+1)(0) == 2
assert FIBONACCI(FOUR)(lambda x: x+1)(0) == 3
assert FIBONACCI(FIVE)(lambda x: x+1)(0) == 5
assert FIBONACCI(ADD(TEN)(SIX))(lambda x: x+1)(0) == 987

PARTITION_DP = Z_COMBINATOR(lambda me:
    lambda whole: lambda partition_max:
        IS_ZERO(whole)
        (lambda _: ONE)
        (
            IS_ZERO(partition_max)
            (lambda _: ZERO)
            (lambda _:
                ADD
                (
                    LESS_THAN_OR_EQUALS(partition_max)(whole)
                    (lambda _: me(SUBTRACT(whole)(partition_max))(partition_max))
                    (lambda _: ZERO)
                    (NONE)
                )
                (me(whole)(DEC(partition_max)))
            )
        )
        (NONE)
)
assert PARTITION_DP(ZERO)(ZERO)(lambda x: x+1)(0) == 1
assert PARTITION_DP(TWO)(ZERO)(lambda x: x+1)(0) == 0
assert PARTITION_DP(TEN)(ZERO)(lambda x: x+1)(0) == 0
assert PARTITION_DP(ZERO)(ONE)(lambda x: x+1)(0) == 1
assert PARTITION_DP(ZERO)(NINE)(lambda x: x+1)(0) == 1
assert PARTITION_DP(SIX)(FOUR)(lambda x: x+1)(0) == 9
assert PARTITION_DP(TEN)(TEN)(lambda x: x+1)(0) == 42
assert PARTITION_DP(TEN)(NINE)(lambda x: x+1)(0) == 41
assert PARTITION_DP(TEN)(THREE)(lambda x: x+1)(0) == 14