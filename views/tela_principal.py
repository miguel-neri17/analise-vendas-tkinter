import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.leitor_csv import LeitorCSV
from controllers.controlador import Controlador

def formatar_moeda(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"

class TelaPrincipal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Explorer Pro")
        self.root.geometry("1100x780")

        self.leitor = LeitorCSV()
        self.controlador = Controlador()
        self.df_atual = None

        self._criar_componentes()

    def _criar_componentes(self):

        frame_topo = tk.Frame(self.root, pady=10)
        frame_topo.pack(fill=tk.X, padx=10)

        tk.Button(frame_topo, text="Carregar CSV", command=self.carregar_csv_acao,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_topo, text="Gráfico: Quantidade",
                  command=lambda: self.gerar_grafico_acao("quantidade"),
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_topo, text="Gráfico: Faturamento",
                  command=lambda: self.gerar_grafico_acao("faturamento"),
                  bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_topo, text="Gráfico: Comparativo",
                  command=lambda: self.gerar_grafico_acao("comparativo"),
                  bg="#9C27B0", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_topo, text="Faturamento por Produto",
                  command=self.mostrar_analise_acao,
                  bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.frame_kpi = tk.LabelFrame(self.root, text="Indicadores", pady=6, padx=6)
        self.frame_kpi.pack(fill=tk.X, padx=10)

        linha1 = tk.Frame(self.frame_kpi)
        linha1.pack(fill=tk.X)
        linha2 = tk.Frame(self.frame_kpi)
        linha2.pack(fill=tk.X, pady=(4, 0))

        fonte = ("Arial", 10, "bold")
        self.lbl_registros = tk.Label(linha1, text="Total Registros: 0", font=fonte)
        self.lbl_registros.pack(side=tk.LEFT, padx=10)
        self.lbl_total = tk.Label(linha1, text="Total Vendido: R$ 0,00", font=fonte)
        self.lbl_total.pack(side=tk.LEFT, padx=10)
        self.lbl_qtd_total = tk.Label(linha1, text="Qtd. Total Vendida: 0", font=fonte)
        self.lbl_qtd_total.pack(side=tk.LEFT, padx=10)

        self.lbl_valor_medio = tk.Label(linha2, text="Valor Médio: R$ 0,00", font=fonte)
        self.lbl_valor_medio.pack(side=tk.LEFT, padx=10)
        self.lbl_mais_vendido = tk.Label(linha2, text="Mais Vendido: -", font=fonte)
        self.lbl_mais_vendido.pack(side=tk.LEFT, padx=10)
        self.lbl_diferentes = tk.Label(linha2, text="Produtos Diferentes: 0", font=fonte)
        self.lbl_diferentes.pack(side=tk.LEFT, padx=10)

        frame_filtro = tk.LabelFrame(self.root, text="Filtros (os preenchidos são combinados)", pady=6, padx=6)
        frame_filtro.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(frame_filtro, text="Produto:").pack(side=tk.LEFT, padx=(5, 2))
        self.entry_filtro = tk.Entry(frame_filtro, width=16)
        self.entry_filtro.pack(side=tk.LEFT, padx=2)

        tk.Label(frame_filtro, text="Valor unitário maior que:").pack(side=tk.LEFT, padx=(12, 2))
        self.entry_valor_min = tk.Entry(frame_filtro, width=10)
        self.entry_valor_min.pack(side=tk.LEFT, padx=2)

        tk.Label(frame_filtro, text="Quantidade maior que:").pack(side=tk.LEFT, padx=(12, 2))
        self.entry_qtd_min = tk.Entry(frame_filtro, width=10)
        self.entry_qtd_min.pack(side=tk.LEFT, padx=2)

        tk.Button(frame_filtro, text="Filtrar", command=self.filtrar_acao).pack(side=tk.LEFT, padx=(12, 4))
        tk.Button(frame_filtro, text="Limpar Filtros", command=self.limpar_filtros_acao).pack(side=tk.LEFT, padx=4)

        self.lbl_mensagem = tk.Label(self.root, text="", font=("Arial", 10, "italic"), fg="#C62828")
        self.lbl_mensagem.pack(fill=tk.X, padx=15)

        frame_tabela = tk.Frame(self.root, pady=10)
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10)

        colunas = ("Produto", "Quantidade", "Valor")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def carregar_csv_acao(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
        if caminho:
            self.carregar_arquivo(caminho)

    def carregar_arquivo(self, caminho):
        df = self.leitor.carregar(caminho)
        if df is None:
            messagebox.showerror("Erro", self.leitor.ultimo_erro or "Não foi possível ler o arquivo CSV.")
            return False

        self.df_atual = df
        self.limpar_campos_filtro()
        self.atualizar_interface(self.df_atual)
        messagebox.showinfo("Sucesso", "Arquivo CSV carregado com sucesso!")
        return True

    def atualizar_interface(self, df):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, linha in df.iterrows():
            self.tree.insert("", tk.END, values=list(linha))

        ind = self.controlador.calcular_indicadores(df)

        self.lbl_registros.config(text=f"Total Registros: {ind['registros']}")
        self.lbl_total.config(text=f"Total Vendido: {formatar_moeda(ind['total_vendido'])}")
        self.lbl_qtd_total.config(text=f"Qtd. Total Vendida: {ind['quantidade_total']}")
        self.lbl_valor_medio.config(text=f"Valor Médio: {formatar_moeda(ind['valor_medio'])}")
        if ind["produto_mais_vendido"] is None:
            self.lbl_mais_vendido.config(text="Mais Vendido: -")
        else:
            self.lbl_mais_vendido.config(
                text=f"Mais Vendido: {ind['produto_mais_vendido']} ({ind['qtd_produto_mais_vendido']} un.)")
        self.lbl_diferentes.config(text=f"Produtos Diferentes: {ind['produtos_diferentes']}")

        if df.empty:
            self.lbl_mensagem.config(text="Nenhum resultado encontrado para o filtro informado.")
        else:
            self.lbl_mensagem.config(text="")

    def limpar_campos_filtro(self):
        for campo in (self.entry_filtro, self.entry_valor_min, self.entry_qtd_min):
            campo.delete(0, tk.END)

    def filtrar_acao(self):
        if self.df_atual is None:
            messagebox.showwarning("Aviso", "Por favor, carregue um arquivo CSV primeiro!")
            return
        try:
            valor_min = self.controlador.converter_numero(self.entry_valor_min.get())
            qtd_min = self.controlador.converter_numero(self.entry_qtd_min.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Informe apenas números nos filtros de valor e quantidade.")
            return

        df_filtrado = self.controlador.filtrar(
            self.df_atual,
            nome=self.entry_filtro.get().strip(),
            valor_min=valor_min,
            qtd_min=qtd_min,
        )
        self.atualizar_interface(df_filtrado)

    def limpar_filtros_acao(self):
        self.limpar_campos_filtro()
        if self.df_atual is not None:
            self.atualizar_interface(self.df_atual)

    def mostrar_analise_acao(self):
        if self.df_atual is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV primeiro!")
            return

        analise = self.controlador.analisar_faturamento_por_produto(self.df_atual)

        janela = tk.Toplevel(self.root)
        janela.title("Faturamento por Produto")
        janela.geometry("720x320")

        colunas = list(analise.columns)
        tabela = ttk.Treeview(janela, columns=colunas, show="headings")
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=160, anchor=tk.CENTER)
        for _, linha in analise.iterrows():
            tabela.insert("", tk.END, values=(
                linha["Produto"],
                int(linha["Quantidade Total"]),
                formatar_moeda(linha["Valor Unitário"]),
                formatar_moeda(linha["Faturamento Total"]),
            ))
        tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.janela_analise = janela
        return janela

    def gerar_grafico_acao(self, tipo="quantidade"):
        if self.df_atual is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV para gerar o gráfico!")
            return
        if self.df_atual.empty:
            messagebox.showwarning("Aviso", "Não há dados para gerar o gráfico.")
            return

        fig = Figure(figsize=(7, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        if tipo == "quantidade":
            titulo_janela = "Gráfico de Quantidade Vendida por Produto"
            dados = self.controlador.dados_quantidade_por_produto(self.df_atual)
            ax.bar(dados.index, dados.values, color="#2196F3", edgecolor="black")
            ax.set_title("Quantidade Vendida por Produto")
            ax.set_xlabel("Produto")
            ax.set_ylabel("Quantidade Total")
            for i, v in enumerate(dados.values):
                ax.text(i, v, f"{v:g}", ha="center", va="bottom", fontsize=9)

        elif tipo == "faturamento":
            titulo_janela = "Gráfico de Faturamento Total por Produto"
            dados = self.controlador.dados_faturamento_por_produto(self.df_atual)
            ax.bar(dados.index, dados.values, color="#FF9800", edgecolor="black")
            ax.set_title("Faturamento Total por Produto")
            ax.set_xlabel("Produto")
            ax.set_ylabel("Faturamento (R$)")
            for i, v in enumerate(dados.values):
                ax.text(i, v, formatar_moeda(v), ha="center", va="bottom", fontsize=8)
            ax.margins(y=0.12)

        else:
            titulo_janela = "Gráfico Comparativo de Quantidade Vendida"
            dados, media = self.controlador.dados_comparativo_quantidade(self.df_atual)

            ordem = list(dados.index)[::-1]
            valores = list(dados.values)[::-1]
            ax.barh(ordem, valores, color="#9C27B0", edgecolor="black")
            ax.axvline(media, color="red", linestyle="--", label=f"Média: {media:.1f}")
            ax.set_title("Comparativo de Quantidade Vendida por Produto")
            ax.set_xlabel("Quantidade Total")
            ax.set_ylabel("Produto")
            for i, v in enumerate(valores):
                ax.text(v, i, f" {v:g}", va="center", fontsize=9)
            ax.legend()
            ax.margins(x=0.12)

        fig.tight_layout()

        janela = tk.Toplevel(self.root)
        janela.title(titulo_janela)
        janela.geometry("720x500")
        canvas = FigureCanvasTkAgg(fig, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ultima_janela_grafico = janela
        return janela

    def executar(self):
        self.root.mainloop()
