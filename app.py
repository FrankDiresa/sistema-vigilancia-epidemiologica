import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from utils.data_processor import DataProcessor
from components.vigilancia_tab import VigilanciaTab
from components.control_larvario_tab import ControlLarvarioTab
from components.cerco_tab import CercoTab
from components.inspector_tab import InspectorTab
from components.housing_management import HousingManagement

# Page configuration
st.set_page_config(
    page_title="Sistema de Vigilancia Epidemiológica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure file upload size (200MB)
st.session_state.max_upload_size = 200 * 1024 * 1024  # 200MB

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = None
if 'app_start_time' not in st.session_state:
    st.session_state.app_start_time = datetime.now()

def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Check if the app is responsive
        current_time = datetime.now()
        uptime = current_time - st.session_state.app_start_time
        
        # Health check data
        health_data = {
            'status': 'healthy',
            'timestamp': current_time.isoformat(),
            'uptime_seconds': uptime.total_seconds(),
            'app_version': '1.0.0',
            'streamlit_version': st.__version__,
            'dependencies_status': 'ok'
        }
        
        # Test basic functionality
        test_df = pd.DataFrame({'test': [1, 2, 3]})
        if len(test_df) == 3:
            health_data['pandas_status'] = 'ok'
        
        return health_data
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def main():
    # Health check endpoint - check URL parameters
    query_params = st.query_params
    
    # Handle health check requests
    if 'health' in query_params or 'healthcheck' in query_params:
        st.markdown("# 🟢 Health Check")
        health_data = health_check()
        
        if health_data['status'] == 'healthy':
            st.success("✅ Application is healthy")
        else:
            st.error("❌ Application is unhealthy")
        
        st.json(health_data)
        
        # Add refresh button for monitoring
        if st.button("🔄 Refresh Health Check"):
            st.rerun()
        
        # Don't render the rest of the app for health checks
        return
    # Theme toggle in sidebar
    st.sidebar.markdown("### ⚙️ Configuración")
    
    # Theme selector
    theme_option = st.sidebar.selectbox(
        "🎨 Tema",
        ["Claro", "Oscuro"],
        help="Selecciona el tema de la aplicación"
    )
    
    # Store theme in session state for Plotly charts
    st.session_state['current_theme'] = theme_option
    
    # Apply theme CSS
    if theme_option == "Oscuro":
        st.markdown("""
        <style>
            .stApp {
                background-color: #0e1117 !important;
                color: #fafafa !important;
            }
            .stSidebar {
                background-color: #262730 !important;
            }
            .stTabs [data-baseweb="tab-list"] {
                background-color: #262730 !important;
            }
            .stTabs [data-baseweb="tab"] {
                background-color: #262730 !important;
                color: #fafafa !important;
            }
            .stTabs [aria-selected="true"] {
                background-color: #0e1117 !important;
                color: #fafafa !important;
            }
            .stDataFrame {
                background-color: #262730 !important;
            }
            .stMetric {
                background-color: #262730 !important;
                color: #fafafa !important;
            }
            div[data-testid="metric-container"] {
                background-color: #262730 !important;
                border: 1px solid #4f4f4f !important;
                padding: 5px !important;
                border-radius: 5px !important;
            }
            .stSelectbox > div > div {
                background-color: #262730 !important;
                color: #fafafa !important;
            }
            .stTextInput > div > div > input {
                background-color: #262730 !important;
                color: #fafafa !important;
            }
            .stExpander {
                background-color: #262730 !important;
                border: 1px solid #4f4f4f !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Tema claro con máximo contraste - versión ultra mejorada
        st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            .stSidebar {
                background-color: #f0f0f0 !important;
                border-right: 2px solid #cccccc !important;
            }
            .stSidebar .stSelectbox > div > div {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 2px solid #999999 !important;
                font-weight: 600 !important;
            }
            .stSidebar .stSelectbox label {
                color: #000000 !important;
                font-weight: 700 !important;
            }
            .stSidebar .stMarkdown {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            .stSidebar h1, .stSidebar h2, .stSidebar h3 {
                color: #000000 !important;
                font-weight: 800 !important;
            }
            
            /* TABS con contraste máximo */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #e0e0e0 !important;
                border-bottom: 3px solid #999999 !important;
            }
            .stTabs [data-baseweb="tab"] {
                background-color: #f5f5f5 !important;
                color: #000000 !important;
                border: 2px solid #cccccc !important;
                border-bottom: none !important;
                margin-right: 3px !important;
                font-weight: 600 !important;
            }
            .stTabs [aria-selected="true"] {
                background-color: #0066cc !important;
                color: #ffffff !important;
                border-color: #0066cc !important;
                font-weight: 800 !important;
            }
            
            /* TABLAS con contraste extremo */
            .stDataFrame {
                background-color: #ffffff !important;
                border: 3px solid #999999 !important;
                border-radius: 6px !important;
            }
            .stDataFrame table {
                border-collapse: separate !important;
                border-spacing: 0 !important;
            }
            .stDataFrame th {
                background-color: #d0d0d0 !important;
                color: #000000 !important;
                font-weight: 800 !important;
                border-bottom: 3px solid #999999 !important;
                border-right: 1px solid #999999 !important;
                padding: 8px !important;
            }
            .stDataFrame td {
                color: #000000 !important;
                font-weight: 600 !important;
                border-bottom: 2px solid #cccccc !important;
                border-right: 1px solid #cccccc !important;
                padding: 6px !important;
                background-color: #fafafa !important;
            }
            .stDataFrame tr:nth-child(even) td {
                background-color: #f0f0f0 !important;
            }
            .stDataFrame tr:hover td {
                background-color: #e0e8ff !important;
                color: #000000 !important;
            }
            
            /* MÉTRICAS con contraste máximo */
            .stMetric {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 3px solid #999999 !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            }
            div[data-testid="metric-container"] {
                background-color: #ffffff !important;
                border: 3px solid #999999 !important;
                padding: 12px !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            }
            div[data-testid="metric-container"] > div {
                color: #000000 !important;
            }
            div[data-testid="metric-container"] [data-testid="metric-container-label"] {
                color: #000000 !important;
                font-weight: 800 !important;
                font-size: 14px !important;
            }
            div[data-testid="metric-container"] [data-testid="metric-container-value"] {
                color: #000000 !important;
                font-weight: 900 !important;
                font-size: 24px !important;
            }
            /* Títulos y etiquetas de métricas */
            .metric-label, .metric-title {
                color: #000000 !important;
                font-weight: 800 !important;
            }
            /* TODOS los elementos de texto dentro de métricas - NEGRO PURO */
            div[data-testid="metric-container"] * {
                color: #000000 !important;
            }
            .stMetric * {
                color: #000000 !important;
            }
            /* Valores específicos de métricas */
            div[data-testid="metric-container"] span,
            div[data-testid="metric-container"] p,
            div[data-testid="metric-container"] div {
                color: #000000 !important;
                font-weight: 700 !important;
            }
            
            /* SELECTBOX y INPUTS con contraste */
            .stSelectbox > div > div {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 2px solid #999999 !important;
                font-weight: 600 !important;
            }
            .stTextInput > div > div > input {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 2px solid #999999 !important;
                font-weight: 600 !important;
            }
            .stTextInput > div > div > input:focus {
                border-color: #0066cc !important;
                box-shadow: 0 0 0 0.3rem rgba(0,102,204,.3) !important;
            }
            
            /* EXPANDER con contraste */
            .stExpander {
                background-color: #ffffff !important;
                border: 2px solid #999999 !important;
                border-radius: 8px !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
            }
            .stExpander > div > div {
                background-color: #e0e0e0 !important;
                color: #000000 !important;
                font-weight: 700 !important;
            }
            
            /* BOTONES con contraste máximo */
            .stButton > button {
                background-color: #0066cc !important;
                color: #ffffff !important;
                border: 2px solid #0066cc !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
                font-size: 16px !important;
                padding: 8px 16px !important;
            }
            .stButton > button:hover {
                background-color: #004499 !important;
                border-color: #004499 !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
            }
            .stDownloadButton > button {
                background-color: #006600 !important;
                color: #ffffff !important;
                border: 2px solid #006600 !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
                font-size: 16px !important;
                padding: 8px 16px !important;
            }
            .stDownloadButton > button:hover {
                background-color: #004400 !important;
                border-color: #004400 !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
            }
            
            /* FILE UPLOADER con contraste */
            [data-testid="stFileUploader"] {
                border: 3px dashed #999999 !important;
                border-radius: 10px !important;
                background-color: #f0f0f0 !important;
                color: #000000 !important;
                font-weight: 600 !important;
            }
            [data-testid="stFileUploader"]:hover {
                border-color: #0066cc !important;
                background-color: #e0e8ff !important;
            }
            /* File uploader area con fondo negro - texto blanco */
            .stFileUploader label {
                background-color: #2c3e50 !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                padding: 10px !important;
                border-radius: 8px !important;
            }
            /* Browse files button con fondo negro - texto blanco */
            button[kind="secondary"] {
                background-color: #2c3e50 !important;
                color: #ffffff !important;
                border: 2px solid #2c3e50 !important;
                font-weight: 700 !important;
            }
            button[kind="secondary"]:hover {
                background-color: #1a252f !important;
                border-color: #1a252f !important;
            }
            
            /* Texto "Drag and drop file here" - BLANCO y personalizado */
            [data-testid="stFileUploader"] small {
                color: #ffffff !important;
                font-weight: 700 !important;
            }
            [data-testid="stFileUploader"] span {
                color: #ffffff !important;
                font-weight: 700 !important;
            }
            [data-testid="stFileUploader"] p {
                color: #ffffff !important;
                font-weight: 700 !important;
            }
            /* File uploader instructions específico */
            .uploadedFileText {
                color: #ffffff !important;
                font-weight: 700 !important;
            }
            
            /* Códigos RENIPRESS y otros textos específicos - NEGRO */
            .stText {
                color: #000000 !important;
                font-weight: 700 !important;
            }
            /* Texto general - asegurar negro en modo claro */
            div[data-testid="stText"] {
                color: #000000 !important;
                font-weight: 700 !important;
            }
            
            /* TÍTULOS Y TEXTO con contraste máximo */
            h1, h2, h3, h4, h5, h6 {
                color: #000000 !important;
                font-weight: 800 !important;
            }
            .stMarkdown {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            p {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            
            /* ELEMENTOS DEL SIDEBAR más específicos */
            .stSidebar .element-container {
                background-color: transparent !important;
            }
            .stSidebar .stButton > button {
                background-color: #0066cc !important;
                color: #ffffff !important;
                font-weight: 700 !important;
            }
            /* Sidebar info boxes */
            .stSidebar .stAlert {
                background-color: #e6f3ff !important;
                color: #000000 !important;
                border: 2px solid #0066cc !important;
                font-weight: 600 !important;
            }
            .stSidebar .stInfo {
                background-color: #e6f3ff !important;
                color: #000000 !important;
                border: 2px solid #0066cc !important;
                font-weight: 600 !important;
            }
            /* Contenido dentro de info boxes - NEGRO */
            .stSidebar .stAlert p, .stSidebar .stAlert div, .stSidebar .stAlert span {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            .stSidebar .stInfo p, .stSidebar .stInfo div, .stSidebar .stInfo span {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            
            /* FILTROS específicos */
            .stDateInput > div > div > input {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 2px solid #999999 !important;
                font-weight: 600 !important;
            }
            /* Inputs de fecha con fondo negro - texto blanco */
            input[type="date"] {
                background-color: #2c3e50 !important;
                color: #ffffff !important;
                border: 2px solid #999999 !important;
                font-weight: 600 !important;
            }
            
            /* Asegurar que TODOS los elementos de tabla sean legibles */
            table, th, td {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            
            /* Mejorar contraste en contenedores */
            .element-container {
                color: #000000 !important;
            }
            
            /* Labels y spans con contraste */
            label, span {
                color: #000000 !important;
                font-weight: 600 !important;
            }
        </style>
        <script>
        // Cambiar texto del file uploader a español
        setTimeout(function() {
            const dragTexts = document.querySelectorAll('[data-testid="stFileUploader"] small, [data-testid="stFileUploader"] span');
            dragTexts.forEach(function(element) {
                if (element.textContent.includes('Drag and drop') || element.textContent.includes('drag and drop')) {
                    element.textContent = 'Arrastre y suelte el archivo aquí';
                    element.style.color = '#ffffff';
                    element.style.fontWeight = '700';
                }
            });
        }, 1000);
        </script>
        """, unsafe_allow_html=True)
    
    st.title("📊 Sistema de Vigilancia Epidemiológica")
    st.markdown("---")
    
    # Sidebar for file upload
    with st.sidebar:
        st.markdown("---")
        st.header("📁 Cargar Datos")
        
        # File size info
        st.info("📋 **Requisitos del archivo:**\n"
                "- Formato: CSV (UTF-8)\n"
                "- Columnas: 91 campos\n"
                "- Tamaño máximo: 200MB\n"
                "- Registros: Hasta 150,000+")
        
        uploaded_file = st.file_uploader(
            "Seleccione o arrastre el archivo CSV",
            type=['csv'],
            help="Archivo CSV con datos de inspección epidemiológica"
        )
        
        if uploaded_file is not None:
            # Show file info
            file_size = uploaded_file.size / (1024 * 1024)  # MB
            st.info(f"📁 **{uploaded_file.name}**\n"
                   f"Tamaño: {file_size:.1f} MB")
            
            if file_size > 200:
                st.error("⚠️ El archivo excede el límite de 200MB")
                return
                
            try:
                with st.spinner("🔄 Procesando archivo... Esto puede tomar unos minutos para archivos grandes."):
                    # Múltiples intentos con diferentes codificaciones para compatibilidad de despliegue
                    data = None
                    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
                    successful_encoding = None
                    
                    for encoding in encodings:
                        try:
                            # Reset file pointer for each attempt
                            uploaded_file.seek(0)
                            
                            # Load data with optimizations for large files
                            data = pd.read_csv(
                                uploaded_file, 
                                encoding=encoding,
                                low_memory=False,
                                skipinitialspace=True,  # Skip spaces after delimiter
                                na_values=['', 'NA', 'N/A', 'null', 'NULL', 'NaN'],  # Handle missing values
                                keep_default_na=True
                            )
                            
                            # If successful, store the encoding and break the loop
                            successful_encoding = encoding
                            break
                            
                        except (UnicodeDecodeError, UnicodeError) as e:
                            # Try next encoding
                            if encoding == encodings[-1]:  # Last encoding attempt
                                st.error(f"❌ Error de codificación: {str(e)}")
                                st.info("💡 Intenta guardar tu archivo CSV con codificación UTF-8")
                                return
                            continue
                        except Exception as e:
                            # Other errors, show them but try next encoding
                            if encoding == encodings[-1]:  # Last encoding attempt
                                st.error(f"❌ Error al procesar archivo: {str(e)}")
                                return
                            continue
                    
                    # Validate that we got data
                    if data is None or data.empty:
                        st.error("❌ No se pudo cargar el archivo o está vacío")
                        return
                    
                    # Additional validation for epidemiological data structure
                    if len(data.columns) < 90:  # Should have 91 columns
                        st.warning(f"⚠️ El archivo tiene {len(data.columns)} columnas, se esperaban 91. Continuando con los datos disponibles...")
                    
                    st.session_state.data_processor = DataProcessor(data)
                    st.session_state.data = data
                    
                    # Detectar establecimientos con viviendas faltantes
                    housing_mgmt = HousingManagement()
                    missing_facilities = housing_mgmt.detect_missing_facilities(data)
                    
                    if missing_facilities:
                        # Mostrar diálogo para establecimientos faltantes
                        housing_mgmt.show_missing_facilities_dialog(missing_facilities)
                    
                st.success(f"✅ Archivo cargado exitosamente! (codificación: {successful_encoding})")
                st.metric("📈 Registros", f"{len(data):,}")
                st.metric("📋 Columnas", f"{len(data.columns)}")
                
                # Show data types summary
                with st.expander("📊 Resumen de Datos"):
                    activity_types = data['tipoActividadInspeccion'].value_counts()
                    st.write("**Tipos de Actividad:**")
                    for activity, count in activity_types.items():
                        st.write(f"- {activity}: {count:,} registros")
                
            except Exception as e:
                st.error(f"❌ Error al cargar el archivo: {str(e)}")
                st.info("💡 **Posibles soluciones:**\n"
                       "- Verifique que el archivo sea CSV válido\n"
                       "- Asegúrese de que esté codificado en UTF-8\n"
                       "- Verifique que tenga las 91 columnas requeridas")
                return
    
    # Main content area
    if st.session_state.data is not None:
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Vigilancia", "🦟 Control Larvario", "🔒 Cerco", "👤 Inspectores", "🏠 Gestión Viviendas"])
        
        with tab1:
            vigilancia_tab = VigilanciaTab(st.session_state.data_processor)
            vigilancia_tab.render()
        
        with tab2:
            control_larvario_tab = ControlLarvarioTab(st.session_state.data_processor)
            control_larvario_tab.render()
        
        with tab3:
            cerco_tab = CercoTab(st.session_state.data_processor)
            cerco_tab.render()
        
        with tab4:
            from utils.calculations import EpidemiologicalCalculations
            calculations = EpidemiologicalCalculations(st.session_state.data_processor)
            inspector_tab = InspectorTab(st.session_state.data_processor, calculations)
            inspector_tab.render()
        
        with tab5:
            housing_mgmt = HousingManagement()
            housing_mgmt.show_housing_management_interface()
    else:
        # Welcome screen
        st.markdown("""
        ## 👋 Bienvenido al Sistema de Vigilancia Epidemiológica
        
        Este sistema está diseñado para analizar y visualizar datos de inspecciones epidemiológicas.
        
        ### 📋 Características principales:
        - **Procesamiento de datos masivos**: Maneja más de 150,000 registros
        - **Filtros dinámicos**: Búsqueda y filtrado por múltiples criterios
        - **Cálculos especializados**: Índice Aédico y estadísticas de recipientes
        - **Visualizaciones interactivas**: Dashboards con gráficos dinámicos
        - **Tres módulos de análisis**: Vigilancia, Control Larvario y Cerco
        
        ### 🚀 Para comenzar:
        1. Cargue su archivo CSV usando el panel lateral
        2. Seleccione la pestaña de análisis deseada
        3. Configure los filtros según sus necesidades
        4. Explore los resultados en tiempo real
        
        ---
        **📁 Por favor, cargue un archivo CSV para comenzar el análisis.**
        
        ### 🔍 Health Check
        Para verificar el estado de la aplicación, visite: [Health Check](?health=true)
        """)
        
        # Add application status in sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🔋 Estado del Sistema")
            health_data = health_check()
            if health_data['status'] == 'healthy':
                st.success("✅ Sistema Operativo")
                uptime_hours = float(health_data['uptime_seconds']) / 3600
                st.metric("⏱️ Tiempo Activo", f"{uptime_hours:.1f}h")
            else:
                st.error("❌ Sistema con Problemas")

if __name__ == "__main__":
    main()
