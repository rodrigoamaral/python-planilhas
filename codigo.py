import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcular_idade(data_nasc):
    return (pd.Timestamp('now') - data_nasc) / np.timedelta64(1, "Y")

df  = pd.read_excel("data/funcionarios.xlsx")
df["Data de Nascimento"] = pd.to_datetime(df["Data de Nascimento"], format="%d/%m/%Y")
df["Idade"] = df["Data de Nascimento"].apply(calcular_idade).astype("int")
df = df.set_index("Matrícula")

df_cursos = pd.read_excel("data/cursos.xlsx")

df_realizados = pd.read_excel("data/cursos_realizados.xlsx")
df_realizados["Data de conclusão"] = pd.to_datetime(df_realizados["Data de conclusão"], format="%d/%m/%Y")

df_consolidado = pd.merge(df_realizados, df_cursos, on="Curso")
df_consolidado = df_consolidado.drop(columns=["ID"])

df_total_horas_funcionario = df_consolidado.groupby("Funcionário").sum()

meta = 80
df_total_horas_funcionario["Cumpriu meta"] = df_total_horas_funcionario["Carga Horária"] >= meta
df_total_horas_funcionario.reset_index(inplace=True)

df_horas_por_ano = df_consolidado.groupby(
    [
        df_consolidado["Data de conclusão"].dt.year.rename("ano"), 
        df_consolidado["Data de conclusão"].dt.month.rename("mes")
    ]
).sum()


fig_horas_por_ano = df_horas_por_ano.plot(kind="bar").get_figure()
fig_horas_por_ano.savefig("out/horas_por_ano.png")

fig_total_horas_funcionario = df_total_horas_funcionario.groupby("Cumpriu meta").count().plot.pie(
    y="Carga Horária", 
    title="Cumprimento da Meta",
    labels=["Não", "Sim"],
    explode=(0, 0.075),
    shadow=True,
    autopct="%1.1f%%"
).get_figure()

fig_total_horas_funcionario.savefig("out/total_horas_funcionario.png")

df_total_horas_funcionario.to_csv("out/horas-treinamento.csv", sep=";", index=False)
df_total_horas_funcionario.to_excel("out/horas-treinamento.xlsx")

