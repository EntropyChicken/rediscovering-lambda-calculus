"""
trying to make lambda calculus from nothing
cuz my intuition says you don't necessarily have to do everything according to convention.
you can probably still get a turing-machine-powerful system
even if you don't use church numerals, for example...?
i'll use unary lambda expressions to make lc (lambda calculus) representations
"""

# i remember this was how true and false were defined. pretty cool. i'll do the same
lc_true = lambda a: lambda b: a
lc_false = lambda a: lambda b: b

assert lc_true(2)(3) == 2
assert lc_false(4)(1) == 1

"""
i'll make things that can work with booleans (boolean algebra)
lc_and(lc_true)(lc_true) should be lc_true
lc_and(lc_true)(lc_false) should be lc_false
lc_and(lc_false)(lc_true) should be lc_false
lc_and(lc_false)(lc_false) should be lc_false
"""

lc_and = lambda a: lambda b: a(b(lc_true)(lc_false))(lc_false)
lc_or = lambda a: lambda b: a(lc_true)(b(lc_true)(lc_false))
lc_not = lambda a: a(lc_false)(lc_true)
lc_xor = lambda a: lambda b: a(b(lc_false)(lc_true))(b(lc_true)(lc_false))
# another way to implement it should be lc_xor = lambda a: lambda b: lc_and(lc_or(a)(b))(lc_not(lc_and(a)(b)))

assert lc_not(lc_true)(8)(5) == 5
assert lc_not(lc_false)(8)(5) == 8
assert lc_and(lc_true)(lc_true)(8)(5) == 8
assert lc_and(lc_true)(lc_false)(8)(5) == 5
assert lc_and(lc_false)(lc_true)(8)(5) == 5
assert lc_and(lc_false)(lc_false)(8)(5) == 5
assert lc_or(lc_true)(lc_true)(8)(5) == 8
assert lc_or(lc_true)(lc_false)(8)(5) == 8
assert lc_or(lc_false)(lc_true)(8)(5) == 8
assert lc_or(lc_false)(lc_false)(8)(5) == 5
assert lc_xor(lc_true)(lc_true)(8)(5) == 5
assert lc_xor(lc_true)(lc_false)(8)(5) == 8
assert lc_xor(lc_false)(lc_true)(8)(5) == 8
assert lc_xor(lc_false)(lc_false)(8)(5) == 5

# DeMorgan's Law
for a in [lc_true, lc_false]:
    for b in [lc_true, lc_false]:
        assert lc_not(lc_or(a)(b)) == lc_and(lc_not(a))(lc_not(b))

"""
numbers
for the sake of exploration, i'll intentionally try to do something other than
what i vaguely remember church numerals were.
what if i simply wrap a bunch of lambdas??
if i use the same name every time, only the last one will matter.
definition: an integer number n is just an nth order HOF which returns the nth paramter you give it
"""

lc_one = lambda x:x
lc_two = lambda x: lambda x: x
lc_three = lambda x: lambda x: lambda x: x
lc_four = lambda x: lambda x: lambda x: lambda x: x
lc_five = lambda x: lambda x: lambda x: lambda x: lambda x: x

assert lc_five(1)(2)(3)(4)(5) == 5
assert lc_three(3)(4)(5) == 5

lc_inc = lambda n: lambda x: n
lc_dec = lambda n: n(0)

assert lc_inc(lc_inc(lc_five))(1)(2)(3)(4)(5)(6)(7) == 7
assert lc_dec(lc_dec(lc_five))(1)(2)(3) == 3

print("PASSED ASSERTS!")

lc_add = lambda a: lambda b: lc_add(lc_inc(a))(lc_dec(b)) # uhhhh wait, this is endless recursion
# i need to check for recursion base case: when one of them reaches zero or one
# note: i now realize you can't do python name-based recursion in lambda calculus!

"""
under this system, anything that isn't a lambda function is considered a "zero"
and natural numbers are defined as how many times you can call dec on it before it becomes a "zero"
i can't really test if something is a lambda function with just lambda expressions and calls though...?
i would need to use python stuff in order to.
"""

lc_is_one = lambda n: n(lc_true)(lc_true)(lc_false)

"""
i think it may be impossible to implement lc_is_one
the crux of the problem is that every number takes a different number of parameters
so i can't really do a fixed-number-of-parameters test...?
"""

# this doesn't work
for i in range(1,4):
    num = lc_one
    for j in range(1,i):
        num = lc_inc(num)
    # num is now the representation of i
    print(lc_is_one(num)(1)(2))
# output: 1, funcion, 2, and every iteration from then on would cause an error: int is not callable

"""
i think i get it now
church numerals are designed the way they are so that you always pass in a fixed number of arguments
that way you can at least work with them and know what "type" of thing you're dealing with
whereas if the number of arguments is left unknown (over a particular type or class of thing),
then you instantly get lost in terms of what "type" each variable is
this is also partly why we bother taking in the second argument to lc_true
i see that the second argument is totally unused, but we still need it there to take up space
that way it's a fixed number of arguments being passed in all booleans ("boolean type" variables)
my conclusion:
a nice system should have, for each "variable type", a fixed number of arguments to be passed in
given that you want a particular resulting "variable type" out of it
for example:
booleans: always binary (two choices, of any type, i guess?) in order to give you one of the choices
logic operators: always binary (two booleans. only booleans should be allowed) in order to give you a boolean
numbers: always binary (a unary function that takes in and gives out the same type, and something of that type)
in order to give you a thing of that type? or idk maybe our definition can be broader.
basicall, we can think of everything as having a type.
then, there's a fixed number of arguments and fixed types for each argument,
making everything becomes more organized.
who knows? maybe there's a super clever way to make numbers without fixed numbers of arguments...?
but church numerals seem easier for me to understand!
"""