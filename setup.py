from cx_Freeze import setup, Executable
import os


imagem = os.path.join(os.getcwd(), "tabela_liquidacao.png")  
pasta_padrao = os.path.join(os.getcwd(), "padrao")  


setup(
    name="Calculador de Saldo de Liquidação",
    version="1.0",
    description="Este aplicativo calcula automaticamente o saldo de liquidação e a taxa de juros de empréstimos consignados do INSS.",
    options={
        "build_exe": {
            "include_files": [
                imagem,    # Inclui a imagem
                pasta_padrao  # Inclui a pasta
            ]
        }
    },
    executables=[Executable("Calculadora de Portabilidades.py", icon="icone.ico", base="Win32GUI")]  
)

# Para rodar
# python setup.py build
