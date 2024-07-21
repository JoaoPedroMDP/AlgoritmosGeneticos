import json
from time import strftime
import streamlit as st
import plotly.express as pe
from einstein import main as einstein_main
import csv

DATE_TIME_STR = strftime("%Y-%m-%d_%H-%M-%S")
HISTORY_FILE = 'history_round_{}.csv'

def plot_run(rounds_data):
    def plot_turn(turn, data, parent_node):
        parent_node.markdown(turn)
        cols = parent_node.columns(2)
        parent_node.markdown('#### Primeiros erros das últimas gerações')
        parent_node.write(", " .join([str(x) for x in data['last_ten_first_errors']]))

        cols[0].markdown('#### Evolução de fitness')
        fig = pe.line(
            x=list(range(1, len(data['fitness']) + 1)),
            y=list(data['fitness']),
            labels={'x': 'Geração', 'y': 'Fitness'}
        )
        fig.update_layout(
        uniformtext_minsize=18, uniformtext_mode='hide',
        legend_font_size=18)
        cols[0].plotly_chart(fig, use_container_width=True)
        
        cols[1].markdown('#### Ocorrências de fitnesses')
        fig = pe.line(
            x=list(data['occurrences'].keys()),
            y=list(data['occurrences'].values()),
            labels={'x': 'Valores', 'y': 'Ocorrências'}
        )
        fig.update_layout(
        uniformtext_minsize=18, uniformtext_mode='hide',
        legend_font_size=18)
        cols[1].plotly_chart(fig, use_container_width=True)

    for i, round in enumerate(rounds_data):
        plot_turn(f'### Rodada {i}', round, st)


def plot_runs(runs_data: list[dict]):
    for i in range(len(runs_data)):
        st.markdown(f'## Execução {i + 1}')
        plot_run(runs_data[i]['rounds_data'])


def show_configurations(data):
    def configs(conf_data, parent, title):
        parent.markdown(f'## {title}')
        cols = parent.columns(2)
        cols[0].metric('Número de pais', conf_data['num_parents_mating'])
        cols[1].metric('Elitismo', conf_data['keep_elitism'])
        cols[0].metric('Porcentagem de mutação', conf_data['mutation_percent_genes'])
        cols[1].metric('Tipo de mutação', conf_data['mutation_type'])


    for i, run in enumerate(data):
        cols = st.columns(2)
        configs(run, cols[0], f'Configurações da rodada {i}')


def round_config(round: str):
    l, m, r = st.columns(3)

    # if st.button("Usar última configuração"):
    #     load_last_config()

    num_generations = l.number_input('Número de gerações', step=1, key=f'{round}_num_generations', min_value=1, max_value=5000, value=20)
    pop_size = m.number_input('Tamanho da população', step=1, key=f'{round}_pop_size', min_value=1, max_value=5000, value=20)
    parent_num = r.number_input('Número de pais', step=1, key=f'{round}_parent_num', min_value=1, max_value=pop_size, value=20)
    elitism = l.number_input('Elitismo', key=f'{round}_elitism', value=3)
    mut_perc = m.number_input('Porcentagem de mutação', step=1, key=f'{round}_mut_perc', value=1)
    mut_type = r.selectbox('Tipo de mutação', options=['random', 'swap', 'inversion', 'scramble', 'adaptive'], key=f'{round}_mut_type')
    return {
        "num_generations": num_generations,
        "sol_per_pop": pop_size,
        "num_parents_mating": parent_num,
        "keep_elitism": elitism,
        "mutation_percent_genes": mut_perc,
        "mutation_type": mut_type
    }


def write_to_history(rounds_data: list[dict], configs: list[dict]):
    # Registro apenas a primeira rodada de cada
    def collect_round_data(data, file_name, config):
        useful_data = []
        for run in data:
            print(run)
            useful_data.append({
                'fitness': run['fitness'][0],
                **config
            })

        with open(file_name, "a") as f:
            writer = csv.DictWriter(f, fieldnames=useful_data[0].keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerows(useful_data)

    for i, round in enumerate(rounds_data):
        collect_round_data(round['rounds_data'], HISTORY_FILE.format(i), configs[i])


def app():
    st.markdown("# Einstein")

    round_count = st.number_input("Número de rodadas", step=1)
    rounds_config = []
    for i in range(round_count):
        st.markdown(f"## Rodada {i}")
        rounds_config.append(round_config(f"r{i}_"))

    runs = st.number_input("Passagens", min_value=1, max_value=50)

    if st.button("Rodar"):
        results = []
        for i in range(runs):
            # Devolve outras coisas, só me interessa os dados (primeiro item)
            res = einstein_main(rounds_config)
            results.append(res[0])
        
        write_to_history(results, rounds_config)
        plot_runs(results)


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    app()
