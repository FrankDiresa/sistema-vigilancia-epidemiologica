import streamlit as st
import pandas as pd
from datetime import datetime, date

class FilterComponent:
    def __init__(self, data_processor):
        self.data_processor = data_processor
    
    def render_filters(self, activity_type=None):
        """Render all filter components and return selected values"""
        filters = {}
        
        st.subheader("🔍 Filtros de Búsqueda")
        
        # Create filter columns with reordered filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Year filter
            years = self.data_processor.get_unique_values('year')
            if years:
                selected_year = st.selectbox(
                    "📅 Año",
                    options=['Todos'] + [str(year) for year in years if year],
                    help="Seleccione el año de inspección",
                    key=f"year_filter_{activity_type}"
                )
                if selected_year != 'Todos':
                    filters['year'] = int(selected_year)
            
            # Department filter
            departments = self.data_processor.get_unique_values('departamento_x')
            if departments:
                selected_dept = st.selectbox(
                    "🏛️ Departamento",
                    options=['Todos'] + [dept for dept in departments if dept],
                    help="Seleccione el departamento",
                    key=f"dept_filter_{activity_type}"
                )
                if selected_dept != 'Todos':
                    filters['departamento_x'] = selected_dept
        
        with col2:
            # Province filter
            provinces = self.data_processor.get_unique_values('nombre_prov')
            if provinces:
                selected_prov = st.selectbox(
                    "🏙️ Provincia",
                    options=['Todos'] + [prov for prov in provinces if prov],
                    help="Seleccione la provincia",
                    key=f"prov_filter_{activity_type}"
                )
                if selected_prov != 'Todos':
                    filters['nombre_prov'] = selected_prov
            
            # District filter
            districts = self.data_processor.get_unique_values('distrito')
            if districts:
                selected_dist = st.selectbox(
                    "🏘️ Distrito",
                    options=['Todos'] + [dist for dist in districts if dist],
                    help="Seleccione el distrito",
                    key=f"dist_filter_{activity_type}"
                )
                if selected_dist != 'Todos':
                    filters['distrito'] = selected_dist
        
        with col3:
            # RENIPRESS Code filter
            renipress_codes = self.data_processor.get_unique_values('cod_renipress')
            if renipress_codes:
                selected_renipress = st.selectbox(
                    "🏥 Código RENIPRESS",
                    options=['Todos'] + [str(code) for code in renipress_codes if code],
                    help="Seleccione el código RENIPRESS",
                    key=f"renipress_filter_{activity_type}"
                )
                if selected_renipress != 'Todos':
                    filters['cod_renipress'] = int(selected_renipress)
            
            # Health facility filter
            facilities = self.data_processor.get_unique_values('localidad_eess')
            if facilities:
                selected_facility = st.selectbox(
                    "🏥 Establecimiento de Salud",
                    options=['Todos'] + [facility for facility in facilities if facility],
                    help="Seleccione el establecimiento de salud",
                    key=f"facility_filter_{activity_type}"
                )
                if selected_facility != 'Todos':
                    filters['localidad_eess'] = selected_facility
        
        # Date range filter
        st.markdown("---")
        st.subheader("📅 Filtro por Rango de Fechas")
        
        min_date, max_date = self.data_processor.get_date_range()
        if min_date and max_date:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Fecha de inicio",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date,
                    key=f"start_date_{activity_type}"
                )
            with col2:
                end_date = st.date_input(
                    "Fecha de fin",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date,
                    key=f"end_date_{activity_type}"
                )
            
            # Add date range to filters
            if start_date and end_date:
                filters['date_range'] = (start_date, end_date)
        
        return filters
    
    def apply_date_filter(self, data, date_range):
        """Apply date range filter to data"""
        if date_range and 'fecha_inspeccion' in data.columns:
            start_date, end_date = date_range
            data = data[
                (data['fecha_inspeccion'].dt.date >= start_date) & 
                (data['fecha_inspeccion'].dt.date <= end_date)
            ]
        return data
    
    def render_search_filter(self, options, label, key):
        """Render a searchable selectbox"""
        # Create a text input for search
        search_term = st.text_input(f"Buscar {label}", key=f"search_{key}")
        
        # Filter options based on search term
        if search_term:
            filtered_options = [opt for opt in options if search_term.lower() in str(opt).lower()]
        else:
            filtered_options = options
        
        # Show selectbox with filtered options
        selected = st.selectbox(
            label,
            options=['Todos'] + filtered_options,
            key=key
        )
        
        return selected if selected != 'Todos' else None
