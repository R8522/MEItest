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

    jenis_buku1 = ['K_B_fik', 'R_B_fik', 'D_B_fik']

    jenis_buku2 = ['K_B_ilm', 'R_B_ilm', 'D_B_ilm']

    jenis_buku3 = ['K_majalah', 'R_majalah', 'D_majalah']

    jenis_buku4 = ['K_dvd_fik', 'R_dvd_fik', 'D_dvd_fik']

    jenis_buku5 = ['K_dvd_ilm', 'R_dvd_ilm', 'D_dvd_ilm']

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
            st.write(filtered[jenis_buku1].describe())

            st.write(filtered[jenis_buku2].describe())

            st.write(filtered[jenis_buku3].describe())

            st.write(filtered[jenis_buku4].describe())

            st.write(filtered[jenis_buku5].describe())

        with tab2:
            st.subheader("📊 Perbandingan Jumlah Buku Fiksyen")
        
            jenis_buku_list = ['jenis_buku1', 'jenis_buku2', 'jenis_buku3', 'jenis_buku4', 'jenis_buku5']
        
            for i, jenis in enumerate(jenis_buku_list, start=1):
                st.markdown(f"## Jenis Buku {i}")
        
                # --- Bar Chart ---
                st.markdown("**Jumlah Setiap Kategori (Bar Chart)**")
                total = filtered[jenis].value_counts()  # or use .groupby() if it's categorical
                fig_bar, ax_bar = plt.subplots()
                sns.barplot(x=total.index, y=total.values, palette='Set2', ax=ax_bar)
                ax_bar.set_ylabel("Jumlah Buku")
                ax_bar.set_xlabel("Kategori")
                st.pyplot(fig_bar)
        
                # --- Box Plot ---
                st.markdown("**Taburan Nilai (Boxplot)**")
                fig_box, ax_box = plt.subplots()
                sns.boxplot(y=filtered[jenis], palette='Set3', ax=ax_box)
                ax_box.set_ylabel("Jumlah Buku")
                st.pyplot(fig_box)

        with tab3:
            st.subheader("🧮 Data Mentah")
            st.dataframe(filtered.reset_index(drop=True))

except FileNotFoundError:
    st.error(f"Fail CSV tidak dijumpai di lokasi: {DATA_PATH}")
    st.info("Simpan fail anda sebagai `report_bahandirujuk.csv` dalam folder yang sama.")
