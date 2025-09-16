# Sistema de Vigilancia Epidemiológica

Un sistema completo de análisis y visualización de datos epidemiológicos desarrollado con Streamlit.

## Descripción

Este sistema está diseñado para instituciones de salud pública que necesitan procesar y analizar archivos CSV grandes (hasta 200MB, 150,000+ registros) con información de vigilancia epidemiológica. Proporciona tres módulos principales de análisis: Vigilancia, Control Larvario y Cerco Epidemiológico.

## Características Principales

- ✅ Procesamiento de archivos CSV de hasta 200MB
- ✅ Análisis de datos con 91 columnas de información epidemiológica
- ✅ Cálculo automático del Índice Aédico
- ✅ Análisis de cobertura y estadísticas de recipientes
- ✅ Seguimiento de consumo de larvicidas
- ✅ Análisis de casos febriles
- ✅ Visualizaciones interactivas con Plotly
- ✅ Filtrado dinámico por ubicación geográfica
- ✅ Análisis detallado por inspector
- ✅ Mapas de georeferenciación

## Módulos de Análisis

### 🔍 Vigilancia
- Cálculo del Índice Aédico por establecimiento de salud
- Estadísticas de recipientes por tipo y estado
- Análisis de consumo de larvicidas
- Tendencias mensuales y geográficas

### 🦟 Control Larvario
- Análisis de cobertura de inspecciones
- Tratamiento de recipientes (químico y físico)
- Seguimiento de casos febriles
- Métricas de eficiencia del control larvario

### 🔒 Cerco Epidemiológico
- Análisis de cerco epidemiológico
- Cobertura de intervenciones
- Estadísticas de recipientes en zona de cerco
- Seguimiento de larvicidas y casos febriles

### 👤 Análisis por Inspector
- Rendimiento individual de inspectores
- Productividad diaria y mensual
- Mapas de inspecciones georeferenciadas
- Comparación de eficiencia

## Requisitos del Sistema

### Archivos de Datos
- **Formato**: CSV con codificación UTF-8
- **Columnas**: 91 campos requeridos
- **Tamaño máximo**: 200MB
- **Registros**: Hasta 150,000+ registros

### Dependencias
```
streamlit
pandas
numpy
plotly
```

## Instalación

1. Clona este repositorio:
```bash
git clone <url-del-repositorio>
cd sistema-vigilancia-epidemiologica
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:
```bash
streamlit run app.py --server.port 5000
```

2. Abre tu navegador y ve a `http://localhost:5000`

3. Carga tu archivo CSV usando el panel lateral

4. Explora los diferentes módulos de análisis en las pestañas

## Estructura del Proyecto

```
├── app.py                          # Aplicación principal
├── components/                     # Componentes de interfaz
│   ├── vigilancia_tab.py          # Módulo de vigilancia
│   ├── control_larvario_tab.py    # Módulo de control larvario
│   ├── cerco_tab.py               # Módulo de cerco epidemiológico
│   ├── inspector_tab.py           # Análisis por inspector
│   └── filters.py                 # Componentes de filtrado
├── utils/                         # Utilidades
│   ├── data_processor.py          # Procesamiento de datos
│   ├── calculations.py            # Cálculos epidemiológicos
│   └── visualizations.py          # Generación de gráficos
├── pyproject.toml                 # Dependencias del proyecto
└── README.md                      # Este archivo
```

## Configuración para Replit

Si estás ejecutando en Replit, asegúrate de tener la configuración en `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Características Técnicas

- **Framework**: Streamlit para desarrollo rápido de aplicaciones de datos
- **Procesamiento**: Pandas para manipulación eficiente de datos
- **Visualización**: Plotly para gráficos interactivos
- **Arquitectura**: Modular con separación de responsabilidades
- **Gestión de Estado**: Streamlit session state para persistencia de datos
- **Rendimiento**: Optimizado para archivos grandes con gestión de memoria

## Soporte

Para reportar problemas o solicitar características, por favor crea un issue en el repositorio de GitHub.

## Licencia

Este proyecto está disponible bajo licencia MIT.