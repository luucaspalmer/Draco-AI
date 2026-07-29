from backend.system.command_parser import parse_command

frases = [
    "Abra o CMD",
    "Abra o Prompt de Comando",
    "Abra o Terminal",
    "Abra o bloco de notas",
    "Abra a calculadora",
    "Como funciona o CMD?",
    "Qual a capital do Brasil?"
]

for frase in frases:
    print("=" * 50)
    print(frase)

    resultado = parse_command(frase)
    print(resultado)