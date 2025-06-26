import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    layout="wide",
    page_title="Sistem Digital Bagian Marketing",
    page_icon="🎯"
)

# --- JUDUL UTAMA ---
st.title("🎯 Sistem Digital Terintegrasi - Bagian Marketing & Penjualan")
st.markdown("Prototipe interaktif untuk CRM dan sistem otomasi marketing.")

# --- HELPER FUNCTION UNTUK FORMAT MATA UANG ---
def format_rupiah(amount):
    return f"Rp {int(amount):,.0f}".replace(",", ".")

# --- MEMBUAT DATA SAMPEL (SIMULASI DATABASE CRM) ---
def create_marketing_data():
    # Data Prospek (Leads)
    leads_data = {
        'ID Prospek': [f'LEAD-{101+i}' for i in range(8)],
        'Nama': ['Andi Wijaya', 'Siti Aminah', 'Rudi Hartono', 'Dewi Sartika', 'Bambang Susilo', 'Lina Marlina', 'Agus Salim', 'Fitri Handayani'],
        'Perusahaan': ['PT Maju Jaya', 'CV Terang Benderang', 'Toko Bangunan Kokoh', 'PT Indah Kargo', 'Warung Makan Sedap', 'PT Digital Kreatif', 'CV Solusi Cepat', 'Pabrik Garmen Sejahtera'],
        'Sumber': ['Iklan Digital', 'Pameran', 'Website', 'Referensi', 'Iklan Digital', 'Website', 'Pameran', 'Website'],
        'Tanggal Masuk': [datetime.now() - timedelta(days=x) for x in [2, 5, 6, 8, 10, 12, 15, 18]],
        'Status': ['Baru', 'Dihubungi', 'Kualifikasi', 'Gagal', 'Baru', 'Kualifikasi', 'Dihubungi', 'Baru']
    }
    df_leads = pd.DataFrame(leads_data)

    # Data Peluang (Sales Pipeline)
    pipeline_data = {
        'ID Peluang': ['OPP-001', 'OPP-002', 'OPP-003', 'OPP-004', 'OPP-005'],
        'Nama Peluang': ['Proyek Superapp Tahap 1', 'Lisensi Software 1 Tahun', 'Pengadaan Server DC', 'Jasa Konsultasi Big Data', 'Paket Cybersecurity Perusahaan'],
        'Pelanggan': ['PT Digital Kreatif', 'PT Indah Kargo', 'CV Solusi Cepat', 'Toko Bangunan Kokoh', 'Pabrik Garmen Sejahtera'],
        'Estimasi Nilai': [250000000, 80000000, 120000000, 45000000, 95000000],
        'Tahap': ['Presentasi', 'Negosiasi', 'Kualifikasi', 'Proposal', 'Presentasi'],
        'PIC Sales': ['Budi (Sales)', 'Ani (Sales)', 'Budi (Sales)', 'Candra (Sales)', 'Ani (Sales)']
    }
    df_pipeline = pd.DataFrame(pipeline_data)

    # Data Kampanye
    campaign_data = {
        'Nama Kampanye': ['Diskon Akhir Tahun 2024', 'Webinar Big Data Q1 2025', 'Pameran IT Expo 2025'],
        'Status': ['Selesai', 'Selesai', 'Berjalan'],
        'Anggaran': [25000000, 15000000, 40000000],
        'Biaya Aktual': [23500000, 14000000, 31000000],
        'Prospek Dihasilkan': [150, 85, 120],
        'Pendapatan Dihasilkan': [75000000, 90000000, 50000000] # Pendapatan dari prospek tsb
    }
    df_campaigns = pd.DataFrame(campaign_data)
    df_campaigns['ROI (%)'] = ((df_campaigns['Pendapatan Dihasilkan'] - df_campaigns['Biaya Aktual']) / df_campaigns['Biaya Aktual']) * 100

    return df_leads, df_pipeline, df_campaigns

df_leads, df_pipeline, df_campaigns = create_marketing_data()


# --- TABS UNTUK SETIAP MODUL ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard Marketing",
    "📥 Manajemen Prospek (Leads)",
    "🗂️ Manajemen Peluang (Sales Pipeline)",
    "📢 Manajemen Kampanye",
    "👤 Database Pelanggan (CRM)",
    "📈 Analisis & Laporan"
])


