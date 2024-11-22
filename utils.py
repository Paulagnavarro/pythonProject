import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def process_data(data):
    stats = data.describe(include='all').to_dict()
    os.makedirs('static/graphs', exist_ok=True)
    graphs = {}

    # Gráfico de Distribuição do Preço de Compra
    plt.figure()
    sns.histplot(data['buy_price'].dropna())
    plt.xlabel('Preço de Compra')
    plt.title('Distribuição do Preço de Compra')
    buy_price_path = 'static/graphs/dist_price.png'
    plt.savefig(buy_price_path)
    plt.close()
    graphs['Distribuição do Preço de Compra'] = buy_price_path

    # Gráfico de Distribuição da Área Construída
    plt.figure()
    sns.histplot(data['sq_mt_built'].dropna())
    plt.xlabel('Área Construída (m²)')
    plt.title('Distribuição da Área Construída')
    built_area_path = 'static/graphs/dist_sq_mt_built.png'
    plt.savefig(built_area_path)
    plt.close()
    graphs['Distribuição da Área Construída'] = built_area_path

    # Gráfico de Distribuição do Número de Quartos
    plt.figure()
    data['n_rooms'].value_counts().plot(kind='bar')
    plt.xlabel('Número de Quartos')
    plt.ylabel('Contagem')
    plt.title('Distribuição do Número de Quartos')
    room_distribution_path = 'static/graphs/room_distribution.png'
    plt.savefig(room_distribution_path)
    plt.close()
    graphs['Distribuição do Número de Quartos'] = room_distribution_path

    # Gráfico de Pizza: Distribuição do Número de Quartos
    plt.figure()
    data['n_rooms'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.ylabel('')
    plt.title('Distribuição do Número de Quartos')
    room_distribution_pie_path = 'static/graphs/room_distribution_pie.png'
    plt.savefig(room_distribution_pie_path)
    plt.close()
    graphs['Distribuição do Número de Quartos (Pizza)'] = room_distribution_pie_path

    # Boxplot: Preço de Compra por Número de Quartos
    plt.figure()
    sns.boxplot(x='n_rooms', y='buy_price', data=data)
    plt.xlabel('Número de Quartos')
    plt.ylabel('Preço de Compra')
    plt.title('Boxplot do Preço de Compra por Número de Quartos')
    boxplot_path = 'static/graphs/price_boxplot.png'
    plt.savefig(boxplot_path)
    plt.close()
    graphs['Boxplot do Preço de Compra por Número de Quartos'] = boxplot_path

    # Heatmap: Correlação entre Variáveis
    plt.figure(figsize=(10, 8))  # Ajustando o tamanho do gráfico
    # Filtrando apenas colunas numéricas
    numeric_data = data.select_dtypes(include=[float, int])
    correlation_matrix = numeric_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Mapa de Calor das Correlações')
    heatmap_path = 'static/graphs/correlation_heatmap.png'
    plt.savefig(heatmap_path)
    plt.close()
    graphs['Mapa de Calor das Correlações'] = heatmap_path

    return stats, graphs

import folium

def generate_map(data):
    if 'latitude' not in data.columns or 'longitude' not in data.columns:
        return None, "Dados de localização (latitude e longitude) não encontrados no conjunto de dados."

    data = data.dropna(subset=['latitude', 'longitude'])


    if data.empty:
        return None, "Não há dados válidos de localização para gerar o mapa."

    map_center = [data['latitude'].mean(), data['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    for _, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']],
                      popup=f"Preço: R$ {row['buy_price']}, Quartos: {row['n_rooms']}").add_to(m)

    map_path = 'static/graphs/map.html'
    m.save(map_path)
    return map_path, None

import plotly.express as px

def generate_interactive_plots(data):
    graphs = {}

    if 'sq_mt_built' in data.columns and 'buy_price' in data.columns and 'n_rooms' in data.columns:
        # Criando o gráfico de dispersão original (Preço x Área Construída x Quartos)
        fig1 = px.scatter(data,
                          x='sq_mt_built',
                          y='buy_price',
                          size='n_rooms',
                          color='buy_price',
                          labels={'sq_mt_built': 'Área Construída (m²)', 'buy_price': 'Preço de Compra',
                                  'n_rooms': 'Número de Quartos'},
                          hover_data={'sq_mt_built': True, 'buy_price': True, 'n_rooms': True},
                          color_continuous_scale='Viridis',
                          title="Gráfico de Dispersão 'Preço x Área Construída x Quartos'")

        plot_path1 = 'static/graphs/interactive_price_area_rooms.html'
        fig1.write_html(plot_path1)
        graphs['Gráfico de Dispersão: Preço x Área Construída x Quartos'] = plot_path1

    if 'sq_mt_useful' in data.columns and 'sq_mt_built' in data.columns and 'n_rooms' in data.columns:
        # Criando o novo gráfico de dispersão (Área Útil x Área Construída x Quartos)
        fig2 = px.scatter(data,
                          x='sq_mt_useful',
                          y='sq_mt_built',
                          size='n_rooms',
                          color='sq_mt_built',
                          labels={'sq_mt_useful': 'Área Útil (m²)', 'sq_mt_built': 'Área Construída (m²)',
                                  'n_rooms': 'Número de Quartos'},
                          hover_data={'sq_mt_useful': True, 'sq_mt_built': True, 'n_rooms': True},
                          color_continuous_scale='Viridis',
                          title="Gráfico de Dispersão 'Área Útil x Área Construída x Quartos'")

        plot_path2 = 'static/graphs/interactive_useful_built_rooms.html'
        fig2.write_html(plot_path2)
        graphs['Gráfico de Dispersão: Área Útil x Área Construída x Quartos'] = plot_path2

    return graphs
