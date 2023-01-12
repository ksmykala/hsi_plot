import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def hsi_plot(
            temp_df: pd.DataFrame,
            filter_column='disease',
            title='',
            figsize=(12, 8),
            **kwargs
        ):

    temp_df['is_healthy'] = temp_df.disease == 'Control'
    spectra_columns, x = get_spectra_columns_and_range(temp_df)

    fig = plt.figure(figsize=figsize)

    legend_handles = {
        'healthy': None, 'unhealthy': None
    }

    for is_healthy in [False, True]:
        tdf = temp_df.loc[(temp_df.is_healthy == is_healthy), spectra_columns]

        label = 'healthy' if is_healthy else 'unhealthy'
        color = 'limegreen' if is_healthy else 'red'

        _p = plt.plot(
            x, tdf.T, '-',
            color=color, alpha=kwargs.get('alpha', 0.1), label=label)
        if legend_handles[label] is None:
            legend_handles[label] = _p[0]

        plt.xlim(x.min(), x.max())
        plt.ylim(-0.01, 1.01)
        plt.grid(True)
        plt.title(title)

        plt.xlabel(kwargs.get('xlabel', ''), fontsize=14)
        plt.ylabel(kwargs.get('ylabel', ''), fontsize=14)

    fig.legend(
        [
            legend_handles['healthy'],
            legend_handles['unhealthy']
        ],
        [
            'Healthy',
            'Unhealthy'
        ],
        borderaxespad=5

    )
    plt.tight_layout()

    return fig


def get_spectra_columns_and_range(temp_df: pd.DataFrame):
    spectre_cols, non_spectre_cols, spectre_cols_int = filter_spectre_columns(temp_df)

    col_min = spectre_cols[0]
    col_max = spectre_cols[-1]

    return temp_df.loc[:, col_min:col_max].columns.values, np.array(spectre_cols_int)


def filter_spectre_columns(dataframe):
    spectre_cols = []
    spectre_cols_int = []

    non_spectre_cols = []

    for col in list(dataframe.columns):
        try:
            col_int = int(float(col))
            spectre_cols_int.append(col_int)
            spectre_cols.append(col)
        except ValueError:
            non_spectre_cols.append(col)

    return spectre_cols, non_spectre_cols, spectre_cols_int
