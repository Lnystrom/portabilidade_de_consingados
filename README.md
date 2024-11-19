
# Portabilidade de Consignados

**Ferramenta para Facilitar a Portabilidade de Crédito INSS**

Este projeto destina-se a simplificar o processo de portabilidade de crédito consignado para beneficiários do INSS. Utilizando automação para extração de dados e cálculos financeiros, a ferramenta facilita a análise e a gestão de empréstimos consignados, reduzindo o tempo e o esforço de cálculos complexos para funcionários.

## Funcionalidades Principais

1. **Extração de Dados de PDF**: Utilizando a biblioteca `pdfplumber`, o sistema lê e processa automaticamente dados de contratos a partir de arquivos PDF, evitando a inserção manual de dados.
2. **Cálculo de Taxa de Juros**: A função `calcular_taxa` emprega o método Newton-Raphson para encontrar a taxa de juros periódica com base nos valores presentes dos empréstimos e das parcelas.
3. **Cálculo de Valor de Liquidação**: A função `calcular_liquidacao` determina o valor presente das parcelas restantes, utilizando a taxa de juros e o número de parcelas pendentes, permitindo uma análise precisa do saldo devedor.
4. **Geração de Relatórios e Tabelas**: Gera gráficos e tabelas detalhados para visualização dos dados financeiros, exportando relatórios como imagens e arquivos `.csv` para fácil compartilhamento e documentação.

## Estrutura do Projeto

A estrutura básica do código e principais métodos utilizados incluem:

- **Bibliotecas Utilizadas**:
  - `dateutil.relativedelta`: Para calcular a diferença de tempo entre datas.
  - `pdfplumber`: Para extração de dados de arquivos PDF.
  - `datetime` e `calendar`: Para manipulação e formatação de datas.
  - `matplotlib` e `pandas`: Para visualização e organização dos dados em tabelas e gráficos.
  - `scipy.optimize` e `numpy`: Para cálculos financeiros avançados, incluindo o método Newton-Raphson para cálculo de taxas.

- **Funções Principais**:
  - **`calcular_taxa`**: Calcula a taxa de juros periódica com base em parâmetros fornecidos, usando o método de Newton-Raphson para solucionar a função de valor presente dos pagamentos.
  - **`calcular_liquidacao`**: Calcula o valor de liquidação de um empréstimo com base no valor presente das parcelas restantes, usando uma taxa de juros periódica.
  - **Leitura e Extração de PDF**: Extrai dados de contratos ativos, filtra informações relevantes e calcula o valor de liquidação para cada contrato identificado.

## Importância da Automação

Automatizar o processo de extração de dados e cálculos financeiros de portabilidade é essencial para bancos e outras instituições financeiras, especialmente em tarefas repetitivas e de alta precisão. Esta ferramenta:

- **Aumenta a eficiência operacional** ao reduzir o tempo necessário para extrair e processar dados.
- **Minimiza erros humanos** em cálculos financeiros complexos.
- **Proporciona análises financeiras rápidas e precisas** para tomada de decisões informadas, seja para renegociações de empréstimos ou portabilidade para outras instituições.

## Exemplo de Uso

Para utilizar esta ferramenta, execute o código junto a um arquivo PDF em sua pasta contendo os dados dos contratos consignados. O sistema processará as informações e retornará um relatório com a taxa de juros, valor presente, parcelas restantes, e um gráfico resumido dos dados processados sem a necessidade de inputs.

---

## Oportunidades de Melhoria e Propostas Futuras

Atualmente, o sistema enfrenta alguns desafios relacionados à inconsistência dos dados de entrada, especialmente para alguns consignados que apresentam valor emprestado como `R$ 0`. Essa informação incorreta dificulta a interpretação dos dados e afeta a precisão dos cálculos financeiros. 

### Propostas para Melhorias Futura

1. **Tratamento de Dados Inconsistentes**:
   - Implementar verificações de qualidade de dados para identificar e tratar registros com valor emprestado `R$ 0` ou outras inconsistências antes de iniciar os cálculos. Essa medida poderia incluir a adição de regras de validação e notificações sobre dados incompletos ou incorretos.

2. **Integração com Banco de Dados**:
   - Planeja-se integrar o algoritmo a uma base de dados centralizada, permitindo que o sistema fique disponível para toda a rede de agências. Essa melhoria possibilitará o armazenamento seguro de históricos e o acesso em tempo real a cálculos financeiros, facilitando o uso e a atualização dos dados pelos funcionários de diversas unidades.

Essas melhorias visam aumentar a robustez, confiabilidade e escalabilidade da ferramenta, tornando-a um recurso eficiente e acessível para a rede de agências na análise de portabilidade de crédito consignado.