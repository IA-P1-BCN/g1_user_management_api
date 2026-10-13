# service-health Specification

## Purpose
Define los endpoints de liveness y readiness que permiten a cualquier plataforma (local, CI, contenedor, nube) saber si el proceso del servicio está vivo y si sus dependencias están operativas.

## Requirements

### Requirement: Endpoint de liveness
El servicio SHALL exponer `GET /health` que indica si el proceso está vivo, sin depender de la base de datos.

#### Scenario: Servicio arrancado
- **WHEN** se llama a `GET /health` con el servicio en marcha
- **THEN** responde `200` con un JSON que refleja el estado del servicio

#### Scenario: Base de datos caída
- **WHEN** se llama a `GET /health` con la base de datos inaccesible
- **THEN** sigue respondiendo `200`, porque el liveness no depende de la base de datos

### Requirement: Endpoint de readiness
El servicio SHALL exponer `GET /ready` que verifica la conectividad con la base de datos antes de declararse listo.

#### Scenario: Base de datos accesible
- **WHEN** se llama a `GET /ready` con la base de datos accesible
- **THEN** responde `200` con un JSON que refleja el estado de la dependencia

#### Scenario: Base de datos inaccesible
- **WHEN** se llama a `GET /ready` con la base de datos inaccesible
- **THEN** responde `503` con un JSON que identifica la dependencia caída
