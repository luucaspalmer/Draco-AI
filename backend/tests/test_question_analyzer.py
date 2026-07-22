from question.question_analyzer import analyze_question


tests = [

    "Quem criou o Draco?",

    "O que é inteligência artificial?",

    "Como está o clima hoje?",

    "Vai chover amanhã?",

    "Olá Draco"

]


for text in tests:

    print("\nPergunta:")
    print(text)

    print(
        analyze_question(text)
    )