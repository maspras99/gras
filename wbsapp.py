import streamlit as st
import graphviz

# Mengatur konfigurasi halaman agar lebih lebar dan memberikan judul
st.set_page_config(layout="wide", page_title="WBS & Prototipe Proyek")

# --- JUDUL APLIKASI ---
st.title("Pusat Kendali Proyek: WBS & Prototipe Digital")
st.header("Bagian Umum, Keuangan, dan Marketing")
st.markdown("""
Aplikasi ini adalah pusat navigasi untuk proyek transformasi digital Anda.
Di bawah ini Anda dapat melihat **Work Breakdown Structure (WBS)** proyek dan mengakses **prototipe interaktif** untuk setiap bagian.
""")

# --- TAUTAN PROTOTIPE MODUL ---
st.subheader("🚀 Tautan Prototipe Modul")
st.info("Klik tombol di bawah ini untuk membuka prototipe setiap bagian di tab baru.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<a href="https://eva3cvqse7mquxygb5q8zx.streamlit.app/" target="_blank">
           <button style="
                width: 100%; 
                padding: 10px; 
                font-weight: bold; 
                color: white; 
                background-color: #007acc; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer;
            ">
                🏢 Buka Prototipe Bagian Umum
            </button>
        </a>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """<a href="https://qf7rhhyovwri3wyqulvc9u.streamlit.app/" target="_blank">
           <button style="
                width: 100%; 
                padding: 10px; 
                font-weight: bold; 
                color: white; 
                background-color: #007acc; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer;
            ">
                💰 Buka Prototipe Bagian Keuangan
            </button>
        </a>""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """<a href="https://rhvsgmewybn5tmflkaip4m.streamlit.app/" target="_blank">
           <button style="
                width: 100%; 
                padding: 10px; 
                font-weight: bold; 
                color: white; 
                background-color: #007acc; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer;
            ">
                🎯 Buka Prototipe Bagian Marketing
            </button>
        </a>""",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True) # Memberi sedikit spasi
st.markdown("---") # Garis pemisah

# --- 1. PEMBUATAN DIAGRAM VISUAL DENGAN GRAPHVIZ ---
st.subheader("1. Diagram Hirarki Visual (WBS)")

# Membuat objek graph baru
dot = graphviz.Digraph(comment='WBS Transformasi Digital')
dot.attr(rankdir='TB', splines='ortho', nodesep='0.4', ranksep='0.8')
dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')

# Definisi Node (tidak ada perubahan)
dot.node('2.0', '2.0\nTransformasi Digital\nDepartemen Bisnis Inti', fillcolor='#004a7c', fontcolor='white', fontsize='12')
dot.attr('node', fillcolor='#007acc', fontcolor='white')
dot.node('2.1', '2.1\nBagian Umum\nOtomasi & Efisiensi')
dot.node('2.2', '2.2\nBagian Keuangan\nTransparansi & Kontrol Real-time')
dot.node('2.3', '2.3\nBagian Marketing\nPertumbuhan Berbasis Data')
dot.attr('node', fillcolor='#cce5ff', fontcolor='black')
dot.node('2.1.1', '2.1.1\nModul HRIS'); dot.node('2.1.2', '2.1.2\nModul Administrasi Umum'); dot.node('2.1.3', '2.1.3\nPelaporan & Dashboard')
dot.node('2.2.1', '2.2.1\nModul Akuntansi & Keuangan Inti'); dot.node('2.2.2', '2.2.2\nModul Kontrol & Kepatuhan'); dot.node('2.2.3', '2.2.3\nPelaporan & Dashboard')
dot.node('2.3.1', '2.3.1\nModul CRM'); dot.node('2.3.2', '2.3.2\nModul Otomasi Marketing'); dot.node('2.3.3', '2.3.3\nPelaporan & Dashboard')
dot.attr('node', fillcolor='#f0f8ff', fontcolor='black', shape='ellipse', fontsize='9')
dot.node('2.1.1.1', 'Database Personalia'); dot.node('2.1.1.2', 'Sistem Payroll'); dot.node('2.1.1.3', 'Manajemen Absensi & Cuti'); dot.node('2.1.1.4', 'Penilaian Kinerja'); dot.node('2.1.1.5', 'Portal Karyawan')
dot.node('2.1.2.1', 'Manajemen Aset Digital'); dot.node('2.1.2.2', 'Sistem Ticketing Helpdesk'); dot.node('2.1.2.3', 'Digitalisasi Arsip (e-Office)')
dot.node('2.2.1.1', 'COA & Buku Besar'); dot.node('2.2.1.2', 'Otomasi Hutang (AP)'); dot.node('2.2.1.3', 'Otomasi Piutang (AR)'); dot.node('2.2.1.4', 'Manajemen Kas & Bank')
dot.node('2.2.2.1', 'Manajemen Anggaran'); dot.node('2.2.2.2', 'Manajemen Pajak'); dot.node('2.2.2.3', 'Manajemen Aset Tetap')
dot.node('2.3.1.1', 'Database Pelanggan 360°'); dot.node('2.3.1.2', 'Pipeline Penjualan'); dot.node('2.3.1.3', 'Otomasi Tugas Penjualan')
dot.node('2.3.2.1', 'Manajemen Kampanye'); dot.node('2.3.2.2', 'Integrasi Web & Medsos'); dot.node('2.3.2.3', 'Lead Nurturing')

# Definisi Edge/Hubungan (tidak ada perubahan)
dot.edge('2.0', '2.1'); dot.edge('2.0', '2.2'); dot.edge('2.0', '2.3')
dot.edge('2.1', '2.1.1'); dot.edge('2.1', '2.1.2'); dot.edge('2.1', '2.1.3')
dot.edge('2.2', '2.2.1'); dot.edge('2.2', '2.2.2'); dot.edge('2.2', '2.2.3')
dot.edge('2.3', '2.3.1'); dot.edge('2.3', '2.3.2'); dot.edge('2.3', '2.3.3')
dot.edge('2.1.1', '2.1.1.1'); dot.edge('2.1.1', '2.1.1.2'); dot.edge('2.1.1', '2.1.1.3'); dot.edge('2.1.1', '2.1.1.4'); dot.edge('2.1.1', '2.1.1.5')
dot.edge('2.1.2', '2.1.2.1'); dot.edge('2.1.2', '2.1.2.2'); dot.edge('2.1.2', '2.1.2.3')
dot.edge('2.2.1', '2.2.1.1'); dot.edge('2.2.1', '2.2.1.2'); dot.edge('2.2.1', '2.2.1.3'); dot.edge('2.2.1', '2.2.1.4')
dot.edge('2.2.2', '2.2.2.1'); dot.edge('2.2.2', '2.2.2.2'); dot.edge('2.2.2', '2.2.2.3')
dot.edge('2.3.1', '2.3.1.1'); dot.edge('2.3.1', '2.3.1.2'); dot.edge('2.3.1', '2.3.1.3')
dot.edge('2.3.2', '2.3.2.1'); dot.edge('2.3.2', '2.3.2.2'); dot.edge('2.3.2', '2.3.2.3')

st.graphviz_chart(dot, use_container_width=True)

# --- 2. PEMBUATAN RINCIAN INTERAKTIF ---
st.subheader("2. Rincian WBS Interaktif (Klik untuk Detail)")
st.info("Setiap item di bawah ini berisi keterangan lengkap mengenai tujuan dan lingkup dari paket pekerjaan tersebut.")

# -- BAGIAN UMUM --
with st.expander("▶️ **2.1 Bagian Umum - Otomasi dan Efisiensi**"):
    st.markdown("""
    **Tujuan:** Mengubah fungsi administrasi menjadi pendukung operasional yang efisien, terukur, dan berbasis data untuk melayani seluruh organisasi.
    """)
    st.markdown("---") # Garis pemisah

    st.markdown("#### 2.1.1 Modul HRIS (Human Resource Information System)")
    st.markdown("""
    - **Keterangan:** Mengimplementasikan platform terpusat untuk semua data dan proses terkait sumber daya manusia.
    - **2.1.1.1 Implementasi Database Induk Personalia:** Membangun satu sumber kebenaran untuk data karyawan, struktur organisasi, histori jabatan, dan dokumen terkait.
    - **2.1.1.2 Konfigurasi Sistem Penggajian (Payroll) Otomatis:** Otomatisasi perhitungan gaji, tunjangan, potongan (pajak, BPJS), hingga pembuatan slip gaji digital.
    - **2.1.1.3 Konfigurasi Manajemen Absensi & Cuti Online:** Sistem absensi digital dan alur pengajuan serta persetujuan cuti secara online.
    - **2.1.1.4 Implementasi Sistem Penilaian Kinerja Digital:** Platform untuk menetapkan OKR/KPI, melakukan review, dan mencatat feedback kinerja.
    - **2.1.1.5 Pembuatan Portal Karyawan (Self-Service):** Memungkinkan karyawan mengakses data pribadi, slip gaji, dan mengajukan cuti/klaim secara mandiri.
    """)

    st.markdown("#### 2.1.2 Modul Administrasi Umum")
    st.markdown("""
    - **Keterangan:** Mendigitalisasi proses administrasi dan layanan internal untuk meningkatkan kecepatan dan ketertelusuran.
    - **2.1.2.1 Sistem Manajemen Aset Digital:** Pencatatan dan pemantauan aset perusahaan (laptop, kendaraan, dll), termasuk jadwal pemeliharaan.
    - **2.1.2.2 Implementasi Sistem Ticketing Helpdesk Internal:** Platform untuk permintaan bantuan IT, GA, atau HR, dengan monitoring SLA (Service Level Agreement).
    - **2.1.2.3 Digitalisasi Proses Surat-Menyurat dan Arsip (e-Office):** Mengelola surat masuk/keluar dan arsip dokumen penting secara digital.
    """)

    st.markdown("#### 2.1.3 Pelaporan & Dashboard Kinerja Umum")
    st.markdown("""
    - **Keterangan:** Menyediakan visibilitas data untuk Manajer Umum guna pengambilan keputusan strategis terkait operasional internal.
    - **Deliverables:** Dashboard untuk memantau KPI HR (Employee Turnover, Time-to-Hire, Engagement Score) dan efektivitas layanan internal.
    """)

# -- BAGIAN KEUANGAN --
with st.expander("▶️ **2.2 Bagian Keuangan - Transparansi dan Kontrol Real-time**"):
    st.markdown("""
    **Tujuan:** Mengubah fungsi keuangan dari sekadar pencatat transaksi menjadi mitra strategis yang menyediakan data akurat dan real-time.
    """)
    st.markdown("---")

    st.markdown("#### 2.2.1 Modul Akuntansi & Keuangan Inti")
    st.markdown("""
    - **Keterangan:** Mengotomatiskan siklus akuntansi dasar untuk meningkatkan akurasi dan kecepatan pelaporan.
    - **2.2.1.1 Pengaturan Chart of Accounts (COA) dan Buku Besar (GL):** Mendesain dan mengimplementasikan struktur akun yang sesuai standar dan kebutuhan bisnis.
    - **2.2.1.2 Otomasi Proses Hutang (Account Payable):** Digitalisasi proses dari penerimaan invoice vendor, persetujuan, hingga penjadwalan pembayaran.
    - **2.2.1.3 Otomasi Proses Piutang (Account Receivable):** Digitalisasi proses dari pembuatan invoice pelanggan, pengiriman, hingga pemantauan pembayaran dan penagihan.
    - **2.2.1.4 Implementasi Manajemen Kas & Rekonsiliasi Bank Otomatis:** Memantau posisi kas secara real-time dan otomasi proses pencocokan transaksi bank dengan catatan perusahaan.
    """)

    st.markdown("#### 2.2.2 Modul Kontrol & Kepatuhan")
    st.markdown("""
    - **Keterangan:** Memastikan kepatuhan terhadap regulasi dan memberikan kontrol yang lebih baik terhadap anggaran dan aset perusahaan.
    - **2.2.2.1 Implementasi Manajemen Anggaran (Budgeting):** Platform untuk penyusunan, persetujuan, dan pemantauan realisasi anggaran per departemen.
    - **2.2.2.2 Konfigurasi Modul Perpajakan:** Otomatisasi perhitungan PPN & PPh serta integrasi dengan sistem e-Faktur.
    - **2.2.2.3 Implementasi Manajemen Aset Tetap:** Pencatatan aset, penyusutan otomatis, dan pelaporan nilai buku aset.
    """)

    st.markdown("#### 2.2.3 Pelaporan & Dashboard Keuangan")
    st.markdown("""
    - **Keterangan:** Menyediakan laporan dan visualisasi data keuangan yang mudah dipahami untuk semua level manajemen.
    - **Deliverables:** Dashboard Keuangan Eksekutif (Cash Flow, P&L, Neraca), Laporan Keuangan Standar (otomatis), Analisis Rasio Keuangan.
    """)


# -- BAGIAN MARKETING --
with st.expander("▶️ **2.3 Bagian Marketing - Pertumbuhan Berbasis Data**"):
    st.markdown("""
    **Tujuan:** Mengubah tim marketing menjadi mesin pertumbuhan yang dapat diukur, dengan fokus pada ROI dan penyediaan prospek berkualitas.
    """)
    st.markdown("---")

    st.markdown("#### 2.3.1 Modul CRM (Customer Relationship Management)")
    st.markdown("""
    - **Keterangan:** Membangun platform terpusat untuk mengelola semua interaksi dengan pelanggan dan prospek.
    - **2.3.1.1 Implementasi Database Pelanggan 360°:** Mengumpulkan semua data pelanggan (transaksi, interaksi, komplain) dalam satu tampilan.
    - **2.3.1.2 Konfigurasi Pipeline Penjualan:** Visualisasi tahapan penjualan dari prospek (lead) hingga menjadi pelanggan (deal).
    - **2.3.1.3 Otomasi Tugas Penjualan:** Mengotomatiskan pengingat untuk follow-up, penjadwalan, dan pencatatan aktivitas tim penjualan.
    """)

    st.markdown("#### 2.3.2 Modul Otomasi Marketing")
    st.markdown("""
    - **Keterangan:** Mengotomatiskan aktivitas marketing untuk menjangkau audiens yang tepat dengan pesan yang relevan.
    - **2.3.2.1 Implementasi Manajemen Kampanye Marketing:** Merencanakan, mengeksekusi, dan melacak kinerja kampanye (email, media sosial, dll) dari satu tempat.
    - **2.3.2.2 Integrasi dengan Website dan Media Sosial:** Otomatis menangkap data prospek yang masuk dari formulir di website atau iklan digital.
    - **2.3.2.3 Pembuatan Alur Perawatan Prospek (Lead Nurturing):** Mengirimkan konten/email secara otomatis kepada prospek untuk 'memanaskan' mereka sebelum diserahkan ke tim penjualan.
    """)

    st.markdown("#### 2.3.3 Pelaporan & Dashboard Marketing")
    st.markdown("""
    - **Keterangan:** Memberikan visibilitas penuh terhadap efektivitas setiap aktivitas marketing dan penjualan.
    - **Deliverables:** Dashboard Funnel Marketing, Laporan ROI per Kampanye, Dashboard Kinerja Tim Penjualan vs Target.
    """)