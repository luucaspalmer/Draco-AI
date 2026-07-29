from backend.system.system_actions import process_text

frases = [
    "Quero abrir o notepad",
    "Quero o notepad",
    "Preciso do notepad",
    "Me abra o notepad",
    "Pode abrir o notepad?"
]

for frase in frases:
    print("=" * 50)
    print("Entrada:", frase)

    resultado = process_text(frase)

    print("Resultado:", resultado)