# Calculadora Chile API

API REST para calcular variaciones del IPC de Chile y reajustar montos asociados a arriendos, sueldos e inflacion. El proyecto fue desarrollado como una solucion backend pequena, clara y facil de consumir desde otros sistemas.

**Estado:** desplegado en Render.

## Proposito

La API permite consultar una variacion porcentual entre dos periodos disponibles y aplicar ese porcentaje a un monto inicial. El caso de uso principal es automatizar calculos que suelen realizarse manualmente en contextos financieros, laborales y de contratos de arriendo.

El proyecto tambien incluye una interfaz de consola para ejecutar las calculadoras localmente.

## Funcionalidades

- Calculo de variacion del IPC entre dos fechas.
- Reajuste de montos de arriendo.
- Reajuste de sueldos.
- Calculo de inflacion y monto actualizado.
- Validacion de fechas y rangos de consulta.
- Proteccion de endpoints mediante API key.
- Persistencia local de los datos del IPC en formato JSON.
- Modulo preparado para actualizar datos desde el Banco Central de Chile.
- Documentacion interactiva generada por FastAPI.

## Tecnologia utilizada

- **Python:** lenguaje principal.
- **FastAPI:** framework para construir la API REST y su documentacion OpenAPI.
- **Pydantic:** validacion y modelado de los datos de entrada.
- **Uvicorn:** servidor ASGI para ejecutar la aplicacion.
- **python-dotenv:** carga de variables de entorno en desarrollo local.
- **bcchapi:** integracion con datos del Banco Central de Chile.
- **JSON:** almacenamiento de los periodos y valores del IPC.
- **Render:** plataforma de despliegue de la API.

## Estructura del proyecto

```text
.
├── api.py              # Aplicacion FastAPI y endpoints
├── calculations.py     # Logica de variacion y reajuste de montos
├── data_manager.py     # Lectura de data/ipc.json
├── formats.py          # Formateo de valores para la CLI
├── main.py             # Interfaz de consola
├── menus.py            # Menus y entradas de la CLI
├── requirements.txt    # Dependencias del proyecto
├── update_ipc.py       # Integracion para actualizar datos del IPC
├── validations.py      # Validaciones usadas por la CLI
└── data/ipc.json       # Datos historicos del IPC
```

## API

Todos los endpoints requieren el header `X-API-Key`.

### `POST /ipc`

Calcula la variacion porcentual entre dos periodos.

```json
{
  "fecha_inicio": "2023-01-01",
  "fecha_fin": "2024-01-01"
}
```

Respuesta:

```json
{
  "variacion": 3.2
}
```

### `POST /arriendo`

Calcula el monto de arriendo reajustado.

```json
{
  "fecha_inicio": "2023-01-01",
  "fecha_fin": "2024-01-01",
  "monto": 500000
}
```

Respuesta:

```json
{
  "variacion": 3.2,
  "monto_original": 500000,
  "monto_reajustado": 516000
}
```

### `POST /sueldo`

Usa el mismo formato de entrada que `/arriendo` y devuelve el sueldo reajustado.

### `POST /inflacion`

Usa el mismo formato de entrada que `/arriendo` y devuelve la inflacion y el monto actualizado.

## Ejemplo de consumo

```bash
curl -X POST "https://api.calculoschile.cl/ipc" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: TU_API_KEY" \
  -d '{"fecha_inicio":"2023-01-01","fecha_fin":"2024-01-01"}'
```

La documentacion interactiva queda disponible en:

- `https://api.calculoschile.cl/docs`
- `https://api.calculoschile.cl/redoc`

## Configuracion local

Requisitos: Python 3.10 o superior.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear un archivo `.env` local con variables propias:

```dotenv
API_KEY=una-clave-local-segura
BCCH_TOKEN=un-token-del-banco-central
```

Iniciar la API:

```bash
uvicorn api:app --reload
```

La API local queda disponible en `http://127.0.0.1:8000`.

Para ejecutar la interfaz de consola:

```bash
python main.py
```

## Despliegue en Render

La API se despliega como un servicio web de Python en Render.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
- **Variables de entorno:** `API_KEY` y `BCCH_TOKEN`

Las variables sensibles deben configurarse en el panel de Render y no deben subirse al repositorio. El archivo `.env` esta excluido mediante `.gitignore`; para documentar la configuracion puede utilizarse un `.env.example` sin valores reales.

## Seguridad

- Los endpoints validan la API key recibida en `X-API-Key`.
- Las credenciales se gestionan mediante variables de entorno.
- Los archivos `.env`, claves privadas, certificados, credenciales y artefactos locales estan excluidos del control de versiones.
- Antes de publicar el proyecto, las credenciales expuestas accidentalmente deben revocarse y regenerarse.

## Autor

Proyecto desarrollado por Sebastian en Kernel Labs como ejercicio practico de desarrollo backend, integracion de datos y despliegue cloud.
