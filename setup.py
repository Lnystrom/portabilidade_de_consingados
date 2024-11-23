from cx_Freeze import setup, Executable

# Defina os detalhes do seu script Python
setup(
    name="Calculador de Saldo de Liquidação",
    version="1.0",
    description="Este aplicativo calcula automaticamente o saldo de liquidação e a taxa de juros de empréstimos consignados do INSS.",
    options={
        "build_exe": {
            # Inclua os arquivos necessários (por exemplo, gui.py)
            "include_files": ["gui.py"],
        }
    },
    executables=[Executable("main.py", icon="icone.ico")]  # Aqui é onde você adiciona o ícone
)

#python setup.py build
