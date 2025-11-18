import logging
import os
from datetime import datetime

def setup_logger():
    """Configura o sistema de logging"""
    
    # Cria diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Data atual para nome do arquivo
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"logs/tetris_{current_date}.log"
    
    # Configuração do logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # Também exibe no console
        ]
    )
    
    return logging.getLogger('tetris')

# Logger global
logger = setup_logger()

def log_error(error_message, exception=None):
    """Função auxiliar para log de erros"""
    if exception:
        logger.error(f"{error_message}: {str(exception)}", exc_info=True)
    else:
        logger.error(error_message)

def log_info(info_message):
    """Função auxiliar para log de informações"""
    logger.info(info_message)

def log_warning(warning_message):
    """Função auxiliar para log de avisos"""
    logger.warning(warning_message)

def log_debug(debug_message):
    """Função auxiliar para log de debug"""
    logger.debug(debug_message)