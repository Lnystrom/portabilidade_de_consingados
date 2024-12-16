from cx_Freeze import setup, Executable
import os

# Caminho da pasta e arquivo que você quer incluir
imagem = os.path.join(os.getcwd(), "tabela_liquidacao.png")  # Caminho do arquivo de imagem
pasta_padrao = os.path.join(os.getcwd(), "padrao")  # Caminho da pasta que você quer incluir

# Defina os detalhes do seu script Python
setup(
    name="Calculador de Saldo de Liquidação",
    version="1.0",
    description="Este aplicativo calcula automaticamente o saldo de liquidação e a taxa de juros de empréstimos consignados do INSS.",
    options={
        "build_exe": {
            # Inclua os arquivos necessários (imagem e pasta)
            "include_files": [
                imagem,    # Inclui a imagem
                pasta_padrao  # Inclui a pasta
            ]
        }
    },
    executables=[Executable("nova_gui.py", icon="icone.ico")]  # Aqui é onde você adiciona o ícone
)

# Para rodar, você utiliza o comando:
# python setup.py build
