from scipy.optimize import fsolve

# Definindo os parâmetros
PMT = 13.33  # valor da parcela
n = 84      # número de parcelas
VP = 1623.72  # valor emprestado

# Definindo a função para encontrar a raiz
def taxa_juros(r):
    return VP - (PMT * (1 - (1 + r)**-n) / r)

# Estimando a taxa de juros
r_estimada = fsolve(taxa_juros, 0.01)[0]  # Começando com uma estimativa de 1% ao mês

# Convertendo para percentual
taxa_juros_percentual = r_estimada * 100
print(f'Taxa de juros mensal: {taxa_juros_percentual:.2f}%')