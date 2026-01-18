"""
Módulo central de logging da aplicação.

- Garante a criação da pasta `logs` ao lado do projeto.
- Configura um arquivo por nível (debug, info, warning, error) com rotação.
- Mantém comentários explicativos no código para referência rápida.
"""
import logging  # Módulo padrão de logging
import os  # Para manipular caminhos e criar diretórios
from logging.handlers import RotatingFileHandler  # Handler com rotação de arquivos

LOG_DIR = "logs"  # Pasta onde os logs serão gravados
os.makedirs(LOG_DIR, exist_ok=True)  # Cria a pasta de logs, se não existir

# Formato das mensagens de log: data/hora, nível, nome do logger e mensagem
_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

def _level_filter(level: int):
    return lambda record: record.levelno == level  # Só aceita registros exatamente no nível informado

def _build_handler(level: int, name: str) -> RotatingFileHandler:
    # Cria um handler que grava em logs/<name>.log com rotação (1 MB e 5 backups)
    handler = RotatingFileHandler(
        os.path.join(LOG_DIR, f"{name}.log"), 
        maxBytes=1_000_000, 
        backupCount=5, 
        encoding="utf-8"
    )
    handler.setLevel(level)  # Nível mínimo do handler
    handler.addFilter(_level_filter(level))  # Filtra para apenas aquele nível exato
    handler.setFormatter(_FORMATTER)  # Aplica o formato definido
    return handler  # Retorna o handler pronto

def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)  # Obtém (ou cria) um logger com este nome
    if logger.handlers:  # Se já tem handlers, não reconfigura
        return logger
    logger.setLevel(logging.DEBUG)  # Permite todos os níveis a partir de DEBUG
    logger.propagate = False  # Evita que logs subam para o root e dupliquem
    # Adiciona um handler por nível, cada um em seu arquivo
    logger.addHandler(_build_handler(logging.DEBUG, "debug"))
    logger.addHandler(_build_handler(logging.INFO, "info"))
    logger.addHandler(_build_handler(logging.WARNING, "warning"))
    logger.addHandler(_build_handler(logging.ERROR, "error"))
    return logger  # Retorna o logger configurado