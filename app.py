import streamlit as st
import src.hsi_chart as hc
import pandas as pd


def show_hsi_chart():
    df = load_df()
    st.write(df)

    with st.spinner('Rendering plot...'):
        fig = hc.hsi_plot(
            df,
            title='Healthy & unhealthy',
            xlabel='wavelength [nm]',
            ylabel='reflectance',
            alpha=0.3
        )
        st.pyplot(fig)


def load_df(filepath='data/sample_hsi.csv'):
    with st.spinner('Loading dataset...'):
        df = pd.read_csv(filepath)

    return df


if __name__ == "__main__":
    st.title('📈 Hyperspectral plot')
    show_hsi_chart()
