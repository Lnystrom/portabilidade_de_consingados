import requests
from tkinter import *
from tkinter import filedialog

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


def pegar_cotacoes():
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")

    requisicao_dic = requisicao.json()

    cotacao_dolar = requisicao_dic['USDBRL']['bid']
    cotacao_euro = requisicao_dic['EURBRL']['bid']
    cotacao_btc = requisicao_dic['BTCBRL']['bid']

    texto = f'''
    Dólar: {cotacao_dolar}
    Euro: {cotacao_euro}
    BTC: {cotacao_btc}'''

    print(texto)

pegar_cotacoes()

janela = Tk()
janela.title("Simulador de Portabilidade de Consignados")

interação_1 = Label(janela, text="O Extrato de Empréstimos Consignados deve estar em .pdf e ser criado digitalmente")
interação_1.grid(column=0, row=0)

botão = Button(janela, text="Anexar extrato de empréstimos", command=selecionar_arquivo_pdf)
botão.grid(column=0, row=1)


janela.mainloop()