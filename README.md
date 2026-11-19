# Hostel Melimer

Sistema de gestión de un hostel desarrollado en Python. Permite administrar reservas, clientes y habitaciones, consultar reportes y generar comprobantes en PDF. Incluye una interfaz gráfica con CustomTkinter y una interfaz por consola.

## Funcionalidades

### Administración y seguridad

- Inicio de sesión obligatorio para abrir la interfaz gráfica.
- Usuario administrador fijo.
- Contraseña protegida mediante hash SHA-256.
- Acceso mediante contraseña visible u oculta.
- Cierre de sesión que vuelve a mostrar la pantalla de acceso.

### Reservas

- Crear, listar, editar y cancelar reservas.
- Reprogramar reservas canceladas.
- Buscar reservas por DNI.
- Filtrar por habitación, rango de fechas y estado.
- Buscar reservas combinando varios filtros.
- Ingresar fechas manualmente o seleccionarlas desde el calendario.
- Verificar disponibilidad por fechas y cantidad de huéspedes.
- Generar y abrir comprobantes PDF.
- Impedir reservas solapadas en una misma habitación.
- Impedir editar reservas canceladas, finalizadas o ya iniciadas.

### Clientes

- Registrar, buscar, editar y listar clientes.
- Buscar por nombre, DNI o teléfono.
- Filtrar por estado: activo o dado de baja.
- Dar de baja o restaurar clientes.
- Impedir dar de baja a un cliente con reservas vigentes.
- Consultar el historial de reservas de cada cliente.

### Habitaciones

- Consultar el inventario de habitaciones.
- Buscar por número y filtrar por estado.
- Consultar disponibilidad según capacidad y fechas.
- Modificar precio y estado de mantenimiento.
- Impedir poner en mantenimiento una habitación con reservas vigentes o futuras.

### Reportes

- Llegadas del día.
- Clientes frecuentes.
- Habitación más reservada.
- Habitación con mayor facturación.
- Ingresos totales.
- Ocupación actual.

## Tecnologías

- Python.
- CustomTkinter.
- tkcalendar.
- ReportLab.
- Pillow.
- Archivos JSON para persistencia.

## Requisitos

- Python 3.10 o superior.
- Tkinter disponible en la instalación de Python.
- Sistema operativo Windows recomendado para la apertura e impresión de PDF.

## Instalación

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

## Ejecución

### Interfaz gráfica

```bash
python frontend_main.py
```

Al abrir el programa, aparece primero el inicio de sesión. Luego de autenticar al administrador, se carga la ventana principal con el dashboard, reservas, clientes, habitaciones y reportes.

### Acceso inicial

```text
Usuario: admin
Contraseña: admin123
```

Estas credenciales corresponden al administrador fijo del sistema. No existe registro público de usuarios.

La implementación utiliza SHA-256 para el trabajo académico. Para un entorno de producción se recomendaría reemplazarla por una biblioteca como `bcrypt` o `argon2`, que incorpora sal y una protección más adecuada para contraseñas.

### Interfaz por consola

```bash
python main.py
```

La interfaz por consola ofrece menús independientes para reservas, clientes, habitaciones y reportes.

## Datos

La información se almacena en archivos JSON dentro de la carpeta `data`:

```text
data/
├── customers.json
├── reservations.json
├── rooms.json
└── receipts/
```

- `customers.json`: clientes registrados y su estado.
- `reservations.json`: reservas, fechas, huéspedes, habitaciones, importes y estado.
- `rooms.json`: inventario, capacidad, precio y mantenimiento.
- `receipts/`: comprobantes PDF generados por la interfaz gráfica.

Los JSON usan archivos temporales y reemplazo atómico para reducir el riesgo de dejar un archivo corrupto si ocurre un error durante el guardado.

## Estructura principal

```text
TPFinal/
├── frontend_main.py
├── main.py
├── requirements.txt
├── README.md
├── data/
├── frontend/
│   ├── app.py
│   ├── auth/
│   │   ├── admin_auth.py
│   │   └── login.py
│   ├── assets/
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

- DNI de 8 dígitos numéricos.
- Teléfono de 9 dígitos numéricos.
- Nombre con contenido alfabético válido.
- Fechas válidas en formato `dd/mm/yyyy`.
- Check-in hoy o posterior.
- Check-out posterior al Check-in.
- Cantidad de huéspedes entre 1 y 4.
- Disponibilidad real antes de confirmar una reserva.
- Evita solapamientos de reservas en una misma habitación.
- Impide dar de baja a un cliente con reservas vigentes.
- Impide mantener habitaciones que tengan reservas vigentes o futuras.
- Impide editar reservas canceladas, finalizadas o ya iniciadas.
- Escrituras JSON validadas y guardadas de forma atómica.

## Comprobación del código

Para compilar todos los archivos Python y detectar errores sintácticos:

```bash
python -m compileall -q .
```

## Estado de alcance

El sistema incluye acceso administrativo, gestión completa de clientes y reservas, gestión de habitaciones, filtros, reportes y comprobantes PDF.

Como mejoras futuras podrían incorporarse:

- Contraseñas con `bcrypt` o `argon2`.
- Registro y administración de múltiples usuarios.
- Alta de nuevas habitaciones.
- Fecha de inicio y fin para mantenimientos temporales.
- Pruebas automatizadas con `pytest`.

## Autor

Proyecto realizado para la asignatura Fundamentos de la Programación.
