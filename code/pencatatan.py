# Library Utama
import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
from datetime import datetime
# Library Currency
from babel.numbers import format_currency
# Library Aggrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
# Library Tambahan
from fungsi import *

# Membuat UKPBJ
daerah = region_config()
pilih = st.sidebar.selectbox("Pilih Daerah", list(daerah.keys()))
tahun = st.sidebar.selectbox("Pilih Tahun", range(datetime.now().year, datetime.now().year-3, -1))
selected_daerah = daerah.get(pilih, {})
kodeFolder = selected_daerah.get("folder")
kodeRUP = selected_daerah.get("RUP")
kodeLPSE = selected_daerah.get("LPSE")

# Koneksi DuckDB
con = duckdb.connect(database=':memory:')

# URL Dataset Pencatatan
base_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
datasets = {
    'CatatNonTender': f"{base_url}/SPSE-PencatatanNonTender{tahun}.parquet",
    'CatatNonTenderRealisasi': f"{base_url}/SPSE-PencatatanNonTenderRealisasi{tahun}.parquet",
    'CatatSwakelola': f"{base_url}/SPSE-PencatatanSwakelola{tahun}.parquet",
    'CatatSwakelolaRealisasi': f"{base_url}/SPSE-PencatatanSwakelolaRealisasi{tahun}.parquet",
}

st.title(f"TRANSAKSI PENCATATAN")
st.header(f"{pilih} - TAHUN {tahun}")

menu_pencatatan_1, menu_pencatatan_2 = st.tabs(["| PENCATATAN NON TENDER |", "| PENCATATAN SWAKELOLA |"])

