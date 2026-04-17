# 🚀 ESP32 Hardware Monitor

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++ Badge"/>
  <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License Badge"/>
</div>

<p align="center">🌐 <b><a href="README.md">English</a> | <a href="README_es.md">Español</a></b></p>

<br>

> **👋 ¡Bienvenido!** Este es mi primer gran proyecto de programación. Lo construí para aprender, resolver un problema personal y, con suerte, compartir algo genial con la comunidad. ¡Cualquier comentario, sugerencia y "pull request" son muy recomendados y apreciados!
<br>

<div align="center">
  <img src="assets/Data.jpg" alt="Screen Layout Data" width="650"/>
</div>

### 📊 Detalles del Diseño de Pantalla

La interfaz de pantalla está estructurada en componentes **Fijos** y **Modificables** para proporcionar una experiencia consistente pero profundamente personalizable:

- 🟢 **Componentes Fijos:** Todo, desde el vataje (W) de la CPU y la GPU hacia arriba, está mapeado de forma permanente. Esto incluye las temperaturas de la CPU y la GPU, el contador de FPS, los medidores de carga de la CPU y la GPU, y los límites de vataje de la CPU/GPU. El **reloj en tiempo real** en la esquina inferior derecha también es fijo.
- 🛠️ **Espacios Modificables:** Los espacios para mostrar texto ubicados *debajo* del vataje de la CPU y la GPU (con la excepción del reloj) ¡son totalmente personalizables! Puedes mapear estos 6 espacios para mostrar cualquier dato del sensor de hardware de LHM que desees (como la RAM, VRAM, RPM del ventilador del gabinete o velocidades de red) utilizando la aplicación Configurador.

<br>

<div align="center">
  <img src="assets/preview.jpg" alt="ESP32 Hardware Monitor Presentation" width="650"/>
</div>

<br>

Un ecosistema independiente y altamente receptivo para monitorear los signos vitales del hardware de tu PC directamente a través de una pantalla TFT ESP32. Mantente al tanto de las métricas esenciales de tu sistema (temperaturas, vataje, carga, RPM y FPS) en tiempo real sin ocupar un valioso espacio en el monitor de tu PC.

Este proyecto une a la perfección los sensores de hardware de tu PC con tu pantalla externa ESP32 utilizando un agente de Windows nativo, ligero y en segundo plano, y una robusta comunicación Serial sobre USB.

---

## ✨ Características

- **Agente de Windows Discreto:** Una aplicación silenciosa en la bandeja del sistema que lee métricas en tiempo real de forma nativa a través de la API de LibreHardwareMonitor.
- **Mapeo Dinámico de Sensores:** Incluye un Configurador GUI incorporado (accesible desde la bandeja del sistema) que te permite mapear cualquier sensor de hardware (CPU, GPU, RAM, Red, Ventiladores, etc.) a los espacios de tu pantalla ESP32.
- **Profunda Integración de Hardware:** Analiza y captura datos MSR, desde la temperatura de la CPU, uso de energía del paquete, hasta la tasa de fotogramas (FPS) en pantalla completa de DirectX, utilizando "hooks" dinámicos avanzados.
- **Configuración Automática Inteligente:** Escanea y se conecta al puerto COM del Arduino objetivo automáticamente al instante. ¡No se necesita configuración manual del puerto serie!
- **Gráficos e Interfaz Elegantes:** Una interfaz TFT hermosa y receptiva diseñada a través de SquareLine Studio, impulsada por el motor gráfico estándar de la industria LVGL.
- **Automatizaciones Silenciosas:** Menús integrados en la bandeja del sistema para manipular las tasas de actualización de datos e integrarse perfectamente con el Programador de Tareas de Windows para un inicio automático e invisible en el arranque.

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalados y configurados los siguientes elementos:
- **Hardware:** Una placa de desarrollo ESP32 con una pantalla TFT compatible.
  - *Nota: Este proyecto fue desarrollado y probado específicamente en la placa **ESP32-2432S028R** utilizando el controlador de pantalla **ILI9341**.*