# --- ISI TAB 1: DASHBOARD MARKETING ---
with tab1:
    st.header("Dashboard Kinerja Marketing & Penjualan")
    st.markdown(f"Data per tanggal: `{datetime.now().strftime('%d %B %Y')}`")

    # KPI Utama
    leads_mtd = df_leads[df_leads['Tanggal Masuk'] >= datetime.now() - timedelta(days=30)].shape[0]
    deals_won = 3 # Simulasi
    conversion_rate = (deals_won / leads_mtd) * 100 if leads_mtd > 0 else 0
    sales_mtd = df_pipeline[df_pipeline['Tahap'] != 'Menang']['Estimasi Nilai'].sum() # Simulasi penjualan bulan ini
    cpl = df_campaigns['Biaya Aktual'].sum() / df_campaigns['Prospek Dihasilkan'].sum() # Cost Per Lead

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Prospek Baru (30 hari)", f"{leads_mtd} Prospek")
    col2.metric("Tingkat Konversi", f"{conversion_rate:.2f}%", help="Persentase prospek yang menjadi pelanggan.")
    col3.metric("Total Penjualan (Bulan Ini)", format_rupiah(sales_mtd))
    col4.metric("Biaya per Prospek (CPL)", format_rupiah(cpl))
    
    st.markdown("---")

    st.subheader("Funnel Penjualan (Sales Funnel)")
    
    # Data untuk funnel chart
    funnel_data = pd.DataFrame({
        'Tahap': ['Prospek Masuk (Leads)', 'Prospek Terkualifikasi (MQL)', 'Peluang Dibuat (SQL)', 'Penjualan Menang (Won)'],
        'Jumlah': [df_leads.shape[0], df_leads[df_leads['Status']=='Kualifikasi'].shape[0], df_pipeline.shape[0], deals_won]
    })
    funnel_data['Tahap'] = pd.Categorical(funnel_data['Tahap'], categories=['Prospek Masuk (Leads)', 'Prospek Terkualifikasi (MQL)', 'Peluang Dibuat (SQL)', 'Penjualan Menang (Won)'], ordered=True)

    # Membuat funnel chart dengan Altair
    chart = alt.Chart(funnel_data).mark_bar().encode(
        x=alt.X('Jumlah:Q', title='Jumlah'),
        y=alt.Y('Tahap:O', sort='-x', title='Tahapan Funnel'),
        color=alt.Color('Tahap:N', legend=None),
        tooltip=['Tahap', 'Jumlah']
    ).properties(
        title='Visualisasi Funnel dari Prospek hingga Penjualan'
    )
    
    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudge text to right so it doesn't overlap
    ).encode(
        text='Jumlah:Q'
    )

    st.altair_chart((chart + text), use_container_width=True)

# --- ISI TAB 2: MANAJEMEN PROSPEK (LEADS) ---
with tab2:
    st.header("📥 Manajemen Prospek (Leads)")
    st.info("Mengelola semua calon pelanggan yang masuk sebelum diserahkan ke tim penjualan.")

    col_lead1, col_lead2 = st.columns([1, 2])
    with col_lead1:
        st.subheader("Input Prospek Baru")
        with st.form("lead_form"):
            nama = st.text_input("Nama Kontak")
            perusahaan = st.text_input("Nama Perusahaan")
            email = st.text_input("Email")
            sumber = st.selectbox("Sumber Prospek", options=df_leads['Sumber'].unique())
            submitted = st.form_submit_button("Simpan Prospek")
            if submitted:
                st.success(f"Prospek '{nama}' dari '{perusahaan}' berhasil disimpan.")

    with col_lead2:
        st.subheader("Daftar Prospek Masuk")
        status_filter = st.multiselect("Filter berdasarkan Status:", options=df_leads['Status'].unique(), default=df_leads['Status'].unique())
        filtered_leads = df_leads[df_leads['Status'].isin(status_filter)]
        st.dataframe(filtered_leads, use_container_width=True)


# --- ISI TAB 3: MANAJEMEN PELUANG (SALES PIPELINE) ---
with tab3:
    st.header("🗂️ Manajemen Peluang (Sales Pipeline)")
    st.info("Visualisasi semua proses penjualan aktif dalam Papan Kanban.")

    # Simulasi Papan Kanban menggunakan kolom
    tahapan_pipeline = df_pipeline['Tahap'].unique()
    kolom_kanban = st.columns(len(tahapan_pipeline))

    for i, tahap in enumerate(tahapan_pipeline):
        with kolom_kanban[i]:
            st.subheader(tahap)
            deals_in_stage = df_pipeline[df_pipeline['Tahap'] == tahap]
            for index, deal in deals_in_stage.iterrows():
                with st.expander(f"{deal['Nama Peluang']}"):
                    st.markdown(f"**Pelanggan:** {deal['Pelanggan']}")
                    st.markdown(f"**Nilai:** {format_rupiah(deal['Estimasi Nilai'])}")
                    st.markdown(f"**PIC:** {deal['PIC Sales']}")
                    st.button("Lihat Detail", key=f"btn_{deal['ID Peluang']}")


