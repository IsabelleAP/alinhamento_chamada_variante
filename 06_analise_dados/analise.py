import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

arquivo = "../05_anotacao_variante/databases/Art_vep.tsv"

with open(arquivo) as f:
    for line in f:
        if line.startswith("#") and not line.startswith("##"):
            header = line.strip().lstrip("#").split("\t")
            break

vep = pd.read_csv(arquivo, sep="\t", comment="#", names=header)

print(vep.head())
print(vep.columns)

impact = vep["IMPACT"].value_counts()
gene = vep["Gene"].value_counts().head(10)
filtro = vep[vep["IMPACT"].isin(["HIGH", "MODERATE"])]
clinvar = vep[vep["clinvar_CLNSIG"] != "-"]["clinvar_CLNSIG"].value_counts()
conhecidas = (vep["clinvar_CLNSIG"] != "-").sum()
total = len(vep)

print(f"{conhecidas} de {total} variantes possuem registro no ClinVar")
print(impact)
print(gene)
print(filtro)
print(clinvar)

### Gráfico
ax = clinvar.plot(kind="bar", figsize=(8,10), color="green")
plt.title("Registro no Clinvar")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig("clinvar_plot.png", bbox_inches="tight", dpi=300)