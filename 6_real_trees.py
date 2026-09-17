TRUE = lambda a: lambda b: a
FALSE = lambda a: lambda b: b
AND = lambda bool_1: lambda bool_2: bool_1(bool_2(TRUE)(FALSE))(FALSE)
OR = lambda bool_1: lambda bool_2: bool_1(TRUE)(bool_2(TRUE)(FALSE))
NOT = lambda bool: bool(FALSE)(TRUE)
IDENTITY = lambda x: x
NONE = lambda x: x # only use this dummy variable where its value does not matter. don't use it as an identity function
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
ELEVEN = INC(TEN)
TWELVE = INC(ELEVEN)
THIRTEEN = INC(TWELVE)
FOURTEEN = INC(THIRTEEN)
FIFTEEN = INC(FOURTEEN)
SIXTEEN = INC(FIFTEEN)
SEVENTEEN = INC(SIXTEEN)
EIGHTEEN = INC(SEVENTEEN)
NINETEEN = INC(EIGHTEEN)
TWENTY = INC(NINETEEN)
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
GREATER_THAN_OR_EQUALS = lambda num_1: lambda num_2: IS_ZERO(SUBTRACT(num_2)(num_1))
EQUALS = lambda num_1: lambda num_2: AND(LESS_THAN_OR_EQUALS(num_1)(num_2))(GREATER_THAN_OR_EQUALS(num_1)(num_2))
LESS_THAN = lambda num_1: lambda num_2: NOT(GREATER_THAN_OR_EQUALS(num_1)(num_2))
GREATER_THAN = lambda num_1: lambda num_2: NOT(LESS_THAN_OR_EQUALS(num_1)(num_2))

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

