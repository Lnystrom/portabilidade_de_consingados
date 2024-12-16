
# Portabilidade de Consignados

**Ferramenta para Facilitar a Portabilidade de Crédito Consignado para Beneficiários do INSS**

Este projeto tem como objetivo facilitar a análise e a gestão de empréstimos consignados para beneficiários do INSS, automatizando o processo de extração de dados, cálculos financeiros e geração de relatórios. A ferramenta utiliza bibliotecas de Python para extrair informações de contratos consignados, calcular taxas de juros, valores de liquidação e gerar relatórios detalhados.

## Instalação
Basta baixar o arquivo executável clicando [nesse link](https://drive.google.com/uc?export=download&id=chOCXt7ZGDe0lU9ah-nV8U8MG5_XB).

## Funcionalidades Principais

1. **Extração de Dados de Contratos em PDF**  
   A ferramenta usa a biblioteca `pdfplumber` para ler automaticamente arquivos PDF de contratos consignados e extrair as informações necessárias de forma eficiente, evitando a inserção manual de dados.

2. **Cálculo de Taxa de Juros**  
   A função `calcular_taxa` utiliza o método de Newton-Raphson para encontrar a taxa de juros periódica com base nos valores de empréstimo e parcelas, proporcionando cálculos precisos e rápidos.

3. **Cálculo de Valor de Liquidação**  
   Com a função `calcular_liquidacao`, o sistema calcula o valor presente das parcelas restantes de um empréstimo, levando em consideração a taxa de juros e o número de parcelas pendentes. Isso permite uma análise precisa do saldo devedor.

4. **Geração de Relatórios e Gráficos**  
   A ferramenta gera gráficos e tabelas com dados financeiros extraídos dos contratos, oferecendo uma visualização clara das informações. Além disso, permite a exportação dos relatórios para arquivos `.csv` ou imagens, facilitando o compartilhamento e documentação.

## Estrutura do Projeto

A estrutura do código é organizada em duas partes principais:

### 1. Interface Gráfica (GUI)
- **Bibliotecas**: `customtkinter`, `fitz`, `PIL` e `webbrowser`
- Responsável pela interação com o usuário, permitindo a entrada do CPF, seleção de arquivos PDF e criação de pastas para armazenar os dados.
- A interface é criada com `customtkinter`, fornecendo uma experiência de usuário simples e eficiente para navegar entre as etapas do processo.


### 2. Processamento de Dados e Cálculos

#### **Bibliotecas Utilizadas**

- `pdfplumber`: Extração de dados de contratos em PDF.
- `scipy.optimize`: Método de otimização para cálculo da taxa de juros (Newton-Raphson).
- `matplotlib`: Visualização gráfica.
- `numpy`: Operações numéricas.
- `pandas`: Manipulação de dados.
- `datetime`: Manipulação de datas.

## Como Usar
---
1. **Preparação**:
   - Certifique-se de não retirar o executável de dentro da pasta em que veio

2. **Executar o Sistema**:
   - Execute o arquivo `Calculadora de Portabilidades.exe` para abrir a interface gráfica.
   - Insira o CPF do cliente e clique em "Criar pasta" para armazenar os dados.
   - Selecione o arquivo PDF do contrato consignado e clique em "Anexar Extrato".
   - A ferramenta processará os dados do contrato, realizará os cálculos financeiros e exibirá o valor de liquidação e outras informações importantes.
   - Ao final, o sistema gerará um relatório detalhado, exportando os dados para uma pasta de saída.

## Exemplo de Uso

Após executar a ferramenta, a interface gráfica solicitará que o usuário forneça o CPF e o arquivo PDF do contrato consignado. A ferramenta processará automaticamente o arquivo e exibirá informações como:

- Valor do empréstimo
- Valor das parcelas
- Taxa de juros
- Valor de liquidação do contrato

Esses dados podem ser exportados para relatórios ou analisados diretamente na interface.

## Oportunidades de Melhoria

Atualmente, o sistema lida bem com a extração de dados, mas algumas melhorias podem ser feitas:

1. **Integração com Banco de Dados**:  
   Para escalar a solução, seria útil integrar a ferramenta com um banco de dados centralizado, permitindo o armazenamento e acesso rápido a informações históricas de contratos de diferentes clientes.
