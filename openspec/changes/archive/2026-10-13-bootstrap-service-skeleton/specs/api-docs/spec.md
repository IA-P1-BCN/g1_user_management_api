# Spec Delta

## Purpose

Garantiza que la documentación interactiva de la API está siempre disponible en todos los entornos, para que cualquier equipo pueda integrarse con el servicio sin leer el código.

## ADDED Requirements

### Requirement: Documentación interactiva siempre activa
El servicio SHALL servir Swagger UI en `/docs` y ReDoc en `/redoc` en todos los entornos.

#### Scenario: Acceso a Swagger UI
- **WHEN** se navega a `/docs`
- **THEN** responde `200` con la interfaz de Swagger UI

#### Scenario: Acceso a ReDoc
- **WHEN** se navega a `/redoc`
- **THEN** responde `200` con la interfaz de ReDoc
