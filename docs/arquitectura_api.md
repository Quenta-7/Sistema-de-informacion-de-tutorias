/api
│── app.py                 # Punto de entrada
│── config.py              # Configuración general
│── /routes                # Blueprints de rutas
│     ├── user_routes.py
│     ├── auth_routes.py
│── /controllers           # Lógica de endpoints
│     ├── user_controller.py
│     ├── auth_controller.py
│── /models                # Modelos de base de datos
│     ├── user_model.py
│── /services              # Lógica reutilizable
│     ├── user_service.py
│── /database
│     ├── db.py            # Inicialización de la base de datos

