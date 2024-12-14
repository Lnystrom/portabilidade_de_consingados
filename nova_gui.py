import shutil
import os
import customtkinter
from screeninfo import get_monitors

# Bibliotecas de data
from dateutil.relativedelta import relativedelta
from datetime import datetime
import calendar

# Bibliotecas para manipulação de arquivos PDF
import pdfplumber

# Bibliotecas para gráficos
import matplotlib.pyplot as plt
import fitz  # PyMuPDF
from PIL import Image, ImageTk

# Bibliotecas para manipulação de dados
import pandas as pd
import numpy as np

# Bibliotecas de otimização
from scipy.optimize import fsolve
from dateutil.relativedelta import relativedelta
from datetime import datetime

dados_filtrados = []
first_table = True

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

def verificar_dados(parcelas, valor_parcela, valor_emprestado, taxa, contrato, argumentos):
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

    while valor_emprestado <= 0 or taxa <= 1.3:
        # # print("Os dados fornecidos são inválidos.")
        # argumentos[0]['label_6'].configure(text=f"O contrato {contrato} está com valor emprestado incorreto para o cálculo, por favor informe um valor emprestado válido (VALOR LIBERADO): ")
        # argumentos[0]['label_6'].pack(pady=50, side='top', anchor='s')
        # argumentos[0]['label_imagem_1'].pack()

        def mostrar_pdf(label_imagem_1):
            # Abrir o PDF
            doc = fitz.open(f"{pasta}/consignado.pdf")
            
            # Carregar a página desejada
            pagina = doc.load_page(2)  # Página 2 (contagem começa do 0)
            
            # Converter a página para um pixmap (imagem)
            imagem_1 = pagina.get_pixmap()
            
            # Converter o pixmap para uma imagem PIL
            imagem_pil = Image.frombytes("RGB", [imagem_1.width, imagem_1.height], imagem_1.samples)
            
            # Definir as dimensões do widget (tamanho fixo de 50% de A4 em paisagem)
            largura_widget = 1227  # 50% da largura A4 em paisagem
            altura_widget = 868   # 50% da altura A4 em paisagem

            # Verificar se o widget tem dimensões válidas (não zero)
            if largura_widget > 0 and altura_widget > 0:
                # Calcular a proporção para redimensionar mantendo a proporção da imagem
                proporcao = min(largura_widget / imagem_pil.width, altura_widget / imagem_pil.height)
                nova_largura = int(imagem_pil.width * proporcao)
                nova_altura = int(imagem_pil.height * proporcao)

                # Verificar se as novas dimensões são válidas
                if nova_largura > 0 and nova_altura > 0:
                    # Redimensionar a imagem mantendo a proporção
                    imagem_redimensionada = imagem_pil.resize((nova_largura, nova_altura), Image.LANCZOS)

                    # Converter a imagem redimensionada para o formato que o Tkinter pode usar
                    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
                    
                    # Exibir a imagem no label
                    label_imagem_1.configure(image=imagem_tk, text="")
                    label_imagem_1.image = imagem_tk  # Manter a referência para evitar que a imagem seja descartada
                else:
                    print("Erro: as dimensões da imagem redimensionada não são válidas.")
            else:
                print("Erro: as dimensões do widget são inválidas.")

        print(contrato)
        
        def freeze_until_button():
            def gravar_valor_emprestado():
                argumentos[0]['novo_valor_emprestado'].set(float(entrada_verificar.get().replace(',', '.')))
                popup.destroy()
                # button.pack(pady=50)

            # Esta função congela a interface até que o botão seja pressionado
            print("Interface congelada!")
            popup = customtkinter.CTkToplevel()  # Cria uma janela pop-up
            popup.geometry(f'{argumentos[0]["largura"]}x{argumentos[0]["altura"]}+{argumentos[0]["x"]}+{argumentos[0]["y"]}')
            popup.title("Congelado")
            frame_1_pop = customtkinter.CTkFrame(popup)
            label_1_pop = customtkinter.CTkLabel(frame_1_pop, font=("Arial", 20))
            label_imagem_1 = customtkinter.CTkLabel(frame_1_pop, width=1753, height=1240)
            entrada_verificar = customtkinter.CTkEntry(
                frame_1_pop,
                placeholder_text="Informe o valor emprestado"
            )

            valor_emprestado_botao = customtkinter.CTkButton(
                frame_1_pop, text="alterar valor liberado", command=gravar_valor_emprestado, width=100
            )
            mostrar_pdf(label_imagem_1)
            argumentos[0]['draw_header'](frame_1_pop)
            frame_1_pop.pack(fill="both", expand=True)
            label_1_pop.configure(text=f"O contrato {contrato} está com valor emprestado incorreto para o cálculo, por favor informe um valor emprestado válido (VALOR LIBERADO): ")
            label_1_pop.pack()
            entrada_verificar.pack()
            valor_emprestado_botao.pack()
            label_imagem_1.pack()
            


            # button = customtkinter.CTkButton(frame_1_pop, text="Descongelar", command=popup.destroy)  # Botão para fechar o popup
            popup.wait_window()  # Congela a execução até que o popup seja fechado
            print("Interface desbloqueada!")

        freeze_until_button()

        valor_emprestado = float(argumentos[0]['novo_valor_emprestado'].get())
        taxa = np.round(calcular_taxa(parcelas, valor_parcela, valor_emprestado)*100,2)
        
    # Retorna os valores validados
    argumentos[0]['label_6'].configure(text="Valores regularizados")
    return valor_emprestado, taxa

