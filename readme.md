# README

¡Bienvenido al proyecto!

## Descripción

Este proyecto tiene como objetivo generar datos sintéticos para fines de prueba.

## Instalación

Para instalar el proyecto, siga estos pasos:

1. Clonar el repositorio: `git clone https://github.com/tu-nombre-de-usuario/tu-repo.git`
2. Navegar al directorio del proyecto: `cd tu-repo`
3. Instalar las dependencias: `pip install -r requirements.txt`

## Descripción del Proyecto

Este proyecto tiene como objetivo crear colecciones de datos sintéticos utilizando la biblioteca Faker y datos generados por Ollama. El propósito principal es facilitar la generación de datos realistas para pruebas y desarrollo, permitiendo a los desarrolladores simular diferentes escenarios sin necesidad de utilizar datos reales.

### Características principales:
- **Generación de datos con Faker**: Utiliza la biblioteca Faker para crear datos sintéticos realistas, como nombres, direcciones, números de teléfono, etc.
- **Integración con Ollama**: Genera datos adicionales utilizando la API de Ollama, lo que permite obtener datos más variados y específicos.
- **Traducción automática**: Traduce los datos generados al español utilizando la biblioteca Googletrans.
- **Interfaz gráfica**: Proporciona una interfaz gráfica para facilitar la entrada y edición de datos JSON.
- **Personalización de datos**: Permite seleccionar y editar claves específicas del JSON para generar datos personalizados.
- **Almacenamiento de resultados**: Guarda los datos generados en archivos JSON para su posterior uso.
- **Ejecución automatizada**: Modifica y ejecuta automáticamente el código generado para producir los datos sintéticos.

Este proyecto es ideal para desarrolladores que necesitan datos de prueba realistas y variados para sus aplicaciones, sin comprometer la privacidad ni la seguridad de los datos reales.

## Uso

Para utilizar este proyecto, siga los siguientes pasos:

1. Ejecute el script `main.py`.
2. Se abrirá una ventana donde deberá pegar un JSON correctamente estructurado en el formato `{clave1:valor1, clave2:valor2, ...}`.
3. Seleccione las claves para las cuales desea generar datos y edite los valores según sea necesario.
4. Especifique las relaciones entre las claves seleccionadas y el número de elementos que desea generar para cada clave.
5. El programa generará los datos realizando solicitudes a la API de Ollama y los traducirá al español automáticamente.
6. El programa extraerá las claves que se generarán con Faker y las variables que contienen los datos para las claves seleccionadas.
7. El programa generará funciones con Faker utilizando los datos proporcionados por Ollama.
8. El programa modificará el archivo `code.txt`, que sirve como plantilla para generar datos, y lo completará con las funciones de Faker y las variables generadas.
9. Finalmente, el programa ejecutará el archivo `code_to_execute.py` para generar los datos sintéticos finales.

