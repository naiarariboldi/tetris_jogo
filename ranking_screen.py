import pygame as pg
from ranking import RankingDB
from logger import log_error, log_info, log_debug

def ranking_screen(window):
    try:
        db = RankingDB()
        log_info("Tela de ranking aberta")

        fonte = pg.font.SysFont("Arial", 32)
        fonte_small = pg.font.SysFont("Arial", 24)
        largura = window.get_width()
        altura = window.get_height()

        rodando = True
        while rodando:
            window.fill((0, 0, 0))

            titulo = fonte.render("RANKING", True, (255, 255, 255))
            window.blit(titulo, (largura // 2 - titulo.get_width() // 2, 40))

            top = db.get_top()

            y = 120
            i = 1
            for linha in top:
                nome = linha[0] if linha[0] not in (None, "") else f"ID {i}"
                texto = fonte_small.render(
                    f"{nome} - {linha[1]} pts - {linha[2]} - {linha[3]}",
                    True, (255, 255, 255)
                )
                window.blit(texto, (60, y))
                y += 35
                i += 1

            sair = fonte_small.render("Pressione ESC para voltar", True, (255,255,255))
            window.blit(sair, (largura // 2 - sair.get_width() // 2, altura - 80))

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    log_info("Tela de ranking fechada")
                    rodando = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    log_info("Tela de ranking fechada pelo usuário")
                    rodando = False
                    
    except Exception as e:
        log_error("Erro na tela de ranking", e)