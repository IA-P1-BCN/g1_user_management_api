# observability Specification

## Purpose
Establece el logging estructurado del servicio: todo log es JSON parseable y cada petición HTTP queda registrada con los metadatos necesarios para depurar y auditar.

## Requirements

### Requirement: Logging estructurado en JSON
El servicio SHALL emitir sus logs en formato JSON con nivel, mensaje y marca temporal.

#### Scenario: El servicio emite un log
- **WHEN** el servicio emite cualquier mensaje de log
- **THEN** la salida es una línea JSON parseable con nivel, mensaje y marca temporal

### Requirement: Log de petición HTTP con metadatos
El servicio MUST registrar cada petición HTTP con un identificador único de petición, la ruta, el código de estado y la duración.

#### Scenario: Petición HTTP atendida
- **WHEN** el servicio atiende una petición HTTP
- **THEN** se emite un log JSON con request id, ruta, estado y duración

#### Scenario: Log sin datos sensibles
- **WHEN** se registra el log de una petición
- **THEN** no contiene secretos ni datos personales de usuarios
