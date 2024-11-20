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

from gui import start_gui

def calcular_taxa(n_periodos, pmt, valor_presente, chute_inicial=0.01):
    """
    Calcula a taxa de juros periódica usando o método de Newton-Raphson.
    
    :param n_periodos: Número total de períodos (parcelas)
    :param pmt: Valor da parcela paga em cada período
    :param valor_presente: Valor do empréstimo inicial
    :param chute_inicial: Estimativa inicial para a taxa de juros
    :return: Taxa de juros periódica ou None se não for possível calcular
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
        taxa = fsolve(funcao_taxa, chute_inicial, maxfev=1000)  # Aumentar maxfev se necessário
        return taxa if taxa > 0 else None  # Retorna None se a taxa for negativa
    except Exception as e:
        print(f"Erro: {e}")
        return None

def calcular_liquidacao(valor_parcela, meses_restantes, taxa_juros_mensal):
    """
    Calcula o valor de liquidação de um empréstimo considerando o valor presente das parcelas restantes.
    
    :param valor_parcela: Valor da parcela mensal (float).
    :param meses_restantes: Número de meses restantes para pagamento (int).
    :param taxa_juros_mensal: Taxa de juros mensal (em percentual).
    :return: Valor total a ser pago (float).
    """
    # Converter taxa de juros percentual para decimal
    taxa_juros_decimal = taxa_juros_mensal / 100
    
    # Calcular o valor presente das parcelas restantes
    valor_presente = 0
    for i in range(1, meses_restantes + 1):
        valor_presente += valor_parcela / ((1 + taxa_juros_decimal) ** i)
    
    return valor_presente

dados_filtrados = []

out_file = start_gui()
print("Arquivo:", out_file)


with pdfplumber.open(out_file) as pdf:
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
                    # Calcular o valor de liquidação
                    valor_liquidacao = np.round(calcular_liquidacao(valor_parcela, meses_restantes, taxa), 2)

                    # Adicionar informações ao filtro
                    dados_filtrados.append([contrato, banco, situacao, inicio_de_desconto, str(data_vencimento), valor_parcela, parcelas, meses_restantes, valor_emprestado, taxa, valor_liquidacao])
                    print("processamento concluído!")

# Imprimir o cabeçalho da tabela original
cabecalho_original = ['Número do Contrato', 'Banco de Origem', 'Situação', 'Início de Desconto', 'Data de Vencimento', 'PMT(R$)',  'Parcelas','Meses Restantes', 'Valor Emprestado (R$)', 'Taxa Original (%)', 'Valor de Liquidação(R$)']
# print(f"{cabecalho_original[0]:<20} {cabecalho_original[1]:<30} {cabecalho_original[2]:<10} {cabecalho_original[3]:<15} {cabecalho_original[4]:<15} {cabecalho_original[5]:<10} {cabecalho_original[6]:<15} {cabecalho_original[7]:<15}{cabecalho_original[8]:<6}{cabecalho_original[9]:<6}{cabecalho_original[10]:<6}")

# Imprimir o resultado da tabela original
# for item in dados_filtrados:
#     print(f"{item[0]:<20} {item[1]:<30} {item[2]:<10} {item[3]:<15} {item[4]:<15} {item[5]:<10} {item[6]:<15.2f} {item[7]:<15.2f} {item[8]:<20.2f}{round(item[9], 2):<20}{item[10]:<20.2f}")

# Criar DataFrame com os dados
df = pd.DataFrame(dados_filtrados, columns=cabecalho_original)
df.to_csv("tabela_liquidacao.csv", index=False)

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
plt.savefig("tabela_liquidacao.png", bbox_inches='tight', dpi=300)

# trocar vencimento por parcelas restantes