with menu_pencatatan_1:
    try:
        # Baca dan gabungkan dataset pencatatan non tender
        dfCatatNonTender = read_df_duckdb(datasets['CatatNonTender'])
        dfCatatNonTenderRealisasi = read_df_duckdb(datasets['CatatNonTenderRealisasi'])[[
            "kd_nontender_pct", "jenis_realisasi", "no_realisasi", 
            "tgl_realisasi", "nilai_realisasi", "nama_penyedia", "npwp_penyedia"
        ]]
        dfGabung = dfCatatNonTender.merge(dfCatatNonTenderRealisasi, how='left', on='kd_nontender_pct')

        # Tampilkan header dan tombol unduh
        col1, col2 = st.columns((7,3))
        with col1:
            st.subheader(f"PENCATATAN NON TENDER TAHUN {tahun}")
        with col2:
            st.download_button(
                label = "📥 Download Data Pencatatan Non Tender",
                data = download_excel(dfGabung),
                file_name = f"SPSEPencatatanNonTender-{kodeFolder}-{tahun}.xlsx",
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        st.divider()

        # Filter berdasarkan sumber dana
        sumber_dana_options = ['SEMUA'] + list(dfGabung['sumber_dana'].unique())
        sumber_dana_cnt = st.radio("**Sumber Dana :**", sumber_dana_options, key="CatatNonTender")
        
        # Filter data
        if sumber_dana_cnt == 'SEMUA':
            dfGabung_filter = dfGabung
        else:
            dfGabung_filter = dfGabung[dfGabung['sumber_dana'] == sumber_dana_cnt]
        
        # Hitung jumlah paket berdasarkan status
        status_counts = {
            'Berjalan': len(dfGabung_filter[dfGabung_filter['status_nontender_pct_ket'] == 'Paket Sedang Berjalan']),
            'Selesai': len(dfGabung_filter[dfGabung_filter['status_nontender_pct_ket'] == 'Paket Selesai']), 
            'Dibatalkan': len(dfGabung_filter[dfGabung_filter['status_nontender_pct_ket'] == 'Paket Dibatalkan'])
        }

        # Tampilkan metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Pencatatan NonTender Berjalan", f"{status_counts['Berjalan']:,}")
        col2.metric("Pencatatan NonTender Selesai", f"{status_counts['Selesai']:,}")
        col3.metric("Pencatatan NonTender Dibatalkan", f"{status_counts['Dibatalkan']:,}")

        st.divider()

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi Berdasarkan Kategori Pengadaan dan Metode Pemilihan
            grafik_cnt_1, grafik_cnt_2, grafik_cnt_3, grafik_cnt_4 = st.tabs(["| Jumlah Transaksi - Kategori Pengadaan |","| Nilai Transaksi - Kategori Pengadaan |","| Jumlah Transaksi - Metode Pemilihan |","| Nilai Transaksi - Metode Pemilihan |"])
            
            with grafik_cnt_1:

                st.subheader("Berdasarkan Jumlah Kategori Pemilihan")

                ##### Query data grafik jumlah transaksi Pencatatan Non Tender berdasarkan Kategori Pengadaan

                sql_cnt_kp_jumlah = """
                    SELECT kategori_pengadaan AS KATEGORI_PENGADAAN, COUNT(kd_nontender_pct) AS JUMLAH_PAKET
                    FROM dfGabung_filter GROUP BY KATEGORI_PENGADAAN ORDER BY JUMLAH_PAKET DESC
                """

                tabel_cnt_kp_jumlah = con.execute(sql_cnt_kp_jumlah).df()

                grafik_cnt_1_1, grafik_cnt_1_2 = st.columns((3,7))

                with grafik_cnt_1_1:

                    gb = GridOptionsBuilder.from_dataframe(tabel_cnt_kp_jumlah)
                    gb.configure_default_column(resizable=True, filterable=True, sortable=True)
                    gb.configure_column("KATEGORI_PENGADAAN", header_name="KATEGORI PENGADAAN")
                    gb.configure_column("JUMLAH_PAKET", 
                                      header_name="JUMLAH PAKET",
                                      type=["numericColumn", "numberColumnFilter"])
                    
                    grid_options = gb.build()
                    
                    AgGrid(
                        tabel_cnt_kp_jumlah,
                        gridOptions=grid_options,
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        height=len(tabel_cnt_kp_jumlah) * 35,
                        width='100%',
                        allow_unsafe_jscode=True
                    )

                with grafik_cnt_1_2:

                    figcntkph = px.pie(tabel_cnt_kp_jumlah, 
                                     values="JUMLAH_PAKET", 
                                     names="KATEGORI_PENGADAAN", 
                                     title="Grafik Pencatatan Non Tender - Jumlah Paket - Kategori Pengadaan",
                                     hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Set3,
                                     labels={'JUMLAH_PAKET':'Jumlah Paket', 'KATEGORI_PENGADAAN':'Kategori Pengadaan'})
                    
                    figcntkph.update_traces(textposition='inside', 
                                          textinfo='percent+label',
                                          pull=[0.1]*len(tabel_cnt_kp_jumlah))
                    
                    figcntkph.update_layout(
                        showlegend=True,
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.2),
                        title_x=0.5,
                        title_font_size=16
                    )
                    
                    st.plotly_chart(figcntkph, theme=None, use_container_width=True)

            with grafik_cnt_2:

                st.subheader("Berdasarkan Nilai Kategori Pemilihan")

                ##### Query data grafik nilai transaksi Pencatatan Non Tender berdasarkan Kategori Pengadaan

                sql_cnt_kp_nilai = """
                    SELECT kategori_pengadaan AS KATEGORI_PENGADAAN, SUM(nilai_realisasi) AS NILAI_REALISASI
                    FROM dfGabung_filter GROUP BY KATEGORI_PENGADAAN ORDER BY NILAI_REALISASI
                """

                tabel_cnt_kp_nilai = con.execute(sql_cnt_kp_nilai).df()

                grafik_cnt_2_1, grafik_cnt_2_2 = st.columns((3,7))

                with grafik_cnt_2_1:

                    gb = GridOptionsBuilder.from_dataframe(tabel_cnt_kp_nilai)
                    gb.configure_default_column(resizable=True, filterable=True, sortable=True)
                    gb.configure_column("KATEGORI_PENGADAAN", header_name="KATEGORI PENGADAAN")
                    gb.configure_column("NILAI_REALISASI", 
                                      header_name="NILAI REALISASI",
                                      type=["numericColumn", "numberColumnFilter"],
                                      valueFormatter="data.NILAI_REALISASI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 2})")
                    
                    grid_options = gb.build()
                    
                    AgGrid(
                        tabel_cnt_kp_nilai,
                        gridOptions=grid_options,
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        height=len(tabel_cnt_kp_nilai) * 35,
                        width='100%',
                        allow_unsafe_jscode=True
                    )

                with grafik_cnt_2_2:

                    figcntkpn = px.pie(tabel_cnt_kp_nilai, 
                                     values="NILAI_REALISASI", 
                                     names="KATEGORI_PENGADAAN", 
                                     title="Grafik Pencatatan Non Tender - Nilai Transaksi - Kategori Pengadaan",
                                     hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Pastel,
                                     labels={'NILAI_REALISASI':'Nilai Realisasi', 'KATEGORI_PENGADAAN':'Kategori Pengadaan'})
                    
                    figcntkpn.update_traces(textposition='inside', 
                                          textinfo='percent+label',
                                          pull=[0.1]*len(tabel_cnt_kp_nilai))
                    
                    figcntkpn.update_layout(
                        showlegend=True,
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.2),
                        title_x=0.5,
                        title_font_size=16
                    )
                    
                    st.plotly_chart(figcntkpn, theme=None, use_container_width=True)

            with grafik_cnt_3:

                st.subheader("Berdasarkan Jumlah Metode Pemilihan")

                ##### Query data grafik jumlah transaksi Pencatatan Non Tender berdasarkan Metode Pemilihan

                sql_cnt_mp_jumlah = """
                    SELECT mtd_pemilihan AS METODE_PEMILIHAN, COUNT(kd_nontender_pct) AS JUMLAH_PAKET
                    FROM dfGabung_filter GROUP BY METODE_PEMILIHAN ORDER BY JUMLAH_PAKET DESC
                """

                tabel_cnt_mp_jumlah = con.execute(sql_cnt_mp_jumlah).df()

                grafik_cnt_3_1, grafik_cnt_3_2 = st.columns((3,7))

                with grafik_cnt_3_1:

                    gb = GridOptionsBuilder.from_dataframe(tabel_cnt_mp_jumlah)
                    gb.configure_default_column(resizable=True, filterable=True, sortable=True)
                    gb.configure_column("METODE_PEMILIHAN", header_name="METODE PEMILIHAN")
                    gb.configure_column("JUMLAH_PAKET", 
                                      header_name="JUMLAH PAKET",
                                      type=["numericColumn", "numberColumnFilter"])
                    
                    grid_options = gb.build()
                    
                    AgGrid(
                        tabel_cnt_mp_jumlah,
                        gridOptions=grid_options,
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        height=len(tabel_cnt_mp_jumlah) * 35,
                        width='100%',
                        allow_unsafe_jscode=True
                    )

                with grafik_cnt_3_2:

                    figcntmph = px.pie(tabel_cnt_mp_jumlah, 
                                     values="JUMLAH_PAKET", 
                                     names="METODE_PEMILIHAN", 
                                     title="Grafik Pencatatan Non Tender - Jumlah Paket - Metode Pemilihan",
                                     hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Bold,
                                     labels={'JUMLAH_PAKET':'Jumlah Paket', 'METODE_PEMILIHAN':'Metode Pemilihan'})
                    
                    figcntmph.update_traces(textposition='inside', 
                                          textinfo='percent+label',
                                          pull=[0.1]*len(tabel_cnt_mp_jumlah))
                    
                    figcntmph.update_layout(
                        showlegend=True,
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.2),
                        title_x=0.5,
                        title_font_size=16
                    )
                    
                    st.plotly_chart(figcntmph, theme=None, use_container_width=True)

            with grafik_cnt_4:

                st.subheader("Berdasarkan Nilai Metode Pemilihan")

                ##### Query data grafik nilai transaksi Pencatatan Non Tender berdasarkan Metode Pemilihan

                sql_cnt_mp_nilai = """
                    SELECT mtd_pemilihan AS METODE_PEMILIHAN, SUM(nilai_realisasi) AS NILAI_REALISASI
                    FROM dfGabung_filter GROUP BY METODE_PEMILIHAN ORDER BY NILAI_REALISASI
                """

                tabel_cnt_mp_nilai = con.execute(sql_cnt_mp_nilai).df()

                grafik_cnt_4_1, grafik_cnt_4_2 = st.columns((3,7))

                with grafik_cnt_4_1:

                    gb = GridOptionsBuilder.from_dataframe(tabel_cnt_mp_nilai)
                    gb.configure_default_column(resizable=True, filterable=True, sortable=True)
                    gb.configure_column("METODE_PEMILIHAN", header_name="METODE PEMILIHAN")
                    gb.configure_column("NILAI_REALISASI", 
                                      header_name="NILAI REALISASI",
                                      type=["numericColumn", "numberColumnFilter"],
                                      valueFormatter="data.NILAI_REALISASI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 2})")
                    
                    grid_options = gb.build()
                    
                    AgGrid(
                        tabel_cnt_mp_nilai,
                        gridOptions=grid_options,
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        height=len(tabel_cnt_mp_nilai) * 35,
                        width='100%',
                        allow_unsafe_jscode=True
                    )

                with grafik_cnt_4_2:

                    figcntmpn = px.pie(tabel_cnt_mp_nilai, 
                                     values="NILAI_REALISASI", 
                                     names="METODE_PEMILIHAN", 
                                     title="Grafik Pencatatan Non Tender - Nilai Transaksi - Metode Pemilihan",
                                     hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Dark24,
                                     labels={'NILAI_REALISASI':'Nilai Realisasi', 'METODE_PEMILIHAN':'Metode Pemilihan'})
                    
                    figcntmpn.update_traces(textposition='inside', 
                                          textinfo='percent+label',
                                          pull=[0.1]*len(tabel_cnt_mp_nilai))
                    
                    figcntmpn.update_layout(
                        showlegend=True,
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.2),
                        title_x=0.5,
                        title_font_size=16
                    )
                    
                    st.plotly_chart(figcntmpn, theme=None, use_container_width=True)

        st.divider()
        
        SPSE_CNT_radio_1, SPSE_CNT_radio_2 = st.columns((2,8))
        with SPSE_CNT_radio_1:
            status_options = ['SEMUA'] + list(dfGabung_filter['status_nontender_pct_ket'].unique())
            status_nontender_cnt = st.radio("**Status NonTender :**", status_options)
        with SPSE_CNT_radio_2:
            satker_options = ['SEMUA'] + list(dfGabung_filter['nama_satker'].unique())
            status_opd_cnt = st.selectbox("**Pilih Satker :**", satker_options)

        st.divider()

        # Modify query based on selections
        where_clauses = []
        if status_nontender_cnt != 'SEMUA':
            where_clauses.append(f"status_nontender_pct_ket = '{status_nontender_cnt}'")
        if status_opd_cnt != 'SEMUA':
            where_clauses.append(f"nama_satker = '{status_opd_cnt}'")
            
        where_sql = " AND ".join(where_clauses)
        if where_sql:
            where_sql = "WHERE " + where_sql

        sql_CatatNonTender_query = f"""
            SELECT nama_paket AS NAMA_PAKET, jenis_realisasi AS JENIS_REALISASI, no_realisasi AS NO_REALISASI, tgl_realisasi AS TGL_REALISASI, pagu AS PAGU,
            total_realisasi AS TOTAL_REALISASI, nilai_realisasi AS NILAI_REALISASI FROM dfGabung_filter
            {where_sql}
        """

        sql_CatatNonTender_query_grafik = f"""
            SELECT kategori_pengadaan AS KATEGORI_PENGADAAN, mtd_pemilihan AS METODE_PEMILIHAN, nilai_realisasi AS NILAI_REALISASI
            FROM dfGabung_filter
            {where_sql}
        """

        df_CatatNonTender_tabel = con.execute(sql_CatatNonTender_query).df()
        df_CatatNonTender_grafik = con.execute(sql_CatatNonTender_query_grafik).df()

        data_cnt_pd_1, data_cnt_pd_2, data_cnt_pd_3, data_cnt_pd_4 = st.columns((2,3,3,2))
        data_cnt_pd_1.subheader("")
        data_cnt_pd_2.metric(label=f"Jumlah Pencatatan Non Tender ({status_nontender_cnt})", value="{:,}".format(df_CatatNonTender_tabel.shape[0]))
        data_cnt_pd_3.metric(label=f"Nilai Total Pencatatan Non Tender ({status_nontender_cnt})", value="{:,}".format(df_CatatNonTender_tabel['NILAI_REALISASI'].sum()))
        data_cnt_pd_4.subheader("")

        st.divider()

        ### Tabel Pencatatan Non Tender
        # Konfigurasi AgGrid
        gb = GridOptionsBuilder.from_dataframe(df_CatatNonTender_tabel)
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        gb.configure_column("NAMA_PAKET", header_name="NAMA PAKET")
        gb.configure_column("JENIS_REALISASI", header_name="JENIS REALISASI") 
        gb.configure_column("NO_REALISASI", header_name="NO REALISASI")
        gb.configure_column("TGL_REALISASI", header_name="TGL REALISASI")
        gb.configure_column("PAGU", header_name="PAGU")
        gb.configure_column("TOTAL_REALISASI", 
                          header_name="TOTAL REALISASI",
                          type=["numericColumn", "numberColumnFilter"],
                          valueFormatter="data.TOTAL_REALISASI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 2})")
        gb.configure_column("NILAI_REALISASI",
                          header_name="NILAI REALISASI", 
                          type=["numericColumn", "numberColumnFilter"],
                          valueFormatter="data.NILAI_REALISASI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 2})")

        grid_options = gb.build()

        # Menampilkan tabel dengan AgGrid
        AgGrid(
            df_CatatNonTender_tabel,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=True,
            autoSizeColumns=True,
            height=700,
            width='100%',
            allow_unsafe_jscode=True
        )

    except Exception as e:
        st.error(f"Error: {e}")

