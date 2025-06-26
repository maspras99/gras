import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    layout="wide",
    page_title="Sistem Digital Bagian Umum",
    page_icon="🏢"
)

# --- JUDUL UTAMA ---
st.title("🏢 Sistem Digital Terintegrasi - Bagian Umum")
st.markdown("Prototipe interaktif untuk modul-modul di bawah Manajer Umum.")

# --- MEMBUAT DATA SAMPEL (SIMULASI DATABASE) ---
def create_sample_data():
    # Data Karyawan
    karyawan_data = {
        'ID Karyawan': ['EMP-001', 'EMP-002', 'EMP-003', 'EMP-004', 'EMP-005'],
        'Nama': ['Budi Santoso', 'Citra Lestari', 'Doni Wijaya', 'Eka Putri', 'Fajar Nugraha'],
        'Jabatan': ['Staff HR', 'Akuntan', 'IT Support', 'Legal Officer', 'Receptionist'],
        'Departemen': ['Umum', 'Keuangan', 'Data & Informasi', 'Umum', 'Umum'],
        'Tanggal Masuk': pd.to_datetime(['2022-01-15', '2021-11-20', '2023-03-10', '2022-08-01', '2024-01-05']),
        'Status': ['Aktif', 'Aktif', 'Aktif', 'Aktif', 'Aktif']
    }
    df_karyawan = pd.DataFrame(karyawan_data)

    # Data Aset
    aset_data = {
        'ID Aset': ['ASSET-01', 'ASSET-02', 'ASSET-03', 'ASSET-04', 'ASSET-05'],
        'Nama Aset': ['Laptop Dell XPS 15', 'Mobil Toyota Avanza', 'Proyektor Epson', 'Laptop Macbook Pro', 'Motor Honda Vario'],
        'Kategori': ['Elektronik', 'Kendaraan', 'Elektronik', 'Elektronik', 'Kendaraan'],
        'Pengguna': ['Doni Wijaya', 'Operasional', 'Umum', 'Citra Lestari', 'Operasional'],
        'Status': ['Digunakan', 'Tersedia', 'Tersedia', 'Digunakan', 'Perbaikan']
    }
    df_aset = pd.DataFrame(aset_data)

    # Data Tiket Helpdesk
    tiket_data = {
        'ID Tiket': ['TKT-101', 'TKT-102', 'TKT-103', 'TKT-104'],
        'Pelapor': ['Citra Lestari', 'Budi Santoso', 'Fajar Nugraha', 'Doni Wijaya'],
        'Kategori': ['IT', 'HR', 'GA', 'IT'],
        'Judul': ['Tidak bisa login ke sistem ERP', 'Permintaan data cuti', 'Lampu ruangan mati', 'Request instalasi software'],
        'Tanggal': pd.to_datetime([datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1), datetime.now(), datetime.now()]),
        'Status': ['Selesai', 'Dalam Proses', 'Baru', 'Baru']
    }
    df_tiket = pd.DataFrame(tiket_data)
    
    # Data Dokumen Legal
    legal_data = {
        'ID Dokumen': ['LGL-001', 'LGL-002', 'LGL-003'],
        'Nama Dokumen': ['Perjanjian Sewa Gedung Kantor', 'Izin Usaha Perdagangan (SIUP)', 'Perjanjian Kerja Sama Klien A'],
        'Jenis': ['Perjanjian', 'Perizinan', 'Perjanjian'],
        'Tanggal Terbit': pd.to_datetime(['2022-07-01', '2021-09-15', '2023-05-20']),
        'Tanggal Kedaluwarsa': pd.to_datetime(['2025-07-01', '2026-09-15', '2025-08-20']),
    }
    df_legal = pd.DataFrame(legal_data)

    return df_karyawan, df_aset, df_tiket, df_legal

df_karyawan, df_aset, df_tiket, df_legal = create_sample_data()


# --- TABS UNTUK SETIAP MODUL ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard Utama", 
    "👥 Modul Personalia (HRIS)", 
    "🚚 Modul Administrasi & Aset (GA)",
    "🎫 Modul Layanan Internal (Help Desk)",
    "⚖️ Modul Legal & Kepatuhan",
    "📰 Modul Humas (PR)"
])


# --- ISI TAB 1: DASHBOARD UTAMA ---
with tab1:
    st.header("Ringkasan Kinerja Bagian Umum")
    st.markdown(f"Data diperbarui pada: `{datetime.now().strftime('%d %B %Y, %H:%M:%S')}`")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Karyawan Aktif", f"{df_karyawan[df_karyawan['Status'] == 'Aktif'].shape[0]} Orang")
    col2.metric("🚚 Total Aset Terdaftar", f"{df_aset.shape[0]} Unit")
    col3.metric("🎫 Tiket Helpdesk Terbuka", f"{df_tiket[df_tiket['Status'] != 'Selesai'].shape[0]} Tiket")
    col4.metric("⚖️ Dokumen Akan Kedaluwarsa", f"{df_legal[df_legal['Tanggal Kedaluwarsa'] < datetime.now() + timedelta(days=365)].shape[0]} Dok")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Status Tiket Helpdesk")
        chart_data = df_tiket['Status'].value_counts().reset_index()
        chart_data.columns = ['Status', 'Jumlah']
        st.bar_chart(chart_data.set_index('Status'))

    with col_chart2:
        st.subheader("Aset Berdasarkan Kategori")
        chart_data_aset = df_aset['Kategori'].value_counts().reset_index()
        chart_data_aset.columns = ['Kategori', 'Jumlah']
        st.bar_chart(chart_data_aset.set_index('Kategori'))


