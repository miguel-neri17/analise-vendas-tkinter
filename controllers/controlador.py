import pandas as pd

class Controlador:

    @staticmethod
    def _valido(df):
        return (
            df is not None
            and not df.empty
            and "Quantidade" in df.columns
            and "Valor" in df.columns
        )

    @staticmethod
    def converter_numero(texto):
        texto = (texto or "").strip()
        if texto == "":
            return None
        return float(texto.replace(",", "."))

    def calcular_total_registros(self, df):
        if df is not None:
            return len(df)
        return 0

    def calcular_soma_vendas(self, df):
        if self._valido(df):
            return (df["Quantidade"] * df["Valor"]).sum()
        return 0

    def calcular_quantidade_total(self, df):
        if self._valido(df):
            return int(df["Quantidade"].sum())
        return 0

    def calcular_valor_medio(self, df):
        if self._valido(df):
            return df["Valor"].mean()
        return 0

    def produto_mais_vendido(self, df):
        if self._valido(df):
            por_produto = df.groupby("Produto")["Quantidade"].sum()
            return por_produto.idxmax(), int(por_produto.max())
        return None, 0

    def produto_maior_valor(self, df):
        if self._valido(df):
            linha = df.loc[df["Valor"].idxmax()]
            return linha["Produto"], linha["Valor"]
        return None, 0

    def contar_produtos_diferentes(self, df):
        if self._valido(df):
            return int(df["Produto"].nunique())
        return 0

    def calcular_indicadores(self, df):
        nome, qtd = self.produto_mais_vendido(df)
        return {
            "registros": self.calcular_total_registros(df),
            "total_vendido": self.calcular_soma_vendas(df),
            "quantidade_total": self.calcular_quantidade_total(df),
            "valor_medio": self.calcular_valor_medio(df),
            "produto_mais_vendido": nome,
            "qtd_produto_mais_vendido": qtd,
            "produtos_diferentes": self.contar_produtos_diferentes(df),
        }

    def filtrar_por_produto(self, df, nome_produto):
        if df is not None and nome_produto:
            return df[df["Produto"].str.contains(nome_produto, case=False, na=False, regex=False)]
        return df

    def filtrar_por_valor_minimo(self, df, valor_min):
        if df is not None and valor_min is not None:
            return df[df["Valor"] > valor_min]
        return df

    def filtrar_por_quantidade_minima(self, df, qtd_min):
        if df is not None and qtd_min is not None:
            return df[df["Quantidade"] > qtd_min]
        return df

    def filtrar(self, df, nome=None, valor_min=None, qtd_min=None):
        resultado = self.filtrar_por_produto(df, nome)
        resultado = self.filtrar_por_valor_minimo(resultado, valor_min)
        resultado = self.filtrar_por_quantidade_minima(resultado, qtd_min)
        return resultado

    def analisar_faturamento_por_produto(self, df):
        colunas = ["Produto", "Quantidade Total", "Valor Unitário", "Faturamento Total"]
        if not self._valido(df):
            return pd.DataFrame(columns=colunas)

        base = df.copy()
        base["Faturamento"] = base["Quantidade"] * base["Valor"]

        analise = (
            base.groupby("Produto")[["Quantidade", "Faturamento"]]
            .sum()
            .reset_index()
        )
        analise["Valor Unitário"] = analise["Faturamento"] / analise["Quantidade"]
        analise = analise.rename(
            columns={"Quantidade": "Quantidade Total", "Faturamento": "Faturamento Total"}
        )
        analise = analise[colunas].sort_values("Faturamento Total", ascending=False)
        return analise.reset_index(drop=True)

    def dados_quantidade_por_produto(self, df):
        if not self._valido(df):
            return pd.Series(dtype=float)
        return df.groupby("Produto")["Quantidade"].sum()

    def dados_faturamento_por_produto(self, df):
        analise = self.analisar_faturamento_por_produto(df)
        return analise.set_index("Produto")["Faturamento Total"]

    def dados_comparativo_quantidade(self, df):
        serie = self.dados_quantidade_por_produto(df).sort_values(ascending=False)
        media = serie.mean() if not serie.empty else 0
        return serie, media
