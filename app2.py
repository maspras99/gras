import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(layout="wide", page_title="WBS Interaktif: Pengembangan Platform Digital")

st.title("WBS Interaktif: Pengembangan Platform Digital Revolusioner")
st.markdown("---")

# --- Inisialisasi Database ---
def init_db():
    conn = sqlite3.connect('wbs_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  section TEXT,
                  wbs_id TEXT,
                  task_name TEXT,
                  description TEXT,
                  personnel_role TEXT,
                  personnel_count INTEGER,
                  start_date TEXT,
                  end_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  wbs_id TEXT,
                  milestone_name TEXT,
                  milestone_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Fungsi untuk Memuat Data dari Database ---
def load_tasks():
    conn = sqlite3.connect('wbs_database.db')
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()
    return df.to_dict('records') if not df.empty else []

def load_milestones():
    conn = sqlite3.connect('wbs_database.db')
    df = pd.read_sql_query("SELECT * FROM milestones", conn)
    conn.close()
    return df.to_dict('records') if not df.empty else []

# --- Inisialisasi Session State untuk Data Tugas dan Milestone ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()
if 'milestones' not in st.session_state:
    st.session_state.milestones = load_milestones()

# --- Data WBS Awal Berdasarkan Dokumen ---
initial_wbs_structure = {
    "Manajemen Proyek (PMO)": [
        {"id": "1.1", "name": "Inisiasi Proyek", "desc": "Proses awal proyek."},
        {"id": "1.1.1", "name": "Mendefinisikan Piagam Proyek", "desc": "Membuat dokumen piagam proyek."},
        {"id": "1.1.2", "name": "Mengidentifikasi Stakeholder Kunci", "desc": "Identifikasi pihak terkait."},
        {"id": "1.1.3", "name": "Mengadakan Rapat Kick-off Proyek", "desc": "Rapat pembukaan proyek."},
        {"id": "1.2", "name": "Perencanaan Proyek", "desc": "Merencanakan seluruh aspek proyek."},
        {"id": "1.2.1", "name": "Mengembangkan Rencana Proyek Induk", "desc": "Membuat rencana utama proyek."},
        {"id": "1.2.1.1", "name": "Menetapkan Ruang Lingkup Proyek", "desc": "Tentukan batasan proyek."},
        {"id": "1.2.1.2", "name": "Membuat Jadwal Proyek Detil", "desc": "Buat Gantt Chart."},
        {"id": "1.2.1.3", "name": "Menentukan Anggaran Proyek", "desc": "Tetapkan anggaran."},
        {"id": "1.2.1.4", "name": "Mendefinisikan Metodologi Pengembangan", "desc": "Pilih Agile/Waterfall."},
        {"id": "1.2.2", "name": "Menyusun Rencana Manajemen Risiko", "desc": "Identifikasi dan mitigasi risiko."},
        {"id": "1.2.3", "name": "Menyusun Rencana Komunikasi Proyek", "desc": "Rencanakan komunikasi."},
        {"id": "1.2.4", "name": "Menyusun Rencana Kualitas Proyek", "desc": "Atur standar kualitas."},
        {"id": "1.2.5", "name": "Menyusun Rencana Sumber Daya Proyek", "desc": "Kelola sumber daya."},
        {"id": "1.3", "name": "Eksekusi Proyek", "desc": "Melaksanakan rencana proyek."},
        {"id": "1.3.1", "name": "Mengelola Tim Proyek", "desc": "Koordinasi antar bagian."},
        {"id": "1.3.2", "name": "Mengadakan Rapat Kemajuan Reguler", "desc": "Rapat stand-up/sprint review."},
        {"id": "1.3.3", "name": "Mengelola Permintaan Perubahan", "desc": "Proses change request."},
        {"id": "1.3.4", "name": "Mengkoordinasikan Sumber Daya", "desc": "Kelola manusia dan materi."},
        {"id": "1.4", "name": "Pemantauan & Kontrol Proyek", "desc": "Pantau dan kendalikan proyek."},
        {"id": "1.4.1", "name": "Melacak Kemajuan Proyek", "desc": "Cek jadwal proyek."},
        {"id": "1.4.2", "name": "Memantau Penggunaan Anggaran", "desc": "Pantau anggaran."},
        {"id": "1.4.3", "name": "Mengidentifikasi dan Mengatasi Risiko", "desc": "Kelola risiko proyek."},
        {"id": "1.4.4", "name": "Melaporkan Status Proyek", "desc": "Lapor ke stakeholder."},
        {"id": "1.4.5", "name": "Melakukan Kontrol Kualitas Deliverables", "desc": "Periksa kualitas output."},
        {"id": "1.5", "name": "Penutupan Proyek", "desc": "Selesaikan dan tutup proyek."},
        {"id": "1.5.1", "name": "Memverifikasi Penyelesaian Cakupan", "desc": "Cek penyelesaian cakupan."},
        {"id": "1.5.2", "name": "Mengumpulkan Pembelajaran", "desc": "Dokumentasi lesson learned."},
        {"id": "1.5.3", "name": "Mengarsipkan Dokumentasi Proyek", "desc": "Arsipkan dokumen."},
        {"id": "1.5.4", "name": "Melakukan Serah Terima Proyek", "desc": "Serah terima ke pemilik."},
    ],
    "Bagian Umum": [
        {"id": "2.1", "name": "Personalia & Legal", "desc": "Kelola SDM dan kepatuhan hukum."},
        {"id": "2.1.1", "name": "Analisis Kebutuhan Sumber Daya Tambahan", "desc": "Evaluasi kebutuhan SDM."},
        {"id": "2.1.2", "name": "Proses Rekrutmen & Onboarding", "desc": "Rekrut dan onboard karyawan."},
        {"id": "2.1.3", "name": "Review Kontrak Vendor Eksternal", "desc": "Periksa kontrak pihak ketiga."},
        {"id": "2.1.4", "name": "Memastikan Kepatuhan Regulasi", "desc": "Koordinasi dengan security & legal."},
        {"id": "2.2", "name": "Humas & Komunikasi Internal", "desc": "Kelola komunikasi internal."},
        {"id": "2.2.1", "name": "Mengembangkan Strategi Komunikasi Internal", "desc": "Buat strategi komunikasi."},
        {"id": "2.2.2", "name": "Mengelola Informasi & Pengumuman", "desc": "Bagikan info ke karyawan."},
        {"id": "2.2.3", "name": "Mengkoordinasikan Acara Internal", "desc": "Atur event kick-off/selebrasi."},
        {"id": "2.3", "name": "Administrasi Umum & Sekretaris", "desc": "Dukung administrasi proyek."},
        {"id": "2.3.1", "name": "Mengelola Fasilitas & Perlengkapan", "desc": "Sediakan fasilitas proyek."},
        {"id": "2.3.2", "name": "Mendukung Perjalanan Dinas", "desc": "Atur perjalanan tim."},
        {"id": "2.3.3", "name": "Mengelola Dokumen Administratif", "desc": "Kelola dokumen proyek."},
        {"id": "2.3.4", "name": "Dukungan Help Desk & IT", "desc": "Koordinasi tech support."},
        {"id": "2.3.5", "name": "Peran Security & Office Boy", "desc": "Pengamanan dan kebersihan."},
    ],
    "Bagian Keuangan": [
        {"id": "3.1", "name": "Anggaran Proyek", "desc": "Kelola anggaran proyek."},
        {"id": "3.1.1", "name": "Menyusun Anggaran Detil per Fase", "desc": "Buat anggaran per fase."},
        {"id": "3.1.2", "name": "Mengalokasikan Dana per Departemen", "desc": "Alokasikan dana departemen."},
        {"id": "3.2", "name": "Akuntansi & Pelaporan Keuangan Proyek", "desc": "Kelola akuntansi proyek."},
        {"id": "3.2.1", "name": "Memproses Pembayaran Vendor & Gaji", "desc": "Proses pembayaran."},
        {"id": "3.2.2", "name": "Melacak Pengeluaran vs. Anggaran", "desc": "Pantau pengeluaran."},
        {"id": "3.2.3", "name": "Menyusun Laporan Keuangan Reguler", "desc": "Buat laporan keuangan."},
        {"id": "3.3", "name": "Pajak & Kepatuhan Keuangan", "desc": "Pastikan kepatuhan pajak."},
        {"id": "3.3.1", "name": "Memastikan Kepatuhan Pajak", "desc": "Cek kepatuhan pajak."},
        {"id": "3.3.2", "name": "Mengelola Aspek Legal Keuangan", "desc": "Kelola legal keuangan."},
        {"id": "3.4", "name": "Analisis Keuangan Proyek", "desc": "Analisis keuangan proyek."},
        {"id": "3.4.1", "name": "Melakukan Analisis Biaya-Manfaat", "desc": "Hitung cost-benefit."},
        {"id": "3.4.2", "name": "Menghitung ROI Proyek", "desc": "Hitung return on investment."},
        {"id": "3.4.3", "name": "Membuat Proyeksi Keuangan", "desc": "Buat proyeksi keuangan."},
    ],
    "Bagian Marketing": [
        {"id": "4.1", "name": "Riset Pasar & Audiens", "desc": "Lakukan riset pasar."},
        {"id": "4.1.1", "name": "Melakukan Riset Kebutuhan Pengguna", "desc": "Analisis kebutuhan pengguna."},
        {"id": "4.1.2", "name": "Menganalisis Kompetitor & Tren", "desc": "Cek kompetitor dan tren."},
        {"id": "4.1.3", "name": "Mengidentifikasi Target Audiens", "desc": "Tentukan audiens utama."},
        {"id": "4.2", "name": "Pengembangan Strategi Pemasaran", "desc": "Buat strategi pemasaran."},
        {"id": "4.2.1", "name": "Mendefinisikan Nilai Jual Unik", "desc": "Tentukan USP produk."},
        {"id": "4.2.2", "name": "Merumuskan Pesan Pemasaran", "desc": "Buat pesan pemasaran."},
        {"id": "4.2.3", "name": "Menentukan Saluran Pemasaran", "desc": "Pilih saluran pemasaran."},
        {"id": "4.2.4", "name": "Menyusun Rencana Kampanye", "desc": "Buat rencana peluncuran."},
        {"id": "4.3", "name": "Produksi Konten & Materi Pemasaran", "desc": "Buat konten pemasaran."},
        {"id": "4.3.1", "name": "Mendesain Branding & Identitas Visual", "desc": "Buat branding produk."},
        {"id": "4.3.2", "name": "Menulis Konten Iklan & Promosi", "desc": "Buat konten iklan."},
        {"id": "4.3.3", "name": "Membuat Aset Visual & Video", "desc": "Buat aset visual/video."},
        {"id": "4.3.4", "name": "Mengembangkan Materi Penjualan", "desc": "Buat sales kit."},
        {"id": "4.4", "name": "Peluncuran & Promosi", "desc": "Luncurkan dan promosikan."},
        {"id": "4.4.1", "name": "Mengimplementasikan Kampanye Digital", "desc": "Jalankan kampanye digital."},
        {"id": "4.4.2", "name": "Melakukan Aktivitas Public Relations", "desc": "Atur media outreach."},
        {"id": "4.4.3", "name": "Mengorganisir Event Peluncuran", "desc": "Atur event peluncuran."},
        {"id": "4.5", "name": "Penjualan & Penagihan", "desc": "Kelola penjualan dan penagihan."},
        {"id": "4.5.1", "name": "Mengembangkan Strategi Penjualan", "desc": "Buat strategi penjualan."},
        {"id": "4.5.2", "name": "Menyusun Target Penjualan", "desc": "Tetapkan target penjualan."},
        {"id": "4.5.3", "name": "Melakukan Aktivitas Pra-Penjualan", "desc": "Jalankan lead generation."},
        {"id": "4.5.4", "name": "Mengelola Proses Penagihan", "desc": "Koordinasi dengan keuangan."},
    ],
    "Bagian Data & Informasi": [
        {"id": "5.1", "name": "Software", "desc": "Kembangkan aplikasi dan UI/UX."},
        {"id": "5.1.1", "name": "Research & Development", "desc": "Riset dan pengembangan."},
        {"id": "5.1.1.1", "name": "Analisis Kebutuhan Fungsional & Non-Fungsional", "desc": "Analisis kebutuhan produk."},
        {"id": "5.1.1.2", "name": "Merumuskan Spesifikasi Teknis", "desc": "Buat spesifikasi teknis."},
        {"id": "5.1.1.3", "name": "Riset Teknologi & Alat", "desc": "Pilih teknologi yang tepat."},
        {"id": "5.1.1.4", "name": "Desain Arsitektur Sistem", "desc": "Rancang arsitektur sistem."},
        {"id": "5.1.1.5", "name": "Melakukan Proof of Concept", "desc": "Uji konsep teknologi baru."},
        {"id": "5.1.1.6", "name": "Perencanaan Skalabilitas & Keamanan", "desc": "Rencanakan skalabilitas."},
        {"id": "5.1.1.7", "name": "Pengembangan Algoritma Kunci", "desc": "Kembangkan AI/ML jika ada."},
        {"id": "5.1.2", "name": "Creative Director & UI/UX Designer", "desc": "Desain UX dan UI."},
        {"id": "5.1.2.1", "name": "Desain Pengalaman Pengguna", "desc": "Lakukan UX research."},
        {"id": "5.1.2.2", "name": "Desain Antarmuka Pengguna", "desc": "Buat wireframes dan mockups."},
        {"id": "5.1.2.3", "name": "Mengembangkan Desain Sistem", "desc": "Buat design system."},
        {"id": "5.1.2.4", "name": "Uji Usability", "desc": "Lakukan user testing."},
        {"id": "5.1.3", "name": "Mobile Development", "desc": "Kembangkan aplikasi mobile."},
        {"id": "5.1.3.1", "name": "Pengembangan Aplikasi Android", "desc": "Kembangkan aplikasi Android."},
        {"id": "5.1.3.2", "name": "Pengembangan Aplikasi iOS", "desc": "Kembangkan aplikasi iOS."},
        {"id": "5.1.3.3", "name": "Integrasi API dengan Backend", "desc": "Integrasi API."},
        {"id": "5.1.3.4", "name": "Pengujian Unit & Integrasi", "desc": "Uji aplikasi mobile."},
        {"id": "5.1.4", "name": "Fullstack Programmer", "desc": "Kembangkan frontend dan backend."},
        {"id": "5.1.4.1", "name": "Pengembangan Frontend Web", "desc": "Kembangkan frontend web."},
        {"id": "5.1.4.2", "name": "Pengembangan Backend Aplikasi", "desc": "Kembangkan backend."},
        {"id": "5.1.4.3", "name": "Integrasi dengan Database", "desc": "Integrasi database."},
        {"id": "5.1.4.4", "name": "Pengujian Unit & Integrasi", "desc": "Uji aplikasi web."},
        {"id": "5.1.5", "name": "Ahli Database", "desc": "Kelola database."},
        {"id": "5.1.5.1", "name": "Desain Skema Database", "desc": "Rancang skema database."},
        {"id": "5.1.5.2", "name": "Implementasi Database", "desc": "Implementasikan database."},
        {"id": "5.1.5.3", "name": "Optimasi Query & Performa", "desc": "Optimasi database."},
        {"id": "5.1.5.4", "name": "Perencanaan Backup & Recovery", "desc": "Rencanakan backup."},
        {"id": "5.1.6", "name": "DevOps Engineer", "desc": "Kelola deployment dan infrastruktur."},
        {"id": "5.1.6.1", "name": "Implementasi CI/CD Pipeline", "desc": "Atur CI/CD pipeline."},
        {"id": "5.1.6.2", "name": "Otomatisasi Deployment", "desc": "Otomatisasi infrastruktur."},
        {"id": "5.1.6.3", "name": "Pemantauan Aplikasi", "desc": "Pantau aplikasi."},
        {"id": "5.1.6.4", "name": "Manajemen Log & Audit Trail", "desc": "Kelola log dan audit."},
        {"id": "5.1.7", "name": "Graphic Designer & Copywriter", "desc": "Buat aset grafis dan teks."},
        {"id": "5.1.7.1", "name": "Mendesain Aset Grafis untuk Aplikasi", "desc": "Buat ikon dan ilustrasi."},
        {"id": "5.1.7.2", "name": "Mendesain Visual untuk Website", "desc": "Buat visual website."},
        {"id": "5.1.7.3", "name": "Menulis Mikrocopy dalam Aplikasi", "desc": "Buat teks aplikasi."},
        {"id": "5.1.7.4", "name": "Menyusun Teks Deskriptif", "desc": "Buat deskripsi fitur."},
        {"id": "5.1.8", "name": "Video Grapher & Editor", "desc": "Buat dan edit video."},
        {"id": "5.1.8.1", "name": "Merencanakan & Mengambil Rekaman", "desc": "Rencana dan ambil video."},
        {"id": "5.1.8.2", "name": "Mengedit Video Promosi", "desc": "Edit video promosi."},
        {"id": "5.1.9", "name": "Support (Tech Support)", "desc": "Dukung teknis produk."},
        {"id": "5.1.9.1", "name": "Mengembangkan Dokumentasi Produk", "desc": "Buat dokumentasi pengguna."},
        {"id": "5.1.9.2", "name": "Menyusun FAQ & Artikel Bantuan", "desc": "Buat FAQ dan artikel."},
        {"id": "5.1.9.3", "name": "Memberikan Dukungan Teknis", "desc": "Dukung selama uji coba."},
        {"id": "5.2", "name": "Data Center & Cyber Security", "desc": "Kelola data center dan keamanan."},
        {"id": "5.2.1", "name": "Data Center & IT Infrastructure", "desc": "Atur infrastruktur server."},
        {"id": "5.2.1.1", "name": "Perencanaan Infrastruktur Server", "desc": "Rencanakan server."},
        {"id": "5.2.1.2", "name": "Pengadaan & Konfigurasi Server", "desc": "Konfigurasi server."},
        {"id": "5.2.1.3", "name": "Desain & Implementasi Jaringan", "desc": "Rancang jaringan."},
        {"id": "5.2.1.4", "name": "Konfigurasi Cloud Services", "desc": "Atur layanan cloud."},
        {"id": "5.2.1.5", "name": "Manajemen Penyimpanan Data", "desc": "Kelola penyimpanan."},
        {"id": "5.2.1.6", "name": "Implementasi Sistem Operasi", "desc": "Pasang sistem operasi."},
        {"id": "5.2.1.7", "name": "Manajemen Backup & Disaster Recovery", "desc": "Rencanakan backup."},
        {"id": "5.2.1.8", "name": "Monitoring Performa Infrastruktur", "desc": "Pantau infrastruktur."},
        {"id": "5.2.1.9", "name": "Penanganan Insiden Operasional", "desc": "Tangani insiden."},
        {"id": "5.2.2", "name": "Cyber Security", "desc": "Pastikan keamanan sistem."},
        {"id": "5.2.2.1", "name": "Desain Keamanan Sistem", "desc": "Review arsitektur keamanan."},
        {"id": "5.2.2.2", "name": "Menetapkan Kebijakan Keamanan", "desc": "Buat kebijakan keamanan."},
        {"id": "5.2.2.3", "name": "Melakukan Penilaian Kerentanan", "desc": "Lakukan vulnerability assessment."},
        {"id": "5.2.2.4", "name": "Melakukan Penetration Testing", "desc": "Uji penetrasi sistem."},
        {"id": "5.2.2.5", "name": "Mengembangkan Rencana Tanggap Insiden", "desc": "Buat rencana tanggap insiden."},
        {"id": "5.2.2.6", "name": "Melakukan Forensik Digital", "desc": "Analisis insiden jika ada."},
        {"id": "5.2.2.7", "name": "Implementasi Kontrol Keamanan", "desc": "Pasang firewall dan IDS."},
        {"id": "5.2.2.8", "name": "Menerapkan Praktik DevSecOps", "desc": "Integrasi DevSecOps."},
        {"id": "5.2.2.9", "name": "Audit Keamanan Sistem", "desc": "Lakukan audit berkala."},
        {"id": "5.2.2.10", "name": "Pelatihan Kesadaran Keamanan", "desc": "Latih tim proyek."},
    ]
}

# --- Fungsi untuk Menyimpan Data ke Database ---
def save_task(task):
    conn = sqlite3.connect('wbs_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (section, wbs_id, task_name, description, personnel_role, personnel_count, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (task['section'], task['wbs_id'], task['task_name'], task['description'], task['personnel_role'], task['personnel_count'], task['start_date'].strftime('%Y-%m-%d'), task['end_date'].strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()

def save_milestone(wbs_id, milestone_name, milestone_date):
    conn = sqlite3.connect('wbs_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO milestones (wbs_id, milestone_name, milestone_date) VALUES (?, ?, ?)",
              (wbs_id, milestone_name, milestone_date.strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()

# --- Sidebar untuk Navigasi dan Input Form ---
st.sidebar.header("Navigasi & Input")
menu_selection = st.sidebar.radio(
    "Pilih Menu:",
    ("Input Tugas Baru", "Lihat WBS & Analisis")
)

# --- Fungsi untuk Menambah Tugas Baru ---
if menu_selection == "Input Tugas Baru":
    st.header("Input Tugas, Personil, dan Timeline Baru")

    st.subheader("Detail Tugas")
    
    # Dropdown untuk bagian utama - DI LUAR FORM agar bisa berinteraksi real-time
    selected_section_form = st.selectbox(
        "Pilih Bagian Utama:",
        list(initial_wbs_structure.keys()),
        key="selected_section_form"
    )

    # Dapatkan sub-sections berdasarkan bagian utama yang dipilih
    sub_sections = initial_wbs_structure[selected_section_form]
    sub_section_options = [f"{s['id']} {s['name']} - {s['desc']}" for s in sub_sections]
    
    # Dropdown untuk sub-bagian - DI LUAR FORM agar bisa berubah real-time
    selected_sub_section_str = st.selectbox(
        "Pilih Sub-Bagian (WBS ID & Nama):",
        sub_section_options,
        key="sub_section_selectbox"
    )

    # Ekstrak WBS ID, Nama, dan Deskripsi dari pilihan sub-section
    wbs_id = selected_sub_section_str.split(' ')[0]
    task_name_from_wbs = " ".join(selected_sub_section_str.split(' ')[1:]).split(' - ')[0].strip()
    description_from_wbs = selected_sub_section_str.split(' - ')[1].strip()

    # Inisialisasi atau update session state berdasarkan pilihan WBS
    if 'current_wbs_selection' not in st.session_state or st.session_state.current_wbs_selection != selected_sub_section_str:
        st.session_state.current_wbs_selection = selected_sub_section_str
        st.session_state.default_task_name = task_name_from_wbs
        st.session_state.default_description = description_from_wbs

    # FORM dimulai di sini - hanya untuk input yang tidak perlu interaksi real-time
    with st.form("task_input_form"):
        # Input untuk nama tugas dan deskripsi dengan nilai default dari session state
        custom_task_name = st.text_input(
            "Nama Tugas Detil (misal: 'Pembuatan SOP HRD')",
            value=st.session_state.get('default_task_name', task_name_from_wbs),
            key="custom_task_name_input"
        )
        custom_description = st.text_area(
            "Uraian Tugas Detil",
            value=st.session_state.get('default_description', description_from_wbs),
            key="custom_description_input"
        )

        st.subheader("Detail Personil")
        # Combo box untuk peran personil berdasarkan bagian utama
        personnel_roles = {
            "Manajemen Proyek (PMO)": ["Project Manager", "Coordinator", "Quality Assurance"],
            "Bagian Umum": ["Manajer Umum", "Personalia", "Legal", "Humas", "Administrasi Umum", "Respsionis", "Help Desk", "Security", "Driver", "Office Boy"],
            "Bagian Keuangan": ["Manajer Keuangan", "Akuntan", "Pajak", "Administrasi Keuangan"],
            "Bagian Marketing": ["Penjualan dan Penagihan"],
            "Bagian Data & Informasi": [
                "Manajer Software", "Ahli Sistem Analis", "Ahli Security Sistem", "Creative Director", "Android Programmer",
                "IOS Programmer", "Fullstack Programmer", "Ahli Database", "UI/UX Designer", "Devops", "Graphic Designer",
                "Copywriter", "Videografer-Editor", "Technical Support", "Manajemen Resiko (DC)", "Devops (DC)",
                "Sistem Analis (DC)", "Mechanical Electric (DC)", "Network Engineer (DC)", "Cloud Engineer (DC)",
                "Technical Support (DC)", "CISO (CS)", "Security Architect Dan Analyzer (CS)",
                "Incident Response - Forensic Team (CS)", "Penetration Tester (Pentester) (CS)", "DevSecOps Engineer (CS)",
                "Ahli Data Platform", "Administrator", "Ahli Database", "Ahli Back End", "Ahli Data Analis",
                "Ahli Data Scientist", "Ahli Data Visualisasi", "Ahli Front End"
            ]
        }
        personnel_role = st.selectbox(
            "Peran Personil:",
            personnel_roles.get(selected_section_form, []),
            key="personnel_role_input"
        )
        personnel_count = st.number_input("Jumlah Personil (Orang):", min_value=1, value=1)

        st.subheader("Timeline Proyek")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Tanggal Mulai:", datetime.now())
        with col2:
            end_date = st.date_input("Tanggal Selesai:", datetime.now() + timedelta(days=7))

        st.subheader("Input Milestone (Opsional)")
        milestone_name = st.text_input("Nama Milestone (Contoh: 'Rilis Alpha')")
        milestone_date = st.date_input("Tanggal Milestone:", datetime.now() + timedelta(days=14))

        if start_date > end_date:
            st.error("Tanggal selesai tidak boleh sebelum tanggal mulai.")

        submitted = st.form_submit_button("Tambah Tugas dan Milestone")

        if submitted and start_date <= end_date:
            new_task = {
                'section': selected_section_form,
                'wbs_id': wbs_id,
                'task_name': custom_task_name,
                'description': custom_description,
                'personnel_role': personnel_role,
                'personnel_count': personnel_count,
                'start_date': start_date,
                'end_date': end_date
            }
            save_task(new_task)
            st.session_state.tasks = load_tasks()  # Perbarui daftar tugas dari DB
            st.success("Tugas berhasil ditambahkan ke database!")

            if milestone_name and milestone_date:
                save_milestone(wbs_id, milestone_name, milestone_date)
                st.session_state.milestones = load_milestones()  # Perbarui daftar milestone dari DB
                st.success("Milestone berhasil ditambahkan ke database!")

            # Reset session state untuk form baru
            st.session_state.default_task_name = task_name_from_wbs
            st.session_state.default_description = description_from_wbs

# --- Tampilan WBS & Analisis ---
elif menu_selection == "Lihat WBS & Analisis":
    st.header("WBS, Timeline, dan Analisis Personil")

    if not st.session_state.tasks:
        st.info("Belum ada tugas yang diinputkan. Silakan ke menu 'Input Tugas Baru' untuk menambahkan.")
    else:
        df_tasks = pd.DataFrame(st.session_state.tasks)
        df_milestones = pd.DataFrame(st.session_state.milestones)

        # --- Tampilan Tabel Tugas ---
        st.subheader("Daftar Tugas yang Diinput")
        st.dataframe(df_tasks.sort_values(by=['section', 'wbs_id']))

        st.markdown("---")

        # --- Tampilan Tabel Milestone ---
        st.subheader("Daftar Milestone")
        st.dataframe(df_milestones.sort_values(by='milestone_date'))

        st.markdown("---")

        # --- Gantt Chart ---
        st.subheader("Gantt Chart Proyek")
        df_tasks['start_date'] = pd.to_datetime(df_tasks['start_date'])
        df_tasks['end_date'] = pd.to_datetime(df_tasks['end_date'])
        df_tasks['Gantt Task Name'] = df_tasks['wbs_id'] + ' - ' + df_tasks['task_name']

        if not df_tasks.empty:
            # Buat Gantt Chart dengan px.timeline
            fig_gantt = px.timeline(
                df_tasks,
                x_start="start_date",
                x_end="end_date",
                y="Gantt Task Name",
                color="section",
                hover_name="task_name",
                hover_data={"wbs_id": True, "description": True, "personnel_role": True, "personnel_count": True, "start_date": "|%Y-%m-%d", "end_date": "|%Y-%m-%d"},
                title="Timeline Tugas Proyek (Gantt Chart)"
            )

            # Tambahkan milestone sebagai garis vertikal dan teks
            if not df_milestones.empty:
                df_milestones['milestone_date'] = pd.to_datetime(df_milestones['milestone_date'])
                for _, milestone in df_milestones.iterrows():
                    fig_gantt.add_vline(
                        x=milestone['milestone_date'].timestamp() * 1000,  # Konversi ke milidetik
                        line_dash="dash",
                        line_color="red",
                        annotation_text=milestone['milestone_name'],
                        annotation_position="top",
                        annotation=dict(font_size=12, font_color="red")
                    )

            fig_gantt.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_gantt, use_container_width=True)
        else:
            st.warning("Tidak ada data tugas untuk ditampilkan di Gantt Chart.")

        st.markdown("---")

        # --- Grafik Distribusi Personil ---
        st.subheader("Distribusi Personil Berdasarkan Peran")
        if 'personnel_role' in df_tasks.columns and not df_tasks.empty:
            personnel_distribution = df_tasks.groupby('personnel_role')['personnel_count'].sum().reset_index()
            
            if not personnel_distribution.empty:
                fig_personnel = go.Figure(data=[
                    go.Bar(x=personnel_distribution['personnel_role'], y=personnel_distribution['personnel_count'], marker_color='skyblue')
                ])
                fig_personnel.update_layout(
                    title="Total Jumlah Personil per Peran",
                    xaxis_title="Peran Personil",
                    yaxis_title="Jumlah Orang"
                )
                st.plotly_chart(fig_personnel, use_container_width=True)
            else:
                st.info("Tidak ada data personil untuk divisualisasikan.")
        else:
            st.info("Kolom 'personnel_role' tidak ditemukan atau data kosong.")

        st.markdown("---")

        # --- Grafik Tugas per Bagian ---
        st.subheader("Jumlah Tugas per Bagian Utama")
        tasks_per_section = df_tasks['section'].value_counts().reset_index()
        tasks_per_section.columns = ['Section', 'Number of Tasks']

        if not tasks_per_section.empty:
            fig_tasks_section = go.Figure(data=[
                go.Pie(labels=tasks_per_section['Section'], values=tasks_per_section['Number of Tasks'])
            ])
            fig_tasks_section.update_layout(title="Persentase Jumlah Tugas per Bagian")
            st.plotly_chart(fig_tasks_section, use_container_width=True)
        else:
            st.info("Tidak ada data tugas per bagian untuk divisualisasikan.")

        st.markdown("---")

        # Optional: Clear all tasks and milestones
        if st.button("Hapus Semua Tugas dan Milestone"):
            conn = sqlite3.connect('wbs_database.db')
            c = conn.cursor()
            c.execute("DELETE FROM tasks")
            c.execute("DELETE FROM milestones")
            conn.commit()
            conn.close()
            st.session_state.tasks = []
            st.session_state.milestones = []
            st.success("Semua tugas dan milestone telah dihapus dari database!")
            st.rerun()