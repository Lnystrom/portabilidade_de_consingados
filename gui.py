import shutil
import os
import tkinter as tk
from tkinter import filedialog

def start_gui():
    # Criação da janela principal (Tk)
    janela = tk.Tk()
    janela.title("Simulador de Portabilidade de Consignados")
    janela.geometry("500x400")
    janela.configure(bg="#2C3E50")  # Cor de fundo azul marinho

    # Criar a variável result após a criação da janela
    result = tk.StringVar()

    def selecionar_arquivo_pdf():
        global caminho_destino
        arquivo_pdf = filedialog.askopenfilename(title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")])

        if arquivo_pdf:
            print(f"Arquivo selecionado: {arquivo_pdf}")
            nome_da_pasta = gravar_texto()  # A pasta é criada e seu nome é retornado

            if not os.path.exists(nome_da_pasta):
                print(f"A pasta de destino não existe: {nome_da_pasta}")
                return

            caminho_destino = os.path.join(nome_da_pasta, "consignado.pdf")

            try:
                shutil.copy(arquivo_pdf, caminho_destino)
                print(f"Arquivo copiado para: {caminho_destino}")
                mostrar_interacao_3()  # Exibir a 3ª interação após o arquivo ser copiado
            except Exception as e:
                print(f"Ocorreu um erro ao copiar o arquivo: {e}")
        else:
            print("Nenhum arquivo foi selecionado.")

    def gravar_texto():
        CPF = entrada.get()
        CPF_extraido.config(text=f"CPF Registrado: {CPF}")
        nome_da_pasta = str(CPF)
        if not len(nome_da_pasta):
            nome_da_pasta = "saida"
        try:
            os.makedirs(nome_da_pasta)
            print(f"Pasta '{nome_da_pasta}' criada com sucesso!")
        except FileExistsError:
            print(f"A pasta '{nome_da_pasta}' já existe.")
        result.set(nome_da_pasta)
        return nome_da_pasta

    def mostrar_interacao_2():
        # Remove widgets da 1ª interação
        interação_1.grid_forget()
        entrada.grid_forget()
        botao.grid_forget()
        CPF_extraido.grid_forget()

        # Exibe a 2ª interação (Texto informativo sobre o PDF)
        interação_2.grid(column=0, row=0, padx=20, pady=20, columnspan=2, sticky="nsew")
        botão.grid(column=0, row=1, padx=20, pady=10, columnspan=2, sticky="nsew")

    def mostrar_interacao_3():
        # Remove widgets da 2ª interação
        interação_2.grid_forget()
        botão.grid_forget()

        # Exibe a 3ª interação
        caminho_pasta = result.get()
        label_resultado = tk.Label(janela, text=f"Os arquivos estarão disponíveis na pasta '{caminho_pasta}'", font=("Georgia", 14), bg="#FFFFFF", fg="#2C3E50")
        label_resultado.grid(column=0, row=0, padx=20, pady=20)

        # Botão para processar o arquivo e fechar a janela
        botao_processar = tk.Button(janela, text="Processar Arquivo", command=fechar_janela, font=("Georgia", 14), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
        botao_processar.grid(column=0, row=1, padx=20, pady=10, columnspan=2, sticky="nsew")

    def fechar_janela():
        # Fecha a janela
        janela.quit()  # Encerra o mainloop
        janela.destroy()  # Destroi a janela

        # Aqui o código de processamento necessário pode ser executado após o fechamento da janela
        processar_arquivo()

    def processar_arquivo():
        # Aqui você pode colocar o que precisa ser feito após o fechamento da janela
        caminho_pasta = result.get()
        print(f"Processando os arquivos na pasta {caminho_pasta}...")
        # Lógica de processamento do arquivo
        # Exemplo: mover ou alterar arquivos, gerar relatório, etc.
        print("Processamento concluído!")

    # UI propriamente dita
    interação_1 = tk.Label(janela, text="Digite o CPF do cliente:", font=("Georgia", 18), bg="#2C3E50", fg="#FFFFFF")
    interação_1.grid(column=0, row=0, padx=20, pady=20, columnspan=2, sticky="nsew")

    # Campo de entrada (Entry)
    entrada = tk.Entry(janela, font=("Georgia", 14), bd=2, relief="solid", width=30, justify="center")
    entrada.grid(column=0, row=1, padx=20, pady=10, columnspan=2, sticky="nsew")

    # Botão para capturar a entrada
    botao = tk.Button(janela, text="Mostrar Entrada", command=lambda: [gravar_texto(), mostrar_interacao_2()], font=("Georgia", 14), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
    botao.grid(column=0, row=2, padx=20, pady=10, columnspan=2, sticky="nsew")

    # Exibir CPF:
    CPF_extraido = tk.Label(janela, text="", font=("Georgia", 14), bg="#2C3E50", fg="#FFFFFF")
    CPF_extraido.grid(column=0, row=3, padx=20, pady=10, columnspan=2, sticky="nsew")

    # Parte 2: Iniciar a interação 2
    interação_2 = tk.Label(janela, text="O arquivo deve estar em .pdf e ser criado digitalmente", font=("Georgia", 14, "italic"), bg="#2C3E50", fg="#FFFFFF")
    
    # Botão para anexar o extrato
    botão = tk.Button(janela, text="Anexar Extrato", command=selecionar_arquivo_pdf, font=("Georgia", 14), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)

    # Exibe a janela principal
    janela.mainloop()

    # A função retorna o resultado da pasta final
    return result.get()


# Chama a função start_gui e evita que ela reabra
if __name__ == "__main__":
    out_folder = start_gui()
    print(f"Resultado da pasta de destino: {out_folder}")