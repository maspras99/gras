import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    layout="wide",
    page_title="Sistem Digital Bagian Keuangan",
    page_icon="💰"
)

# --- JUDUL UTAMA ---
st.title("💰 Sistem Digital Terintegrasi - Bagian Keuangan")
st.markdown("Prototipe interaktif untuk modul-modul di bawah Manajer Keuangan.")

# --- HELPER FUNCTION UNTUK FORMAT MATA UANG ---
def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

# --- MEMBUAT DATA SAMPEL (SIMULASI DATABASE KEUANGAN) ---
def create_financial_data():
    # Bagan Akun (Chart of Accounts)
    coa_data = {
        'Nomor Akun': ['1110', '1120', '1210', '2110', '3110', '4110', '5110', '5120'],
        'Nama Akun': ['Kas & Bank', 'Piutang Usaha', 'Aset Tetap', 'Hutang Usaha', 'Modal Disetor', 'Pendapatan Jasa', 'Beban Gaji', 'Beban Sewa'],
        'Tipe Akun': ['Aset', 'Aset', 'Aset', 'Liabilitas', 'Ekuitas', 'Pendapatan', 'Beban', 'Beban']
    }
    df_coa = pd.DataFrame(coa_data)

    # Hutang Usaha (AP)
    ap_data = {
        'ID Tagihan': ['INV-V001', 'INV-V002', 'INV-V003'],
        'Vendor': ['PT Sinar Jaya', 'CV Maju Mundur', 'PT Koneksi Cepat'],
        'Tanggal Tagihan': pd.to_datetime([datetime.now() - timedelta(days=20), datetime.now() - timedelta(days=10), datetime.now() - timedelta(days=5)]),
        'Tanggal Jatuh Tempo': pd.to_datetime([datetime.now() + timedelta(days=10), datetime.now() + timedelta(days=20), datetime.now() + timedelta(days=25)]),
        'Jumlah': [15000000, 8500000, 25000000],
        'Status': ['Belum Dibayar', 'Belum Dibayar', 'Sudah Dibayar']
    }
    df_ap = pd.DataFrame(ap_data)

    # Piutang Usaha (AR)
    ar_data = {
        'ID Invoice': ['INV-C001', 'INV-C002', 'INV-C003', 'INV-C004'],
        'Pelanggan': ['PT Klien Sejahtera', 'CV Mitra Abadi', 'PT Klien Sejahtera', 'PT Sukses Selalu'],
        'Tanggal Invoice': pd.to_datetime([datetime.now() - timedelta(days=45), datetime.now() - timedelta(days=15), datetime.now() - timedelta(days=10), datetime.now() - timedelta(days=2)]),
        'Jumlah': [50000000, 75000000, 25000000, 120000000],
        'Status': ['Lunas', 'Terkirim', 'Terkirim', 'Draf']
    }
    df_ar = pd.DataFrame(ar_data)
    
    # Anggaran vs Aktual
    budget_data = {
        'Kategori Biaya': ['Beban Gaji', 'Beban Sewa', 'Beban Marketing', 'Beban Operasional'],
        'Anggaran': [250000000, 80000000, 50000000, 35000000],
        'Aktual': [245000000, 80000000, 55000000, 30000000]
    }
    df_budget = pd.DataFrame(budget_data)
    df_budget['Varian'] = df_budget['Anggaran'] - df_budget['Aktual']
    df_budget['Varian (%)'] = (df_budget['Varian'] / df_budget['Anggaran']) * 100

    return df_coa, df_ap, df_ar, df_budget

df_coa, df_ap, df_ar, df_budget = create_financial_data()


# --- TABS UNTUK SETIAP MODUL ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard Keuangan",
    "📓 Akuntansi & Jurnal",
    "🧾 Hutang Usaha (AP)",
    "📈 Piutang Usaha (AR)",
    "⚖️ Pajak & Kepatuhan",
    "💡 Anggaran & Analisis"
])


