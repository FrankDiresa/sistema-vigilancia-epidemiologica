"""
Utilidades para mejorar las tablas del sistema con funcionalidades adicionales
como filas de suma total, formateo mejorado, etc.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union

def add_total_row(df: pd.DataFrame, 
                  exclude_columns: Optional[List[str]] = None,
                  total_label: str = "TOTAL",
                  label_column: Optional[str] = None) -> pd.DataFrame:
    """
    Agrega una fila de suma total a un DataFrame.
    
    Args:
        df: DataFrame original
        exclude_columns: Lista de columnas a excluir del cálculo de suma
        total_label: Etiqueta para la fila total
        label_column: Columna donde colocar la etiqueta TOTAL (primera columna string por defecto)
    
    Returns:
        DataFrame con fila de suma total agregada
    """
    
    if df.empty:
        return df
    
    # Crear copia del DataFrame original
    df_copy = df.copy()
    
    # Identificar columnas numéricas
    numeric_columns = df_copy.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remover columnas excluidas
    if exclude_columns:
        numeric_columns = [col for col in numeric_columns if col not in exclude_columns]
    
    # Si no hay columnas numéricas, retornar el DataFrame original
    if not numeric_columns:
        return df_copy
    
    # Crear fila de totales
    total_row = {}
    
    # Inicializar todas las columnas
    for col in df_copy.columns:
        if col in numeric_columns:
            # Sumar valores numéricos, ignorando NaN
            total_value = df_copy[col].sum()
            # Mantener el formato de la columna original
            if df_copy[col].dtype == 'int64':
                total_row[col] = int(total_value) if not pd.isna(total_value) else 0
            else:
                total_row[col] = round(total_value, 2) if not pd.isna(total_value) else 0.0
        else:
            # Para columnas no numéricas, usar string vacío
            total_row[col] = ""
    
    # Determinar dónde colocar la etiqueta TOTAL
    if label_column and label_column in df_copy.columns:
        total_row[label_column] = total_label
    else:
        # Buscar la primera columna de tipo string/object para colocar el TOTAL
        text_columns = df_copy.select_dtypes(include=['object', 'string']).columns
        if not text_columns.empty:
            total_row[text_columns[0]] = total_label
        elif df_copy.columns.any():
            # Si no hay columnas de texto, usar la primera columna
            total_row[df_copy.columns[0]] = total_label
    
    # Agregar la fila total al DataFrame
    total_df = pd.DataFrame([total_row])
    result_df = pd.concat([df_copy, total_df], ignore_index=True)
    
    return result_df

def format_dataframe_for_display(df: pd.DataFrame,
                                float_columns: Optional[List[str]] = None,
                                int_columns: Optional[List[str]] = None,
                                percentage_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Formatea un DataFrame para mostrar con mejor legibilidad.
    
    Args:
        df: DataFrame a formatear
        float_columns: Columnas a formatear como flotante con 2 decimales
        int_columns: Columnas a formatear como enteros
        percentage_columns: Columnas a formatear como porcentajes
    
    Returns:
        DataFrame formateado
    """
    
    df_formatted = df.copy()
    
    # Formatear columnas de flotantes
    if float_columns:
        for col in float_columns:
            if col in df_formatted.columns:
                df_formatted[col] = df_formatted[col].round(2)
    
    # Formatear columnas de enteros
    if int_columns:
        for col in int_columns:
            if col in df_formatted.columns:
                df_formatted[col] = df_formatted[col].fillna(0).astype(int)
    
    # Formatear columnas de porcentajes
    if percentage_columns:
        for col in percentage_columns:
            if col in df_formatted.columns:
                df_formatted[col] = df_formatted[col].round(1)
    
    return df_formatted

def create_enhanced_dataframe(df: pd.DataFrame,
                             add_totals: bool = True,
                             total_label: str = "TOTAL",
                             exclude_from_total: Optional[List[str]] = None,
                             label_column: Optional[str] = None) -> pd.DataFrame:
    """
    Función principal para crear DataFrames mejorados con totales y formato.
    
    Args:
        df: DataFrame original
        add_totals: Si agregar fila de totales
        total_label: Etiqueta para la fila total
        exclude_from_total: Columnas a excluir del cálculo de suma
        label_column: Columna donde colocar la etiqueta TOTAL
    
    Returns:
        DataFrame mejorado
    """
    
    if df.empty:
        return df
    
    enhanced_df = df.copy()
    
    # Agregar fila de totales si se solicita
    if add_totals:
        enhanced_df = add_total_row(
            enhanced_df,
            exclude_columns=exclude_from_total,
            total_label=total_label,
            label_column=label_column
        )
    
    return enhanced_df