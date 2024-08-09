import json
from time import strftime, time
import numpy as np
import streamlit as st
import plotly.express as pe
from plotly import tools
from convert_data import get_sorted_indexes, to_dataframe, to_matrix, translate_matrix_values
from einstein import main as einstein_main
import csv
import plotly.graph_objects as go

from test_einstein import SOLUTION
from ga_qiEinstein import COLUMNS, ROWS, TRANSLATION_DICTS
from ga_qiEinstein.custom_ga import CustomGA

DATE_TIME_STR = strftime("%Y-%m-%d_%H-%M-%S")
HISTORY_FILE = 'history_round_{}.csv'


def plot_run(data):
    def plot_turn(turn, data, parent_node):
        cols = parent_node.columns(2)
        cols[0].markdown(turn)
        cols[1].metric("Tempo", value="{}s".format(round(data['total_time_s'], 2)))
        cols[0].markdown('#### Evolução de fitness')
        fig = pe.line(
            x=list(range(1, len(data['fitness']) + 1)),
            y=list(data['fitness']),
            labels={'x': 'Geração', 'y': 'Fitness'},
            range_y=[-30, 0],
            range_x=[0, len(data['fitness']) + 1]
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

        parent_node.markdown(f"#### Melhor solução")
        matrix = to_matrix(data['sol'], 5)
        sorted = [get_sorted_indexes(row) for row in matrix]
        translated = translate_matrix_values(sorted, TRANSLATION_DICTS)
        df = to_dataframe(translated, COLUMNS, ROWS)

        def custom_styling():
            row = 0
            def style(*args, **kwargs):
                nonlocal row
                print(row)
                styles = ['background-color: lightgreen; color: black' if x == SOLUTION[row][i] else '' for i, x in enumerate(args[0])]
                row += 1
                return styles
            
            return style
        df = df.style.apply(custom_styling(), axis=1)
        
        parent_node.table(df)

    cols = st.columns(2)
    # Histograma de pesos
    cols[0].markdown('#### Pesos')
    weights = data['weight_history']
    z = [list(x.values()) for x in weights]
    fig = go.Figure(data=[go.Surface(z=z)])
    fig.update_layout(
        uniformtext_minsize=18, uniformtext_mode='hide',
        legend_font_size=18, height=800)
    fig.update_scenes(
        xaxis_title='X - Regra',
        yaxis_title='Y - Geração',
        zaxis_title='Z - Peso'
    )
    cols[0].plotly_chart(fig)

    # Histograma de erros
    cols[1].markdown('#### Erros')
    errors = data['error_history']
    z = [list(x.values()) for x in errors]
    fig = go.Figure(data=[go.Surface(z=z)])
    fig.update_layout(
        uniformtext_minsize=18, uniformtext_mode='hide',
        legend_font_size=18, height=800)
    fig.update_scenes(
        xaxis_title='X - Regra',
        yaxis_title='Y - Geração',
        zaxis_title='Z - Erro'
    )
    cols[1].plotly_chart(fig)

    for i, round_data in enumerate(data['rounds_data']):
        plot_turn(f'### Rodada {i} (fitness: {round_data["sol_fit"]})', round_data, st)


def round_config(round: str, global_config: dict = None):
    l, m, r = st.columns(3)

    if global_config is None:
        global_config = {
            'num_generations': 100,
            'sol_per_pop': 100,
            'num_parents_mating': 10,
            'keep_elitism': 2,
            'mutation_percent_genes': 10,
            'mutation_type': 'random'
        }

    num_generations = l.number_input(
        'Número de gerações', step=20,
        key=f'{round}_num_generations', min_value=1, max_value=500000,
        value=global_config['num_generations']
        )

    pop_size = m.number_input(
        'Tamanho da população', step=20,
        key=f'{round}_pop_size', min_value=1, max_value=500000,
        value=global_config['sol_per_pop']
        )

    parent_num = r.number_input(
        'Número de pais', step=1,
        key=f'{round}_parent_num', min_value=1, max_value=pop_size,
        value=global_config['num_parents_mating']
        )

    elitism = l.number_input(
        'Elitismo', key=f'{round}_elitism', 
        value=global_config['keep_elitism']
        )
    
    mut_perc = m.number_input(
        'Porcentagem de mutação', step=1,
        key=f'{round}_mut_perc',
        value=global_config['mutation_percent_genes']
        )

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


def advance_progress_callback(progress_bar, total):
    current = 0
    start_time = time()

    def advance(gaint: CustomGA):
        # Preciso receber gaint como parametro pois essa função será chamada
        # dentro do Pygad, e deve receber esse parâmetro
        nonlocal current
        nonlocal start_time
        current += 1
        progress_bar.progress(
            current / total, 
            text=f"{current} -> Melhor fitness: {gaint.best_solution()[1]}, tempo total: {round(time() - start_time, 2)}s"
        )
 
    return advance

def app():
    st.markdown("# Einstein")

    round_count = st.number_input("Número de rodadas", step=1, min_value=1)
    rounds_config = []
    st.markdown("## Configurações das rodadas")
    st.markdown("As configurações cascateam. Isso significa que o que for configurado na rodada 1 será usado como padrão para a rodada 2 e assim por diante, a não ser que uma nova configuração seja feita em rodadas posteriores")

    for i in range(round_count):
        with st.expander(f"## Rodada {i+1}"):
            if len(rounds_config) == 0:
                config = round_config(f"r{i}_")
            else:
                config = round_config(f"r{i}_", rounds_config[i-1])
        
        config['progress_bar'] = advance_progress_callback(st.progress(0), config['num_generations'])
        rounds_config.append(config)

    if st.button("Rodar"):
        # Devolve outras coisas, só me interessa os dados (primeiro item)
        data = einstein_main(rounds_config)[0]
        plot_run(data)


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    app()