- **Dependencias de Software:**
  - [Arduino IDE](https://www.arduino.cc/en/software) (para compilar/cargar el código ESP32).
  - Python 3.13 o anterior (si se ejecuta desde el código fuente).
  - ESP32 Board Manager instalado en Arduino IDE.

## 📂 Instalación y Configuración

### 1. Firmware del Hardware (ESP32)

Debido a las diferentes configuraciones de pines ("pinout") en las distintas placas de desarrollo ESP32, debes compilar el firmware directamente usando Arduino IDE para asegurar la compatibilidad.

1. Descarga **`ESP32_Firmware.zip`** desde la pestaña **Releases** más reciente en GitHub y extráelo. (Alternativamente, puedes clonar o descargar el código fuente de este repositorio).
2. Abre Arduino IDE.
3. Carga el firmware `.ino` ubicado en la carpeta extraída `ESP32`.
4. Selecciona tu placa ESP32 específica y verifica la configuración de tus pines si es necesario.
5. Selecciona el puerto COM de tu placa.
6. Haz clic en **Upload (Subir)** para compilar y flashear el firmware.

### 2. Configuración del Software (Windows)
Puedes instalar la aplicación mediante el asistente de configuración, ejecutarla como un ejecutable portátil o compilarla tú mismo desde el código fuente.

**Opción A: Usar el Instalador (Recomendado)**
1. Descarga `ESP32_Hardware_Monitor_Setup.exe` desde la pestaña **Releases** en GitHub (o ejecútalo desde el directorio `Software\Installer Output`).
2. Ejecuta el instalador para elegir la ubicación de instalación y crear automáticamente accesos directos en el escritorio.
3. Inicia la aplicación desde tu Escritorio o Menú Inicio.
   > **Nota:** Solicitará privilegios de Administrador una vez para comunicarse de manera segura con el controlador proxy de kernel `PawnIO` necesario para el mapeo térmico de AMD/Intel.

**Opción B: Usar el Ejecutable Portátil**
1. Descarga `ESP32 Hardware Monitor.exe` desde la pestaña **Releases** en GitHub (o ejecútalo desde el directorio `Software\ESP32 HWM`).
2. Ejecuta `ESP32 Hardware Monitor.exe`. 
   > **Nota:** Solicitará privilegios de Administrador una vez, de forma similar al instalador.

**Opción C: Compilar desde el Código Fuente**
1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/RD-MN/ESP32_HardwareMonitor.git
   ```
2. Ejecuta `Software\BuildExec.bat`. Este script compilará el código fuente de Python (`LHMToSerial.py`) en un archivo independiente `ESP32 Hardware Monitor.exe` usando PyInstaller.

## 🚀 Uso

Una vez flasheado el hardware y ejecutándose el agente de Windows:
1. Conecta tu ESP32 a tu PC vía USB.
2. La aplicación de Windows detectará automáticamente el ESP32 y comenzará a transmitir datos.
3. **Integración en la Bandeja del Sistema:** Busca el ícono de ESP32 Hardware Monitor en la bandeja de la barra de tareas de Windows (íconos ocultos).
4. **Haz clic derecho en el ícono** para acceder a funciones clave:
   - **Abrir Configuraciones ESP32HWM**: Abre la aplicación Configurador integrada para personalizar tu pantalla, seleccionando fácilmente qué sensores de hardware aparecen en los 6 espacios de la pantalla.
   - Ajustar las **Tasas de Actualización (Refresh Rates)**.
   - Habilitar/Deshabilitar **Ejecutar al Inicio (Run on Startup)** para una experiencia de arranque automática e invisible.

## 🤝 Contribuir

¡Las contribuciones, problemas (issues) y solicitudes de funciones son bienvenidos! Como es mi primer gran proyecto, me encantaría recibir comentarios o *pull requests* para ayudar a mejorar el código.

1. Haz un Fork del proyecto
2. Crea tu rama para la nueva función (`git checkout -b feature/NuevaFuncionIncreible`)
3. Haz un commit con tus cambios (`git commit -m 'Agregar NuevaFuncionIncreible'`)
4. Empuja el código a tu rama (`git push origin feature/NuevaFuncionIncreible`)
5. Abre un Pull Request

## ⚠️ Descargo de Responsabilidad

Este es un proyecto personal por hobby y parte del desarrollo fue asistido por **Antigravity AI**. Aunque se ha hecho un gran esfuerzo para asegurar la estabilidad, siempre existe la posibilidad de bugs, errores no controlados o casos límite. Por favor, úsalo a tu propia discreción. ¡No dudes en abrir un *issue* si encuentras algún comportamiento extraño!

## Licencias

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

### Licencias de Terceros

- [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) - [Mozilla Public License 2.0 (MPL-2.0)](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/blob/master/LICENSE)
- [LVGL](https://lvgl.io/) - [Licencia MIT](https://github.com/lvgl/lvgl/blob/master/LICENCE.txt)
- [Paquetes de Arduino Core](https://www.arduino.cc/) - [LGPL](https://www.gnu.org/licenses/lgpl-2.1.html)
