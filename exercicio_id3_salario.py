import math
import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib-cache"))

import matplotlib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def entropia(valores):
    total = len(valores)
    contagens = valores.value_counts()

    return -sum(
        (quantidade / total) * math.log2(quantidade / total)
        for quantidade in contagens
    )


def ganho_informacao(df_original, atributo, alvo):
    entropia_total = entropia(df_original[alvo])
    entropia_ponderada = 0

    for _, grupo in df_original.groupby(atributo):
        peso = len(grupo) / len(df_original)
        entropia_ponderada += peso * entropia(grupo[alvo])

    return entropia_total - entropia_ponderada


# 1. Dados de treinamento com a nova coluna Salario.
# Nesta tabela, Salario Baixo aparece nos casos em que o colaborador saiu.
data = {
    "NivelSatisfacao": ["Baixo", "Baixo", "Alto", "Alto", "Baixo", "Alto"],
    "NumeroProjetos": ["Muitos", "Muitos", "Poucos", "Muitos", "Poucos", "Poucos"],
    "Salario": ["Baixo", "Baixo", "Alto", "Alto", "Alto", "Alto"],
    "Saiu": ["Sim", "Sim", "Não", "Não", "Não", "Não"],
}

df_original = pd.DataFrame(data)

# 2. Calculo manual da entropia e do ganho de informacao.
atributos = ["NivelSatisfacao", "NumeroProjetos", "Salario"]
ganhos = {
    atributo: ganho_informacao(df_original, atributo, "Saiu")
    for atributo in atributos
}

print("--- Ganho de Informação ---")
print(f"Entropia inicial da classe Saiu: {entropia(df_original['Saiu']):.4f}")
for atributo, ganho in ganhos.items():
    print(f"{atributo}: {ganho:.4f}")
print(f"Atributo escolhido na raiz pelo ID3: {max(ganhos, key=ganhos.get)}")

# 3. Pre-processamento: codificacao categorica.
df = df_original.copy()
encoders = {}

for coluna in atributos + ["Saiu"]:
    encoder = LabelEncoder()
    df[coluna] = encoder.fit_transform(df[coluna])
    encoders[coluna] = encoder

X = df[atributos]
y = df["Saiu"]

# 4. Treinamento do modelo com criterio de entropia, equivalente ao ID3.
clf = DecisionTreeClassifier(criterion="entropy", random_state=42)
clf.fit(X, y)

print("\n--- Importância calculada pelo modelo ---")
for atributo, importancia in zip(atributos, clf.feature_importances_):
    print(f"{atributo}: {importancia:.4f}")

# 5. Teste de uma nova entrada.
nova_entrada = pd.DataFrame(
    [
        {
            "NivelSatisfacao": "Baixo",
            "NumeroProjetos": "Muitos",
            "Salario": "Baixo",
        }
    ]
)

nova_entrada_codificada = nova_entrada.copy()
for coluna in atributos:
    nova_entrada_codificada[coluna] = encoders[coluna].transform(
        nova_entrada_codificada[coluna]
    )

predicao = clf.predict(nova_entrada_codificada[atributos])
resultado = encoders["Saiu"].inverse_transform(predicao)

print("\n--- Simulador de Decisão ---")
print("Entrada: Satisfação Baixa, Muitos Projetos e Salário Baixo")
print(f"Resultado previsto: {resultado[0]}")

# 6. Visualizacao da arvore.
plt.figure(figsize=(10, 6))
plot_tree(
    clf,
    feature_names=atributos,
    class_names=[f"Saiu={classe}" for classe in encoders["Saiu"].classes_],
    filled=True,
    rounded=True,
)
plt.tight_layout()
plt.savefig("arvore_turnover_salario.png", dpi=160)

print("\nGráfico salvo em: arvore_turnover_salario.png")
