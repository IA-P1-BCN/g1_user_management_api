# Spec Delta

## Purpose

Establece que toda la configuración del servicio proviene del entorno, se valida una sola vez al arranque y falla rápido ante cualquier valor requerido ausente; los secretos nunca viven en el código.

## ADDED Requirements

### Requirement: Configuración por entorno validada al arranque
El servicio SHALL cargar su configuración desde variables de entorno (con soporte de `.env` en local) y MUST fallar al arrancar si falta una variable requerida.

#### Scenario: Variables requeridas presentes
- **WHEN** el servicio arranca con `SECRET_KEY` y `DATABASE_URL` definidas
- **THEN** el arranque completa y la configuración queda validada

#### Scenario: Variable requerida ausente
- **WHEN** el servicio arranca sin `SECRET_KEY`
- **THEN** el arranque falla inmediatamente con un error que nombra la variable ausente

### Requirement: Sin secretos en el código ni en los logs
El servicio MUST mantener los secretos solo en el entorno; los logs y las respuestas de error SHALL no exponer valores de secretos.

#### Scenario: Log de una petición con secretos configurados
- **WHEN** se emite el log de una petición en un servicio con `SECRET_KEY` configurada
- **THEN** el log contiene metadatos de la petición pero nunca el valor del secreto
