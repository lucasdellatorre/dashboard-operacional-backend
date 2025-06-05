-- Tabela IP
DROP TABLE IF EXISTS ip CASCADE;

CREATE TABLE ip (
    id SERIAL PRIMARY KEY,
    internal_ticket_number VARCHAR(255) NOT NULL,
    ip VARCHAR(255) NOT NULL,
    versao VARCHAR(50) NOT NULL,
    numero_id INTEGER NOT NULL,
    data VARCHAR(50),
    hora VARCHAR(50),
    timestamp TIMESTAMP
);

INSERT INTO ip (internal_ticket_number, ip, versao, numero_id, data, hora, timestamp)
VALUES
('ticket-001', '192.168.0.1', 'v1', 10, '2025-06-05', '14:00', NOW()),
('ticket-002', '10.0.0.1', 'v1', 11, '2025-06-05', '14:30', NOW());

-- Tabela MENSAGEM
DROP TABLE IF EXISTS mensagem CASCADE;

CREATE TABLE mensagem (
    id SERIAL PRIMARY KEY,
    internal_ticket_number VARCHAR(255) NOT NULL,
    grupo_id VARCHAR(255) NOT NULL,
    numero_id INTEGER NOT NULL,
    remetente VARCHAR(255),
    remetente_ip VARCHAR(255),
    remetente_dispositivo VARCHAR(255),
    tipo_mensagem VARCHAR(50),
    estilo_mensagem VARCHAR(50),
    tamanho_mensagem VARCHAR(50),
    data VARCHAR(50),
    hora VARCHAR(50),
    timestamp TIMESTAMP,
    destinatario VARCHAR(255),
    message_external_id VARCHAR(255),
    remetente_porta VARCHAR(50)
);

-- Mensagens associadas aos IPs inseridos acima
INSERT INTO mensagem (
    internal_ticket_number, grupo_id, numero_id, remetente_ip, destinatario, timestamp
) VALUES
('ticket-001', 'grupo1', 10, '192.168.0.1', '5511999999999', NOW()),
('ticket-001', 'grupo1', 10, '192.168.0.1', '5511999999999', NOW()),
('ticket-001', 'grupo1', 10, '192.168.0.1', '5511999999999', NOW()),
('ticket-001', 'grupo1', 10, '192.168.0.1', '5511999999999', NOW()),
('ticket-002', 'grupo2', 11, '10.0.0.1', '5511888888888', NOW()),
('ticket-002', 'grupo2', 11, '10.0.0.1', '5511888888888', NOW());
