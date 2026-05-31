# AgroCrédito Colombia - Seguridad Alimentaria 🌾

[![Python](https://img.shields.io/badge/python-3.10+-green?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![CRISP-ML](https://img.shields.io/badge/Metodolog%C3%ADa-CRISP--ML-blue?style=flat-square)](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**AgroCrédito Colombia** es una plataforma de inteligencia artificial diseñada para transformar el campo colombiano. Usa Machine Learning para predecir tasas de crédito justas, conecta agricultores con subsidios gubernamentales, y promueve la tecnología rural para garantizar la **seguridad alimentaria** de Colombia y del mundo.

---

## 🎯 Objetivos del Proyecto

1. **Volver al Campo**: Incentivar a los colombianos, especialmente jóvenes, a regresar al campo para cultivar.
2. **Créditos Justos**: Usar IA para predecir tasas de interés personalizadas y accesibles.
3. **Tecnología Rural**: Promover energía solar, riego inteligente, drones y sensores IoT.
4. **Seguridad Alimentaria**: Aumentar la producción de alimentos para las mesas colombianas y la exportación.
5. **Economía Joven**: Crear oportunidades económicas viables en el sector agropecuario.

---

## 📊 Sectores Productivos

| Sector | Productos | Tecnología Asociada |
|--------|-----------|---------------------|
| 🌱 Agricultura | Café, cacao, arroz, frutas, hortalizas | Riego, drones, sensores |
| 🐄 Ganadería | Leche, carne bovina, ovina | GPS, apps de monitoreo |
| 🐟 Piscicultura | Tilapia, trucha, camarón | Sistemas de control |
| 🐷 Porcícola | Cerdo, lechón | Automatización |
| 🐔 Avicultura | Pollo, huevo, pavo | Sensores ambientales |
| ☀️ Energía Solar | Placas, bombas solares | IoT |
| 🤖 Tecnología Agrícola | Drones, riego, sensores | IA y monitoreo |

---

## 🧠 Modelo de Machine Learning

- **Algoritmo**: Regresión Lineal Múltiple
- **R²**: 89.2%
- **MAE**: 0.75 puntos porcentuales
- **Variable objetivo**: Tasa de interés E.A.
- **11 variables predictoras**: Edad, experiencia, hectáreas, ingresos, monto, plazo, garantía, subsidio, tecnologías, energía solar, riego

### Impacto de Coeficientes

| Variable | Efecto en Tasa |
|----------|----------------|
| Subsidio LEC Finagro | -4.34% E.A. |
| Garantía FAG | -2.36% E.A. |
| Energía Solar | -0.69% E.A. |
| Tecnologías | -0.35% E.A. por tech |
| Experiencia | -0.04% E.A. por año |
| Plazo | +0.02% E.A. por mes |

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar pipeline completo
```bash
python generate_data.py    # Genera dataset de 2,000 registros
python run_etl.py          # Limpia y prepara datos
python run_modeling.py     # Entrena modelo y guarda .pkl
```

### 3. Lanzar la plataforma
```bash
streamlit run app.py --server.port 8510
```

### 4. Abrir Landing Page
Abre `index.html` en tu navegador para ver la landing page interactiva.

---

## 📁 Estructura del Proyecto

```
proyecto_ml_crisp/
├── data/
│   ├── creditos_rurales.csv           # Dataset original (2,000 registros)
│   └── creditos_rurales_limpio.csv    # Dataset limpio
├── 01_ETL_Preparation.ipynb           # ETL y limpieza
├── 02_EDA_Exploration.ipynb           # Análisis exploratorio
├── 03_Model_Evaluation.ipynb          # Modelado y evaluación
├── app.py                             # App Streamlit (puerto 8510)
├── dashboard_avanzado.html            # Dashboard interactivo
├── generate_data.py                   # Generador de datos
├── run_etl.py                         # Script ETL
├── run_modeling.py                    # Script de modelado
├── model_utils.py                     # Funciones utilitarias
├── modelo_creditos.pkl                # Modelo serializado
├── index.html                         # Landing page
├── requirements.txt                   # Dependencias
└── README.md                          # Documentación
```

---

## 🌾 Call to Action

> **"Volvamos al campo. Cultivemos nuestro futuro. Alimentemos a Colombia."**

La plataforma AgroCrédito Colombia es una invitación a todos los colombianos a:
- **Consultar su crédito** con solo su cédula
- **Adoptar tecnología** para producir más y mejor
- **Exportar** productos colombianos al mundo
- **Garantizar** la seguridad alimentaria de nuestras familias

---

*Desarrollado con fines educativos y de impacto social. Licencia MIT.*