# --- ISI TAB 1: DASHBOARD KEUANGAN ---
with tab1:
    st.header("Dashboard Kinerja Keuangan")
    st.markdown(f"Posisi per: `{datetime.now().strftime('%d %B %Y')}`")

    # KPI Utama
    kas_bank = 580500000  # Simulasi
    total_ar = df_ar[df_ar['Status'] == 'Terkirim']['Jumlah'].sum()
    total_ap = df_ap[df_ap['Status'] == 'Belum Dibayar']['Jumlah'].sum()
    pnl_mtd = 85750000 # Simulasi Profit/Loss Month-to-Date

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Posisi Kas & Bank", format_rupiah(kas_bank))
    col2.metric("Total Piutang (AR)", format_rupiah(total_ar), help="Total invoice yang belum dibayar oleh pelanggan.")
    col3.metric("Total Hutang (AP)", format_rupiah(total_ap), help="Total tagihan dari vendor yang belum dibayar.")
    col4.metric("Laba/Rugi (Bulan Ini)", format_rupiah(pnl_mtd), delta="15.2%")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Pendapatan vs. Biaya (3 Bulan Terakhir)")
        chart_pnl_data = pd.DataFrame({
            'Bulan': ['April 2025', 'Mei 2025', 'Juni 2025'],
            'Pendapatan': [250000000, 280000000, 310000000],
            'Biaya': [180000000, 195000000, 224250000]
        })
        st.bar_chart(chart_pnl_data.set_index('Bulan'))
        
    with col_chart2:
        st.subheader("Aging Piutang Usaha")
        aging_data = pd.DataFrame({
            'Kategori': ['Lancar (0-30 hr)', 'Telat (31-60 hr)', 'Telat (61-90 hr)', '> 90 hr'],
            'Jumlah': [df_ar[df_ar['Status'] == 'Terkirim']['Jumlah'].sum(), 45000000, 12000000, 5000000] # Simulasi data telat
        })
        st.bar_chart(aging_data.set_index('Kategori'))


# --- ISI TAB 2: AKUNTANSI & JURNAL ---
with tab2:
    st.header("📓 Akuntansi & Jurnal Umum (General Ledger)")
    st.info("Pencatatan semua transaksi keuangan perusahaan.")

    st.subheader("Input Jurnal Manual")
    with st.form("jurnal_form"):
        c1, c2 = st.columns([1, 2])
        tanggal_jurnal = c1.date_input("Tanggal Transaksi", datetime.now())
        keterangan_jurnal = c2.text_input("Keterangan Transaksi", "Contoh: Pembayaran beban sewa kantor Juni 2025")
        
        st.write("Detail Jurnal:")
        # Menggunakan data editor untuk input dinamis
        jurnal_detail = pd.DataFrame([
            {"Akun": "Beban Sewa", "Debit": 80000000, "Kredit": 0},
            {"Akun": "Kas & Bank", "Debit": 0, "Kredit": 80000000}
        ])
        edited_jurnal = st.data_editor(jurnal_detail, num_rows="dynamic", use_container_width=True)
        
        submitted = st.form_submit_button("Posting Jurnal")
        if submitted:
            total_debit = edited_jurnal['Debit'].sum()
            total_kredit = edited_jurnal['Kredit'].sum()
            if total_debit == total_kredit:
                st.success(f"Jurnal berhasil diposting! Total Debit: {format_rupiah(total_debit)}, Total Kredit: {format_rupiah(total_kredit)}")
            else:
                st.error(f"Jurnal tidak seimbang! Total Debit ({format_rupiah(total_debit)}) tidak sama dengan Total Kredit ({format_rupiah(total_kredit)}).")
    
    st.markdown("---")
    st.subheader("Bagan Akun (Chart of Accounts)")
    st.dataframe(df_coa, use_container_width=True)