# --- ISI TAB 4: MANAJEMEN KAMPANYE ---
with tab4:
    st.header("📢 Manajemen Kampanye Marketing")
    st.info("Merencanakan, menjalankan, dan mengukur efektivitas setiap kampanye.")

    st.subheader("Daftar Kampanye Marketing")
    df_campaigns_display = df_campaigns.copy()
    df_campaigns_display['Anggaran'] = df_campaigns_display['Anggaran'].apply(format_rupiah)
    df_campaigns_display['Biaya Aktual'] = df_campaigns_display['Biaya Aktual'].apply(format_rupiah)
    df_campaigns_display['Pendapatan Dihasilkan'] = df_campaigns_display['Pendapatan Dihasilkan'].apply(format_rupiah)
    df_campaigns_display['ROI (%)'] = df_campaigns_display['ROI (%)'].apply(lambda x: f"{x:.2f}%")
    st.dataframe(df_campaigns_display, use_container_width=True)

    with st.expander("Buat Kampanye Baru (Simulasi)"):
        with st.form("campaign_form"):
            nama_kampanye = st.text_input("Nama Kampanye")
            jenis_kampanye = st.selectbox("Jenis Kampanye", ["Iklan Digital", "Pameran", "Webinar", "Email Marketing"])
            anggaran = st.number_input("Anggaran", min_value=0, step=1000000)
            tgl_mulai = st.date_input("Tanggal Mulai")
            tgl_selesai = st.date_input("Tanggal Selesai")
            if st.form_submit_button("Simpan Rencana Kampanye"):
                st.success(f"Kampanye '{nama_kampanye}' dengan anggaran {format_rupiah(anggaran)} berhasil disimpan.")


# --- ISI TAB 5: DATABASE PELANGGAN (CRM) ---
with tab5:
    st.header("👤 Database Pelanggan (CRM)")
    st.info("Pusat informasi 360° untuk setiap interaksi dan transaksi dengan pelanggan.")

    pelanggan_list = df_pipeline['Pelanggan'].unique()
    pelanggan_dipilih = st.selectbox("Pilih Pelanggan untuk Dilihat Detailnya:", pelanggan_list)

    if pelanggan_dipilih:
        st.subheader(f"Profil 360°: {pelanggan_dipilih}")
        col_prof1, col_prof2 = st.columns(2)
        with col_prof1:
            st.markdown("##### Informasi Dasar")
            st.text("Kontak Utama: Bpk. Tono")
            st.text("Email: tono@digitalkreatif.com")
            st.text("Telepon: 081234567890")
            st.text("Industri: Teknologi Informasi")

        with col_prof2:
            st.markdown("##### Histori Pembelian")
            histori_pembelian = df_pipeline[df_pipeline['Pelanggan'] == pelanggan_dipilih]
            st.dataframe(histori_pembelian[['Nama Peluang', 'Estimasi Nilai', 'Tahap']], use_container_width=True)

        st.markdown("##### Histori Aktivitas")
        aktivitas_data = {
            "Tanggal": [datetime.now() - timedelta(days=d) for d in [5, 10, 25]],
            "Aktivitas": ["Meeting Presentasi Produk", "Telepon Follow-up", "Kirim Email Penawaran"],
            "PIC": ["Budi (Sales)", "Budi (Sales)", "Ani (Sales)"],
            "Catatan": ["Klien tertarik dengan fitur A & B.", "Meminta proposal dikirim minggu depan.", "Proposal awal telah dikirim."]
        }
        st.dataframe(pd.DataFrame(aktivitas_data), use_container_width=True)

# --- ISI TAB 6: ANALISIS & LAPORAN ---
with tab6:
    st.header("📈 Analisis & Laporan Kinerja")
    st.info("Laporan mendalam untuk evaluasi kinerja tim penjualan dan efektivitas marketing.")

    st.subheader("Kinerja Tim Penjualan (Kuartal Ini)")
    sales_perf_data = {
        'Nama Sales': ['Budi (Sales)', 'Ani (Sales)', 'Candra (Sales)'],
        'Target Penjualan': [400000000, 400000000, 350000000],
        'Pencapaian Aktual': [df_pipeline[df_pipeline['PIC Sales'] == 'Budi (Sales)']['Estimasi Nilai'].sum(),
                               df_pipeline[df_pipeline['PIC Sales'] == 'Ani (Sales)']['Estimasi Nilai'].sum(),
                               df_pipeline[df_pipeline['PIC Sales'] == 'Candra (Sales)']['Estimasi Nilai'].sum()]
    }
    df_sales_perf = pd.DataFrame(sales_perf_data)
    df_sales_perf_melted = df_sales_perf.melt('Nama Sales', var_name='Kategori', value_name='Jumlah')
    
    chart_perf = alt.Chart(df_sales_perf_melted).mark_bar().encode(
        x='Nama Sales:N',
        y='Jumlah:Q',
        color='Kategori:N',
        xOffset="Kategori:N" # Untuk membuat grouped bar chart
    ).properties(
        title='Perbandingan Target vs. Pencapaian per Sales'
    )
    st.altair_chart(chart_perf, use_container_width=True)

    st.subheader("Return on Investment (ROI) per Kampanye")
    st.dataframe(df_campaigns[['Nama Kampanye', 'ROI (%)']], use_container_width=True)