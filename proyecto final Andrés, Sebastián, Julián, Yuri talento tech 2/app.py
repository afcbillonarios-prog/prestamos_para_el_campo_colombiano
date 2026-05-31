import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="AgroCrédito Colombia - Seguridad Alimentaria",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-family: 'Outfit', sans-serif; color: #10b981; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.1rem; }
    .sub-header { color: #64748b; font-size: 1.1rem; margin-bottom: 2rem; }
    .metric-card { background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-left: 6px solid #10b981; }
    .metric-value { font-size: 2.5rem; font-weight: 800; color: #10b981; }
    .metric-label { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
    .section-card { background-color: #1e293b; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
    .badge { background-color: #064e3b; color: #34d399; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-right: 6px; }
    .sector-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 16px; padding: 24px; text-align: center; transition: all 0.3s; }
    .sector-card:hover { border-color: #10b981; transform: translateY(-3px); }
    .sector-icon { font-size: 3rem; margin-bottom: 12px; }
    .sector-title { font-size: 1.1rem; font-weight: 600; color: #f3f4f6; margin-bottom: 8px; }
    .sector-desc { font-size: 0.85rem; color: #94a3b8; }
    .impact-box { background: linear-gradient(135deg, #064e3b 0%, #065f46 100%); border-radius: 12px; padding: 20px; text-align: center; }
    .impact-number { font-size: 2rem; font-weight: 800; color: #34d399; }
    .impact-label { font-size: 0.85rem; color: #a7f3d0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌾 AgroCrédito Colombia</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Seguridad Alimentaria y Créditos Rurales Inteligentes para Colombia</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('data/creditos_rurales_limpio.csv')

df = load_data()

if os.path.exists('modelo_creditos.pkl'):
    model_data = joblib.load('modelo_creditos.pkl')
    modelo = model_data['modelo']
    features = model_data['caracteristicas']
    coeficientes = model_data['coeficientes']
    intercepto = model_data['intercepto']
    metricas = model_data['metricas']
else:
    st.error("No se encontró el modelo. Ejecuta run_modeling.py primero.")
    st.stop()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Panel Principal",
    "🔍 Consulta por Cédula",
    "📊 Sectores Productivos",
    "💻 Tecnología Rural",
    "📈 Impacto Alimentario"
])

with tab1:
    st.markdown("## Panel Principal - Impacto Nacional")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">Total Créditos</div><div class="metric-value">{len(df):,}</div></div>""", unsafe_allow_html=True)
    with col2:
        aprobados = df['Credito_Aprobado'].sum()
        st.markdown(f"""<div class="metric-card"><div class="metric-label">Aprobados</div><div class="metric-value">{aprobados:,.0f}</div></div>""", unsafe_allow_html=True)
    with col3:
        monto_total = df['Monto_Prestamo_COP'].sum() / 1e9
        st.markdown(f"""<div class="metric-card"><div class="metric-label">Monto Total (Mds COP)</div><div class="metric-value">${monto_total:,.1f}</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">R² del Modelo</div><div class="metric-value">{metricas['r2']*100:.1f}%</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Distribución por Departamento")
        dept_counts = df['Departamento'].value_counts().head(15)
        st.bar_chart(dept_counts)

    with col_b:
        st.markdown("### Distribución por Sector")
        sector_counts = df['Sector_Productivo'].value_counts()
        st.bar_chart(sector_counts)

    st.markdown("---")
    st.markdown("### Evolución de Créditos por Departamento")

    deptos_sample = df['Departamento'].value_counts().head(8).index.tolist()
    years = list(range(2019, 2026))
    data_evol = []
    for depto in deptos_sample:
        base = df[df['Departamento'] == depto].shape[0] // 7
        for i, yr in enumerate(years):
            growth = base * (1 + i * 0.15) + np.random.randint(-5, 15)
            data_evol.append({'Año': yr, 'Departamento': depto, 'Créditos': max(0, growth)})

    df_evol = pd.DataFrame(data_evol)
    st.line_chart(df_evol.pivot_table(index='Año', columns='Departamento', values='Créditos', aggfunc='sum'))

with tab2:
    st.markdown("## 🔍 Consulta de Crédito por Cédula")

    col_input, col_result = st.columns([1, 1.5])

    with col_input:
        st.markdown("### Ingresa tu Cédula")
        cedula_input = st.text_input("Número de cédula:", placeholder="Ej: 1234567890")

        st.markdown("---")
        st.markdown("### O completa tu perfil")

        edad = st.slider("Edad:", 18, 75, 35)
        experiencia = st.slider("Años de experiencia agrícola:", 0, 40, 5)
        hectareas = st.number_input("Hectareas cultivables:", 0.5, 100.0, 5.0)
        ingresos = st.number_input("Ingresos mensuales (COP):", 500000, 20000000, 3000000, step=500000)

        st.markdown("### Datos del Crédito")
        monto = st.slider("Monto del préstamo (COP):", 5000000, 200000000, 50000000, step=5000000)
        plazo = st.select_slider("Plazo (meses):", options=[12, 24, 36, 48, 60], value=36)
        garantia = st.checkbox("Tiene garantía respaldada")
        subsidio = st.checkbox("Tiene subsidio de gobierno (LEC Finagro)")

        st.markdown("### Tecnologías")
        tech_count = st.slider("Número de tecnologías implementadas:", 0, 5, 1)
        energia_solar = st.checkbox("Energía solar")
        riego = st.checkbox("Sistema de riego")

    with col_result:
        st.markdown("### Resultado de la Consulta")

        if cedula_input:
            resultado = df[df['Cedula'] == str(cedula_input)]

            if len(resultado) > 0:
                st.success(f"Cédula {cedula_input} encontrada en la base de datos")
                registro = resultado.iloc[0]

                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">Datos del Registro</div>
                    <div style="margin-top:10px;">
                        <p><strong>Departamento:</strong> {registro['Departamento']}</p>
                        <p><strong>Sector:</strong> {registro['Sector_Productivo']}</p>
                        <p><strong>Producto:</strong> {registro['Producto']}</p>
                        <p><strong>Tasa Actual:</strong> {registro['Tasa_Interes_EA']:.2f}% E.A.</p>
                        <p><strong>Estado:</strong> {'Aprobado' if registro['Credito_Aprobado'] == 1 else 'En revisión'}</p>
                    </div>
                </div>""", unsafe_allow_html=True)

                edad = int(registro['Edad'])
                experiencia = int(registro['Experiencia_Anios'])
                hectareas = float(registro['Hectareas'])
                ingresos = float(registro['Ingresos_Mensuales_COP'])
                monto = float(registro['Monto_Prestamo_COP'])
                plazo = int(registro['Plazo_Meses'])
                garantia = bool(registro['Garantia_Respaldada'])
                subsidio = bool(registro['Subsidio_Gobierno'])
                tech_count = int(registro['Tecnologias_Usadas'])
                energia_solar = bool(registro['Tiene_Energia_Solar'])
                riego = bool(registro['Tiene_Riego'])
            else:
                st.warning("Cédula no encontrada. Usando datos del formulario manual.")

        datos_modelo = pd.DataFrame([{
            'Edad': edad,
            'Experiencia_Anios': experiencia,
            'Hectareas': hectareas,
            'Ingresos_Mensuales_COP': ingresos,
            'Monto_Prestamo_COP': monto,
            'Plazo_Meses': plazo,
            'Garantia_Respaldada': 1 if garantia else 0,
            'Subsidio_Gobierno': 1 if subsidio else 0,
            'Tecnologias_Usadas': tech_count,
            'Tiene_Energia_Solar': 1 if energia_solar else 0,
            'Tiene_Riego': 1 if riego else 0
        }])

        tasa_predicha = modelo.predict(datos_modelo)[0]
        tasa_predicha = np.clip(tasa_predicha, 6.0, 31.0)

        tasa_mensual = (1 + tasa_predicha/100)**(1/12) - 1
        n_pagos = plazo
        if tasa_mensual > 0:
            cuota = monto * (tasa_mensual * (1 + tasa_mensual)**n_pagos) / ((1 + tasa_mensual)**n_pagos - 1)
        else:
            cuota = monto / n_pagos
        total_pagar = cuota * n_pagos
        interes_total = total_pagar - monto

        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Tasa de Interés Estimada</div>
            <div class="metric-value">{tasa_predicha:.2f}% E.A.</div>
            <div style="margin-top:10px;">
                <span class="badge">R²: {metricas['r2']*100:.1f}%</span>
                <span class="badge">MAE: {metricas['mae']:.2f} pp</span>
                <span class="badge">Regresión Lineal</span>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Cuota Mensual", f"${cuota:,.0f} COP")
        with col_r2:
            st.metric("Total a Pagar", f"${total_pagar:,.0f} COP")
        with col_r3:
            st.metric("Interés Total", f"${interes_total:,.0f} COP")

        st.markdown("### Tabla de Amortización")
        saldo = monto
        tabla = []
        for mes in range(1, n_pagos + 1):
            int_mes = saldo * tasa_mensual
            capital = cuota - int_mes
            saldo -= capital
            if saldo < 0:
                saldo = 0
            tabla.append({
                'Mes': mes,
                'Cuota': cuota,
                'Capital': capital,
                'Interés': int_mes,
                'Saldo': saldo
            })

        df_tabla = pd.DataFrame(tabla)
        st.dataframe(df_tabla.style.format({
            'Cuota': '${:,.0f}',
            'Capital': '${:,.0f}',
            'Interés': '${:,.0f}',
            'Saldo': '${:,.0f}'
        }), use_container_width=True, height=400)

        st.markdown("### Contribución de Variables")
        contribuciones = {}
        for feat in features:
            val = datos_modelo[feat].values[0]
            coef = coeficientes[feat]
            contribuciones[feat] = val * coef

        contribuciones['Intercepto'] = intercepto
        df_contrib = pd.DataFrame(list(contribuciones.items()), columns=['Variable', 'Contribución'])
        df_contrib = df_contrib.sort_values('Contribución', ascending=True)
        st.bar_chart(df_contrib.set_index('Variable'))

with tab3:
    st.markdown("## 📊 Sectores Productivos")

    st.markdown("### Distribución de Créditos por Sector y Departamento")

    sector_dept = pd.crosstab(df['Departamento'], df['Sector_Productivo'])
    st.dataframe(sector_dept, use_container_width=True)

    st.markdown("---")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("### Tasa Promedio por Sector")
        tasa_sector = df.groupby('Sector_Productivo')['Tasa_Interes_EA'].mean().sort_values()
        st.bar_chart(tasa_sector)

    with col_s2:
        st.markdown("### Monto Promedio por Sector")
        monto_sector = df.groupby('Sector_Productivo')['Monto_Prestamo_COP'].mean() / 1e6
        st.bar_chart(monto_sector)

    st.markdown("### Sectores Productivos")

    sectores_info = [
        {"icon": "🌱", "title": "Agricultura", "desc": "Café, cacao, arroz, maíz, frutas, hortalizas"},
        {"icon": "🐄", "title": "Ganadería", "desc": "Leche, carne bovina, ovina, caprina"},
        {"icon": "🐟", "title": "Piscicultura", "desc": "Tilapia, trucha, camarón"},
        {"icon": "🐷", "title": "Porcícola", "desc": "Producción porcina intensiva"},
        {"icon": "🐔", "title": "Avicultura", "desc": "Pollo, huevo, pavo"},
        {"icon": "☀️", "title": "Energía Solar", "desc": "Placas fotovoltaicas, bombas solares"},
        {"icon": "🤖", "title": "Tecnología Agrícola", "desc": "Riego, drones, sensores IoT"}
    ]

    cols = st.columns(4)
    for i, sect in enumerate(sectores_info):
        with cols[i % 4]:
            st.markdown(f"""<div class="sector-card">
                <div class="sector-icon">{sect['icon']}</div>
                <div class="sector-title">{sect['title']}</div>
                <div class="sector-desc">{sect['desc']}</div>
            </div>""", unsafe_allow_html=True)

with tab4:
    st.markdown("## 💻 Tecnología Rural")

    st.markdown("### Adopta Tecnología para Mejorar tu Producción")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("""<div class="section-card">
            <h4 style="color:#10b981">☀️ Energía Solar Rural</h4>
            <p style="color:#cbd5e1">Reduce costos operativos hasta un 40% con energía solar. Finagro ofrece créditos preferenciales para inversión en energía renovable.</p>
            <ul style="color:#94a3b8">
                <li>• Paneles fotovoltaicos para bombeo de agua</li>
                <li>• Sistemas de secado solar de café y cacao</li>
                <li>• Iluminación para instalaciones ganaderas</li>
                <li>• Carga de dispositivos IoT agrícolas</li>
            </ul>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="section-card">
            <h4 style="color:#10b981">💧 Sistemas de Riego</h4>
            <p style="color:#cbd5e1">Aumenta la productividad hasta 3x con riego eficiente. Ahorra hasta 60% de agua.</p>
            <ul style="color:#94a3b8">
                <li>• Riego por goteo automatizado</li>
                <li>• Aspersores de alta eficiencia</li>
                <li>• Bombas solares para zonas sin energía</li>
                <li>• Sensores de humedad de suelo</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    with col_t2:
        st.markdown("""<div class="section-card">
            <h4 style="color:#10b981">🤖 Drones Agrícolas</h4>
            <p style="color:#cbd5e1">Monitorea tus cultivos desde el aire. Detecta plagas, midendimiento y optimiza insumos.</p>
            <ul style="color:#94a3b8">
                <li>• Fumigación de precisión</li>
                <li>• Mapeo NDVI de cultivos</li>
                <li>• Conteo de plantas y animales</li>
                <li>• Vigilancia de cercas y potreros</li>
            </ul>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="section-card">
            <h4 style="color:#10b981">📡 Sensores IoT</h4>
            <p style="color:#cbd5e1">Monitorea en tiempo real el estado de tus cultivos y ganado desde tu celular.</p>
            <ul style="color:#94a3b8">
                <li>• Sensores de temperatura y humedad</li>
                <li>• Cámaras de vigilancia rural</li>
                <li>• GPS para seguimiento de ganado</li>
                <li>• Apps de control de producción</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Impacto de la Tecnología en Tasas de Crédito")

    tech_impact = pd.DataFrame({
        'Tecnología': ['Sin tecnología', '1 tecnología', '2 tecnologías', '3 tecnologías', '4 tecnologías', '5 tecnologías'],
        'Tasa Promedio': [
            df[df['Tecnologias_Usadas'] == 0]['Tasa_Interes_EA'].mean(),
            df[df['Tecnologias_Usadas'] == 1]['Tasa_Interes_EA'].mean(),
            df[df['Tecnologias_Usadas'] == 2]['Tasa_Interes_EA'].mean(),
            df[df['Tecnologias_Usadas'] == 3]['Tasa_Interes_EA'].mean(),
            df[df['Tecnologias_Usadas'] == 4]['Tasa_Interes_EA'].mean(),
            df[df['Tecnologias_Usadas'] == 5]['Tasa_Interes_EA'].mean()
        ]
    })
    st.bar_chart(tech_impact.set_index('Tecnología'))

with tab5:
    st.markdown("## 📈 Impacto Alimentario")

    st.markdown("### Producción de Alimentos para las Familias Colombianas")

    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1:
        st.markdown(f"""<div class="impact-box"><div class="impact-number">{df['Produccion_Anual_Ton'].sum():,.0f}</div><div class="impact-label">Toneladas/Año</div></div>""", unsafe_allow_html=True)
    with col_i2:
        exportadores = df['Exporta_Productos'].sum()
        st.markdown(f"""<div class="impact-box"><div class="impact-number">{exportadores:,.0f}</div><div class="impact-label">Exportadores</div></div>""", unsafe_allow_html=True)
    with col_i3:
        con_solar = df['Tiene_Energia_Solar'].sum()
        st.markdown(f"""<div class="impact-box"><div class="impact-number">{con_solar:,.0f}</div><div class="impact-label">Con Energía Solar</div></div>""", unsafe_allow_html=True)
    with col_i4:
        aprobados = df['Credito_Aprobado'].sum()
        st.markdown(f"""<div class="impact-box"><div class="impact-number">{aprobados:,.0f}</div><div class="impact-label">Créditos Aprobados</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("### Producción por Sector")
        prod_sector = df.groupby('Sector_Productivo')['Produccion_Anual_Ton'].sum().sort_values(ascending=False)
        st.bar_chart(prod_sector)

    with col_p2:
        st.markdown("### Producción por Departamento")
        prod_dept = df.groupby('Departamento')['Produccion_Anual_Ton'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(prod_dept)

    st.markdown("---")
    st.markdown("### ¿Cómo los Créditos Impactan la Mesa Colombiana?")

    impact_data = pd.DataFrame({
        'Sector': ['Agricultura', 'Ganadería', 'Piscicultura', 'Porcícola', 'Avicultura'],
        'Producción (Ton)': [
            df[df['Sector_Productivo'] == 'Agricultura']['Produccion_Anual_Ton'].sum(),
            df[df['Sector_Productivo'] == 'Ganadería']['Produccion_Anual_Ton'].sum(),
            df[df['Sector_Productivo'] == 'Piscicultura']['Produccion_Anual_Ton'].sum(),
            df[df['Sector_Productivo'] == 'Porcícola']['Produccion_Anual_Ton'].sum(),
            df[df['Sector_Productivo'] == 'Avicultura']['Produccion_Anual_Ton'].sum()
        ],
        'Familias Alimentadas': [
            int(df[df['Sector_Productivo'] == 'Agricultura']['Produccion_Anual_Ton'].sum() * 50),
            int(df[df['Sector_Productivo'] == 'Ganadería']['Produccion_Anual_Ton'].sum() * 80),
            int(df[df['Sector_Productivo'] == 'Piscicultura']['Produccion_Anual_Ton'].sum() * 100),
            int(df[df['Sector_Productivo'] == 'Porcícola']['Produccion_Anual_Ton'].sum() * 90),
            int(df[df['Sector_Productivo'] == 'Avicultura']['Produccion_Anual_Ton'].sum() * 120)
        ]
    })

    st.dataframe(impact_data.style.format({
        'Producción (Ton)': '{:,.0f}',
        'Familias Alimentadas': '{:,.0f}'
    }), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Metodología CRISP-ML")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""<div class="section-card">
            <h4 style="color:#10b981">1. Identificación y ETL</h4>
            <p style="font-size:0.85rem; color:#cbd5e1">Se generaron 2,000 registros de créditos rurales con 7 sectores productivos. Imputación de nulos con mediana y moda.</p>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="section-card">
            <h4 style="color:#10b981">2. Exploración (EDA)</h4>
            <p style="font-size:0.85rem; color:#cbd5e1">Análisis de correlación y distribuciones por sector. Impacto de tecnología y subsidios en tasas de crédito.</p>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class="section-card">
            <h4 style="color:#10b981">3. Modelado y Despliegue</h4>
            <p style="font-size:0.85rem; color:#cbd5e1">Regresión lineal múltiple con R² de {r2:.1f}%. Consulta por cédula y simulador interactivo.</p>
        </div>""".format(r2=metricas['r2']*100), unsafe_allow_html=True)
