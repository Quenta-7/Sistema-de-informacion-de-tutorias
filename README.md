# 📘 Sistema de Información de Tutorías

Sistema de información de tutorías para la Escuela Profesional de Ingeniería Informática y de Sistemas de la Universidad Nacional de San Antonio Abad del Cusco.

Este sistema tiene como propósito digitalizar y gestionar los procesos de tutoría académica, personal y profesional, facilitando la comunicación entre tutores, administradores y verificadores, y asegurando un seguimiento integral del estudiante.

---

## 🧩 REQUERIMIENTOS

### 1. REQUERIMIENTOS FUNCIONALES

**RF1.** El sistema debe permitir al **administrador** crear, modificar y eliminar **cronogramas de tutorías** por semestre académico.  
**RF2.** El sistema debe permitir al **administrador** asignar tutorados a tutores y cambiar asignaciones según necesidad.  
**RF3.** El sistema debe permitir al **tutor** registrar información de tutorías **académicas, personales y profesionales** de cada estudiante.  
**RF4.** El sistema debe permitir al **tutor** generar e imprimir una **constancia de tutoría** para el tutorado.  
**RF5.** El sistema debe permitir al **verificador** consultar tutorías por **tipo, fecha, tutor y estudiante**, en diferentes semestres.  
**RF6.** El sistema debe permitir al **administrador** visualizar reportes históricos de las tutorías de cada estudiante.  
**RF7.** El sistema debe permitir al **usuario autenticarse** con credenciales únicas según su rol (administrador, tutor o verificador).  
**RF8.** El sistema debe permitir **subir archivos digitales** del seguimiento académico del estudiante.  
**RF9.** El sistema debe permitir **filtrar y exportar reportes** en formato PDF o Excel.  
**RF10.** El sistema debe registrar **todas las acciones críticas** en un log de auditoría (creación, modificación o eliminación de datos).

---

### 2. REQUERIMIENTOS NO FUNCIONALES

**RNF1.** El sistema debe garantizar la **seguridad y confidencialidad** de la información almacenada, especialmente la de los estudiantes.  
**RNF2.** El sistema debe estar disponible el **99% del tiempo** durante el semestre académico.  
**RNF3.** El sistema debe ser **accesible desde navegadores web modernos** (Chrome, Edge, Firefox).  
**RNF4.** El sistema debe tener una **interfaz responsiva y fácil de usar**, compatible con dispositivos móviles.  
**RNF5.** Las operaciones de carga y visualización deben completarse en un **tiempo menor a 3 segundos** bajo condiciones normales.  
**RNF6.** El sistema debe implementar **control de versiones** en GitHub o Azure DevOps para garantizar trazabilidad.  
**RNF7.** El sistema debe estar desarrollado bajo la **metodología ágil Scrum**, documentando sprints y retrospectivas.  
**RNF8.** La base de datos debe permitir **copias de seguridad automáticas** y recuperación ante fallos.  
**RNF9.** El sistema debe estar desarrollado en **lenguaje Python (Flask)** con base de datos **MySQL o PostgreSQL**.  
**RNF10.** El sistema debe cumplir con los **estándares de codificación y documentación** definidos por el equipo de desarrollo.

---

## 👥 ROLES DEL SISTEMA
- **Administrador:** Gestiona cronogramas, asignaciones y reportes.  
- **Tutor:** Registra y actualiza la información de tutorías.  
- **Verificador:** Supervisa y consulta el estado de las tutorías realizadas.

---

## ⚙️ TECNOLOGÍAS SUGERIDAS
- **Backend:** Python (Flask)  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap o Tailwind  
- **Base de Datos:** MySQL / PostgreSQL  
- **Control de Versiones:** GitHub / Azure DevOps  
- **Diseño de Interfaz:** Figma / Adobe XD / Gimp  

---

## 📅 METODOLOGÍA
El desarrollo se organiza en **sprints** de dos semanas bajo la metodología **Scrum**, entregando incrementos funcionales en cada iteración.  
Los roles incluyen: *Product Owner*, *Scrum Master*, *Development Team*, *Quality Assurance*, *UX/UI Designer* y *DevOps Engineer*.

---

## 🧠 AUTORES
**Equipo de Desarrollo:**  
- José Francisco Quentasi Juachin  
- Hernan Washintong Ramos Alata  

**Docente:**  
- Ing. Carlos Ramon Quispe Onofre 

---

© 2025 Universidad Nacional de San Antonio Abad del Cusco – Escuela Profesional de Ingeniería Informática y de Sistemas
