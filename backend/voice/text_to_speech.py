"""
Draco AI
Text To Speech

Responsável por converter texto em áudio
utilizando o Piper.
"""

from pathlib import Path
import subprocess


class TextToSpeech:

    def __init__(self):

        # Raiz do projeto Draco AI
        self.project_root = Path(__file__).resolve().parents[2]

        # Diretório do Piper
        self.piper_dir = self.project_root / "piper"

        # Executável
        self.piper_exe = self.piper_dir / "piper.exe"

        # Modelo de voz
        self.voice_model = (
            self.piper_dir
            / "voices"
            / "pt_BR-faber-medium.onnx"
        )

        # Pasta de saída
        self.output_dir = self.piper_dir / "output"

        self.output_dir.mkdir(
            exist_ok=True
        )


    def speak(
        self,
        text,
        filename="output.wav"
    ):

        """
        Converte texto em áudio usando Piper.
        """

        output_file = (
            self.output_dir
            / filename
        )


        # Verificações básicas

        if not self.piper_exe.exists():

            raise FileNotFoundError(
                f"Piper não encontrado:\n{self.piper_exe}"
            )


        if not self.voice_model.exists():

            raise FileNotFoundError(
                f"Modelo de voz não encontrado:\n{self.voice_model}"
            )


        command = [

            str(self.piper_exe),

            "--model",
            str(self.voice_model),

            "--output_file",
            str(output_file)

        ]


        print("\nGerando voz...\n")

        try:

            process = subprocess.run(

                command,

                input=text,

                text=True,

                capture_output=True

            )


        except Exception as error:

            raise RuntimeError(
                f"Erro ao executar Piper:\n{error}"
            )


        # Debug

        print(
            "Código retorno:",
            process.returncode
        )


        if process.stdout:

            print(
                "Piper STDOUT:"
            )

            print(
                process.stdout
            )


        if process.stderr:

            print(
                "Piper STDERR:"
            )

            print(
                process.stderr
            )


        # Verifica falha

        if process.returncode != 0:

            raise RuntimeError(
                "Piper falhou ao gerar áudio."
            )


        print(
            f"\nÁudio criado em:\n{output_file}"
        )


        return output_file