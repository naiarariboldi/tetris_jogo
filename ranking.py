import sqlite3
import datetime
from logger import log_error, log_info, log_debug

class RankingDB:
    def __init__(self, db_name="ranking.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.create_table()
            log_info(f"Banco de dados ranking inicializado: {db_name}")
        except Exception as e:
            log_error("Erro ao inicializar banco de dados", e)
            raise

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                pontuacao INTEGER,
                dificuldade TEXT,
                data TEXT
            )
            """)
            self.conn.commit()
            log_debug("Tabela ranking verificada/criada")
        except Exception as e:
            log_error("Erro ao criar tabela ranking", e)
            raise

    def add_score(self, nome, pontuacao, dificuldade):
        try:
            data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            c = self.conn.cursor()
            c.execute(
                "INSERT INTO ranking (nome, pontuacao, dificuldade, data) VALUES (?, ?, ?, ?)",
                (nome, pontuacao, dificuldade, data)
            )
            self.conn.commit()
            log_info(f"Pontuação adicionada: {pontuacao} pts, Dificuldade: {dificuldade}")
        except Exception as e:
            log_error("Erro ao adicionar pontuação", e)
            raise

    def get_top(self, limit=10):
        try:
            c = self.conn.cursor()
            c.execute("SELECT nome, pontuacao, dificuldade, data FROM ranking ORDER BY pontuacao DESC LIMIT ?", (limit,))
            resultados = c.fetchall()
            log_debug(f"Top {limit} pontuações recuperadas")
            return resultados
        except Exception as e:
            log_error("Erro ao recuperar top pontuações", e)
            return []