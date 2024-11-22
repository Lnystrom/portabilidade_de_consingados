Claro! Aqui está um modelo de `README.md` baseado no conteúdo que você enviou:

---

# Portabilidade de Consignados

**Ferramenta para Facilitar a Portabilidade de Crédito Consignado para Beneficiários do INSS**

Este projeto tem como objetivo facilitar a análise e a gestão de empréstimos consignados para beneficiários do INSS, automatizando o processo de extração de dados, cálculos financeiros e geração de relatórios. A ferramenta utiliza bibliotecas poderosas de Python para extrair informações de contratos consignados, calcular taxas de juros, valores de liquidação e gerar relatórios detalhados.

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
- **Bibliotecas**: `Tkinter`, `screeninfo`
- Responsável pela interação com o usuário, permitindo a entrada do CPF, seleção de arquivos PDF e criação de pastas para armazenar os dados.
- A interface é criada com `Tkinter`, fornecendo uma experiência de usuário simples e eficiente para navegar entre as etapas do processo.

### 2. Processamento de Dados e Cálculos
- **Bibliotecas**: `pdfplumber`, `scipy.optimize`, `matplotlib`, `numpy`, `pandas`, `datetime`
- **Funções**:
  - **`calcular_taxa`**: Calcula a taxa de juros periódica usando o método de Newton-Raphson.
  - **`calcular_liquidacao`**: Calcula o valor de liquidação de um empréstimo, levando em consideração as parcelas restantes e a taxa de juros.
  - **Leitura de PDF**: Extração de dados de contratos consignados em formato PDF e validação dos dados antes de realizar cálculos.

## Como Usar

1. **Preparação**:
   - Certifique-se de ter o Python instalado (recomendado Python 3.7 ou superior).
   - Instale as dependências necessárias. Você pode fazer isso com o comando:
     ```bash
     pip install -r requirements.txt
     ```

2. **Executar o Sistema**:
   - Execute o arquivo `main.py` para abrir a interface gráfica.
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

1. **Tratamento de Dados Inconsistentes**:  
   Adicionar mais validações e verificações de consistência dos dados extraídos dos contratos, especialmente para situações em que o valor do empréstimo é zero ou inválido.

2. **Integração com Banco de Dados**:  
   Para escalar a solução, seria útil integrar a ferramenta com um banco de dados centralizado, permitindo o armazenamento e acesso rápido a informações históricas de contratos de diferentes clientes.

3. **Melhorias na Interface Gráfica**:  
   Aperfeiçoar a interface para incluir mais opções de visualização, como filtros por banco ou status dos contratos, e permitir a customização de relatórios.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento do sistema.
- **Tkinter**: Biblioteca para a criação da interface gráfica do usuário (GUI).
- **pdfplumber**: Para leitura e extração de dados de arquivos PDF.
- **Scipy**: Usado para otimização, incluindo o cálculo de taxas de juros através do método de Newton-Raphson.
- **Matplotlib**: Para gerar gráficos e visualizações.
- **Pandas**: Para manipulação e análise de dados.