import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Ativa conversores de data para o matplotlib
register_matplotlib_converters()

# ======== 1. Importação e Limpeza dos Dados ========

# Importa os dados
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Remove outliers (top 2.5% e bottom 2.5%)
low = df['value'].quantile(0.025)
high = df['value'].quantile(0.975)
df = df[(df['value'] >= low) & (df['value'] <= high)]

# ======== 2. Gráfico de Linha ========

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df.index, df['value'], color='red', linewidth=1)

    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.tight_layout()
    fig.savefig('line_plot.png')
    return fig

# ======== 3. Gráfico de Barras ========

def draw_bar_plot():
    # Prepara os dados agrupando por ano e mês
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Calcula a média diária de visualizações por mês/ano
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Cria o gráfico
    fig = df_grouped.plot(
        kind='bar',
        figsize=(10, 8),
        ylabel='Average Page Views'
    ).get_figure()

    plt.xlabel('Years')
    plt.legend(title='Months', labels=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])

    fig.tight_layout()
    fig.savefig('bar_plot.png')
    return fig

# ======== 4. Gráficos de Boxplot ========

def draw_box_plot():
    # Prepara o DataFrame
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month

    # Ordena os meses para o gráfico de meses ficar de Jan a Dec
    df_box = df_box.sort_values('month_num')

    # Cria os gráficos
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico 1: Boxplot por Ano
    sns.boxplot(
        x='year',
        y='value',
        data=df_box,
        ax=axes[0]
    )
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Gráfico 2: Boxplot por Mês
    sns.boxplot(
        x='month',
        y='value',
        data=df_box,
        ax=axes[1]
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.tight_layout()
    fig.savefig('box_plot.png')
    return fig