# counts number of partitions (order doesn't matter) that sum to whole, using pieces of size at most partition_max
DP_COUNT_PARTITION = Z_COMBINATOR(lambda me:
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
assert DP_COUNT_PARTITION(ZERO)(ZERO)(lambda x: x+1)(0) == 1
assert DP_COUNT_PARTITION(TWO)(ZERO)(lambda x: x+1)(0) == 0
assert DP_COUNT_PARTITION(TEN)(ZERO)(lambda x: x+1)(0) == 0
assert DP_COUNT_PARTITION(ZERO)(ONE)(lambda x: x+1)(0) == 1
assert DP_COUNT_PARTITION(ZERO)(NINE)(lambda x: x+1)(0) == 1
assert DP_COUNT_PARTITION(SIX)(FOUR)(lambda x: x+1)(0) == 9
assert DP_COUNT_PARTITION(TEN)(TEN)(lambda x: x+1)(0) == 42
assert DP_COUNT_PARTITION(TEN)(NINE)(lambda x: x+1)(0) == 41
assert DP_COUNT_PARTITION(TEN)(THREE)(lambda x: x+1)(0) == 14

MAKE_PAIR = lambda a: lambda b: lambda extraction_num: EQUALS(extraction_num)(ZERO)(a)(b)
HALF = lambda num: num(lambda num_bool_pair: num_bool_pair(ONE)(MAKE_PAIR(INC(num_bool_pair(ZERO)))(FALSE))(MAKE_PAIR(num_bool_pair(ZERO))(TRUE)))(MAKE_PAIR(ZERO)(FALSE))(ZERO)
assert HALF(ZERO)(lambda x: x+1)(0) == 0
assert HALF(ONE)(lambda x: x+1)(0) == 0
assert HALF(TWO)(lambda x: x+1)(0) == 1
assert HALF(THREE)(lambda x: x+1)(0) == 1
assert HALF(FOUR)(lambda x: x+1)(0) == 2
assert HALF(FIVE)(lambda x: x+1)(0) == 2

MAKE_TRIPLET = lambda a: lambda b: lambda c: lambda extraction_num: EQUALS(extraction_num)(ZERO)(a)(EQUALS(extraction_num)(ONE)(b)(c))
assert MAKE_TRIPLET(TEN)(NINE)(EIGHT)(ONE)(lambda x: x+1)(0) == 9
assert MAKE_TRIPLET(TEN)(NINE)(EIGHT)(TWO)(lambda x: x+1)(0) == 8

MAKE_QUADRUPLET = lambda a: lambda b: lambda c: lambda d: lambda extraction_num: EQUALS(extraction_num)(ZERO)(a)(EQUALS(extraction_num)(ONE)(b)(EQUALS(extraction_num)(TWO)(c)(d)))
assert MAKE_QUADRUPLET(TEN)(NINE)(EIGHT)(SEVEN)(ZERO)(lambda x: x+1)(0) == 10
assert MAKE_QUADRUPLET(TEN)(NINE)(EIGHT)(SEVEN)(ONE)(lambda x: x+1)(0) == 9
assert MAKE_QUADRUPLET(TEN)(NINE)(EIGHT)(SEVEN)(THREE)(lambda x: x+1)(0) == 7

MAKE_SINGLE = lambda a: lambda extraction_num: a

# a linked list is an implicit data structure made by nesting many triplets
# element zero of the triplet can be anyhting
# element one should be a boolean indicating whether there is another node
# element two may be another triplet in the linked list
my_linked_list = MAKE_TRIPLET(FIVE)(TRUE)(
    MAKE_TRIPLET(SEVEN)(TRUE)(
        MAKE_TRIPLET(TWO)(TRUE)(
            MAKE_TRIPLET(FOUR)(TRUE)(
                MAKE_TRIPLET(ONE)(TRUE)(
                    MAKE_TRIPLET(TEN)(TRUE)(
                        MAKE_TRIPLET(NINE)(FALSE)(NONE)
                    )
                )
            )
        )
    )
)
SUM = Z_COMBINATOR(lambda me:
    lambda linked_list:
        ADD
        (linked_list(ZERO))
        (
            linked_list(ONE)
            (lambda _: me(linked_list(TWO)))
            (lambda _: ZERO)
            (NONE)
        )
)
assert SUM(my_linked_list)(lambda x: x+1)(0) == 38
assert SUM(my_linked_list(TWO))(lambda x: x+1)(0) == 33
assert SUM(my_linked_list(TWO)(TWO))(lambda x: x+1)(0) == 26

MAKE_LINKED_LIST_STUB = lambda element: MAKE_TRIPLET(element)(FALSE)(NONE)
PUSH_FRONT = lambda element: lambda linked_list: MAKE_TRIPLET(element)(TRUE)(linked_list) # argument order to look left-to-right on screen
PUSH_BACK = Z_COMBINATOR(lambda me:
    lambda linked_list: lambda element:
        linked_list(ONE)
        (lambda _: PUSH_FRONT(linked_list(ZERO))(me(linked_list(TWO))(element)))
        (lambda _: PUSH_FRONT(linked_list(ZERO))(MAKE_LINKED_LIST_STUB(element)))
        (NONE)
)

nice_linked_list = PUSH_FRONT(THREE)(PUSH_FRONT(EIGHT)(PUSH_FRONT(FIVE)(PUSH_FRONT(FOUR)(MAKE_LINKED_LIST_STUB(SEVEN)))))
assert SUM(nice_linked_list)(lambda x: x+1)(0) == 27


GET_ITEM = Z_COMBINATOR(lambda me:
    lambda linked_list: lambda index:
        IS_ZERO(index)
        (lambda _: linked_list(ZERO))
        (lambda _: me(linked_list(TWO))(DEC(index)))
        (NONE)
)
assert GET_ITEM(my_linked_list)(ZERO)(lambda x: x+1)(0) == 5
assert GET_ITEM(nice_linked_list)(ONE)(lambda x: x+1)(0) == 8
assert GET_ITEM(my_linked_list)(SIX)(lambda x: x+1)(0) == 9
assert GET_ITEM(nice_linked_list)(FOUR)(lambda x: x+1)(0) == 7
assert GET_ITEM(PUSH_BACK(nice_linked_list)(TWO))(FIVE)(lambda x: x+1)(0) == 2

SET_ITEM = Z_COMBINATOR(lambda me:
    lambda linked_list: lambda index: lambda element:
        IS_ZERO(index)
        (lambda _: PUSH_FRONT(element)(linked_list(TWO)))
        (lambda _: PUSH_FRONT(linked_list(ZERO))(SET_ITEM(linked_list(TWO))(DEC(index))(element)))
        (NONE)
)
assert GET_ITEM(SET_ITEM(my_linked_list)(THREE)(TEN))(TWO)(lambda x: x+1)(0) == 2
assert GET_ITEM(SET_ITEM(my_linked_list)(THREE)(TEN))(THREE)(lambda x: x+1)(0) == 10
assert GET_ITEM(SET_ITEM(my_linked_list)(FOUR)(TEN))(THREE)(lambda x: x+1)(0) == 4

LEN = Z_COMBINATOR(lambda me:
    lambda linked_list:
        linked_list(ONE)
        (lambda _: INC(me(linked_list(TWO))))
        (lambda _: ONE)
        (NONE)
)
assert LEN(my_linked_list)(lambda x: x+1)(0) == 7
assert LEN(nice_linked_list)(lambda x: x+1)(0) == 5

# ends when you pass in FALSE after a new addition (if you want to continue, pass TRUE after an addition)
MAKE_LINKED_LIST_INTERNAL = Z_COMBINATOR(lambda me:
    lambda linked_list: lambda element: lambda expect_more_arguments:
        expect_more_arguments
        (lambda _: me(PUSH_BACK(linked_list)(element))) # since it already took its linked_list arg, it should just take in element and expect_more_arguments next
        (lambda _: PUSH_BACK(linked_list)(element))
        (NONE)
)
MAKE_LINKED_LIST = lambda element_1: lambda expect_more_arguments_1: expect_more_arguments_1(lambda _: lambda element_2: lambda expect_more_arguments_2: MAKE_LINKED_LIST_INTERNAL(MAKE_LINKED_LIST_STUB(element_1))(element_2)(expect_more_arguments_2))(lambda _: MAKE_LINKED_LIST_STUB(element_1))(NONE)
epic_linked_list = MAKE_LINKED_LIST(ONE)(TRUE)(TWO)(TRUE)(THREE)(TRUE)(FOUR)(TRUE)(FIVE)(TRUE)(SIX)(TRUE)(SEVEN)(TRUE)(EIGHT)(TRUE)(NINE)(TRUE)(TEN)(FALSE)
assert LEN(epic_linked_list)(lambda x: x+1)(0) == 10
assert SUM(epic_linked_list)(lambda x: x+1)(0) == 55
assert GET_ITEM(epic_linked_list)(ZERO)(lambda x: x+1)(0) == 1
assert GET_ITEM(epic_linked_list)(ONE)(lambda x: x+1)(0) == 2
assert GET_ITEM(epic_linked_list)(DEC(LEN(epic_linked_list)))(lambda x: x+1)(0) == 10

TERM_SUM = Z_COMBINATOR(lambda me:
    lambda linked_list: lambda unary_term_function:
        ADD
        (unary_term_function(linked_list(ZERO)))
        (
            linked_list(ONE)
            (lambda _: me(linked_list(TWO))(unary_term_function))
            (lambda _: ZERO)
            (NONE)
        )
)
assert TERM_SUM(epic_linked_list)(lambda x: INC(x))(lambda x: x+1)(0) == 65
assert TERM_SUM(epic_linked_list)(lambda x: NINE)(lambda x: x+1)(0) == 90
assert TERM_SUM(epic_linked_list)(lambda x: SUBTRACT(TWENTY)(x))(lambda x: x+1)(0) == 145

# a tree is represented by a tree node that is a triple
# element zero is anything
# element one is a boolean: whether or not it has children (at least 1 child)
# element two is a linked list where each triple in the linked list is a child (which is a tree node)
my_little_tree = MAKE_TRIPLET(TWENTY)(TRUE)(MAKE_LINKED_LIST_STUB(
    MAKE_TRIPLET(FIVE)(FALSE)(NONE)
))
my_tree = MAKE_TRIPLET(NINE)(TRUE)(MAKE_LINKED_LIST(
    MAKE_TRIPLET(FOUR)(TRUE)(MAKE_LINKED_LIST(
        MAKE_TRIPLET(ELEVEN)(FALSE)(NONE)
    )(TRUE)(
        MAKE_TRIPLET(EIGHTEEN)(TRUE)(MAKE_LINKED_LIST(
            MAKE_TRIPLET(NINETEEN)(TRUE)(MAKE_LINKED_LIST(
                MAKE_TRIPLET(ONE)(TRUE)(MAKE_LINKED_LIST(
                    MAKE_TRIPLET(TWO)(FALSE)(NONE)
                )(TRUE)(
                    MAKE_TRIPLET(TWENTY)(FALSE)(NONE)
                )(TRUE)(
                    MAKE_TRIPLET(TWENTY)(FALSE)(NONE)
                )(TRUE)(
                    MAKE_TRIPLET(TWENTY)(FALSE)(NONE)
                )(TRUE)(
                    MAKE_TRIPLET(FOUR)(TRUE)(MAKE_LINKED_LIST(
                        MAKE_TRIPLET(SIX)(FALSE)(NONE)
                    )(FALSE))
                )(TRUE)(
                    MAKE_TRIPLET(ONE)(TRUE)(MAKE_LINKED_LIST(
                        MAKE_TRIPLET(SEVEN)(FALSE)(NONE)
                    )(FALSE))
                )(FALSE))
            )(FALSE))
        )(FALSE))
    )(FALSE))
)(TRUE)(
    MAKE_TRIPLET(THREE)(TRUE)(MAKE_LINKED_LIST(
        MAKE_TRIPLET(FOURTEEN)(TRUE)(MAKE_LINKED_LIST(
            MAKE_TRIPLET(EIGHTEEN)(TRUE)(MAKE_LINKED_LIST(
                MAKE_TRIPLET(TWENTY)(TRUE)(MAKE_LINKED_LIST(
                    MAKE_TRIPLET(ZERO)(TRUE)(MAKE_LINKED_LIST(
                        MAKE_TRIPLET(TWELVE)(TRUE)(MAKE_LINKED_LIST(
                            MAKE_TRIPLET(ONE)(TRUE)(MAKE_LINKED_LIST(
                                MAKE_TRIPLET(TEN)(FALSE)(NONE)
                            )(FALSE))
                        )(FALSE))
                    )(FALSE))
                )(TRUE)(
                    MAKE_TRIPLET(ONE)(TRUE)(MAKE_LINKED_LIST(
                        MAKE_TRIPLET(ELEVEN)(TRUE)(MAKE_LINKED_LIST(
                            MAKE_TRIPLET(TWELVE)(FALSE)(NONE)
                        )(FALSE))
                    )(FALSE))
                )(FALSE))
            )(TRUE)(
                MAKE_TRIPLET(TEN)(FALSE)(NONE)
            )(FALSE))
        )(FALSE))
    )(TRUE)(
        MAKE_TRIPLET(SIXTEEN)(FALSE)(NONE)
    )(FALSE))
)(TRUE)(
    MAKE_TRIPLET(SEVEN)(TRUE)(MAKE_LINKED_LIST(
        MAKE_TRIPLET(ZERO)(TRUE)(MAKE_LINKED_LIST(
            MAKE_TRIPLET(TWO)(FALSE)(NONE)
        )(FALSE))
    )(TRUE)(
        MAKE_TRIPLET(FIVE)(TRUE)(MAKE_LINKED_LIST(
            MAKE_TRIPLET(THREE)(TRUE)(MAKE_LINKED_LIST(
                MAKE_TRIPLET(THIRTEEN)(FALSE)(NONE)
            )(FALSE))
        )(FALSE))
    )(FALSE))
)(FALSE))

DFS_SUM = Z_COMBINATOR(lambda me:
    lambda tree:
        ADD
        (tree(ZERO))
        (
            tree(ONE)
            (lambda _: TERM_SUM(tree(TWO))(lambda subtree: me(subtree)))
            (lambda _: ZERO)
            (NONE)
        )
)
assert DFS_SUM(my_little_tree)(lambda x: x+1)(0) == 25
assert DFS_SUM(my_tree)(lambda x: x+1)(0) == 300
# trees :D