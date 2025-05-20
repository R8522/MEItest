import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Dashboard Bahan Dirujuk", layout="wide")
st.title("📚 Dashboard Analisis Bahan Dirujuk")

# Load your dataset directly (already in working directory)
DATA_PATH = "/content/report_bahandirujuk.csv"

try:
    data = pd.read_csv("report_bahandirujuk.csv")

    # Optional cleanup
    data = data.drop(columns=['id_record', 'aduan_id'], errors='ignore')
    data.fillna(0, inplace=True)

    # Sidebar filters
    st.sidebar.header("🎯 Penapis")
    perkhid_list = sorted(data['perkhidmatan'].dropna().unique())
    selected_perkhid = st.sidebar.multiselect(
        "Pilih Perkhidmatan", perkhid_list, default=perkhid_list[:1]
    )

    jenis_buku = ['K_B_fik', 'R_B_fik', 'D_B_fik']

    # Filter data
    filtered = data[data['perkhidmatan'].isin(selected_perkhid)]

    # Handle empty selection
    if filtered.empty:
        st.warning("Tiada data untuk perkhidmatan yang dipilih.")
    else:
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📈 Ringkasan", "📊 Graf", "🧮 Data Mentah"])

        with tab1:
            st.subheader(f"📌 Statistik Ringkasan - {', '.join(selected_perkhid)}")
            st.write(filtered[jenis_buku].describe())

        with tab2:
            st.subheader("📊 Perbandingan Jumlah Buku Fiksyen")

            # Bar Chart
            st.markdown("**Jumlah Setiap Kategori (Jumlah Keseluruhan)**")
            total = filtered[jenis_buku].sum()
            fig, ax = plt.subplots()
            sns.barplot(x=total.index, y=total.values, palette='Set2', ax=ax)
            ax.set_ylabel("Jumlah Buku")
            ax.set_xlabel("Kategori")
            st.pyplot(fig)

            # Box Plot
            st.markdown("**Taburan Nilai (Boxplot)**")
            fig2, ax2 = plt.subplots()
            sns.boxplot(data=filtered[jenis_buku], palette='Set3', ax=ax2)
            ax2.set_ylabel("Jumlah Buku")
            st.pyplot(fig2)

        with tab3:
            st.subheader("🧮 Data Mentah")
            st.dataframe(filtered.reset_index(drop=True))

except FileNotFoundError:
    st.error(f"Fail CSV tidak dijumpai di lokasi: {DATA_PATH}")
    st.info("Simpan fail anda sebagai `report_bahandirujuk.csv` dalam folder yang sama.")
