import csv
import streamlit as st
import plotly.express as pe
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_history(filename):
    # csv file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        history = list(reader)

    return history


def plot(title, filename, parent):
    parent.markdown(title)
    columns = ['Fitness (min)', 'Gerações', 'População', 'Progenitores', 'Elitismo', 'Perc. Mutação', 'mut']
    history = load_history(filename)
    df = pd.DataFrame(history, 
        columns=columns
    )

    df = df.drop(axis='columns', columns=['mut'] )
    df = df.drop(axis='rows', index=[0])

    df['Fitness (min)'] = df['Fitness (min)'].apply(lambda x : int(x) * -1)


    for col in df.columns:
        # scaler = MinMaxScaler((0, 100))
        # df_normalized = pd.DataFrame(scaler.fit_transform(df[col]), columns=df.columns)
        fig = pe.line(df[col], markers=True)
        parent.markdown("### " + col)
        parent.plotly_chart(fig, use_container_width=True)


def main():
    st.title('Histórico')
    left, right = st.columns(2)
    plot("## Primeira rodada", 'history_first_rounds.csv', left)
    plot("## Segunda rodada", 'history_second_rounds.csv', right)


if __name__ == '__main__':
    main()