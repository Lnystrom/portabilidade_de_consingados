import pdfplumber
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd



def calcular_cet(valor_emprestado, valor_total_pago, meses_restantes):
    # Cálculo do CET
    cet_mensal = ((valor_total_pago / valor_emprestado) ** (1 / meses_restantes)) - 1
    return cet_mensal * 100  # Retornando em percentual

def calcular_liquidacao(valor_emprestado, taxa_juros_mensal, meses_restantes):
    """
    Calcula o valor de liquidação de um empréstimo.
    
    :param valor_emprestado: Valor total emprestado (float).
    :param taxa_juros_mensal: Taxa de juros mensal (em percentual).
    :param meses_restantes: Número de meses restantes para pagamento (int).
    :return: Valor total a ser pago (float).
    """
    # Converter taxa de juros percentual para decimal
    taxa_juros_decimal = taxa_juros_mensal / 100
    
    # Calcular o valor de liquidação usando a fórmula do montante
    valor_liquidacao = valor_emprestado / ((1 + taxa_juros_decimal) ** meses_restantes)
    
    return valor_liquidacao

# Abrir o PDF com pdfplumber
with pdfplumber.open("consignado.pdf") as pdf:
    # Variável para armazenar o texto filtrado
    dados_filtrados = []

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
                    data_vencimento = linha[6].replace('\n', '') # Aqui deve estar a data no formato mm/yyyy
                    parcelas = int(linha[7].replace('\n', ''))    # Quantidade de parcelas
                    valor_emprestado = float(linha[9].replace('.', '').replace(',', '.').replace('R$', '').strip())  # Valor emprestado (index 9)

                    # Calcular o valor total pago considerando as parcelas
                    valor_total_pago = valor_emprestado + (valor_emprestado * 0.05 * parcelas)  # Exemplo: adicionando 5% do valor por parcela

                    # Calcular o CET mensal
                    meses_restantes = (datetime.strptime(data_vencimento, '%m/%Y') - datetime.strptime(data_inclusao, '%d/%m/%y')).days // 30
                    cet_mensal = round(calcular_cet(valor_emprestado, valor_total_pago, meses_restantes), 2)

                     # Calcular o valor de liquidação
                    valor_liquidacao = round(calcular_liquidacao(valor_emprestado, cet_mensal, meses_restantes), 2)

                    # Adicionar informações ao filtro
                    dados_filtrados.append([contrato, banco, situacao, data_inclusao, str(data_vencimento), parcelas, valor_emprestado, cet_mensal, valor_liquidacao])

# Imprimir o cabeçalho da tabela original
cabecalho_original = ['Número do Contrato', 'Banco de Origem', 'Situação', 'Data de Inclusão', 'Data de Vencimento', 'Parcelas', 'Valor Emprestado', 'CET Mensal (%)', 'Valor de Liquidação']
print(f"\nTabela Original:")
print(f"{cabecalho_original[0]:<20} {cabecalho_original[1]:<30} {cabecalho_original[2]:<10} {cabecalho_original[3]:<15} {cabecalho_original[4]:<15} {cabecalho_original[5]:<10} {cabecalho_original[6]:<15} {cabecalho_original[7]:<15}{cabecalho_original[8]:<6}")

# Imprimir o resultado da tabela original
for item in dados_filtrados:
    print(f"{item[0]:<20} {item[1]:<30} {item[2]:<10} {item[3]:<15} {item[4]:<15} {item[5]:<10} R${item[6]:<15.2f} {item[7]:<15.2f} R${item[8]:<20.2f}")


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