def ler_pdf(out_folder, argumentos):
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
                        
                        valor_emprestado, taxa = verificar_dados(parcelas, valor_parcela, valor_emprestado, taxa, contrato, argumentos)
                        
                        # Calcular o valor de liquidação
                        valor_liquidacao = np.round(calcular_liquidacao(valor_parcela, meses_restantes, taxa), 2)
                        print(f"{taxa}")
                        # Adicionar informações ao filtro
                        dados_filtrados.append([contrato, banco, situacao, inicio_de_desconto, str(data_vencimento), valor_parcela, parcelas, meses_restantes, valor_emprestado, taxa, valor_liquidacao])
                        print("processamento concluído!")

def imprimir_resultados(out_folder):
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


def start_gui():
    customtkinter.set_appearance_mode(
        "System"
    )  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme(
        "blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"

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

    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()

            # configure window
            self.title("CustomTkinter complex_example.py")
            self.geometry(f"{largura}x{altura}+{x}+{y}")

            # configure grid layout (4x4)
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            # Definig the frames
            self.lista_de_frames = [
                customtkinter.CTkFrame(self),
                customtkinter.CTkFrame(self),
                customtkinter.CTkFrame(self),
                customtkinter.CTkFrame(self),
                customtkinter.CTkFrame(self),
                customtkinter.CTkFrame(self),
                customtkinter.CTkFrame(self)
            ]

            self.frame_atual = 0

            # Criar a variável result após a criação da janela
            self.result = customtkinter.StringVar()
            self.novo_valor_emprestado = customtkinter.StringVar()

            def selecionar_arquivo_pdf():
                global caminho_destino
                arquivo_pdf = customtkinter.filedialog.askopenfilename(
                    title="Selecione um arquivo PDF",
                    filetypes=[("Arquivos PDF", "*.pdf")],
                )

                if arquivo_pdf:
                    print(f"Arquivo selecionado: {arquivo_pdf}")
                    nome_da_pasta = (
                        gravar_texto()
                    )  # A pasta é criada e seu nome é retornado

                    if not os.path.exists(nome_da_pasta):
                        print(f"A pasta de destino não existe: {nome_da_pasta}")
                        return

                    caminho_destino = os.path.join(nome_da_pasta, "consignado.pdf")

                    try:
                        shutil.copy(arquivo_pdf, caminho_destino)
                        print(f"Arquivo copiado para: {caminho_destino}")
                    except Exception as e:
                        print(f"Ocorreu um erro ao copiar o arquivo: {e}")
                else:
                    print("Nenhum arquivo foi selecionado.")

            def gravar_texto():
                cpf = entrada.get()
                print(cpf)
                nome_da_pasta = str(cpf)
                if not len(nome_da_pasta):
                    nome_da_pasta = "saida"
                try:
                    os.makedirs(nome_da_pasta)
                    print(f"Pasta '{nome_da_pasta}' criada com sucesso!")
                except FileExistsError:
                    print(f"A pasta '{nome_da_pasta}' já existe.")
                self.result.set(nome_da_pasta)
                global first_table
                first_table = False
                cpf_botao.configure(state='disabled')
                global pasta
                pasta = nome_da_pasta
                return nome_da_pasta

            def gravar_valor_emprestado():
                valor_emprestado = entrada_verificar.get()
                print(valor_emprestado)
                self.novo_valor_emprestado.set(float(valor_emprestado))

            def executar_funções():
                global first_table
                if first_table == True:
                    out_folder = "padrao"
                else: 
                    out_folder = self.result.get()
                    print(out_folder)
                show_next_frame()
                ler_pdf(out_folder, argumentos_ler_pdf)                

            def imprimir_resultados_final():
                imprimir_resultados(self.result.get())
                show_next_frame()

            def encerrar():
                self.destroy()

            # Função para esconder todos os frames
            def hide_all_frames():
                for frame in self.lista_de_frames:
                    frame.pack_forget()

            # Função para exibir o próximo frame
            def show_next_frame():
                hide_all_frames()  # Esconde todos os frames
                self.frame_atual = (self.frame_atual + 1) % len(
                    self.lista_de_frames
                )  # Avança para o próximo frame (circular)
                self.lista_de_frames[self.frame_atual].pack(
                    fill="both", expand=True
                )  # Exibe o próximo frame
                if self.frame_atual <= 2:
                    forward_button = customtkinter.CTkButton(
                        self.lista_de_frames[self.frame_atual],
                        text="Next page",
                        command=show_next_frame
                    )  # Cria o botão "Next Page" para o novo frame
                if self.frame_atual == 3:
                    forward_button = customtkinter.CTkButton(
                        self.lista_de_frames[self.frame_atual],
                        text="Processar arquivo",
                        command=executar_funções,
                    )  # Cria o botão "Next Page" para o novo frame
                
                if self.frame_atual == 4:
                    forward_button = customtkinter.CTkButton(
                        self.lista_de_frames[self.frame_atual],
                        text="Next frame",
                        command=show_next_frame,
                    )  # Cria o botão "Next Page" para o novo frame

                if self.frame_atual == 5:
                    forward_button = customtkinter.CTkButton(
                        self.lista_de_frames[self.frame_atual],
                        text="Criar tabelas",
                        command=imprimir_resultados_final
                    )  # Cria o botão "Next Page" para o novo frame

                if self.frame_atual == 6:
                    forward_button = customtkinter.CTkButton(
                        self.lista_de_frames[self.frame_atual],
                        text="Encerrar programa",
                        command=encerrar,
                    )  # Cria o botão "Next Page" para o novo frame

                forward_button.pack(pady=200, side="bottom", anchor="n")


            # Função para desenhar as barrinhas no topo (cabeçalho)
            def draw_header(frame):
                canvas = customtkinter.CTkCanvas(frame, width=screen_width, height=75)
                canvas.pack()
                canvas.create_rectangle(
                    0, 0, screen_width, 25, fill="#e4ebf1"
                )  # Retângulo azul
                canvas.create_rectangle(
                    0, 25, screen_width, 50, fill="#11115c"
                )  # Retângulo vermelho
                canvas.create_rectangle(
                    0, 50, screen_width, 75, fill="#95a6ba"
                )  # Retângulo preto

            # Show the first frame initially
            self.lista_de_frames[0].pack(fill="both", expand=True)

            # --- Frame 1: Home Page ---
            draw_header(
                self.lista_de_frames[0]
            )  # Desenha o cabeçalho no primeiro frame
            label_1 = customtkinter.CTkLabel(
                self.lista_de_frames[0], text="Calculadora de Portabilidade", font=("Arial", 40)
            )
            label_1.pack(pady=300, side = "top", anchor = "s")

            # --- Frame 2: Identificação do cliente ---
            draw_header(self.lista_de_frames[1])  # Desenha o cabeçalho no segundo frame
            label_2 = customtkinter.CTkLabel(
                self.lista_de_frames[1], text="Digite o CPF", font=("Arial", 20)
            )
            label_2.pack(pady=20)
            
            # Campo de entrada (Entry)
            entrada = customtkinter.CTkEntry(self.lista_de_frames[1])
            entrada.pack()
            cpf_botao = customtkinter.CTkButton(
                self.lista_de_frames[1], text="Gravar cpf", command=gravar_texto
            )
            cpf_botao.pack()

            # --- Frame 3: Selecionar arquivo ---
            draw_header(
                self.lista_de_frames[2]
            )  # Desenha o cabeçalho no terceiro frame
            label_3 = customtkinter.CTkLabel(
                self.lista_de_frames[2], text="Anexar PDF", font=("Arial", 20)
            )
            label_3.pack(pady=20)
            selecionar_botao = customtkinter.CTkButton(
                self.lista_de_frames[2],
                text="Selecionar arquivo PDF",
                command=selecionar_arquivo_pdf,
            )
            selecionar_botao.pack()

            # --- Frame 4: Processar arquivo ---
            draw_header(self.lista_de_frames[3])  # Desenha o cabeçalho no quarto frame
            label_4 = customtkinter.CTkLabel(
                self.lista_de_frames[3], text="Processar arquivo", font=("Arial", 20)
            )
            label_4.pack(pady=20)

            # --- Frame 5: Correção de dados ---
            draw_header(self.lista_de_frames[4])  # Desenha o cabeçalho no quarto frame
            label_5 = customtkinter.CTkLabel(
                self.lista_de_frames[4], text="Correção de Dados", font=("Arial", 20)
            )
            label_5.pack(pady=20)

            label_6 = customtkinter.CTkLabel(
                self.lista_de_frames[4], font=("Arial", 20)
            )

            entrada_verificar = customtkinter.CTkEntry(
                self.lista_de_frames[4],
                placeholder_text="Informe o valor emprestado"
            )
            

            valor_emprestado_botao = customtkinter.CTkButton(
                self.lista_de_frames[4], text="alterar valor liberado", command=gravar_valor_emprestado, width=100
            )

            # --- Frame 6: Criar tabela ---
            draw_header(self.lista_de_frames[5])  
            label_7 = customtkinter.CTkLabel(
                self.lista_de_frames[5], text="Tabelas de valor de liquidação", font=("Arial", 20)
            ) 
            label_8 = customtkinter.CTkLabel(
                self.lista_de_frames[5], text=f"As tabelas estarão disponíveis, salvas, na pasta com CPF indicado", font=("Arial", 20)
            )                  
            label_7.pack(pady=20)  
            label_8.pack(pady=20)

            # --- Frame 7: Mostrar tabela e fechar programa ---
            draw_header(self.lista_de_frames[6])  
            label_10 = customtkinter.CTkLabel(
                self.lista_de_frames[6], text="Valores de liquidação atualizados", font=("Arial", 20)
            )
            label_10.pack(pady=20)



            # Cria o botão "Next Page" para o primeiro frame
            forward_button = customtkinter.CTkButton(
                self.lista_de_frames[self.frame_atual],
                text="Next page",
                command=show_next_frame,
            )

            forward_button.pack()#pady=250, side="bottom", anchor="n"
            argumentos_ler_pdf =  [
                {
                    'label_6': label_6,
                    'valor_emprestado_botao': valor_emprestado_botao,
                    'novo_valor_emprestado': self.novo_valor_emprestado,
                    'altura': altura,
                    'largura': largura,
                    'x': x,
                    'y': y,
                    'draw_header': draw_header,
                }
            ]

    app = App()
    app.mainloop()

start_gui()

#batata push