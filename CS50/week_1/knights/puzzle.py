from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
ASentence = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave), Implication(AKnight, ASentence), Implication(AKnave, Not(ASentence))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
ASentence = And(AKnave, BKnave)
knowledge1 = And(
    And(Or(AKnight, AKnave), Or(BKnight, BKnave)),
    Implication(AKnight, ASentence),
    Implication(AKnave, Not(ASentence))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
ASentence = Or(And(AKnave, BKnave), And(AKnight, BKnight))
BSentence = Or(And(AKnave, BKnight), And(AKnight, BKnave))
knowledge2 = And(
    And(Or(AKnight, AKnave), Or(BKnight, BKnave)),
    Implication(AKnight, ASentence),
    Implication(AKnave, Not(ASentence)),
    Implication(BKnight, BSentence),
    Implication(BKnave, Not(BSentence))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
ASentence1 = Or(AKnight, AKnave)
ASentence2 = And(ASentence1, BKnave)
BSentence = CKnave
CSentence = AKnight
knowledge3 = And(
    And(Or(AKnight, AKnave), Or(BKnight, BKnave), Or(CKnight, CKnave)),
    Implication(AKnight, ASentence1),
    Implication(AKnave, Not(ASentence1)),
    Implication(BKnight, BSentence),
    Implication(BKnight, ASentence2),
    Implication(BKnave, ASentence1),
    Implication(BKnave, Not(BSentence)),
    Implication(CKnight, CSentence),
    Implication(CKnave, Not(CSentence)),
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
