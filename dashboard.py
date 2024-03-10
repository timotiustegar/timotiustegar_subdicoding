import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
st.set_page_config(page_title="Dashboard Air Quality", layout="wide")

def season_cond(month):
    if month in [3, 4, 5]:
        return 'Semi'
    elif month in [6, 7, 8]:
        return 'Panas'
    elif month in [9, 10, 11]:
        return 'Gugur'
    else:
        return 'Dingin'

aoti, chang, guan, geo = st.tabs(["Aotizhongxin", "Changping", "Guanyuan", "Geoanalysis"])

with aoti:
    # Membaca data
    aotizhongxin_df = pd.read_csv("data/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
    # Membersihkan data
    aotizhongxin_df.fillna(aotizhongxin_df.mean(numeric_only=True), inplace=True)
    aotizhongxin_df.fillna(value="NE", inplace=True)
    # Menampilkan dataframe
    st.title("Tabel Aotizhongxin")
    st.dataframe(aotizhongxin_df, use_container_width=True)
    # EDA
    graph_col, title_col = st.columns([7, 5])  
    with graph_col:
        groupped_month = aotizhongxin_df.copy()
        groupped_month["yearMonth"] = groupped_month['year'].astype(str) + '-' + groupped_month['month'].apply(lambda x: '{:02d}'.format(x))
        groupped_month.groupby("yearMonth").agg({
            "PM2.5": "mean",
            "PM10": "mean"
        }).reset_index()
        fig = plt.figure(figsize=[8, 5])
        sns.lineplot(data=groupped_month , x="yearMonth", y="PM2.5", label="PM2.5")
        sns.lineplot(data=groupped_month , x="yearMonth", y="PM10", label="PM10")

        plt.title("Tren Polusi Partikel 2.5mm dan 10mm Aotizhongxin Station")
        plt.xlabel("Bulan Pemeriksaan")
        plt.xticks(rotation=90)
        plt.ylabel("Tingkat Polusi")
        plt.legend()

        #tampilkan
        st.pyplot(fig)
    with title_col:
        st.header("Tren Polusi Partikel 2.5mm dan 10mm Aotizhongxin Station")

    st.header("Pola polusi udara pada setiap musim berbeda")
    # Copy tabel sebelum melakukan analisa
    aotizhongxin_season = aotizhongxin_df.copy()
    # Satukan 3 feature waktu menjadi 1
    aotizhongxin_season['date'] = pd.to_datetime(aotizhongxin_season[['year', 'month', 'day']])
    # Group tabel perharinya
    groupped_date = aotizhongxin_season.groupby("date").agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()
    # Berikan klasifikasi label musim berdasarkan bulan sebagai ketentuannya
    groupped_date["season"] = groupped_date['date'].dt.month.apply(lambda x : season_cond(x))

    # Kelola subplot visualisasi
    fig = plt.figure(figsize=[14,7])
    grid = plt.GridSpec(nrows=2, ncols=4)
    ax1 = plt.subplot(grid[0,0:4])
    ax2 = plt.subplot(grid[1,0])
    ax3 = plt.subplot(grid[1,1])
    ax4 = plt.subplot(grid[1,2])
    ax5 = plt.subplot(grid[1,3])

    # Plot semua visualisasi yang dibutuhkan
    sns.scatterplot(data=groupped_date, x="PM2.5", y="PM10", hue="season", palette={"Semi":"#da4167", "Panas":"#74a57f", "Gugur":"#ffd166", "Dingin":"#083d77"}, ax=ax1)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Semi"], x="PM2.5", y="PM10", color="#da4167", ax=ax2)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Panas"], x="PM2.5", y="PM10", color="#74a57f", ax=ax3)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Gugur"], x="PM2.5", y="PM10", color="#ffd166", ax=ax4)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Dingin"], x="PM2.5", y="PM10", color="#083d77", ax=ax5)
    st.pyplot(fig)

    # Filter semua data yang mengalami peningkatan polusi diatas 100 poin PM2.5 dibanding data sebelumnya
    significant_increase = aotizhongxin_season[(aotizhongxin_season['PM2.5'].diff() > 100) & (aotizhongxin_season['PM2.5'].shift(1)!=3)]

    # Mengambil data peningkatan polusi signifikan terakhir dan 1 data sebelum peningkatan polusi
    index_selected = aotizhongxin_season[aotizhongxin_season['No'] == significant_increase.tail(1)["No"].values[0]].index[0]
    selected_data = aotizhongxin_season.iloc[index_selected - 1 : index_selected + 1]

    st.header("Waktu terakhir terjadinya peningkatan polusi udara secara signifikan")
    if not significant_increase.empty:
        last_increase_date = significant_increase['date'].max()
        st.text(f"Terakhir kali terjadi peningkatan polusi di stasiun Aotizhongxin: {last_increase_date.date()}")
        st.dataframe(selected_data)
    else:
        st.text(f"Tidak ada peningkatan polusi di stasiun Aotizhongxin")

with chang:
    # Membaca data
    changping_df = pd.read_csv("data/PRSA_Data_Changping_20130301-20170228.csv")
    # Membersihkan data
    changping_df.fillna(changping_df.mean(numeric_only=True), inplace=True)
    changping_df.fillna(value="NE", inplace=True)
    # Menampilkan dataframe
    st.title("Tabel Changping")
    st.dataframe(changping_df, use_container_width=True)
    # EDA
    graph_col, title_col = st.columns([7, 5])  
    with graph_col:
        groupped_month = changping_df.copy()
        groupped_month["yearMonth"] = groupped_month['year'].astype(str) + '-' + groupped_month['month'].apply(lambda x: '{:02d}'.format(x))
        groupped_month.groupby("yearMonth").agg({
            "PM2.5": "mean",
            "PM10": "mean"
        }).reset_index()
        fig = plt.figure(figsize=[8, 5])
        sns.lineplot(data=groupped_month , x="yearMonth", y="PM2.5", label="PM2.5")
        sns.lineplot(data=groupped_month , x="yearMonth", y="PM10", label="PM10")

        plt.title("Tren Polusi Partikel 2.5mm dan 10mm Changping Station")
        plt.xlabel("Bulan Pemeriksaan")
        plt.xticks(rotation=90)
        plt.ylabel("Tingkat Polusi")
        plt.legend()

        #tampilkan
        st.pyplot(fig)
    with title_col:
        st.header("Tren Polusi Partikel 2.5mm dan 10mm Changping Station")

    st.header("Pola polusi udara pada setiap musim berbeda")
    # Copy tabel sebelum melakukan analisa
    changping_season = changping_df.copy()
    # Satukan 3 feature waktu menjadi 1
    changping_season['date'] = pd.to_datetime(changping_season[['year', 'month', 'day']])
    # Group tabel perharinya
    groupped_date = changping_season.groupby("date").agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()
    # Berikan klasifikasi label musim berdasarkan bulan sebagai ketentuannya
    groupped_date["season"] = groupped_date['date'].dt.month.apply(lambda x : season_cond(x))

    # Kelola subplot visualisasi
    fig = plt.figure(figsize=[14,7])
    grid = plt.GridSpec(nrows=2, ncols=4)
    ax1 = plt.subplot(grid[0,0:4])
    ax2 = plt.subplot(grid[1,0])
    ax3 = plt.subplot(grid[1,1])
    ax4 = plt.subplot(grid[1,2])
    ax5 = plt.subplot(grid[1,3])

    # Plot semua visualisasi yang dibutuhkan
    sns.scatterplot(data=groupped_date, x="PM2.5", y="PM10", hue="season", palette={"Semi":"#da4167", "Panas":"#74a57f", "Gugur":"#ffd166", "Dingin":"#083d77"}, ax=ax1)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Semi"], x="PM2.5", y="PM10", color="#da4167", ax=ax2)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Panas"], x="PM2.5", y="PM10", color="#74a57f", ax=ax3)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Gugur"], x="PM2.5", y="PM10", color="#ffd166", ax=ax4)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Dingin"], x="PM2.5", y="PM10", color="#083d77", ax=ax5)
    st.pyplot(fig)

    # Filter semua data yang mengalami peningkatan polusi diatas 100 poin PM2.5 dibanding data sebelumnya
    significant_increase = changping_season[(changping_season['PM2.5'].diff() > 100) & (changping_season['PM2.5'].shift(1)!=3)]

    # Mengambil data peningkatan polusi signifikan terakhir dan 1 data sebelum peningkatan polusi
    index_selected = changping_season[changping_season['No'] == significant_increase.tail(1)["No"].values[0]].index[0]
    selected_data = changping_season.iloc[index_selected - 1 : index_selected + 1]

    st.header("Waktu terakhir terjadinya peningkatan polusi udara secara signifikan")
    if not significant_increase.empty:
        last_increase_date = significant_increase['date'].max()
        st.text(f"Terakhir kali terjadi peningkatan polusi di stasiun Changping: {last_increase_date.date()}")
        st.dataframe(selected_data)
    else:
        st.text(f"Tidak ada peningkatan polusi di stasiun Changping")

with guan:
    # Membaca data
    guanyuan_df = pd.read_csv("data/PRSA_Data_Guanyuan_20130301-20170228.csv")
    # Membersihkan data
    guanyuan_df.fillna(guanyuan_df.mean(numeric_only=True), inplace=True)
    guanyuan_df.fillna(value="NE", inplace=True)
    # Menampilkan dataframe
    st.title("Tabel Guanyuan")
    st.dataframe(guanyuan_df, use_container_width=True)

    # EDA
    graph_col, title_col = st.columns([7, 5])  
    with graph_col:
        groupped_month = guanyuan_df.copy()
        groupped_month["yearMonth"] = groupped_month['year'].astype(str) + '-' + groupped_month['month'].apply(lambda x: '{:02d}'.format(x))
        groupped_month.groupby("yearMonth").agg({
            "PM2.5": "mean",
            "PM10": "mean"
        }).reset_index()
        fig = plt.figure(figsize=[8, 5])
        sns.lineplot(data=groupped_month , x="yearMonth", y="PM2.5", label="PM2.5")
        sns.lineplot(data=groupped_month , x="yearMonth", y="PM10", label="PM10")

        plt.title("Tren Polusi Partikel 2.5mm dan 10mm Guanyuan Station")
        plt.xlabel("Bulan Pemeriksaan")
        plt.xticks(rotation=90)
        plt.ylabel("Tingkat Polusi")
        plt.legend()

        #tampilkan
        st.pyplot(fig)
    with title_col:
        st.header("Tren Polusi Partikel 2.5mm dan 10mm Guanyuan Station")

    st.header("Pola polusi udara pada setiap musim berbeda")
    # Copy tabel sebelum melakukan analisa
    guanyuan_season = guanyuan_df.copy()
    # Satukan 3 feature waktu menjadi 1
    guanyuan_season['date'] = pd.to_datetime(guanyuan_season[['year', 'month', 'day']])
    # Group tabel perharinya
    groupped_date = guanyuan_season.groupby("date").agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()
    # Berikan klasifikasi label musim berdasarkan bulan sebagai ketentuannya
    groupped_date["season"] = groupped_date['date'].dt.month.apply(lambda x : season_cond(x))

    # Kelola subplot visualisasi
    fig = plt.figure(figsize=[14,7])
    grid = plt.GridSpec(nrows=2, ncols=4)
    ax1 = plt.subplot(grid[0,0:4])
    ax2 = plt.subplot(grid[1,0])
    ax3 = plt.subplot(grid[1,1])
    ax4 = plt.subplot(grid[1,2])
    ax5 = plt.subplot(grid[1,3])

    # Plot semua visualisasi yang dibutuhkan
    sns.scatterplot(data=groupped_date, x="PM2.5", y="PM10", hue="season", palette={"Semi":"#da4167", "Panas":"#74a57f", "Gugur":"#ffd166", "Dingin":"#083d77"}, ax=ax1)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Semi"], x="PM2.5", y="PM10", color="#da4167", ax=ax2)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Panas"], x="PM2.5", y="PM10", color="#74a57f", ax=ax3)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Gugur"], x="PM2.5", y="PM10", color="#ffd166", ax=ax4)
    sns.scatterplot(data=groupped_date[groupped_date["season"]=="Dingin"], x="PM2.5", y="PM10", color="#083d77", ax=ax5)
    st.pyplot(fig)

    # Filter semua data yang mengalami peningkatan polusi diatas 100 poin PM2.5 dibanding data sebelumnya
    significant_increase = guanyuan_season[(guanyuan_season['PM2.5'].diff() > 100) & (guanyuan_season['PM2.5'].shift(1)!=3)]

    # Mengambil data peningkatan polusi signifikan terakhir dan 1 data sebelum peningkatan polusi
    index_selected = guanyuan_season[guanyuan_season['No'] == significant_increase.tail(1)["No"].values[0]].index[0]
    selected_data = guanyuan_season.iloc[index_selected - 1 : index_selected + 1]

    st.header("Waktu terakhir terjadinya peningkatan polusi udara secara signifikan")
    if not significant_increase.empty:
        last_increase_date = significant_increase['date'].max()
        st.text(f"Terakhir kali terjadi peningkatan polusi di stasiun Guanyuan: {last_increase_date.date()}")
        st.dataframe(selected_data)
    else:
        st.text(f"Tidak ada peningkatan polusi di stasiun Guanyuan")

with geo:
    st.header("Persebaran polusi udara")
    st.text("Persebaran polusi udara pada daerah padat dan sepi penduduk")
    pm10_col, pm25_col = st.columns(2)
    with pm10_col:
        fig = plt.figure(figsize=[8, 5])

        # Melihat bagaimana persebaran polusi partikel 10mm
        sns.histplot(aotizhongxin_df['PM10'], bins=30, alpha=0.5, label='Aotizhongxin')
        sns.histplot(changping_df['PM10'], bins=30, alpha=0.5, label='Changping')

        plt.legend()
        st.pyplot(fig)
    with pm25_col:
        fig = plt.figure(figsize=[8, 5])

        # Melihat bagaimana persebaran polusi partikel 2.5mm
        sns.histplot(aotizhongxin_df['PM2.5'], bins=30, alpha=0.5, label='Aotizhongxin')
        sns.histplot(changping_df['PM2.5'], bins=30, alpha=0.5, label='Changping')

        plt.legend()
        st.pyplot(fig)
    # Melihat kadar Sulfur Dioksida, Nitrogen Dioksida, dan Karbon Monoksida dalam udara pada masing masing stasiun
    all_df = pd.concat([aotizhongxin_df, changping_df, guanyuan_df], axis=0)
    groupped_station = all_df.groupby("station").agg({
        "SO2":"mean",
        "NO2":"mean",
        "CO":"mean"
    })
    st.header("Perbedaan kadar zat dalam udara")
    st.text("Perbedaan kadar zat udara pada daerah padat dan sepi penduduk")
    data_col, heat_col = st.columns([4, 8])
    with data_col:
        st.dataframe(groupped_station)
    with heat_col:
    # Visualisasi perbedaan
        fig = plt.figure(figsize=[7,5])
        sns.heatmap(groupped_station, annot=True)
        st.pyplot(fig)