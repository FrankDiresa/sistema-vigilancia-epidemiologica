import pandas as pd
import numpy as np
from datetime import datetime

class DataProcessor:
    def __init__(self, data):
        self.data = data.copy()
        self.process_data()
        
        # Health facilities reference data
        self.health_facilities = {
            5060: {"name": "LA LIBERTAD", "total_houses": 136},
            5044: {"name": "GUSTAVO LANATTA LUJAN", "total_houses": 4282},
            7276: {"name": "LA PRIMAVERA", "total_houses": 1822},
            7435: {"name": "MESONES MURO", "total_houses": 426},
            7006: {"name": "SAN FRANCISCO", "total_houses": 188},
            5126: {"name": "MIRAFLORES", "total_houses": 206},
            5135: {"name": "VISTA ALEGRE", "total_houses": 41},
            5136: {"name": "LA VICTORIA", "total_houses": 486},
            5137: {"name": "PUEBLO LIBRE", "total_houses": 50},
            7225: {"name": "MORROPON", "total_houses": 90},
            7285: {"name": "SAN LUIS", "total_houses": 1874},
            5095: {"name": "SAN JUAN DE LA LIBERTAD", "total_houses": 456},
            5096: {"name": "JOSE OLAYA", "total_houses": 280},
            7258: {"name": "SANTA ISABEL", "total_houses": 138},
            7259: {"name": "LA UNION", "total_houses": 100},
            5066: {"name": "EL MILAGRO", "total_houses": 505},
            1720: {"name": "SAN RAFAEL", "total_houses": 804},
            1744: {"name": "LA VICTORIA", "total_houses": 7191},
            1659: {"name": "PROGRESO", "total_houses": 9674},
            1660: {"name": "LA UNION", "total_houses": 4576},
            1661: {"name": "SAN PEDRO", "total_houses": 11249},
            1662: {"name": "VICTOR RAUL", "total_houses": 2309},
            1663: {"name": "TUPAC AMARU", "total_houses": 1799},
            1664: {"name": "LA ESPERANZA", "total_houses": 2004},
            1715: {"name": "SAN JACINTO", "total_houses": 10725},
            1706: {"name": "VILLA MARIA", "total_houses": 5568},
            1681: {"name": "ALTO PERU", "total_houses": 374},
            2664: {"name": "BELLAVISTA", "total_houses": 3738},
            8828: {"name": "SAN MARTIN", "total_houses": 2213},
            2570: {"name": "SANTA ROSA", "total_houses": 350},
            1345: {"name": "SAN JOSE", "total_houses": 90},
            1368: {"name": "SANTA ROSA", "total_houses": 153},
            23961: {"name": "MIRAFLORES", "total_houses": 365},
            3760: {"name": "LECHEMAYO", "total_houses": 716},
            3749: {"name": "PALMAPAMPA", "total_houses": 1924}
        }
    
    def process_data(self):
        """Process and clean the data"""
        # Convert date columns
        date_columns = ['fecha_inspeccion', '_createdAt_x', '_createdAt_y', 'hora_ingreso', 
                       'hora_salida', 'fecha_creacion', 'recuperacion_fecha', 
                       'recuperacion_fecha_asignacion']
        
        for col in date_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
        
        # Extract year from fecha_inspeccion
        if 'fecha_inspeccion' in self.data.columns:
            self.data['year'] = self.data['fecha_inspeccion'].dt.year
        
        # Fill NaN values for numeric columns
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        self.data[numeric_columns] = self.data[numeric_columns].fillna(0)
        
        # Fill NaN values for text columns
        text_columns = self.data.select_dtypes(include=['object']).columns
        self.data[text_columns] = self.data[text_columns].fillna('')
    
    def get_filtered_data(self, activity_type=None, filters=None):
        """Filter data based on activity type and additional filters"""
        filtered_data = self.data.copy()
        
        # Filter by activity type
        if activity_type:
            filtered_data = filtered_data[
                filtered_data['tipoActividadInspeccion'].str.lower() == activity_type.lower()
            ]
        
        # Apply additional filters
        if filters:
            for key, value in filters.items():
                if value and key in filtered_data.columns:
                    if isinstance(value, list):
                        filtered_data = filtered_data[filtered_data[key].isin(value)]
                    else:
                        filtered_data = filtered_data[filtered_data[key] == value]
        
        return filtered_data
    
    def get_unique_values(self, column_name, sorted_order=True):
        """Get unique values from a column"""
        if column_name not in self.data.columns:
            return []
        
        unique_values = self.data[column_name].dropna().unique()
        
        if sorted_order:
            # Try to sort numerically first, then alphabetically
            try:
                unique_values = sorted(unique_values, key=lambda x: float(x) if str(x).replace('.', '').isdigit() else float('inf'))
            except:
                unique_values = sorted(unique_values, key=str)
        
        # Convert to list if it's a numpy array
        try:
            if hasattr(unique_values, 'tolist'):
                return unique_values.tolist()
            else:
                return list(unique_values)
        except:
            return list(unique_values)
    
    def get_date_range(self):
        """Get min and max dates from fecha_inspeccion"""
        if 'fecha_inspeccion' in self.data.columns:
            dates = self.data['fecha_inspeccion'].dropna()
            if len(dates) > 0:
                return dates.min().date(), dates.max().date()
        return None, None
    
    def get_container_columns(self):
        """Get all container-related columns organized by type"""
        containers = {
            "Tanque Alto": ["tanque_alto_I", "tanque_alto_P", "tanque_alto_TQ", "tanque_alto_TF"],
            "Tanque Bajo": ["tanque_bajo_I", "tanque_bajo_P", "tanque_bajo_TQ", "tanque_bajo_TF"],
            "Barril/Cilindro": ["barril_cilindro_I", "barril_cilindro_P", "barril_cilindro_TQ", "barril_cilindro_TF"],
            "Sansón/Bidón": ["sanson_bidon_I", "sanson_bidon_P", "sanson_bidon_TQ", "sanson_bidon_TF"],
            "Baldes/Bateas/Tinajas": ["baldes_bateas_tinajas_I", "baldes_bateas_tinajas_P", "baldes_bateas_tinajas_TQ", "baldes_bateas_tinajas_TF"],
            "Llantas": ["llantas_I", "llantas_P", "llantas_TQ", "llantas_TF"],
            "Floreros/Maceteros": ["floreros_maceteros_I", "floreros_maceteros_P", "floreros_maceteros_TQ", "floreros_maceteros_TF"],
            "Latas/Botellas": ["latas_botellas_I", "latas_botellas_D", "latas_botellas_P", "latas_botellas_TQ", "latas_botellas_TF"],
            "Otros": ["otros_I", "otros_P", "otros_TQ", "otros_TF", "otros_D"],
            "Inservibles": ["inservibles_I", "inservibles_P", "inservibles_TQ", "inservibles_TF"]
        }
        return containers
    
    def get_container_status_labels(self):
        """Get container status labels"""
        return {
            "_I": "Inspeccionado(s)",
            "_P": "Positivo(s)",
            "_TQ": "Tratamiento Químico",
            "_TF": "Tratamiento Físico",
            "_D": "Desuso(s)"
        }