# --- ISI TAB 2: MODUL PERSONALIA (HRIS) ---
with tab2:
    st.header("👥 Human Resource Information System (HRIS)")
    st.info("Mengelola data karyawan, pengajuan cuti, dan penilaian kinerja.")
    
    st.subheader("Database Karyawan")
    search_query = st.text_input("Cari Nama Karyawan:", key="hr_search")
    if search_query:
        result_df = df_karyawan[df_karyawan['Nama'].str.contains(search_query, case=False)]
    else:
        result_df = df_karyawan
    st.dataframe(result_df, use_container_width=True)

    st.markdown("---")
    
    col_form, col_view = st.columns([1, 2])
    with col_form:
        st.subheader("Formulir Pengajuan Cuti (Simulasi)")
        with st.form("form_cuti"):
            nama_karyawan = st.selectbox("Pilih Nama Karyawan", options=df_karyawan['Nama'])
            jenis_cuti = st.selectbox("Jenis Cuti", options=["Cuti Tahunan", "Cuti Sakit", "Cuti Melahirkan"])
            tgl_mulai = st.date_input("Tanggal Mulai")
            tgl_selesai = st.date_input("Tanggal Selesai")
            keterangan = st.text_area("Keterangan")
            submitted = st.form_submit_button("Ajukan Cuti")
            if submitted:
                st.success(f"Pengajuan cuti untuk {nama_karyawan} dari {tgl_mulai} hingga {tgl_selesai} berhasil diajukan!")

    with col_view:
        st.subheader("Penilaian Kinerja (Contoh)")
        karyawan_eval = st.selectbox("Pilih Karyawan untuk Evaluasi", options=df_karyawan['Nama'], key="eval")
        st.write(f"**Evaluasi Kinerja untuk: {karyawan_eval}**")
        
        kpi1 = st.slider("KPI 1: Kualitas Kerja", 1, 5, 4)
        kpi2 = st.slider("KPI 2: Ketepatan Waktu", 1, 5, 5)
        kpi3 = st.slider("KPI 3: Kerjasama Tim", 1, 5, 4)
        
        skor_akhir = round((kpi1 + kpi2 + kpi3) / 3, 2)
        st.metric("Skor Kinerja Akhir", skor_akhir)
        st.text_area("Catatan dari Manajer:")

# --- ISI TAB 3: MODUL ADMINISTRASI & ASET (GA) ---
with tab3:
    st.header("🚚 Administrasi Umum & Manajemen Aset")
    st.info("Mengelola aset perusahaan, reservasi fasilitas, dan tugas operasional.")
    
    st.subheader("Database Aset Perusahaan")
    # Menggunakan st.data_editor agar terasa seperti bisa diedit
    st.data_editor(df_aset, use_container_width=True, num_rows="dynamic")

    st.markdown("---")

    col_res, col_task = st.columns(2)
    with col_res:
        st.subheader("Reservasi Fasilitas (Simulasi)")
        fasilitas = st.selectbox("Pilih Fasilitas", ["Ruang Meeting A", "Ruang Meeting B", "Mobil Operasional 1 (Avanza)"])
        tgl_reservasi = st.date_input("Tanggal", key="res_date")
        waktu_mulai = st.time_input("Waktu Mulai", value=datetime.now().time())
        waktu_selesai = st.time_input("Waktu Selesai", value=(datetime.now() + timedelta(hours=1)).time())
        if st.button("Cek Ketersediaan & Pesan"):
            st.success(f"{fasilitas} berhasil dipesan untuk {tgl_reservasi} dari {waktu_mulai} hingga {waktu_selesai}.")

    with col_task:
        st.subheader("Manajemen Tugas Operasional (Driver/Office Boy)")
        tasks = {
            'Selesai': [True, False, False],
            'Tugas': ['Antar dokumen ke Klien A', 'Beli ATK', 'Siapkan ruang meeting B'],
            'PIC': ['Driver', 'Office Boy', 'Office Boy'],
            'Deadline': [datetime.now().strftime('%H:%M'), (datetime.now() + timedelta(hours=2)).strftime('%H:%M'), (datetime.now() + timedelta(hours=1)).strftime('%H:%M')]
        }
        df_tasks = pd.DataFrame(tasks)
        st.data_editor(df_tasks, use_container_width=True, disabled=['Tugas', 'PIC', 'Deadline'])


