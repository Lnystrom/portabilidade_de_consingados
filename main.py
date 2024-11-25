# Bibliotecas de data
from dateutil.relativedelta import relativedelta
from datetime import datetime
import calendar

# Bibliotecas para manipulação de arquivos PDF
import pdfplumber

# Bibliotecas para gráficos
import matplotlib.pyplot as plt

# Bibliotecas para manipulação de dados
import pandas as pd
import numpy as np

# Bibliotecas de otimização
from scipy.optimize import fsolve
from dateutil.relativedelta import relativedelta
from datetime import datetime

# Bilioteca para UI
import shutil
import os
from screeninfo import get_monitors
import customtkinter

# Obter informações sobre os monitores conectados
monitors = get_monitors()

# Se houver múltiplos monitores, escolher o monitor principal ou um específico
monitor = monitors[0]  # Seleciona o monitor primário (primeiro monitor na lista)

screen_width = monitor.width
screen_height = monitor.height

# Definir largura e altura da janela
largura = monitor.width
altura = monitor.height

# Calcula a posição para centralizar a janela no monitor selecionado
x = (screen_width // 2) - (largura // 2)
y = (screen_height // 2) - (altura // 2)

my_custom_theme = {
    "primary_color": "#e3e9f0",      # Main color (Light Grayish Blue)
        "color1": "#e4ebf1",         # Light Grayish Blue
        "color2": "#11115c",         # Azul Banrisul (Dark Blue)
        "color3": "#95a6ba",         # Cinza (Gray)
        "color4": "#908682",         # Olive Gray
        "color5": "#bfbbb6",         # Light Taupe
        "color6": "#7d678f",         # Purple Gray
        "color7": "#b8c2d1",         # Cinza Médio (Medium Gray)
        "color8": "#c4c3c6",         # Light Silver
        "color9": "#aea0ac",         # Lavender Gray
        "color10": "#6c8cac",        # Slate Blue

}

dados_filtrados = []

def start_gui():
    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__() #When you use super().__init__() in a subclass, you're calling the __init__() method of the parent class, allowing the child class to properly initialize the inherited attributes and perform any setup that the parent class requires. 

            # Variável de controle para armazenar o nome da pasta
            
            result = customtkinter.StringVar()

            def gravar_cpf():
                CPF = entrada.get()
                CPF_extraido.configure(text=f"CPF Registrado: {CPF}")
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


            def selecionar_arquivo():
                arquivo_pdf = customtkinter.filedialog.askopenfile(title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")])

                if arquivo_pdf:
                    print(f"Arquivo selecionado: {arquivo_pdf}")
                    nome_da_pasta = gravar_cpf()  # A pasta é criada e seu nome é retornado
                    caminho_destino = os.path.join(nome_da_pasta, "consignado.pdf")

                    try:
                        shutil.copy(arquivo_pdf.name, caminho_destino)  # Certifique-se de usar o 'name' do arquivo
                        print(f"Arquivo copiado para: {caminho_destino}")
                    except Exception as e:
                        print(f"Ocorreu um erro ao copiar o arquivo: {e}")
                else:
                    print("Nenhum arquivo foi selecionado.")

            def ocultar_1():
                welcome_frame.place_forget()
                botao.place_forget()
                
                # Configurar a janela para usar grid
                entrada_frame.place(x=largura/2 -150, y= 550)
                entrada_label.pack()
                entrada.pack()
                entrada_botao.pack()

            def ocultar_2():
                gravar_cpf()
                entrada_frame.place(x=largura+500, y= 50)
                anexo_frame.place(x=largura/2 -250, y= 550)
                anexo_label.pack()
                anexo_botao.pack()

            def ocultar_3():
                selecionar_arquivo()
                anexo_frame.place_forget()

            # configure window
            self.title("Calculadora de Portabilidade")
            self.geometry(f'{largura}x{altura}+{x}+{y}')
            self.configure(fg_color=my_custom_theme["primary_color"])  # Light Grayish Blue

            linhas_frame = customtkinter.CTkFrame(self, fg_color=None, width=largura, height=75)
            linhas_frame.place(x=0,y=0)
            # Create the canvas_1
            canvas_1 = customtkinter.CTkCanvas(linhas_frame, width=largura, height=100)
            canvas_1.pack()
            # Draw the first rectangle with color1
            canvas_1.create_rectangle(0, 0, largura, 25, outline="", width=3, fill="white")
            # Draw the second rectangle with color2
            canvas_1.create_rectangle(0, 25, largura, 75, outline="", width=3, fill=my_custom_theme["color2"])
            # Draw the third rectangle with color3
            canvas_1.create_rectangle(0, 75, largura, 100, outline="", width=3, fill=my_custom_theme["color8"])


            canvas_2 = customtkinter.CTkCanvas(self, width=largura, height=150)
            canvas_2.place(x= 20, y=500, width=largura-20, height=150)
            # Draw the first rectangle with color1
            canvas_2.create_rectangle(0, 0, largura-50, 25, outline="", width=3, fill="white")
            canvas_2.create_rectangle(0, 30, largura-50, 150, outline="", width=3, fill="white")

            #Draw the text
            # texto_1 = customtkinter.CTkLabel(self, largura, 25, text_color="black", text="Bem vindo ao app")

            # Create the initial page (Welcome page)
            welcome_frame = customtkinter.CTkFrame(self, fg_color="white", width=largura-40, height=150)
            welcome_frame.place(x= largura/2.7, y=550)

            welcome_text_1 = customtkinter.CTkLabel(welcome_frame, text="Seja bem vindo à", text_color="black", font=("Times New Roman", 16))
            welcome_text_1.pack()  # Add padding around the label
            welcome_text_2 = customtkinter.CTkLabel(welcome_frame, text="Calculadora de Saldo de Liquidação de Portabilidades", text_color="#5bc2e7", font=("Times New Roman", 20))
            welcome_text_2.pack()  # Add padding around the label

            # Botão para mudar para outra página
            botao = customtkinter.CTkButton(self, text="Calcular Saldo de Liquidação", width=50, height=20, fg_color="white", text_color="black", command=ocultar_1)
            botao.place(x=0,y=2)

            #Página 2
            entrada_frame = customtkinter.CTkFrame(self, fg_color="white", width=largura-40, height=500)
            entrada_label = customtkinter.CTkLabel(entrada_frame, text="Por favor, insira o CPF do Cliente", text_color="black", font=("Times New Roman", 16))
            entrada = customtkinter.CTkEntry(entrada_frame, 250, 25, None, None, bg_color="white", text_color="black")
            CPF_extraido = customtkinter.CTkLabel(entrada_frame)
            entrada_botao = customtkinter.CTkButton(entrada_frame, width=50, height=20, text="Gravar CPF", fg_color= my_custom_theme["color10"], text_color="black", command=ocultar_2)

            #página 3
            anexo_frame = customtkinter.CTkFrame(self, fg_color="white", width=largura-40, height=500)
            anexo_label = customtkinter.CTkLabel(anexo_frame, text="O Extrato de Empréstimos deve estar em .pdf e ser criado digitalmente", text_color="black", font=("Times New Roman", 16))
            anexo_botao = customtkinter.CTkButton(anexo_frame, width=50, height=20, text="Anexar arquivo", fg_color= my_custom_theme["color10"], text_color="black", command=ocultar_3)

            app = App()
            app.mainloop()


out_folder = start_gui()

def leitor_de_pdf(out_folder):
    with pdfplumber.open(f"{out_folder}/consignado.pdf") as pdf:
        # Variável para armazenar o texto filtrado
        # Iterar pelas páginas do PDF
        for page in pdf.pages:
            # Extrair tabelas da página
            for table in page.extract_tables():
                # Pular cabeçalhos
                for linha in table[2:]:
                    # Verificar se a linha tem pelo menos 14 colunas
                    if len(linha) > 13 and linha[2] == "Ativo":  # Coluna de situação (index 2)
                        contrato = linha[0].replace('\n', '')    # Número do contrato
                        banco = linha[1].replace('\n', '')       # Banco
                        situacao = linha[2]                       # Situação (já é 'Ativo')
                        data_inclusao = linha[4].replace('\n', '') # Data de inclusão (index 4)
                        inicio_de_desconto = linha[5].replace('\n', '') # Data de inclusão (index 4)
                        data_vencimento = linha[6].replace('\n', '') # Aqui deve estar a data no formato mm/yyyy
                        data_vencimento_formatada = datetime.strptime(data_vencimento, '%m/%Y').strftime('%d/%m/%y')
                        parcelas = int(linha[7].replace('\n', ''))    # Quantidade de parcelas
                        valor_parcela = float(linha[8].replace('R$', '').replace('.', '').replace(',', '.').strip())  # Valor da parcela (index 8)
                        valor_emprestado = float(linha[9].replace('.', '').replace(',', '.').replace('R$', '').strip())  # Valor emprestado (index 9)

                        # Obter o último dia do mês para data_vencimento
                        mes, ano = map(int, data_vencimento.split('/'))
                        ultimo_dia_mes = calendar.monthrange(ano, mes)[1]
                        data_vencimento_formatada = datetime.strptime(f"{ultimo_dia_mes}/{mes}/{ano}", '%d/%m/%Y')
                        data_atual = datetime.now()

                        # Calcular meses restantes usando relativedelta a partir da data atual
                        diferenca = relativedelta(data_vencimento_formatada, data_atual)
                        meses_restantes = diferenca.years * 12 + diferenca.months
                        
                        # Calcular o valor total pago considerando as parcelas
                        valor_total_pago = parcelas*valor_parcela
                        
                        #calculo de taxa de juros
                        taxa = np.round(calcular_taxa(parcelas, valor_parcela, valor_emprestado)*100,2)
                        
                        valor_emprestado, taxa = verificar_dados(parcelas, valor_parcela, valor_emprestado, taxa, contrato)
                        
                        # Calcular o valor de liquidação
                        valor_liquidacao = np.round(calcular_liquidacao(valor_parcela, meses_restantes, taxa), 2)
                        print(f"{taxa}")
                        # Adicionar informações ao filtro
                        dados_filtrados.append([contrato, banco, situacao, inicio_de_desconto, str(data_vencimento), valor_parcela, parcelas, meses_restantes, valor_emprestado, taxa, valor_liquidacao])
                        print("processamento concluído!")


def calcular_taxa(n_periodos, pmt, valor_presente, chute_inicial=0.01):
    """
    Calcula a taxa de juros periódica usando o método de Newton-Raphson.
    
    A função utiliza o método de Newton-Raphson para encontrar a taxa de juros periódica que satisfaz
    a equação de valor presente das parcelas. Se a taxa calculada for negativa ou se houver erro no cálculo,
    a função retorna None.
    
    Parâmetros:
    -----------
    n_periodos (int): Número total de períodos (parcelas).
    pmt (float): Valor da parcela paga em cada período.
    valor_presente (float): Valor do empréstimo inicial (valor presente).
    chute_inicial (float, opcional): Estimativa inicial para a taxa de juros. O valor padrão é 0.01.
    
    Retorna:
    --------
    float ou None: A taxa de juros periódica calculada ou None se não for possível calcular.
    """


    def funcao_taxa(r):
        # Evitar overflow em cálculos
        try:
            # Evitar divisão por zero e valores de r que gerem overflow
            if r <= 0 or r >= 1:  # Para r <= 0 ou r >= 1, a fórmula não é válida
                return np.inf
            
            # Valor presente menos o montante a ser pago
            return valor_presente - (pmt * (1 - (1 + r) ** -n_periodos) / r)

        except OverflowError:
            return np.inf  # Retornar infinito se ocorrer overflow

    # Usando fsolve para encontrar a taxa
    try:
        taxa = fsolve(funcao_taxa, chute_inicial, maxfev=1000)[0]  # Aumentar maxfev se necessário
        return taxa if taxa > 0 else None  # Retorna None se a taxa for negativa
    except Exception as e:
        print(f"Erro: {e}")
        return None

def calcular_liquidacao(valor_parcela, meses_restantes, taxa_juros_mensal):
    """
    Calcula o valor de liquidação de um empréstimo considerando o valor presente das parcelas restantes.
    
    A função calcula o valor total a ser pago, levando em consideração o valor das parcelas restantes
    e a taxa de juros mensal. O cálculo é feito através da fórmula de valor presente.

    Parâmetros:
    -----------
    valor_parcela (float): Valor da parcela mensal a ser paga.
    meses_restantes (int): Número de meses restantes para o pagamento do empréstimo.
    taxa_juros_mensal (float): Taxa de juros mensal em percentual.

    Retorna:
    --------
    float: Valor total a ser pago, considerando as parcelas restantes e a taxa de juros.
    """
    # Converter taxa de juros percentual para decimal
    taxa_juros_decimal = taxa_juros_mensal / 100
    
    # Calcular o valor presente das parcelas restantes
    valor_presente = 0
    for i in range(1, meses_restantes + 1):
        valor_presente += valor_parcela / ((1 + taxa_juros_decimal) ** i)
    
    return valor_presente

def verificar_dados(parcelas, valor_parcela, valor_emprestado, taxa, contrato):
    """
    Verifica e valida os dados do empréstimo (valor emprestado e taxa de juros).
    
    Se o valor emprestado for menor ou igual a 0 ou a taxa for menor ou igual a 1.3, a função solicita 
    ao usuário que forneça novos valores até que os dados sejam válidos.
    
    Parâmetros:
    -----------
    parcelas (int): Número de parcelas do empréstimo.
    valor_parcela (float): Valor de cada parcela mensal.
    valor_emprestado (float): Valor total emprestado.
    taxa (float): Taxa de juros do empréstimo.
    contrato (str): Número do contrato para identificação.

    Retorna:
    --------
    tuple: Tupla contendo o valor emprestado e a taxa corrigidos, caso necessário.
    """

    if valor_emprestado <= 0 or taxa <= 1.3:
        print("Os dados fornecidos são inválidos.")
        
        # Solicita novamente o valor emprestado até ser válido
        while valor_emprestado <= 0 or taxa <= 1.3:
            try:
                valor_emprestado = float(input(f"O contrato {contrato} está com valor emprestado incorreto para o cáculo, por favor informe um valor emprestado válido (VALOR LIBERADO): "))
                taxa = np.round(calcular_taxa(parcelas, valor_parcela, valor_emprestado)*100,2)
                if valor_emprestado <= 0:
                    print("Valor emprestado deve ser maior que 0.")
            except ValueError:
                print("Por favor, insira um número válido para o valor emprestado.")
    
    # Retorna os valores validados
    return valor_emprestado, taxa

leitor_de_pdf(out_folder)

print("Arquivo:", out_folder)


# Imprimir o cabeçalho da tabela original
cabecalho_original = ['Número do Contrato', 'Banco de Origem', 'Situação', 'Início de Desconto', 'Data de Vencimento', 'PMT(R$)',  'Parcelas','Meses Restantes', 'Valor Emprestado (R$)', 'Taxa Original (%)', 'Valor de Liquidação(R$)']
# print(f"{cabecalho_original[0]:<20} {cabecalho_original[1]:<30} {cabecalho_original[2]:<10} {cabecalho_original[3]:<15} {cabecalho_original[4]:<15} {cabecalho_original[5]:<10} {cabecalho_original[6]:<15} {cabecalho_original[7]:<15}{cabecalho_original[8]:<6}{cabecalho_original[9]:<6}{cabecalho_original[10]:<6}")

# Criar DataFrame com os dados
df = pd.DataFrame(dados_filtrados, columns=cabecalho_original)
df.to_csv(f"{out_folder}/tabela_liquidacao.csv", index=False)

# Configurar o gráfico
fig, ax = plt.subplots(figsize=(24, len(df) * 0.5))  # Tamanho da imagem
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc = 'center', loc='center')

# Estilizar a tabela
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Aumentar a escala da tabela

# Ajustar a largura das colunas
table.auto_set_column_width([0, 1, 2, 3, 4, 5, 6, 7, 8])  # Ajusta automaticamente todas as colunas
table[1, 1].set_width(0.3)  # Define a largura da coluna "Banco de Origem"

# Salvar a tabela como imagem
plt.savefig(f"{out_folder}/tabela_liquidacao.png", bbox_inches='tight', dpi=300)

# trocar vencimento por parcelas restantes