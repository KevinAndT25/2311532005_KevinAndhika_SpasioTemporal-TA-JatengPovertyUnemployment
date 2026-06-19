"""
Aplikasi Visualisasi Spasio-Temporal
Indikator Kemiskinan dan Pengangguran di Jawa Tengah (2007-2025)

Dibuat dengan Streamlit dan Folium
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from folium import GeoJson
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import time

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Jateng Poverty & Unemployment Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Tema Galaksi Dark
st.markdown("""
<style>
    /* Warna tema galaksi */
    :root {
        --galaxy-dark: #00076f;
        --galaxy-purple: #44008b;
        --galaxy-magenta: #9f45b0;
        --galaxy-pink: #e54ed0;
        --galaxy-light: #ffe4f2;
        --bg-dark: #0a0a1a;
        --bg-card: #111128;
        --bg-sidebar: #080820;
        --text-primary: #ffe4f2;
        --text-secondary: #c9a0d0;
        --border-color: #44008b;
        --shadow-color: rgba(159, 69, 176, 0.3);
    }
    
    /* Global styling - Dark Theme */
    .stApp {
        background-color: var(--bg-dark);
    }
    
    .stApp > .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 100%;
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    
    .app-header h1 {
        background: linear-gradient(135deg, #ffe4f2, #e54ed0, #9f45b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .app-header h2 {
        color: var(--galaxy-pink);
        font-size: 18px;
        font-weight: 400;
        margin: 5px 0;
    }
    
    .app-header h3 {
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 300;
        margin: 0;
    }
    
    .app-header hr {
        width: 40%;
        margin: 12px auto;
        border: 1px solid var(--border-color);
        opacity: 0.5;
    }
    
    /* Sidebar styling - Dark */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stButton button {
        font-weight: 500;
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: var(--bg-card);
        border-color: var(--border-color);
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] .stSlider .st-bd {
        background-color: var(--galaxy-magenta);
    }
    
    [data-testid="stSidebar"] .stSlider .st-dc {
        background-color: var(--galaxy-pink);
    }
    
    /* Sidebar header */
    .sidebar-header {
        color: var(--galaxy-light);
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--galaxy-magenta);
        text-shadow: 0 0 20px rgba(159, 69, 176, 0.3);
    }
    
    /* Label styling */
    .stSelectbox label, .stSlider label {
        color: var(--text-secondary) !important;
    }
    
    /* Card styling untuk statistik - Dark */
    .stat-card {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px var(--shadow-color);
        border-left: 4px solid var(--galaxy-pink);
        margin-bottom: 8px;
    }
    
    .stat-card .stat-value {
        font-size: 20px;
        font-weight: 600;
        color: var(--galaxy-light);
    }
    
    .stat-card .stat-label {
        font-size: 12px;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    /* Metric card styling - Dark */
    .metric-card {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 10px 14px;
        box-shadow: 0 1px 3px var(--shadow-color);
        text-align: center;
        border: 1px solid var(--border-color);
    }
    
    .metric-card .metric-value {
        font-size: 22px;
        font-weight: 600;
        background: linear-gradient(135deg, #ffe4f2, #e54ed0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-card .metric-label {
        font-size: 11px;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    /* Folium map styling */
    .folium-map {
        height: 550px !important;
        width: 100% !important;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 8px var(--shadow-color);
    }
    
    /* Section title - Dark */
    .section-title {
        color: var(--galaxy-light);
        font-size: 18px;
        font-weight: 600;
        margin: 15px 0 10px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--border-color);
        text-shadow: 0 0 20px rgba(229, 78, 208, 0.2);
    }
    
    /* Info box styling - Dark */
    .info-box {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 12px 16px;
        color: var(--text-secondary);
        font-size: 14px;
        border-left: 4px solid var(--galaxy-magenta);
    }
    
    /* Success box styling - Dark */
    .success-box {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 10px 16px;
        color: var(--galaxy-light);
        font-size: 14px;
        border-left: 4px solid var(--galaxy-pink);
    }
    
    .success-box b {
        color: var(--galaxy-pink);
    }
    
    /* Button styling - Dark */
    .stButton button {
        background: linear-gradient(135deg, var(--galaxy-purple), var(--galaxy-magenta));
        color: var(--galaxy-light);
        border-radius: 6px;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, var(--galaxy-magenta), var(--galaxy-pink));
        color: var(--galaxy-light);
        box-shadow: 0 0 25px var(--shadow-color);
        transform: scale(1.02);
    }
    
    /* Progress bar - Dark */
    .stProgress .st-bo {
        background-color: var(--bg-card);
    }
    
    .stProgress .st-bv {
        background: linear-gradient(90deg, var(--galaxy-purple), var(--galaxy-pink));
    }
    
    /* Spinner */
    .stSpinner {
        color: var(--galaxy-pink) !important;
    }
    
    /* Footer - Dark */
    .app-footer {
        position: fixed;
        bottom: 5px;
        right: 10px;
        font-size: 10px;
        color: var(--text-secondary);
        z-index: 1000;
        opacity: 0.6;
    }
    
    /* Streamlit default text override */
    .stMarkdown p, .stMarkdown li, .stMarkdown ul {
        color: var(--text-primary);
    }
    
    /* Success message */
    .stAlert[data-baseweb="notification"] {
        background-color: var(--bg-card) !important;
        border-color: var(--galaxy-pink) !important;
        color: var(--galaxy-light) !important;
    }
    
    /* Widget labels */
    .stSelectbox label, .stSlider label, .stRadio label {
        color: var(--text-secondary) !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--border-color) !important;
        opacity: 0.3 !important;
    }
    
    /* Plotly chart container */
    .plotly-container {
        background-color: transparent !important;
    }
    
    /* Selectbox dropdown */
    div[data-baseweb="select"] {
        background-color: var(--bg-card) !important;
        border-color: var(--border-color) !important;
    }
    
    div[data-baseweb="select"] * {
        color: var(--text-primary) !important;
    }
    
    ul[data-baseweb="menu"] {
        background-color: var(--bg-card) !important;
        border-color: var(--border-color) !important;
    }
    
    li[role="option"]:hover {
        background-color: var(--galaxy-purple) !important;
    }
            
    .spacer-100 {
        height: 100px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA (CACHED)
# ============================================
@st.cache_data
def load_master_data():
    """Load data master CSV"""
    df = pd.read_csv('data/df_master.csv')
    df['tahun'] = df['tahun'].astype(int)
    if 'nama_clean' not in df.columns:
        df['nama_clean'] = df['kabupaten'].str.upper().str.replace('KABUPATEN ', '').str.replace('KOTA ', '')
    return df

@st.cache_data
def load_geojson_for_year(year):
    """Load GeoJSON untuk tahun tertentu"""
    file_path = f'data/geojson/jateng_{year}.geojson'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

@st.cache_data
def get_available_years():
    """Mendapatkan daftar tahun yang tersedia"""
    years = []
    for year in range(2007, 2026):
        if os.path.exists(f'data/geojson/jateng_{year}.geojson'):
            years.append(year)
    return years

# ============================================
# FUNGSI UTILITY
# ============================================
def get_indicator_column(indicator_name):
    """Mapping dari nama indikator ke kolom di dataframe"""
    mapping = {
        "Persentase Penduduk Miskin (%)": "persen_miskin",
        "Tingkat Pengangguran Terbuka (%)": "tpt",
        "Garis Kemiskinan (Rp/kapita/bln)": "garis_kemiskinan",
        "Jumlah Penduduk Miskin (ribu jiwa)": "jumlah_miskin"
    }
    return mapping.get(indicator_name, "persen_miskin")

def get_color_palette(indicator_name):
    """Menentukan palet warna berdasarkan indikator"""
    if "Persentase Penduduk Miskin" in indicator_name:
        return 'Oranye'
    elif "Tingkat Pengangguran Terbuka" in indicator_name:
        return 'Blues'
    elif "Garis Kemiskinan" in indicator_name:
        return 'MerahTua'
    elif "Jumlah Penduduk Miskin" in indicator_name:
        return 'Hijau'
    else:
        return 'Oranye'

def format_number(value, indicator_name):
    """Format angka berdasarkan indikator"""
    if pd.isna(value) or value is None:
        return "Tidak tersedia"
    
    if "Garis Kemiskinan" in indicator_name:
        return f"Rp {value:,.0f}"
    elif "Jumlah Penduduk Miskin" in indicator_name:
        return f"{value:,.1f} ribu jiwa"
    else:
        return f"{value:.2f}%"
        
def get_color(value, min_val, max_val, palette):
    """Mendapatkan warna berdasarkan nilai dan palet"""
    if value is None or pd.isna(value):
        return '#cccccc'
    
    if max_val == min_val:
        if palette == 'Oranye':
            return '#ffffb2'
        elif palette == 'Blues':
            return '#eff3ff'
        elif palette == 'MerahTua':
            return '#fadbd8'
        elif palette == 'Hijau':
            return '#e8f8f5'
        else:
            return '#cccccc'
    
    ratio = (value - min_val) / (max_val - min_val)
    
    if palette == 'Oranye':
        if ratio < 0.2:
            return '#ffffb2'
        elif ratio < 0.4:
            return '#fed976'
        elif ratio < 0.6:
            return '#feb24c'
        elif ratio < 0.8:
            return '#fd8d3c'
        else:
            return '#bd0026'
    elif palette == 'Blues':
        if ratio < 0.2:
            return '#eff3ff'
        elif ratio < 0.4:
            return '#c6dbef'
        elif ratio < 0.6:
            return '#9ecae1'
        elif ratio < 0.8:
            return '#6baed6'
        else:
            return '#08519c'

    elif palette == 'MerahTua':
        if ratio < 0.2:
            return '#FADBD8'
        elif ratio < 0.4:
            return '#F5B7B1'
        elif ratio < 0.6:
            return '#EC7063'
        elif ratio < 0.8:
            return '#CB4335'
        else:
            return '#78281F'

    elif palette == 'Hijau':
        if ratio < 0.2:
            return '#E8F8F5'
        elif ratio < 0.4:
            return '#A2D9CE'
        elif ratio < 0.6:
            return '#45B39D'
        elif ratio < 0.8:
            return '#117A65'
        else:
            return '#0E6251'

    else:
        return '#cccccc'
    
def get_all_kabupaten(df):
    """Mendapatkan daftar semua kabupaten"""
    return sorted(df['kabupaten'].unique())

# ============================================
# MEMUAT DATA
# ============================================
with st.spinner("Memuat data..."):
    df_master = load_master_data()
    available_years = get_available_years()
    all_kabupaten = get_all_kabupaten(df_master)

tahun_min = min(available_years) if available_years else 2007
tahun_max = max(available_years) if available_years else 2025

# Inisialisasi session state
if 'selected_tahun' not in st.session_state:
    st.session_state.selected_tahun = 2025
if 'indikator' not in st.session_state:
    st.session_state.indikator = "Persentase Penduduk Miskin (%)"
if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False
if 'clicked_kab_for_chart' not in st.session_state:
    st.session_state.clicked_kab_for_chart = None
if 'map_key' not in st.session_state:
    st.session_state.map_key = 0

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown('<div class="sidebar-header">Kontrol Visualisasi</div>', unsafe_allow_html=True)
    
    # 1. Dropdown Indikator
    indikator = st.selectbox(
        "Pilih Indikator",
        options=[
            "Persentase Penduduk Miskin (%)",
            "Tingkat Pengangguran Terbuka (%)",
            "Garis Kemiskinan (Rp/kapita/bln)",
            "Jumlah Penduduk Miskin (ribu jiwa)"
        ],
        index=0,
        key="indikator_select"
    )
    if st.session_state.indikator != indikator:
        st.session_state.indikator = indikator
        st.session_state.map_key += 1
    
    # 2. Slider Tahun
    tahun = st.slider(
        "Pilih Tahun",
        min_value=tahun_min,
        max_value=tahun_max,
        value=st.session_state.selected_tahun,
        step=1,
        key=f"tahun_slider_{st.session_state.map_key}" 
    )
    st.session_state.selected_tahun = tahun
    
    # 3. Tombol Animasi
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Play", use_container_width=True):
            st.session_state.animation_running = True
    with col2:
        if st.button("Stop", use_container_width=True):
            st.session_state.animation_running = False
    
    # 4. Dropdown Filter Kabupaten
    selected_kab_filter = st.selectbox(
        "Pilih Kabupaten/Kota",
        options=["Semua Kabupaten"] + all_kabupaten,
        index=0,
        key="kab_filter",
        help="Pilih kabupaten/kota untuk melihat detail dan tren temporalnya"
    )
    # Update session state untuk chart
    if selected_kab_filter != "Semua Kabupaten":
        st.session_state.clicked_kab_for_chart = selected_kab_filter
    else:
        st.session_state.clicked_kab_for_chart = None
    
    # 5. Tombol Reset
    if st.button("Reset", use_container_width=True):
        st.session_state.selected_tahun = 2025
        st.session_state.indikator = "Persentase Penduduk Miskin (%)"
        st.session_state.animation_running = False
        st.session_state.map_key += 1 
        st.session_state.clicked_kab_for_chart = None
        st.rerun()

# ============================================
# ANIMASI TAHUNAN
# ============================================

if 'animation_year_index' not in st.session_state:
    st.session_state.animation_year_index = 0

if st.session_state.animation_running:
    st.cache_data.clear()
    
    years_list = list(range(tahun_min, tahun_max + 1))
    total_years = len(years_list)
    
    idx = st.session_state.animation_year_index
    
    current_year = years_list[idx]
    st.session_state.selected_tahun = current_year
    
    st.session_state.map_key += 1
    
    progress = (idx + 1) / total_years
    
    if idx >= total_years - 1:
        st.session_state.animation_running = False
        st.session_state.animation_year_index = 0
        st.sidebar.success("Animasi selesai")
        time.sleep(0.5)
        st.rerun()
    else:
        time.sleep(0.6)
        st.session_state.animation_year_index = idx + 1
        st.rerun()

# ============================================
# PREPARE DATA UNTUK TAHUN YANG DIPILIH
# ============================================
current_year = st.session_state.selected_tahun
indikator = st.session_state.indikator
indicator_col = get_indicator_column(indikator)
color_palette = get_color_palette(indikator)
palette = color_palette 

# Filter data untuk tahun yang dipilih
df_tahun = df_master[df_master['tahun'] == current_year].copy()

# Buat dictionary untuk lookup nilai per kabupaten
kab_value_dict = dict(zip(df_tahun['nama_clean'].str.upper(), df_tahun[indicator_col]))
kab_per_dict = dict(zip(df_tahun['nama_clean'].str.upper(), df_tahun['persen_miskin']))
kab_tpt_dict = dict(zip(df_tahun['nama_clean'].str.upper(), df_tahun['tpt']))
kab_garis_dict = dict(zip(df_tahun['nama_clean'].str.upper(), df_tahun['garis_kemiskinan']))
kab_jumlah_dict = dict(zip(df_tahun['nama_clean'].str.upper(), df_tahun['jumlah_miskin']))

# Ambil nilai untuk pembuatan color map
values_for_colormap = df_tahun[indicator_col].dropna().tolist()
values_list = [v for v in kab_value_dict.values() if not pd.isna(v)]
min_val = min(values_list) if values_list else 0
max_val = max(values_list) if values_list else 1

# ============================================
# MEMBUAT PETA FOLIUM
# ============================================
m = folium.Map(
    location=[-7.3, 110.0],
    zoom_start=8.5,
    tiles='CartoDB positron',
    control_scale=True
)

# Load GeoJSON
geojson_data = load_geojson_for_year(current_year)

if geojson_data:
    for feature in geojson_data['features']:
        kab_name = feature['properties'].get('nama_clean', feature['properties'].get('NAME_2', ''))
        kab_name_upper = kab_name.upper()
        
        value = kab_value_dict.get(kab_name_upper)
        persen_value = kab_per_dict.get(kab_name_upper)
        tpt_value = kab_tpt_dict.get(kab_name_upper)
        garis_value = kab_garis_dict.get(kab_name_upper)
        jumlah_value = kab_jumlah_dict.get(kab_name_upper)
        color = get_color(value, min_val, max_val, palette)
        
        # Tooltip HTML (hover) - Dark theme
        tooltip_html = f"""
        <div style="font-family: Arial; padding: 8px; min-width: 200px; background: #111128; border: 1px solid #44008b; border-radius: 8px;">
            <h5 style="margin: 0 0 5px 0; color: #ffe4f2; font-weight: 600;">{kab_name}</h5>
            <p style="margin: 0; font-size: 12px; color: #c9a0d0;">Tahun {current_year}</p>
            <hr style="margin: 5px 0; border: 0.5px solid #44008b; opacity: 0.5;">
            <table style="width: 100%; font-size: 13px;">
                <tr><td style="color: #c9a0d0;"><b>{st.session_state.indikator}</b></td><td style="text-align: right; font-weight: 600; color: #ffe4f2;">{format_number(value, st.session_state.indikator)}</td></tr>
            </table>
        </div>
        """
        
        # Popup HTML (click) - Dark theme
        popup_html = f"""
        <div style="font-family: Arial; padding: 10px; min-width: 220px; background: #111128; border: 1px solid #44008b; border-radius: 8px;">
            <h4 style="margin: 0 0 8px 0; color: #ffe4f2; font-weight: 600;">{kab_name}</h4>
            <p style="margin: 0 0 8px 0; font-size: 12px; color: #c9a0d0;">Tahun {current_year}</p>
            <hr style="margin: 8px 0; border: 0.5px solid #44008b; opacity: 0.5;">
            <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                <tr><td style="padding: 3px 0; color: #c9a0d0;"><b>Persentase Penduduk Miskin</b></td><td style="padding: 3px 0; text-align: right; font-weight: 500; color: #ffe4f2;">{format_number(persen_value, 'Persentase Kemiskinan (%)')}</td></tr>
                <tr><td style="padding: 3px 0; color: #c9a0d0;"><b>Tingkat Pengangguran Terbuka</b></td><td style="padding: 3px 0; text-align: right; font-weight: 500; color: #ffe4f2;">{format_number(tpt_value, 'Tingkat Pengangguran Terbuka (%)')}</td></tr>
                <tr><td style="padding: 3px 0; color: #c9a0d0;"><b>Garis Kemiskinan</b></td><td style="padding: 3px 0; text-align: right; font-weight: 500; color: #ffe4f2;">{format_number(garis_value, 'Garis Kemiskinan (Rp/kapita/bln)')}</td></tr>
                <tr><td style="padding: 3px 0; color: #c9a0d0;"><b>Jumlah Penduduk Miskin</b></td><td style="padding: 3px 0; text-align: right; font-weight: 500; color: #ffe4f2;">{format_number(jumlah_value, 'Jumlah Penduduk Miskin')}</td></tr>
            </table>
        </div>
        """
        
        folium.GeoJson(
            feature,
            style_function=lambda x, c=color: {
                'fillColor': c,
                'color': 'white',
                'weight': 1,
                'fillOpacity': 0.85,
            },
            tooltip=folium.Tooltip(tooltip_html, sticky=True),
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)

# ============================================
# TAMPILKAN PETA
# ============================================
st.markdown("""
<div class="app-header">
    <h1>Visualisasi Spasio-Temporal</h1>
    <h2>Indikator Kemiskinan dan Pengangguran</h2>
    <h3>Provinsi Jawa Tengah | 2007 - 2025</h3>
    <hr>
</div>
""", unsafe_allow_html=True)

map_container = st.container()
map_placeholder = st.empty()
with map_container:
    output = st_folium(
        m,
        width=None,
        height=550,
        returned_objects=["last_object_clicked"],
        key=f"folium_map_{current_year}"
    )

# ============================================
# HANDLE KLIK PETA UNTUK UPDATE DROPDOWN DAN CHART
# ============================================
clicked_kab_name = None

if output and output.get('last_object_clicked'):
    clicked_props = output['last_object_clicked'].get('properties', {})
    clicked_kab_name = clicked_props.get('nama_clean', '')
    if not clicked_kab_name:
        clicked_kab_name = clicked_props.get('NAME_2', '')
    if not clicked_kab_name:
        clicked_kab_name = clicked_props.get('kabupaten', '')
    
    if clicked_kab_name:
        clicked_kab_name = clicked_kab_name.upper().strip()

if clicked_kab_name:
    matching_rows = df_master[df_master['nama_clean'].str.upper() == clicked_kab_name]
    
    if len(matching_rows) > 0:
        matched_kab = matching_rows['kabupaten'].iloc[0]
        st.session_state.clicked_kab_for_chart = matched_kab
        
        if matched_kab in all_kabupaten:
            st.session_state.kab_filter = matched_kab
            st.rerun()
    else:
        matching_rows2 = df_master[df_master['kabupaten'].str.upper() == clicked_kab_name]
        if len(matching_rows2) > 0:
            matched_kab = matching_rows2['kabupaten'].iloc[0]
            st.session_state.clicked_kab_for_chart = matched_kab
            if matched_kab in all_kabupaten:
                st.session_state.kab_filter = matched_kab
                st.rerun()

# ============================================
# LEGEND BOX DI SUDUT KANAN BAWAH PETA
# ============================================

legend_colors = []
legend_labels = []

current_year = st.session_state.selected_tahun
indikator = st.session_state.indikator

if len(values_for_colormap) > 0:
    min_val = min(values_for_colormap)
    max_val = max(values_for_colormap)
    step = (max_val - min_val) / 5
    
    if color_palette == 'Oranye':
        colors = ['#ffffb2', '#fed976', '#feb24c', '#fd8d3c', '#bd0026']
    elif color_palette == 'Blues':
        colors = ['#eff3ff', '#c6dbef', '#9ecae1', '#6baed6', '#08519c']
    elif color_palette == 'MerahTua':
        colors = ['#FADBD8', '#F5B7B1', '#EC7063', '#CB4335', '#78281F']
    elif color_palette == 'Hijau':
        colors = ['#E8F8F5', '#A2D9CE', '#45B39D', '#117A65', '#0E6251']
    else:
        colors = ['#ffffb2', '#fed976', '#feb24c', '#fd8d3c', '#bd0026']
    
    for i in range(5):
        lower = min_val + i * step
        upper = min_val + (i + 1) * step
        
        if "Garis Kemiskinan" in indikator:
            range_text = f"Rp {lower:,.0f} - Rp {upper:,.0f}"
        elif "Jumlah Penduduk Miskin" in indikator:
            range_text = f"{lower:,.1f} - {upper:,.1f} ribu"
        else:
            range_text = f"{lower:.1f}% - {upper:.1f}%"
        
        legend_colors.append(colors[i])
        legend_labels.append(range_text)

legend_html = '<div style="position: fixed; bottom: 20px; right: 20px; background: rgba(17, 17, 40, 0.95); border: 1px solid #44008b; border-radius: 10px; padding: 12px 18px; box-shadow: 0 2px 10px rgba(159, 69, 176, 0.3); z-index: 1000; font-family: Arial, sans-serif; min-width: 200px;">'
legend_html += f'<h4 style="margin: 0 0 5px 0; font-size: 14px; font-weight: 600; text-align: center; color: #ffe4f2;">{indikator}</h4>'
legend_html += f'<div style="margin: 0 0 10px 0; font-size: 11px; text-align: center; color: #c9a0d0; border-bottom: 1px solid #44008b; padding-bottom: 5px;">Tahun {current_year}</div>'

for color, label in zip(legend_colors, legend_labels):
    legend_html += f'<div style="display: flex; align-items: center; margin-bottom: 4px; font-size: 11px;">'
    legend_html += f'<div style="width: 25px; height: 12px; margin-right: 8px; border-radius: 2px; border: 0.5px solid #44008b; background-color: {color}; flex-shrink: 0;"></div>'
    legend_html += f'<span style="font-size: 11px; color: #ffe4f2;">{label}</span>'
    legend_html += '</div>'

legend_html += '<div style="margin-top: 6px; font-size: 9px; color: #c9a0d0; text-align: center; border-top: 0.5px solid #44008b; padding-top: 5px;"></div>'
legend_html += '</div>'

st.markdown(legend_html, unsafe_allow_html=True)

# ============================================
# DUAL-AXIS LINE CHART
# ============================================
st.markdown('<div class="section-title">Analisis Tren Temporal Kabupaten Terpilih</div>', unsafe_allow_html=True)

kab_name_for_chart = st.session_state.clicked_kab_for_chart

if kab_name_for_chart:
    st.markdown(f'<div class="success-box"><b>Sedang dianalisis:</b> {st.session_state.clicked_kab_for_chart}</div>', unsafe_allow_html=True)
    
    kab_data = df_master[df_master['kabupaten'] == kab_name_for_chart].copy()
    kab_data = kab_data.sort_values('tahun')
    
    provinsi_data = df_master.groupby('tahun')[['persen_miskin', 'tpt', 'garis_kemiskinan', 'jumlah_miskin']].mean().reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=kab_data['tahun'],
            y=kab_data['persen_miskin'],
            name="% Miskin (Kab)",
            line=dict(color='#d7191c', width=3),
            mode='lines+markers',
            marker=dict(size=6)
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=kab_data['tahun'],
            y=kab_data['tpt'],
            name="TPT (Kab)",
            line=dict(color='#2b83ba', width=3),
            mode='lines+markers',
            marker=dict(size=6)
        ),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(
            x=provinsi_data['tahun'],
            y=provinsi_data['persen_miskin'],
            name="% Miskin (Prov)",
            line=dict(color='#fdae61', width=2, dash='dot'),
            opacity=0.7
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=provinsi_data['tahun'],
            y=provinsi_data['tpt'],
            name="TPT (Prov)",
            line=dict(color="#68a6cd", width=2, dash='dot'),
            opacity=0.7
        ),
        secondary_y=False
    )
    
    fig.update_layout(
        title=f"Tren {kab_name_for_chart} vs Rata-rata Provinsi Jawa Tengah (2007-2025)",
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        height=450,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffe4f2')
    )
    
    fig.update_xaxes(title_text="Tahun", gridcolor='#44008b', color='#c9a0d0')
    fig.update_yaxes(title_text="Persentase Penduduk Miskin (%)", secondary_y=False, color='#d7191c')
    fig.update_yaxes(title_text="Tingkat Pengangguran Terbuka (%)", secondary_y=True, color='#2b83ba')
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{kab_data['persen_miskin'].iloc[-1]:.2f}%</div>
            <div class="metric-label">% Miskin Terbaru (2025)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{kab_data['persen_miskin'].min():.2f}%</div>
            <div class="metric-label">% Miskin Terendah ({kab_data.loc[kab_data['persen_miskin'].idxmin(), 'tahun']})</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{kab_data['persen_miskin'].max():.2f}%</div>
            <div class="metric-label">% Miskin Tertinggi ({kab_data.loc[kab_data['persen_miskin'].idxmax(), 'tahun']})</div>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{kab_data['tpt'].iloc[-1]:.2f}%</div>
            <div class="metric-label">TPT Terbaru (2025)</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{kab_data['tpt'].min():.2f}%</div>
            <div class="metric-label">TPT Terendah ({kab_data.loc[kab_data['tpt'].idxmin(), 'tahun']})</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{kab_data['tpt'].max():.2f}%</div>
            <div class="metric-label">TPT Tertinggi ({kab_data.loc[kab_data['tpt'].idxmax(), 'tahun']})</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="info-box">Pilih kabupaten/kota dari dropdown di sidebar untuk melihat analisis tren temporalnya</div>', unsafe_allow_html=True)


st.markdown('<div class="spacer-100"></div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="app-footer">
    Sumber: BPS Jawa Tengah | 2007-2025
</div>
""", unsafe_allow_html=True)