with menu_pencatatan_2:
    try:
        # Baca dan gabungkan dataset pencatatan swakelola
        dfCatatSwakelola = read_df_duckdb(datasets['CatatSwakelola'])
        dfCatatSwakelolaRealisasi = read_df_duckdb(datasets['CatatSwakelolaRealisasi'])[[
            "kd_swakelola_pct", "jenis_realisasi", "no_realisasi", 
            "tgl_realisasi", "nilai_realisasi"
        ]]
        dfGabung = dfCatatSwakelola.merge(dfCatatSwakelolaRealisasi, how='left', on='kd_swakelola_pct')

        # Header dan tombol unduh
        col1, col2 = st.columns((7,3))
        with col1:
            st.subheader(f"PENCATATAN SWAKELOLA TAHUN {tahun}")
        with col2:
            st.download_button(
                label = "📥 Download Data Pencatatan Swakelola",
                data = download_excel(dfGabung),
                file_name = f"SPSEPencatatanSwakelola-{kodeFolder}-{tahun}.xlsx",
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        st.divider()

        # Filter data berdasarkan sumber dana
        sumber_dana_options = ['SEMUA'] + list(dfGabung['sumber_dana'].unique())
        sumber_dana_cs = st.radio("**Sumber Dana :**", sumber_dana_options, key="CatatSwakelola")
        dfGabung_filter = dfGabung if sumber_dana_cs == 'SEMUA' else dfGabung[dfGabung['sumber_dana'] == sumber_dana_cs]

        # Tampilkan metrics status paket
        status_counts = {status: len(dfGabung_filter[dfGabung_filter['status_swakelola_pct_ket'] == f'Paket {status}']) 
                        for status in ['Sedang Berjalan', 'Selesai', 'Dibatalkan']}
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Pencatatan Swakelola Berjalan", f"{status_counts['Sedang Berjalan']:,}")
        col2.metric("Pencatatan Swakelola Selesai", f"{status_counts['Selesai']:,}")
        col3.metric("Pencatatan Swakelola Dibatalkan", f"{status_counts['Dibatalkan']:,}")

        st.divider()

        # st.dataframe(dfCatatSwakelola)
        # st.dataframe(dfCatatSwakelolaRealisasi)
        # st.dataframe(dfGabung)
        # st.dataframe(dfGabung_filter)

        # Filter berdasarkan status dan satker
        SPSE_CS_radio_1, SPSE_CS_radio_2 = st.columns((2,8))
        with SPSE_CS_radio_1:
            status_swakelola_cs = st.radio("**Status Swakelola :**", dfGabung_filter['status_swakelola_pct_ket'].unique())
        with SPSE_CS_radio_2:  
            status_opd_cs = st.selectbox("**Pilih Satker :**", dfGabung_filter['nama_satker'].unique())
        
        st.divider()

        # Query dan tampilkan data
        sql = f"""
        SELECT nama_paket AS NAMA_PAKET, jenis_realisasi AS JENIS_REALISASI, 
               no_realisasi AS NO_REALISASI, tgl_realisasi AS TGL_REALISASI,
               pagu AS PAGU, total_realisasi AS TOTAL_REALISASI, 
               nilai_realisasi AS NILAI_REALISASI, nama_ppk AS NAMA_PPK 
        FROM dfGabung_filter 
        WHERE nama_satker = '{status_opd_cs}' 
        AND status_swakelola_pct_ket = '{status_swakelola_cs}'
        """
        dfCatatSwakelola_tabel = con.execute(sql).df()

        # Tampilkan metrics hasil query
        _, col2, col3, _ = st.columns((2,3,3,2))
        col2.metric(f"Jumlah Pencatatan Swakelola ({status_swakelola_cs})", 
                   value="{:,}".format(dfCatatSwakelola_tabel.shape[0]))
        col3.metric(f"Nilai Total Pencatatan Swakelola ({status_swakelola_cs})", 
                   value="{:,.2f}".format(dfCatatSwakelola_tabel['NILAI_REALISASI'].fillna(0).sum()))

        ### Tabel Pencatatan Swakelola
        # Fill NA values with 0 for numeric columns
        dfCatatSwakelola_tabel = dfCatatSwakelola_tabel.fillna({
            'NILAI_REALISASI': 0,
            'TOTAL_REALISASI': 0,
            'PAGU': 0
        })
        
        gb = GridOptionsBuilder.from_dataframe(dfCatatSwakelola_tabel)
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        gb.configure_column("NAMA_PAKET", header_name="NAMA PAKET")
        gb.configure_column("JENIS_REALISASI", header_name="JENIS REALISASI") 
        gb.configure_column("NO_REALISASI", header_name="NO REALISASI")
        gb.configure_column("TGL_REALISASI", header_name="TGL REALISASI")
        gb.configure_column("PAGU", header_name="PAGU")
        gb.configure_column("TOTAL_REALISASI", 
                          header_name="TOTAL REALISASI",
                          type=["numericColumn","numberColumnFilter"],
                          valueFormatter="'Rp ' + x.toLocaleString()")
        gb.configure_column("NILAI_REALISASI", 
                          header_name="NILAI REALISASI",
                          type=["numericColumn","numberColumnFilter"], 
                          valueFormatter="'Rp ' + x.toLocaleString()")
        gb.configure_column("NAMA_PPK", header_name="NAMA PPK")

        grid_options = gb.build()

        AgGrid(
            dfCatatSwakelola_tabel,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=True,
            height=700,
            width='100%',
            allow_unsafe_jscode=True
        )

    except Exception as e:
        st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")