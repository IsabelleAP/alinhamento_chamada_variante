import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar arquivo anotado pelo VEP

arquivo = "../05_anotacao_variante/databases/Art_vep.tsv"

# O arquivo VEP possui linhas de comentário (#)
# Precisa capturar o cabeçalho correto
with open(arquivo) as f:
    for linha in f:
        if linha.startswith("#") and not linha.startswith("##"):
            cabecalho = linha.strip().lstrip("#").split("\t")
            break

vep = pd.read_csv(arquivo, sep="\t", comment="#", names=cabecalho)
print(vep.head())
print(vep.columns)

# 2. Quantas variantes possuem registro no ClinVar?

variantes_conhecidas = (vep["clinvar_CLNSIG"] != "-").sum()
variantes_novas = (vep["clinvar_CLNSIG"] == "-").sum()
total_variantes = len(vep)

print("\nResumo ClinVar")
print(f"Total de variantes: {total_variantes}")
print(f"Variantes conhecidas: {variantes_conhecidas}")
print(f"Variantes sem registro: {variantes_novas}")


# 3. Qual o significado clínico das variantes conhecidas?

clinvar = vep[vep["clinvar_CLNSIG"] != "-"]["clinvar_CLNSIG"].value_counts()
print("\nClassificação clínica das variantes:")
print(clinvar)

# 4. Impacto funcional das variantes

impacto_variantes = vep["IMPACT"].value_counts()
print("\nImpacto funcional das variantes:")
print(impacto_variantes)

# 5. Genes mais afetados

genes_mais_afetados = vep["Gene"].value_counts().head(10)

print("\nTop 10 genes com mais variantes:")
print(genes_mais_afetados)

# 6. Variantes potencialmente mais relevantes
variantes_relevantes = vep[vep["IMPACT"].isin(["HIGH", "MODERATE"])]
print("\nVariantes com impacto potencialmente relevante:")
print(variantes_relevantes.head())

# 7. Gráfico: classificação clínica no ClinVar
ax = clinvar.plot(kind="bar", figsize=(8,6), color="green")
ax.set_title("Classificação clínica das variantes (ClinVar)")
ax.set_xlabel("Categoria clínica")
ax.set_ylabel("Número de variantes")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("clinvar_plot.png", dpi=300, bbox_inches="tight")

# 8. Distribuição das variantes ao longo do cromossomo
# Extrair posição genômica da coluna Location
vep["posicao"] = vep["Location"].str.split(":").str[1].str.split("-").str[0].astype(int)
fig, ax = plt.subplots(figsize=(8,5))
ax.hist(vep["posicao"], bins=50, color="green")
ax.set_title("Distribuição das variantes no cromossomo 20")
ax.set_xlabel("Posição genômica")
ax.set_ylabel("Número de variantes")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("distribuicao_variantes_chr20.png", dpi=300, bbox_inches="tight")
plt.show()
