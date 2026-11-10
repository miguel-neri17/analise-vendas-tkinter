import os

import pandas as pd

class LeitorCSV:

    COLUNAS_OBRIGATORIAS = ["Produto", "Quantidade", "Valor"]

    def __init__(self):

        self.ultimo_erro = None

    def carregar(self, caminho_arquivo):
        self.ultimo_erro = None

        if not caminho_arquivo or not os.path.isfile(caminho_arquivo):
            self.ultimo_erro = "Arquivo não encontrado."
            return None

        try:

            df = pd.read_csv(caminho_arquivo, skipinitialspace=True)
        except Exception as e:
            self.ultimo_erro = f"Não foi possível ler o arquivo: {e}"
            return None

        df.columns = [str(c).strip() for c in df.columns]

        faltando = [c for c in self.COLUNAS_OBRIGATORIAS if c not in df.columns]
        if faltando:
            self.ultimo_erro = (
                "Arquivo inválido. Colunas obrigatórias ausentes: "
                + ", ".join(faltando)
            )
            return None

        df = df[self.COLUNAS_OBRIGATORIAS].copy()
        df["Produto"] = df["Produto"].astype(str).str.strip()

        for coluna in ("Quantidade", "Valor"):
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

        if df[["Quantidade", "Valor"]].isna().any().any():
            self.ultimo_erro = (
                "Arquivo inválido. As colunas Quantidade e Valor devem conter "
                "apenas números."
            )
            return None

        return df
