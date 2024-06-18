import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
        """
        引数：こうかとんRect, または, 爆弾Rect
        戻り値：真理値タプル（横方向、縦方向）
        画面内ならTrue／画面外ならFalse
        """
        yoko, tate = True, True
        if rct.left < 0 or WIDTH < rct.right: # 横方向判定
            yoko = False
        if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向判定
            tate = False
        return yoko, tate
    
# def kk_angle() -> tuple[bool, bool]:
#     """
#     引数：こうかとんRect
#     戻り値：真理値タプル(縦方向、横方向、斜め方向)
#     右向き, 下向きならTrue／左向き, 上向きならFalse
#     """
#     angles = 

def gm_ov(screen):
    """
    ゲームオーバー画面の設定
    引数：画面の大きさ
    爆弾がこうかとんに当たると、
    ・画面をブラックアウトする
    ・画面中央に「game over」の文字を配置
    ・画面の高さ半分、幅の外側からそれぞれ四分の一の位置
    　に泣いているこうかとんの画像を配置
    ・5秒間表示したら画面を閉じる
    """
    black_surface = pg.Surface((WIDTH, HEIGHT))  # ブラックアウト用のSurfaceを作成
    black_surface.set_alpha(128)  # 半透明に設定
    black_surface.fill((0, 0, 0))  # 黒色に設定
    screen.blit(black_surface, (0, 0))  # 画面をブラックアウトする
    kk_cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    screen.blit(kk_cry_img, (WIDTH // 4, HEIGHT // 2))
    screen.blit(kk_cry_img, (WIDTH // (4/3), HEIGHT // 2))

    # "Game Over"の文字列を表示
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pg.display.update()
    pg.time.wait(5000)  # 5秒間表示

def main(): 
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bom_img = pg.Surface((20,20)) # 一辺が20の正方形Surface
    pg.draw.circle(bom_img, (255,0,0), (10,10), 10) # の中心に半径10の赤い円を描画
    bom_img.set_colorkey((0,0,0)) # 四隅の黒を透過させる
    bom_rct = bom_img.get_rect()
    bom_rct.center = random.randint(0, WIDTH), random.randint(0,HEIGHT)
    vx, vy = +5, +5
    count = 0
    clock = pg.time.Clock()
    tmr = 0
    dic = {
        pg.K_UP:(0,-5), 
        pg.K_DOWN:(0,+5), 
        pg.K_LEFT:(-5,0), 
        pg.K_RIGHT:(+5,0),
    }
    # kk_dic = {
    #     pg.K_UP:-90,
    #     pg.K_DOWN:+90,
    #     pg.K_LEFT:0,
    #     pg.K_RIGHT:+180,
    # }
    clock = pg.time.Clock()
    tmr = 0
    # angle = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        if kk_rct.colliderect(bom_rct):  # 衝突判定
            gm_ov(screen)  # ゲームオーバー画面を表示
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in dic.items():
            if key_lst[k]: # "dctから要素を取り出す"
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                # angle = kk_dic[k]                
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        yoko, tate = check_bound(bom_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        # kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), angle, 2.0)
        screen.blit(kk_img, kk_rct)
        # accs = [a for a in range(1, 11)]
        # if tmr % 5 == 0:
        #     if count <= 10:
        #         count += 1
        #     else:
        #         count = 10
        bom_rct.move_ip(+vx, +vy)
        screen.blit(bom_img, bom_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
