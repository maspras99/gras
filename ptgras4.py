
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go

# Konfigurasi halaman
st.set_page_config(
    page_title="PT GRAS - Organizational Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data struktur organisasi
org_structure = {
    "Divisi": ["Kepala Divisi", "SOFTWARE", "SOFTWARE", "DATA CENTER & CYBER SECURITY", 
               "DATA CENTER & CYBER SECURITY", "BIG DATA", "BIG DATA", "Personal CS"],
    "Jabatan": ["CEO", "Manager Software", "R&D Team", "Manager DC & CS", 
                "Personal DC Team", "Manager Big Data", "Ahli Data Platform", "CBO Team"],
    "Jumlah Staf": [1, 1, 14, 1, 7, 1, 7, 4],
    "Detail Tim": [
        "Budi Santoso (CEO)",
        "Andi Wijaya (Manager)",
        "14 roles: Sistem Analis, Security Specialist, Creative Director, Android/iOS Programmer, dll",
        "Citra Dewi (Manager)",
        "7 roles: Network Engineer, Cloud Engineer, System Analis, dll",
        "Eko Prasetyo (Manager)",
        "7 roles: Data Scientist, Data Analyst, Back End Specialist, dll",
        "4 roles: Security Architect, Penetration Tester, Incident Response, dll"
    ]
}

# Data contoh staf
staff_data = {
    "Nama": ["Andi Wijaya", "Dewi Kurnia", "Rudi Hartono", "Sari Dewi", "Ahmad Fauzi", 
             "Citra Lestari", "Faisal Rahman", "Gina Permata", "Eko Prasetyo", "Hana Wijaya"],
    "Divisi": ["SOFTWARE", "SOFTWARE", "SOFTWARE", "SOFTWARE", "SOFTWARE",
               "DATA CENTER & CYBER SECURITY", "DATA CENTER & CYBER SECURITY", "DATA CENTER & CYBER SECURITY", "BIG DATA", "BIG DATA"],
    "Jabatan": ["Manager Software", "Android Programmer", "iOS Programmer", "UI/UX Designer", 
                "DevOps Engineer", "Manager DC & CS", "Network Engineer", "Security Analyst", 
                "Manager Big Data", "Data Scientist"],
    "Pengalaman": [8, 5, 4, 6, 5, 7, 4, 6, 9, 5],
    "Gaji (juta)": [35, 18, 17, 20, 22, 30, 15, 25, 40, 23],
    "Status": ["Aktif", "Aktif", "Aktif", "Aktif", "Aktif", 
               "Aktif", "Aktif", "Aktif", "Aktif", "Aktif"]
}

# Konversi ke DataFrame
org_df = pd.DataFrame(org_structure)
staff_df = pd.DataFrame(staff_data)

# Warna gradient untuk visualisasi
colors = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']

# CSS styling langsung dalam script
st.markdown("""
<style>
    /* Header styling */
    .header {
        background: linear-gradient(135deg, #003f5c 0%, #58508d 50%, #bc5090 100%);
        padding: 2rem;
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    .header p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #003f5c 0%, #58508d 100%);
        padding: 1rem;
        color: white;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .sidebar-header h2 {
        margin: 0;
    }
    .sidebar-header p {
        margin: 0;
        opacity: 0.9;
        font-size: 0.9rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #58508d;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card .label {
        color: #003f5c !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    .metric-card .value {
        color: #003f5c !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    
    /* Top cards */
    .top-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #ff7c43;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .top-card b {
        color: #003f5c;
        font-size: 1.1rem;
    }
    .top-card p {
        margin: 0.3rem 0 0 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        border: 1px solid #e0e0e0 !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #003f5c 0%, #58508d 100%) !important;
        color: white !important;
        border-color: #003f5c !important;
    }
    
    /* Main background */
    .stApp {
        background-color: #f5f7fa;
        background-image: radial-gradient(circle at 10% 20%, rgba(91, 141, 255, 0.05) 0%, rgba(0, 0, 0, 0) 90%);
    }
    
    /* Animasi */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

# Header dengan gradient
st.markdown("""
<div class="header animate-in">
    <h1>PT GRAS ORGANIZATIONAL DASHBOARD</h1>
    <p>Visualisasi Struktur Organisasi & Alokasi Sumber Daya</p>
</div>
""", unsafe_allow_html=True)

# Sidebar informasi
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header animate-in">
        <h2>PT GRAS</h2>
        <p>Digital Transformation Company</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔎 Filter Data")
    # Initialize session state for filters
    if 'selected_div' not in st.session_state:
        st.session_state.selected_div = staff_df['Divisi'].unique().tolist()
    if 'selected_pos' not in st.session_state:
        st.session_state.selected_pos = staff_df['Jabatan'].unique().tolist()

    # Select All button for divisions
    if st.button("Pilih Semua Divisi"):
        st.session_state.selected_div = staff_df['Divisi'].unique().tolist()

    selected_div = st.multiselect(
        "Pilih Divisi",
        options=staff_df['Divisi'].unique(),
        default=st.session_state.selected_div,
        key="div_multiselect"
    )
    st.session_state.selected_div = selected_div

    # Select All button for roles
    if st.button("Pilih Semua Jabatan"):
        st.session_state.selected_pos = staff_df['Jabatan'].unique().tolist()

    selected_pos = st.multiselect(
        "Pilih Jabatan",
        options=staff_df['Jabatan'].unique(),
        default=st.session_state.selected_pos,
        key="pos_multiselect"
    )
    st.session_state.selected_pos = selected_pos
    
    st.markdown("---")
    st.markdown("### 📅 Update Terakhir")
    st.write(datetime.now().strftime("%d %B %Y %H:%M"))
    
    st.markdown("---")
    st.markdown("### 📊 Data Mentah")
    if st.checkbox("Tampilkan Data Staf"):
        st.subheader("Data Staf")
        st.dataframe(staff_df, use_container_width=True)
    if st.checkbox("Tampilkan Data Struktur Organisasi"):
        st.subheader("Data Struktur Organisasi")
        st.dataframe(org_df, use_container_width=True)

# Tab layout
tab1, tab2, tab3 = st.tabs(["Struktur Organisasi", "Distribusi Staf", "Analisis Tim"])

with tab1:
    st.subheader("📋 Hierarki Organisasi PT GRAS")
    
    # Visualisasi struktur organisasi
    cols = st.columns([1, 3])
    
    with cols[0]:
        st.markdown("""
        <div style="text-align:center; margin-bottom:2rem;">
            <img src="https://cdn-icons-png.flaticon.com/512/1570/1570887.png" width="100">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card animate-in">
            <div class="label">Total Divisi</div>
            <div class="value">{len(org_df['Divisi'].unique())}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card animate-in">
            <div class="label">Total Jabatan</div>
            <div class="value">{len(org_df['Jabatan'])}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card animate-in">
            <div class="label">Total Staf</div>
            <div class="value">{org_df['Jumlah Staf'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        # Tree map struktur organisasi
        fig = px.treemap(
            org_df, 
            path=['Divisi', 'Jabatan'], 
            values='Jumlah Staf',
            color='Jumlah Staf',
            color_continuous_scale=colors,
            hover_data=['Detail Tim']
        )
        fig.update_traces(
            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>Jumlah Staf: %{value}<br>%{customdata[0]}"
        )
        fig.update_layout(
            margin=dict(t=0, l=0, r=0, b=0),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("👥 Distribusi Sumber Daya Manusia")
    st.markdown("Visualisasi distribusi staf berdasarkan divisi dan jabatan dengan desain modern dan interaktif.", unsafe_allow_html=True)

    # Filter data based on sidebar selections
    filtered_staff = staff_df[
        (staff_df['Divisi'].isin(selected_div)) & 
        (staff_df['Jabatan'].isin(selected_pos))
    ]

    # Check if filtered data is empty
    if filtered_staff.empty:
        st.warning("Tidak ada data staf yang sesuai dengan filter yang dipilih. Silakan sesuaikan filter di sidebar.")
    else:
        # 2-column layout with spacing
        col1, col2 = st.columns([2, 1], gap="medium")
        
        with col1:
            # Bar Chart: Staff Count by Division
            total_staff = filtered_staff.shape[0]
            division_counts = filtered_staff.groupby('Divisi').size().reset_index(name='Jumlah Staf')
            division_counts['Persentase'] = (division_counts['Jumlah Staf'] / total_staff * 100).round(2)
            fig_bar = px.bar(
                division_counts,
                x='Divisi',
                y='Jumlah Staf',
                title="Jumlah Staf per Divisi",
                color='Divisi',
                color_discrete_sequence=colors,
                text='Jumlah Staf',
                height=500
            )
            fig_bar.update_traces(
                textposition='outside',
                textfont=dict(size=14, color='#003f5c'),
                marker=dict(line=dict(color='white', width=1.5)),
                opacity=0.9,
                hovertemplate="<b>%{x}</b><br>Jumlah: %{y}<br>Persentase: %{customdata}%",
                customdata=division_counts['Persentase']
            )
            fig_bar.update_layout(
                title=dict(
                    text="Jumlah Staf per Divisi",
                    font=dict(size=26, color='#003f5c', family="Arial Black"),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis_title="Divisi",
                yaxis_title="Jumlah Staf",
                xaxis=dict(tickangle=45, title_font=dict(size=18), tickfont=dict(size=12)),
                yaxis=dict(title_font=dict(size=18), tickfont=dict(size=12), gridcolor='rgba(200,200,200,0.2)'),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=80, b=100, l=60, r=60),
                font=dict(size=12, color='#003f5c'),
                bargap=0.2
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': True})

            # Divider
            st.markdown("<hr style='border: 1px solid rgba(0,63,92,0.1); margin: 20px 0;'>", unsafe_allow_html=True)

            # Stacked Bar Chart: Roles per Division
            role_counts = filtered_staff.groupby(['Divisi', 'Jabatan']).size().reset_index(name='Jumlah')
            fig_stacked = px.bar(
                role_counts,
                x='Divisi',
                y='Jumlah',
                color='Jabatan',
                title="Distribusi Jabatan per Divisi",
                color_discrete_sequence=colors,
                height=500
            )
            fig_stacked.update_traces(
                marker=dict(line=dict(color='white', width=1.5)),
                opacity=0.9,
                hovertemplate="<b>%{x}</b><br>Jabatan: %{fullData.name}<br>Jumlah: %{y}"
            )
            fig_stacked.update_layout(
                title=dict(
                    text="Distribusi Jabatan per Divisi",
                    font=dict(size=26, color='#003f5c', family="Arial Black"),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis_title="Divisi",
                yaxis_title="Jumlah Staf",
                xaxis=dict(tickangle=45, title_font=dict(size=18), tickfont=dict(size=12)),
                yaxis=dict(title_font=dict(size=18), tickfont=dict(size=12), gridcolor='rgba(200,200,200,0.2)'),
                legend_title="Jabatan",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.4,
                    xanchor="center",
                    x=0.5,
                    bgcolor='rgba(0,0,0,0)',
                    bordercolor='#003f5c',
                    borderwidth=1,
                    font=dict(size=12, color='#003f5c')
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=80, b=150, l=60, r=60),
                font=dict(size=12, color='#003f5c'),
                bargap=0.15
            )
            st.plotly_chart(fig_stacked, use_container_width=True, config={'displayModeBar': True})

        with col2:
            # Pie Chart: Percentage of Staff per Division
            fig_pie = px.pie(
                division_counts,
                names='Divisi',
                values='Jumlah Staf',
                title="Persentase Staf per Divisi",
                color_discrete_sequence=colors,
                height=450
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(size=14, color='white'),
                marker=dict(line=dict(color='white', width=1.5)),
                hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}",
                pull=[0.05] * len(division_counts)
            )
            fig_pie.update_traces(opacity=0.9)  # Set opacity at trace level
            fig_pie.update_layout(
                title=dict(
                    text="Persentase Staf per Divisi",
                    font=dict(size=26, color='#003f5c', family="Arial Black"),
                    x=0.5,
                    xanchor='center'
                ),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1.0,
                    xanchor="left",
                    x=0.0,
                    bgcolor='rgba(0,0,0,0)',
                    bordercolor='#003f5c',
                    borderwidth=1,
                    font=dict(size=12, color='#003f5c')
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=80, b=50, l=60, r=60),
                font=dict(size=12, color='#003f5c')
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': True})

            # Metric: Total Staff in Filtered Data
            total_staff_filtered = filtered_staff.shape[0]
            st.markdown(f"""
            <div class="metric-card animate-in">
                <div class="label">Total Staf (Filtered)</div>
                <div class="value">{total_staff_filtered}</div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.subheader("📊 Analisis Komposisi Tim")
    
    # 2 kolom utama
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sunburst divisi-jabatan-gaji
        fig = px.sunburst(
            staff_df,
            path=['Divisi', 'Jabatan', 'Nama'],
            values='Gaji (juta)',
            color='Pengalaman',
            color_continuous_scale=colors,
            title="Struktur Gaji berdasarkan Jabatan"
        )
        fig.update_layout(
            title=dict(
                text="Struktur Gaji berdasarkan Jabatan",
                font=dict(size=26, color='#003f5c', family="Arial Black"),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=80, b=50, l=60, r=60),
            font=dict(size=12, color='#003f5c')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🔍 Statistik Utama")
        
        # Metric cards dengan styling
        avg_exp = staff_df['Pengalaman'].mean()
        avg_salary = staff_df['Gaji (juta)'].mean()
        total_cost = staff_df['Gaji (juta)'].sum()
        
        st.markdown(f"""
        <div class="metric-card animate-in">
            <div class="label">Rata-rata Pengalaman</div>
            <div class="value">{avg_exp:.1f} Tahun</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card animate-in">
            <div class="label">Rata-rata Gaji</div>
            <div class="value">Rp {avg_salary:.1f} Juta</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card animate-in">
            <div class="label">Total Biaya Gaji/bulan</div>
            <div class="value">Rp {total_cost} Juta</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Top 3 gaji tertinggi
        st.markdown("### 🏆 Top 3 Gaji Tertinggi")
        top3 = staff_df.nlargest(3, 'Gaji (juta)')
        for _, row in top3.iterrows():
            st.markdown(f"""
            <div class="top-card animate-in">
                <b>{row['Nama']}</b>
                <p>{row['Jabatan']} - Rp {row['Gaji (juta)']} juta</p>
            </div>
            """, unsafe_allow_html=True)

# JavaScript untuk animasi
st.markdown("""
<script>
    // Animasi saat elemen muncul
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    });
    
    document.querySelectorAll('.metric-card, .top-card, .plot-container, .stDataFrame').forEach(el => {
        observer.observe(el);
    });
</script>
""", unsafe_allow_html=True)