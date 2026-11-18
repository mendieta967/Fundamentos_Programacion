# Hostel Melimer

Sistema de gestion de un hostel desarrollado en Python. Permite administrar reservas, clientes y habitaciones, consultar reportes y generar comprobantes en PDF. Incluye una interfaz grafica con CustomTkinter y una interfaz por consola.

## Funcionalidades

- Gestion de reservas:
  - Crear, listar, buscar, editar y cancelar reservas.
  - Reprogramar reservas canceladas.
  - Verificar disponibilidad de habitaciones por fechas y cantidad de huespedes.
  - Generar comprobantes de reserva en PDF.
- Gestion de clientes:
  - Registrar, buscar, editar y dar de baja o restaurar clientes.
  - Consultar el historial de reservas de cada cliente.
- Gestion de habitaciones:
  - Consultar habitaciones disponibles.
  - Buscar habitaciones por numero.
  - Modificar precio y estado de mantenimiento.
- Reportes:
  - Llegadas del dia.
  - Clientes frecuentes.
  - Habitacion mas reservada.
  - Habitacion con mayor facturacion.
  - Ingresos totales.
  - Ocupacion actual.

## Tecnologias

- Python
- CustomTkinter
- tkcalendar
- ReportLab
- Pillow
- Archivos JSON para persistencia

## Requisitos

- Python 3.10 o superior.
- Tkinter disponible en la instalacion de Python.
- Sistema operativo Windows recomendado para la apertura e impresion de PDF.

## Instalacion

Desde una terminal ubicada en la carpeta del proyecto:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecucion

### Interfaz grafica

```bash
python frontend_main.py
```

El punto de entrada crea la ventana principal de Hostel Melimer y carga las vistas de dashboard, reservas, clientes, habitaciones y reportes.

### Interfaz por consola

```bash
python main.py
```

La interfaz por consola ofrece menus para reservas, clientes, habitaciones y reportes.

## Datos

La informacion se almacena en archivos JSON dentro de la carpeta `data`:

```text
data/
├── customers.json
├── reservations.json
├── rooms.json
└── receipts/
```

- `customers.json`: clientes registrados y su estado.
- `reservations.json`: reservas, fechas, importes y estado.
- `rooms.json`: inventario, capacidad, precio y mantenimiento.
- `receipts/`: comprobantes PDF generados por la interfaz grafica.

Las escrituras utilizan archivos temporales y reemplazo atomico para reducir el riesgo de dejar archivos JSON corruptos si ocurre un error durante el guardado.

## Estructura principal

```text
TPFinal/
├── frontend_main.py
├── main.py
├── requirements.txt
├── data/
├── frontend/
│   ├── app.py
│   ├── components/
│   ├── dialogs/
│   ├── pdf/
│   ├── validators/
│   └── views/
├── modules/
│   ├── clients/
│   ├── reports/
│   ├── reservations/
│   ├── room_views/
│   ├── rooms.py
│   └── validations.py
└── storage/
    └── json_storage.py
```

## Validaciones importantes

- DNI de 8 digitos numericos.
- Telefono de 9 digitos numericos.
- Fechas validas en formato `dd/mm/yyyy`.
- Check-in anterior al check-out.
- Cantidad de huespedes entre 1 y 4.
- Evita solapamientos de reservas en una misma habitacion.
- Impide que una habitacion tenga estado de mantenimiento si posee reservas vigentes o futuras.
- Impide dar de baja a un cliente con reservas vigentes.
- Impide editar reservas canceladas, finalizadas o ya iniciadas.

## Comprobacion del codigo

Para compilar todos los archivos Python y detectar errores sintacticos:

```bash
python -m compileall -q .
```

## Autores

Proyecto realizado para la asignatura Fundamentos de la Programacion.
