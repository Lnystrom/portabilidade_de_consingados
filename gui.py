import requests
from tkinter import *
from tkinter import filedialog
from os import mkdir, path, makedirs
import shutil

# Função para abrir o gerenciador de arquivos e copiar o PDF para uma pasta já existente
def selecionar_arquivo_pdf():
    arquivo_pdf = filedialog.askopenfilename(title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")])
    
    # Verifica se um arquivo foi selecionado
    if arquivo_pdf:
        print(f"Arquivo selecionado: {arquivo_pdf}")
        
        # Obtém o nome da pasta que foi criada na função gravar_texto()
        nome_da_pasta = gravar_texto()  # A pasta é criada e seu nome é retornado
        
        # Verifica se a pasta de destino existe
        if not path.exists(nome_da_pasta):
            print(f"A pasta de destino não existe: {nome_da_pasta}")
            return
        
        # Define o caminho completo do destino com nome fixo "consignado.pdf"
        caminho_destino = path.join(nome_da_pasta, "consignado.pdf")
        
        try:
            # Copia o arquivo para a pasta de destino com o nome fixo "consignado.pdf"
            shutil.copy(arquivo_pdf, caminho_destino)
            print(f"Arquivo copiado para: {caminho_destino}")
        except Exception as e:
            print(f"Ocorreu um erro ao copiar o arquivo: {e}")
    else:
        print("Nenhum arquivo foi selecionado.")


#Função para gravar texto
def gravar_texto():
    CPF = entrada.get()
    CPF_extraido.config(text=f"CPF Registrado: {CPF}")
    nome_da_pasta = f"{CPF}"
    try:
        # Cria a pasta
        makedirs(nome_da_pasta)
        print(f"Pasta '{nome_da_pasta}' criada com sucesso!")
    except FileExistsError:
        print(f"A pasta '{nome_da_pasta}' já existe.")

    return nome_da_pasta

#UI propriamente dita

janela = Tk()
janela.title("Simulador de Portabilidade de Consignados")

interação_1 = Label(janela, text="Digite o CPF do cliente:")
interação_1.grid(column=0, row=0)

# Campo de entrada (Entry)
entrada = Entry(janela)
entrada.grid(column=0, row=1)
# Botão para capturar a entrada
botao =Button(janela, text="Mostrar Entrada", command=gravar_texto)
botao.grid(column=0, row=2)
#Exibir CPF:
CPF_extraido = Label(janela, text="")
CPF_extraido.grid(column=0, row=3)

interação_2 = Label(janela, text="O Extrato de Empréstimos Consignados deve estar em .pdf e ser criado digitalmente")
interação_2.grid(column=0, row=4)

botão = Button(janela, text="Anexar extrato de empréstimos", command=selecionar_arquivo_pdf)
botão.grid(column=0, row=5)


janela.mainloop()