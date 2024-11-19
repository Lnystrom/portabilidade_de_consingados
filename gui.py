import requests
from tkinter import *
from tkinter import filedialog
from os import mkdir

# Função para abrir o gerenciador de arquivos
def selecionar_arquivo_pdf():

    # Abre o diálogo para selecionar um arquivo
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")]  # Título da janela de diálogo e filtra para arquivos PDF
    )
    
    # Verifica se um arquivo foi selecionado
    if caminho_arquivo:
        print(f"Arquivo selecionado: {caminho_arquivo}")
    else:
        print("Nenhum arquivo selecionado.")

#Função para gravar texto
def gravar_texto():
    CPF = entrada.get()
    CPF_extraido.config(text=f"CPF Registrado: {CPF}")
    nome_da_pasta = f"{CPF}"
    try:
        # Cria a pasta
        mkdir(nome_da_pasta)
        print(f"Pasta '{nome_da_pasta}' criada com sucesso!")
    except FileExistsError:
        print(f"A pasta '{nome_da_pasta}' já existe.")

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