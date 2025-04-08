import plotly.graph_objects as go
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
    agg = kwargs.get('agg', False)

    fig = go.Figure()

    for is_healthy in [False, True]:
        tdf = temp_df.loc[(temp_df.is_healthy == is_healthy), spectra_columns]
        label = 'Healthy' if is_healthy else 'Unhealthy'
        color = 'limegreen' if is_healthy else 'red'

        if agg:
            # Calculate mean and std for aggregated view
            mean_values = tdf.mean()
            std_values = tdf.std()

            # Add standard deviation band first (so it's behind the mean line)
            fig.add_trace(
                go.Scatter(
                    x=np.concatenate([x, x[::-1]]),
                    y=np.concatenate([
                        mean_values.values + std_values.values,
                        (mean_values.values - std_values.values)[::-1]
                    ]),
                    fill='toself',
                    fillcolor=color,
                    line=dict(color='rgba(0,0,0,0)'),
                    name=f'{label} ±1σ',
                    showlegend=True,
                    opacity=0.5,
                    hoverinfo='skip'
                )
            )

            # Add mean line
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=mean_values.values,
                    mode='lines',
                    line=dict(color=color, width=2),
                    name=f'{label} mean',
                    hovertemplate=(
                        'Wavelength: %{x}<br>'
                        'Mean: %{y:.3f}<br>'
                        '<extra></extra>'
                    )
                )
            )
        else:
            # Calculate std for non-aggregated view
            std_values = tdf.std()
            mean_values = tdf.mean()

            # Original non-aggregated view
            for _, row in tdf.iterrows():
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=row.values,
                        mode='lines',
                        line=dict(color=color, width=1),
                        opacity=kwargs.get('alpha', 0.1),
                        showlegend=False,
                        name=label,
                        hovertemplate=(
                            'Wavelength: %{x}<br>'
                            'Intensity: %{y:.3f}<br>'
                            '<extra></extra>'
                        )
                    )
                )

    # Add legend entries only for non-aggregated view
    if not agg:
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode='lines',
                line=dict(color='limegreen', width=2),
                name='Healthy',
                showlegend=True
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode='lines',
                line=dict(color='red', width=2),
                name='Unhealthy',
                showlegend=True
            )
        )

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=kwargs.get('xlabel', ''),
        yaxis_title=kwargs.get('ylabel', ''),
        xaxis=dict(range=[x.min(), x.max()]),
        yaxis=dict(range=[-0.01, 1.01]),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        width=figsize[0] * 100,
        height=figsize[1] * 100,
        plot_bgcolor='white',
        hovermode='x unified'
    )

    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

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