# --- ISI TAB 4: MODUL LAYANAN INTERNAL (HELP DESK) ---
with tab4:
    st.header("🎫 Sistem Tiket Layanan Internal (Help Desk)")
    st.info("Satu pintu untuk semua permintaan bantuan internal (IT, GA, HR).")
    
    col_tkt_form, col_tkt_list = st.columns([1, 2])
    with col_tkt_form:
        st.subheader("Buat Tiket Baru")
        with st.form("form_tiket"):
            pelapor = st.selectbox("Nama Pelapor", options=df_karyawan['Nama'])
            kategori = st.selectbox("Kategori Masalah", ["IT", "GA (General Affairs)", "HR (Personalia)"])
            judul = st.text_input("Judul Masalah")
            deskripsi = st.text_area("Deskripsi Detail")
            submit_tkt = st.form_submit_button("Kirim Tiket")
            if submit_tkt:
                st.success(f"Tiket '{judul}' berhasil dibuat. Tim {kategori} akan segera menindaklanjuti.")
    
    with col_tkt_list:
        st.subheader("Daftar Tiket Aktif")
        
        def highlight_status(s):
            if s == 'Baru': return 'background-color: #fafa6e'
            elif s == 'Dalam Proses': return 'background-color: #6eb5fa'
            elif s == 'Selesai': return 'background-color: #79f77d'
            else: return ''
        
        # ### PERBAIKAN DI SINI ###
        # Menggunakan .map (cara baru yang direkomendasikan) untuk menghindari warning
        st.dataframe(df_tiket.style.map(highlight_status, subset=['Status']), use_container_width=True)


# --- ISI TAB 5: MODUL LEGAL & KEPATUHAN ---
with tab5:
    st.header("⚖️ Manajemen Dokumen Legal & Kepatuhan")
    st.info("Mengelola dokumen legal perusahaan dan memastikan kepatuhan terhadap regulasi.")

    st.subheader("Database Dokumen Legal")
    st.dataframe(df_legal, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Pengingat Kedaluwarsa")
    days_threshold = st.slider("Tampilkan dokumen yang akan kedaluwarsa dalam (hari):", 30, 365, 90)
    
    soon_to_expire_df = df_legal[
        (df_legal['Tanggal Kedaluwarsa'] > datetime.now()) &
        (df_legal['Tanggal Kedaluwarsa'] <= datetime.now() + timedelta(days=days_threshold))
    ]
    
    if not soon_to_expire_df.empty:
        st.warning(f"Ditemukan {soon_to_expire_df.shape[0]} dokumen akan kedaluwarsa:")
        st.dataframe(soon_to_expire_df, use_container_width=True)
    else:
        st.success(f"Tidak ada dokumen yang akan kedaluwarsa dalam {days_threshold} hari ke depan.")

    st.markdown("---")
    st.subheader("Upload Dokumen Baru (Simulasi)")
    uploaded_file = st.file_uploader("Pilih file PDF, DOCX, atau gambar...", type=['pdf', 'docx', 'jpg', 'png'])
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' berhasil diunggah dan siap untuk diarsipkan.")

# --- ISI TAB 6: MODUL HUMAS (PR) ---
with tab6:
    st.header("📰 Manajemen Hubungan Masyarakat (Humas/PR)")
    st.info("Merencanakan dan melacak kegiatan PR serta mengelola kontak media.")

    col_pr1, col_pr2 = st.columns(2)
    with col_pr1:
        st.subheader("Jadwal Kegiatan & Press Release")
        pr_schedule_data = {
            "Tanggal": [datetime.now().date() + timedelta(days=7), datetime.now().date() + timedelta(days=15)],
            "Kegiatan": ["Press Conference Peluncuran Superapp", "Media Gathering Q3 2025"],
            "Status": ["Direncakanan", "Direncakanan"]
        }
        df_pr_schedule = pd.DataFrame(pr_schedule_data)
        st.table(df_pr_schedule)

    with col_pr2:
        st.subheader("Monitoring Pemberitaan (Contoh)")
        news_data = {
            "Media": ["Detik.com", "Kompas.com"],
            "Judul Berita": ["Perusahaan X Siap Luncurkan Superapp...", "Inovasi Digital dari Perusahaan X..."],
            "Sentimen": ["Positif", "Positif"]
        }
        df_news = pd.DataFrame(news_data)
        st.dataframe(df_news, use_container_width=True)

    st.markdown("---")
    st.subheader("Manajemen Kontak Media")
    media_contacts = {
        'Nama Kontak': ['Andi Pratama', 'Sari Dewi'],
        'Media': ['Detik.com', 'Kompas.com'],
        'Posisi': ['Jurnalis Teknologi', 'Editor Ekonomi'],
        'Email': ['andi.p@detik.com', 'sari.d@kompas.com']
    }
    df_media = pd.DataFrame(media_contacts)
    st.dataframe(df_media, use_container_width=True)