# --- ISI TAB 3: HUTANG USAHA (AP) ---
with tab3:
    st.header("🧾 Hutang Usaha (Accounts Payable)")
    st.info("Mengelola semua tagihan dari vendor atau pemasok.")
    
    st.subheader("Daftar Tagihan Vendor")
    
    # Format kolom jumlah menjadi Rupiah
    df_ap_display = df_ap.copy()
    df_ap_display['Jumlah'] = df_ap_display['Jumlah'].apply(format_rupiah)
    
    st.dataframe(df_ap_display, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Proses Pembayaran (Simulasi)")
    tagihan_dipilih = st.multiselect("Pilih tagihan untuk dibayar:", 
                                     options=df_ap[df_ap['Status'] == 'Belum Dibayar']['ID Tagihan'])
    if tagihan_dipilih:
        total_pembayaran = df_ap[df_ap['ID Tagihan'].isin(tagihan_dipilih)]['Jumlah'].sum()
        st.write(f"**Total yang akan dibayar: {format_rupiah(total_pembayaran)}**")
        if st.button("Proses Pembayaran"):
            st.success(f"Pembayaran untuk tagihan {', '.join(tagihan_dipilih)} sebesar {format_rupiah(total_pembayaran)} berhasil diproses.")


# --- ISI TAB 4: PIUTANG USAHA (AR) ---
with tab4:
    st.header("📈 Piutang Usaha (Accounts Receivable)")
    st.info("Mengelola invoice untuk pelanggan dan memantau penerimaan.")
    
    col_ar1, col_ar2 = st.columns([2, 1])
    with col_ar1:
        st.subheader("Daftar Invoice Pelanggan")
        
        def highlight_status_ar(s):
            if s == 'Terkirim': return 'background-color: #fafa6e' # Yellow
            elif s == 'Lunas': return 'background-color: #79f77d' # Green
            elif s == 'Draf': return 'background-color: #e0e0e0' # Grey
            else: return ''
        
        df_ar_display = df_ar.copy()
        df_ar_display['Jumlah'] = df_ar_display['Jumlah'].apply(format_rupiah)
        st.dataframe(df_ar_display.style.map(highlight_status_ar, subset=['Status']), use_container_width=True)

    with col_ar2:
        st.subheader("Buat Invoice Baru (Simulasi)")
        with st.form("invoice_form"):
            pelanggan = st.selectbox("Pilih Pelanggan", ["PT Klien Sejahtera", "CV Mitra Abadi", "PT Sukses Selalu"])
            tgl_invoice = st.date_input("Tanggal Invoice", datetime.now())
            item = st.text_input("Deskripsi Jasa/Barang", "Jasa Konsultasi IT")
            jumlah = st.number_input("Jumlah Tagihan", min_value=0, value=10000000, step=100000)
            submit_invoice = st.form_submit_button("Simpan & Kirim Invoice")
            if submit_invoice:
                st.success(f"Invoice untuk {pelanggan} sebesar {format_rupiah(jumlah)} berhasil dibuat dan dikirim.")


# --- ISI TAB 5: PAJAK & KEPATUHAN ---
with tab5:
    st.header("⚖️ Pajak & Kepatuhan")
    st.info("Simulasi perhitungan dan jadwal pelaporan pajak.")
    
    c_tax1, c_tax2 = st.columns(2)
    with c_tax1:
        st.subheader("Kalkulator PPN (Pajak Pertambahan Nilai)")
        dpp = st.number_input("Dasar Pengenaan Pajak (DPP)", min_value=0, value=100000000, step=100000)
        ppn_rate = 0.11 # Tarif PPN 11%
        ppn_value = dpp * ppn_rate
        total_dengan_ppn = dpp + ppn_value
        st.metric("PPN (11%)", format_rupiah(ppn_value))
        st.metric("Total dengan PPN", format_rupiah(total_dengan_ppn))

    with c_tax2:
        st.subheader("Jadwal Pelaporan & Pembayaran Pajak")
        jadwal_pajak = {
            "Jenis Pajak": ["PPN Masa", "PPh Pasal 21", "PPh Badan Tahunan"],
            "Batas Bayar": ["Tanggal 15 Bulan Berikutnya", "Tanggal 10 Bulan Berikutnya", "30 April Tahun Berikutnya"],
            "Batas Lapor": ["Akhir Bulan Berikutnya", "Tanggal 20 Bulan Berikutnya", "30 April Tahun Berikutnya"]
        }
        st.table(pd.DataFrame(jadwal_pajak))


# --- ISI TAB 6: ANGGARAN & ANALISIS ---
with tab6:
    st.header("💡 Anggaran & Analisis Kinerja Keuangan (FP&A)")
    st.info("Membandingkan kinerja aktual dengan anggaran dan menganalisis kesehatan keuangan.")

    st.subheader("Analisis Anggaran vs. Aktual (Bulan Ini)")
    
    def style_varian(v):
        # Fungsi ini menerima nilai numerik dari kolom 'Varian'
        color = 'red' if v < 0 else 'green'
        return f'color: {color}'
        
    # ### PERBAIKAN DI SINI ###
    # Menggunakan .map (cara baru) untuk menggantikan .applymap yang usang
    st.dataframe(df_budget.style.map(style_varian, subset=['Varian']).format({
        'Anggaran': format_rupiah,
        'Aktual': format_rupiah,
        'Varian': format_rupiah,
        'Varian (%)': '{:.2f}%'
    }), use_container_width=True)

    st.markdown("---")
    st.subheader("Analisis Rasio Keuangan")
    c_rasio1, c_rasio2, c_rasio3 = st.columns(3)
    c_rasio1.metric("Rasio Lancar (Current Ratio)", "2.5x", help="Kemampuan membayar hutang jangka pendek. > 1.5x dianggap sehat.")
    c_rasio2.metric("Margin Laba Kotor (GPM)", "35.8%", help="Efisiensi biaya produksi terhadap pendapatan.")
    c_rasio3.metric("Rasio Utang terhadap Ekuitas (DER)", "0.8x", help="Tingkat leverage perusahaan. < 1.0x dianggap aman.")