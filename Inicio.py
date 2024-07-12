import json
import os
import streamlit as st
import plotly.express as pe

def plot_run(run_data, title):
    st.markdown(f'## {title}')
    cols = st.columns(2)
    def plot_turn(turn, fitness, parent_node):
        parent_node.markdown(turn)

        parent_node.markdown('#### Evolução de fitness')
        fig = pe.line(
            x=list(range(1, len(fitness) + 1)),
            y=list(fitness),
            labels={'x': 'Geração', 'y': 'Fitness'}
        )
        fig.update_layout(
        uniformtext_minsize=18, uniformtext_mode='hide',
        legend_font_size=18)
        parent_node.plotly_chart(fig, use_container_width=True)

    plot_turn(
        '### Primeira rodada',
        run_data['first_run']['fitness'],
        cols[0]
    )
    plot_turn(
        '### Segunda rodada',
        run_data['second_run']['fitness'],
        cols[1]
    )


def plot_runs_data(data):
    runs_data = data['runs']

    for i, run in enumerate(runs_data):
        plot_run(run, 'Passagem ' + str(i + 1))


def show_configurations(data):
    def configs(conf_data, parent, title):
        parent.markdown(f'## {title}')
        cols = parent.columns(2)
        cols[0].metric('Número de pais', conf_data['num_parents_mating'])
        cols[1].metric('Elitismo', conf_data['keep_elitism'])
        cols[0].metric('Porcentagem de mutação', conf_data['mutation_percent_genes'])
        cols[1].metric('Tipo de mutação', conf_data['mutation_type'])

    cols = st.columns(2)
    fr = data['first_run_config']
    configs(fr, cols[0], 'Configurações da primeira rodada')
    sr = data['second_run_config']
    configs(sr, cols[1], 'Configurações da segunda rodada')


def app():
    file_list = os.listdir('reports')
    selected_file = st.selectbox('Select a file', file_list)
    
    file_data = {}
    with open(f'reports/{selected_file}', 'r') as f:
        file_data = json.load(f)

    show_configurations(file_data)
    plot_runs_data(file_data)


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    app()
