from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# all puzzles common knowledge encoding:

# statement: a character can be a Knight or a Knave, but not both
# encode: Exclusive OR: (AKnight OR AKnave) AND NOT(AKnight AND AKnave)

# statement: Knight always tells the truth
# encode: Implication(Knight, "sentence")

# statement: Knave always lies
# encode: Implication(Knave, NOT("sentence"))

# consider implication for both cases(Knight, Knave) for each character (A, B, C)
# statement: A says "I am both a knight and a knave."
# Assign to A the role of Knight:
# encode: Implication(AKnight, And(AKnight, AKnave))
# Assign to A the role of Knave 
# encode: Implication(AKnave, Not(And(AKnight, AKnave)))

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
   And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
   Implication(AKnight, And(AKnight, AKnave)),
   Implication(AKnave, Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(BKnight, And(BKnight, AKnave)),
    Implication(BKnave, Not(And(BKnave, AKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    Implication(BKnight, Implication(AKnight, AKnave)),
    Implication(BKnight, Implication(AKnave, AKnave)),
    Implication(BKnave, Implication(AKnight, Not(AKnave))),
    Implication(BKnave, Implication(AKnave, Not(AKnave))),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
