import streamlit as st
import src.hsi_chart as hc
import pandas as pd


def show_hsi_chart():
    df = load_df()
    st.write(df)

    # Add toggle for aggregated view
    agg = st.checkbox('Show aggregated view (mean ± std)', value=True)

    with st.spinner('Rendering plot...'):
        fig = hc.hsi_plot(
            df,
            title='Healthy & unhealthy',
            xlabel='wavelength [nm]',
            ylabel='reflectance',
            alpha=0.3,
            agg=agg
        )
        st.plotly_chart(fig, use_container_width=True)


def load_df(filepath='./data/sample_hsi.csv'):
    with st.spinner('Loading dataset...'):
        df = pd.read_csv(filepath)

    return df


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title('📈 Hyperspectral plot')
    show_hsi_chart()
