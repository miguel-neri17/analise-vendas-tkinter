# Análise de Vendas — Data Explorer Pro

Aplicativo desktop em **Python** com **Tkinter** para analisar dados de vendas a partir de um arquivo CSV. Você carrega a planilha, vê os indicadores principais, filtra os registros e gera gráficos, tudo em uma interface simples e sem precisar de internet.

## Funcionalidades

- **Carregar CSV**: escolha qualquer arquivo `.csv` de vendas pelo seletor de arquivos
- **Validação do arquivo**: o app avisa se o arquivo não existe, não pode ser lido, está sem alguma coluna obrigatória ou tem texto nas colunas de números
- **Indicadores (KPIs)**:
  - total de registros
  - total vendido (quantidade × valor)
  - quantidade total vendida
  - valor médio
  - produto mais vendido
  - quantidade de produtos diferentes
- **Filtros combinados** (os campos preenchidos funcionam juntos):
  - nome do produto (busca parcial, sem diferenciar maiúsculas e minúsculas)
  - valor unitário maior que
  - quantidade maior que
  - aceita decimais com vírgula ou ponto
- **Tabela de dados** com rolagem e botão **Limpar Filtros**
- **Faturamento por Produto**: janela com quantidade total, valor unitário e faturamento total de cada produto, ordenada do maior faturamento para o menor
- **Três gráficos** (Matplotlib):
  - *Quantidade*: barras com a quantidade vendida por produto
  - *Faturamento*: barras com o faturamento total por produto
  - *Comparativo*: barras horizontais de quantidade com uma linha de média

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3 | Linguagem principal |
| Tkinter / ttk | Interface gráfica |
| pandas | Leitura do CSV e cálculos |
| Matplotlib | Gráficos |

## Estrutura do projeto

O projeto segue o padrão **MVC**:

```
analise-vendas-tkinter/
├── main.py                      # Ponto de entrada do aplicativo
├── requirements.txt             # Dependências (pandas e matplotlib)
├── models/
│   └── leitor_csv.py            # Model: leitura e validação do CSV
├── controllers/
│   └── controlador.py           # Controller: cálculos, filtros e análises
├── views/
│   └── tela_principal.py        # View: interface Tkinter e gráficos
└── dados/
    └── vendas.csv               # Arquivo de exemplo para testar o app
```

## Como executar

### Pré-requisitos

- [Python 3](https://www.python.org/downloads/) com Tkinter (já vem no instalador oficial para Windows e macOS)
- No Linux, talvez seja preciso instalar o Tkinter separadamente, por exemplo: `sudo apt install python3-tk`

### Passo a passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/miguel-neri17/analise-vendas-tkinter.git
   cd analise-vendas-tkinter
   ```

2. (Opcional) Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o aplicativo:

   ```bash
   python main.py
   ```

## Como usar

1. Clique em **Carregar CSV** e selecione um arquivo. Para testar, use o `dados/vendas.csv` que já vem no projeto.
2. Veja os indicadores no painel **Indicadores**.
3. Use os **Filtros** (produto, valor mínimo e quantidade mínima) e clique em **Filtrar**. Para voltar a ver tudo, clique em **Limpar Filtros**.
4. Clique em **Faturamento por Produto** para abrir a tabela de faturamento.
5. Use os botões **Gráfico: Quantidade**, **Gráfico: Faturamento** e **Gráfico: Comparativo** para visualizar os dados.

## Formato do CSV

O arquivo precisa ter, no mínimo, estas três colunas (outras colunas são ignoradas):

| Coluna | Descrição |
|---|---|
| `Produto` | Nome do produto |
| `Quantidade` | Quantidade vendida (número) |
| `Valor` | Valor unitário do produto (número) |

Exemplo:

```csv
Produto, Quantidade, Valor
Notebook, 10, 4500
Mouse, 20, 190
Monitor, 15, 5000
Teclado, 40, 350
```

## Ideias para o futuro

- Exportar os resultados filtrados e os gráficos
- Suporte a datas, com análise de vendas por período
- Mais tipos de gráfico, como pizza e linha do tempo
- Gerar um executável (`.exe`) para distribuir o app

## Autor

**Miguel Neri** — estudante de Ciência de Dados

- GitHub: [@miguel-neri17](https://github.com/miguel-neri17)
- LinkedIn: [miguel-neri](https://www.linkedin.com/in/miguel-neri-a427b3420)
