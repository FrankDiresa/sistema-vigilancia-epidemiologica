# 🚀 Guía Completa de Despliegue - Sistema de Vigilancia Epidemiológica

## 🎯 Resumen Rápido

**🏆 Plataforma Recomendada: [Streamlit Community Cloud](https://share.streamlit.io)**
- ✅ **GRATIS** para repositorios públicos
- ✅ **OFICIAL** - Creado por los desarrolladores de Streamlit  
- ✅ **AUTOMÁTICO** - Se actualiza con cada git push
- ✅ **FÁCIL** - Despliegue en 3 clics

---

## 📋 Paso 1: Preparar GitHub

### 1.1 Verificar Archivos Necesarios

Tu proyecto ya tiene todos los archivos listos:
```
✅ app.py                    # Archivo principal
✅ requirements.txt          # Dependencias Python
✅ .streamlit/config.toml    # Configuración Streamlit
✅ README.md                 # Documentación
✅ components/               # Módulos de la aplicación
✅ utils/                    # Utilidades
```

### 1.2 Crear Repositorio en GitHub

1. **Ve a [github.com](https://github.com) y haz clic en "New repository"**

2. **Configuración del repositorio:**
   ```
   Repository name: sistema-vigilancia-epidemiologica
   Description: Sistema completo de análisis epidemiológico con Streamlit
   Visibility: Public (IMPORTANTE: debe ser público para plan gratuito)
   ✅ NO marques "Add a README file"
   ✅ NO marques "Add .gitignore"
   ```

3. **Haz clic en "Create repository"**

### 1.3 Subir el Código

```bash
# Inicializar Git (si no está ya)
git init

# Configurar Git con tu información
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"

# Agregar todos los archivos
git add .

# Hacer primer commit
git commit -m "🎉 Sistema de Vigilancia Epidemiológica completo

✅ Características:
- Análisis de vigilancia epidemiológica con Índice Aédico
- Control larvario con estadísticas de recipientes
- Cerco epidemiológico con cobertura y tendencias
- Gestión de datos de viviendas
- Tema claro/oscuro optimizado
- Filas de suma total en todas las tablas
- Exportación Excel y reportes PowerPoint
- Importación CSV robusta para despliegue
- Sistema completo de filtros dinámicos"

# Conectar con GitHub (reemplaza USERNAME con tu usuario)
git remote add origin https://github.com/USERNAME/sistema-vigilancia-epidemiologica.git

# Subir código
git branch -M main
git push -u origin main
```

---

## 🌟 Paso 2: Desplegar en Streamlit Community Cloud

### 2.1 Acceder a la Plataforma

1. **Ve a [share.streamlit.io](https://share.streamlit.io)**
2. **Haz clic en "Sign in with GitHub"**
3. **Autoriza Streamlit Community Cloud** para acceder a tus repositorios

### 2.2 Crear Nueva Aplicación

1. **Haz clic en "New app"**

2. **Configuración de despliegue:**
   ```
   Repository: USERNAME/sistema-vigilancia-epidemiologica
   Branch: main
   Main file path: app.py
   App URL (opcional): tu-nombre-vigilancia
   ```

3. **Haz clic en "Deploy!"**

### 2.3 ¡Listo! 🎉

En **2-3 minutos**, tu aplicación estará disponible en:
```
https://USERNAME-sistema-vigilancia-epidemiologica.streamlit.app
```

O con URL personalizada:
```
https://tu-nombre-vigilancia.streamlit.app
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno (Opcional)

Si necesitas variables de entorno:

1. **En tu app desplegada**, haz clic en "⚙️ Settings"
2. **Ve a "Secrets"**
3. **Agrega variables en formato TOML:**
   ```toml
   [general]
   DATABASE_URL = "postgresql://..."
   API_KEY = "tu-api-key"
   ```

### Logs y Monitoreo

1. **Ver logs**: Haz clic en "☁️ Manage app" → "Logs"
2. **Reiniciar app**: "☁️ Manage app" → "Reboot"
3. **Actualizar**: Solo haz `git push` - se actualiza automáticamente

---

## 🚀 Alternativas de Despliegue

### Opción 2: Render (También Gratis)

1. **Ve a [render.com](https://render.com)**
2. **"New" → "Web Service"**
3. **Conecta tu repositorio de GitHub**
4. **Configuración:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

### Opción 3: Railway

1. **Ve a [railway.app](https://railway.app)**
2. **"Deploy from GitHub repo"**
3. **Selecciona tu repositorio**
4. **Railway detecta automáticamente** que es una app Streamlit

### Opción 4: Heroku

1. **Instalar Heroku CLI**
2. **Crear archivo `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. **Desplegar:**
   ```bash
   heroku create tu-app-name
   git push heroku main
   ```

---

## ❌ Plataformas que NO Soportan Streamlit

### Por qué NO usar ciertas plataformas:

**❌ Netlify / Vercel / GitHub Pages:**
- Solo sirven archivos estáticos (HTML/CSS/JS)
- Streamlit requiere servidor Python ejecutándose
- NO pueden ejecutar código Python server-side

**✅ Para Streamlit, usa siempre:**
- Streamlit Community Cloud (recomendado)
- Render
- Railway  
- Heroku
- Fly.io
- DigitalOcean App Platform

---

## 🔄 Flujo de Actualizaciones

### Para actualizar tu aplicación después de cambios:

```bash
# Hacer cambios en tu código local
# ...

# Agregar cambios
git add .

# Commit con descripción clara
git commit -m "✨ Nueva funcionalidad: descripción del cambio"

# Subir a GitHub
git push origin main
```

**¡Automático!** En 1-2 minutos:
1. ✅ GitHub recibe los cambios
2. ✅ Streamlit Community Cloud detecta la actualización
3. ✅ Rebuild automático
4. ✅ App actualizada en vivo

---

## 🏥 URL Final de Tu Sistema

Una vez completado, tendrás tu sistema de vigilancia epidemiológica disponible 24/7:

```
🌐 https://tu-usuario-vigilancia-epidemiologica.streamlit.app
```

**Accesible desde cualquier parte del mundo** para:
- 👩‍⚕️ Equipos de salud pública
- 📊 Analistas epidemiológicos  
- 🏥 Personal de establecimientos de salud
- 🔬 Investigadores en salud

---

## ✅ Checklist Final

### Antes del despliegue:
- [ ] Código funcionando localmente
- [ ] requirements.txt actualizado
- [ ] Repositorio GitHub público creado
- [ ] Archivos temporales excluidos en .gitignore

### Durante el despliegue:
- [ ] Código subido a GitHub exitosamente
- [ ] Streamlit Community Cloud conectado
- [ ] App desplegada sin errores
- [ ] URL final funcionando

### Después del despliegue:
- [ ] Todas las funcionalidades operando
- [ ] Carga de archivos CSV funcionando
- [ ] Exportaciones Excel funcionando  
- [ ] Tema claro/oscuro funcionando
- [ ] Filas de suma total funcionando
- [ ] Responsive design verificado en móvil/tablet

---

## 📞 Soporte Técnico

### Si encuentras problemas:

1. **Logs de la aplicación**: Ve a tu app → "⚙️ Settings" → "Logs"
2. **Comunidad Streamlit**: [discuss.streamlit.io](https://discuss.streamlit.io)
3. **GitHub Issues**: En tu repositorio para bugs específicos
4. **Documentación oficial**: [docs.streamlit.io](https://docs.streamlit.io)

---

## 🎯 ¡Felicitaciones!

Tu **Sistema de Vigilancia Epidemiológica** está ahora:
- 🌍 **Desplegado globalmente**
- 🔄 **Actualización automática**  
- 💰 **Completamente gratis**
- 🚀 **Listo para producción**

**¡Impactando la salud pública a nivel mundial!** 🏥✨

---

*Guía actualizada - Septiembre 2025*  
*Preparada específicamente para Streamlit Community Cloud*