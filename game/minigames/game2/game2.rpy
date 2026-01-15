# game/minigames/game2/game2.rpy

##############################################################################
# Minigame 2 : 월하의 인연 수집
# - Main / Help (2 pages)
# - Play (Falling Catch)
##############################################################################

# ============================================================================#
# ASSETS (COMMON)
# ============================================================================#
define MG2_BTN_IDLE      = "minigames/common/images/button_idle.webp"
define MG2_BTN_HOVER     = "minigames/common/images/button_hover.webp"
define MG2_UI_HOVER_SFX  = "minigames/common/sound/hover.mp3"

define MG2_FONT = "fonts/Galmuri9.ttf"
define MG2_BTN_ZOOM = 0.55
define MG2_TXT_IDLE  = "#444444"
define MG2_TXT_HOVER = "#FFFFFF"
define MG2_TXT_LIFT  = 2

# ============================================================================#
# ASSETS (GAME2)
# ============================================================================#
define MG2_BG_BG = "minigames/game2/images/bg_game2_bg.webp"

# help2 portraits
define MG2_JIN = "minigames/game2/images/jin.webp"   # 화야진
define MG2_HYO = "minigames/game2/images/hyo.webp"   # 진효
define MG2_WOO = "minigames/game2/images/woo.webp"   # 백담우

# player
define MG2_P_IDLE = "minigames/game2/images/player1.webp"
define MG2_P_L    = "minigames/game2/images/player2.webp"
define MG2_P_R    = "minigames/game2/images/player3.webp"
define MG2_P_FALL = "minigames/game2/images/player4.webp"

# tokens (128/256)
define MG2_DAGGER_128  = "minigames/game2/images/dagger_128.webp"
define MG2_DAGGER_256  = "minigames/game2/images/dagger_256.webp"
define MG2_PENDANT_128 = "minigames/game2/images/pendant_128.webp"
define MG2_PENDANT_256 = "minigames/game2/images/pendant_256.webp"
define MG2_CHESS_128   = "minigames/game2/images/chesspiece_128.webp"
define MG2_CHESS_256   = "minigames/game2/images/chesspiece_256.webp"

# bomb / decor
define MG2_BOMB_128      = "minigames/game2/images/bomb_128.webp"
define MG2_FIREWORKS_128 = "minigames/game2/images/fireworks_128.webp"
define MG2_PLUM_128      = "minigames/game2/images/plumblossom_128.webp"
define MG2_MOON_128      = "minigames/game2/images/moon_128.webp"

# sfx (game2)
define MG2_SFX_COIN     = "minigames/game2/sounds/coin.mp3"
define MG2_SFX_BOMB     = "minigames/game2/sounds/bomb.mp3"


# ============================================================================#
# LABELS (ENTRY)
# ============================================================================#
label minigame2_main:
    $ _old_quick_menu = quick_menu
    $ quick_menu = False
    call screen mg2_main
    $ quick_menu = _old_quick_menu
    return

label minigame2_help:
    call screen mg2_help_1
    jump minigame2_main

label minigame2_help2:
    call screen mg2_help_2
    jump minigame2_main


# ============================================================================#
# MAIN SCREEN
# ============================================================================#
screen mg2_main():
    tag mg2
    modal True

    default hover_help = False
    default hover_start = False

    add MG2_BG_BG:
        fit "cover"

    add Solid("#0008")

    frame:
        xalign 0.5
        yalign 0.55
        xsize 1300
        ysize 700
        background Solid("#FFFFFF55")
        padding (80, 70)

        fixed:
            xfill True
            yfill True

            text "월하의 인연 수집":
                font MG2_FONT
                size 100
                color "#EDE7FF"
                outlines [ (7, "#000000", 0, 0) ]
                xalign 0.5
                yalign 0.22
                textalign 0.5

            hbox:
                spacing 80
                xalign 0.5
                yalign 0.90

                # 도움말
                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG2_BTN_IDLE,  zoom=MG2_BTN_ZOOM)
                        hover Transform(MG2_BTN_HOVER, zoom=MG2_BTN_ZOOM)
                        hovered [ Play("sound", MG2_UI_HOVER_SFX), SetScreenVariable("hover_help", True) ]
                        unhovered SetScreenVariable("hover_help", False)
                        action Jump("minigame2_help")
                        xalign 0.5
                        yalign 0.5

                    text "게임 설명":
                        font MG2_FONT
                        size 30
                        color (MG2_TXT_HOVER if hover_help else MG2_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG2_TXT_LIFT if hover_help else 0)

                # 시작
                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG2_BTN_IDLE,  zoom=MG2_BTN_ZOOM)
                        hover Transform(MG2_BTN_HOVER, zoom=MG2_BTN_ZOOM)
                        hovered [ Play("sound", MG2_UI_HOVER_SFX), SetScreenVariable("hover_start", True) ]
                        unhovered SetScreenVariable("hover_start", False)
                        action Jump("minigame2_play")
                        xalign 0.5
                        yalign 0.5

                    text "게임 시작":
                        font MG2_FONT
                        size 30
                        color (MG2_TXT_HOVER if hover_start else MG2_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG2_TXT_LIFT if hover_start else 0)


# ============================================================================#
# HELP 1/2
# ============================================================================#
define MG2_HELP1_TITLE = "게임 설명"
define MG2_HELP1_BODY = (
"공략 대상의 인연의 증표를 많이 획득해 호감도를 올려보세요!\n"
"\n"
"{size=34}게임 규칙{/size}\n"
"1. 방향키(←/→)로 캐릭터를 조작할 수 있어요.\n"
"2. 화면 위에서 모든 도트 스타일의 인연의 증표가 떨어져요.\n"
"3. 같은 증표를 연속으로 3개 받으면 특별한 증표가 등장합니다!\n"
"4. 특별한 인연의 증표를 받으면 추가 호감도를 획득할 수 있어요.\n"
"5. 폭탄은 2초 행동불가 상태가 되어 증표를 받지 못하니, 피하는 게 좋아요.\n"
"\n"
"{size=34}목표{/size}\n"
"떨어지는 인연의 증표를 최대한 많이 모아 공략 대상의 호감도를 높여보세요!\n"
"결과 화면에서 이번 플레이로 얻은 호감도와 획득량을 확인할 수 있어요."
)

screen mg2_help_1():
    tag mg2
    modal True

    default hover_next = False

    add MG2_BG_BG:
        fit "cover"
    add Solid("#0006")

    frame:
        xalign 0.5
        yalign 0.52
        xsize 1500
        ysize 820
        background Solid("#BFC6CF88")
        padding (60, 50)

        fixed:
            xfill True
            yfill True

            textbutton "X":
                text_font MG2_FONT
                text_size 32
                text_color "#FFFFFF"
                text_hover_color "#DDDDDD"
                hovered Play("sound", MG2_UI_HOVER_SFX)
                action Jump("minigame2_main")
                xalign 0.985
                yalign 0.02

            vbox:
                xpos 40
                ypos 30
                xmaximum 980
                spacing 18

                text MG2_HELP1_TITLE:
                    font MG2_FONT
                    size 72
                    color "#111111"
                    outlines [ (2, "#FFFFFF88", 0, 0) ]

                null height 14

                text MG2_HELP1_BODY:
                    font MG2_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

            fixed:
                xalign 0.94
                yalign 0.93
                xsize 340
                ysize 140

                imagebutton:
                    idle Transform(MG2_BTN_IDLE,  zoom=MG2_BTN_ZOOM)
                    hover Transform(MG2_BTN_HOVER, zoom=MG2_BTN_ZOOM)
                    hovered [ Play("sound", MG2_UI_HOVER_SFX), SetScreenVariable("hover_next", True) ]
                    unhovered SetScreenVariable("hover_next", False)
                    action Jump("minigame2_help2")
                    xalign 0.5
                    yalign 0.5

                text "다음 보기":
                    font MG2_FONT
                    size 30
                    color (MG2_TXT_HOVER if hover_next else MG2_TXT_IDLE)
                    xalign 0.5
                    yalign 0.5
                    yoffset (-MG2_TXT_LIFT if hover_next else 0)


# ============================================================================#
# HELP 2/2
# ============================================================================#
define MG2_HELP2_TITLE = "인연의 증표"

define MG2_HELP2_HYO = (
"{size=32}태휘국 황태자 진효 – 장기말{/size}\n"
"진효에게 세상은 장기판이며, 사람은 모두 말이다.\n"
"\n"
"“공주께서 잡아주신 말은… 제 계획을 완성시키는 마지막 한 수입니다.”\n"
"“흐름을 거스르지 않는 것이 제 원칙입니다. 하지만 공주께서 손대신다면—그것이 곧 정답이죠.”"
)

define MG2_HELP2_JIN = (
"{size=32}거상 화야진 – 호박빛 펜던트{/size}\n"
"화야진에게 ‘호박’은 가난과 멸시를 뒤집고 처음 손에 쥔 부의 씨앗이다.\n"
"\n"
"“이거, 제가 밑바닥에서 처음 손에 쥔 겁니다. 자, 떨어지네요 공주님.”\n"
"“가치 있는 건… 잡으셔야죠. 놓치면 손해니까.”"
)

define MG2_HELP2_WOO = (
"{size=32}호위무사 백담우 – 청월 단검{/size}\n"
"이 단검은 공주가 어린 시절 백담우에게 건네준 첫 번째 인정이다.\n"
"\n"
"“이 단검은… 공주님께서 제게 처음 주신 것이었습니다.”\n"
"“제가 이걸 놓치지 않을 테니, 공주님께서도 저를 놓치지 마세요.”"
)

screen mg2_help_2():
    tag mg2
    modal True

    default hover_prev = False
    default hover_start = False

    add MG2_BG_BG:
        fit "cover"
    add Solid("#0006")

    frame:
        xalign 0.5
        yalign 0.52
        xsize 1500
        ysize 820
        background Solid("#BFC6CF88")
        padding (10, 10)

        fixed:
            xfill True
            yfill True

            textbutton "X":
                text_font MG2_FONT
                text_size 32
                text_color "#FFFFFF"
                text_hover_color "#DDDDDD"
                hovered Play("sound", MG2_UI_HOVER_SFX)
                action Jump("minigame2_main")
                xalign 0.985
                yalign 0.02

            text MG2_HELP2_TITLE:
                font MG2_FONT
                size 72
                color "#111111"
                outlines [ (2, "#FFFFFF88", 0, 0) ]
                xpos 40
                ypos 25

            # --- 우상단: 화야진 ---
            add Transform(MG2_JIN, zoom=0.23) xpos 1240 ypos 80
            add Transform(MG2_PENDANT_128, zoom=0.80) xpos 1200 ypos 95

            text MG2_HELP2_JIN:
                font MG2_FONT
                size 22
                color "#FFFFFF"
                outlines [ (2, "#00000088", 0, 0) ]
                xpos 1200 ypos 130
                xanchor 1.0
                xmaximum 1000
                textalign 1.0
                line_spacing 4

            # --- 좌중단: 진효 ---
            add Transform(MG2_HYO, zoom=0.24) xpos 30 ypos 270
            add Transform(MG2_CHESS_128, zoom=0.80) xpos 170 ypos 265

            text MG2_HELP2_HYO:
                font MG2_FONT
                size 22
                color "#FFFFFF"
                outlines [ (2, "#00000088", 0, 0) ]
                xpos 320 ypos 310
                xmaximum 1000
                line_spacing 4

            # --- 우하단: 백담우 ---
            add Transform(MG2_WOO, zoom=0.24) xpos 1240 ypos 430
            add Transform(MG2_DAGGER_128, zoom=0.80) xpos 1200 ypos 460

            text MG2_HELP2_WOO:
                font MG2_FONT
                size 22
                color "#FFFFFF"
                outlines [ (2, "#00000088", 0, 0) ]
                xpos 1200 ypos 490
                xanchor 1.0
                xmaximum 1000
                textalign 1.0
                line_spacing 4

            # buttons
            fixed:
                xalign 0.10
                yalign 0.95
                xsize 340
                ysize 140
                imagebutton:
                    idle Transform(MG2_BTN_IDLE,  zoom=MG2_BTN_ZOOM)
                    hover Transform(MG2_BTN_HOVER, zoom=MG2_BTN_ZOOM)
                    hovered [ Play("sound", MG2_UI_HOVER_SFX), SetScreenVariable("hover_prev", True) ]
                    unhovered SetScreenVariable("hover_prev", False)
                    action Jump("minigame2_help")
                    xalign 0.5
                    yalign 0.5
                text "이전 보기":
                    font MG2_FONT
                    size 30
                    color (MG2_TXT_HOVER if hover_prev else MG2_TXT_IDLE)
                    xalign 0.5
                    yalign 0.5
                    yoffset (-MG2_TXT_LIFT if hover_prev else 0)

            fixed:
                xalign 0.90
                yalign 0.95
                xsize 340
                ysize 140
                imagebutton:
                    idle Transform(MG2_BTN_IDLE,  zoom=MG2_BTN_ZOOM)
                    hover Transform(MG2_BTN_HOVER, zoom=MG2_BTN_ZOOM)
                    hovered [ Play("sound", MG2_UI_HOVER_SFX), SetScreenVariable("hover_start", True) ]
                    unhovered SetScreenVariable("hover_start", False)
                    action Jump("minigame2_play")
                    xalign 0.5
                    yalign 0.5
                text "게임 시작":
                    font MG2_FONT
                    size 30
                    color (MG2_TXT_HOVER if hover_start else MG2_TXT_IDLE)
                    xalign 0.5
                    yalign 0.5
                    yoffset (-MG2_TXT_LIFT if hover_start else 0)


##############################################################################
# PLAY : 중앙 3:4 영역에서만 진행
##############################################################################

# ---------- SCREEN ----------
define MG2_SW = 1920
define MG2_SH = 1080

# 중앙 3:4
define MG2_FIELD_H = MG2_SH
define MG2_FIELD_W = 1440
define MG2_FIELD_X = 240
define MG2_FIELD_Y = 0

# ---------- GAME CONST ----------
define MG2_DURATION    = 20.0
define MG2_SPAWN_DT    = 0.95
define MG2_TOTAL_SPAWN = 20

define MG2_BOMB_I_1 = 7
define MG2_BOMB_I_2 = 14

# HUD (두루마리)
define MG2_HUD_SCROLL = "minigames/common/images/ui_scroll_long.webp"
define MG2_UI_SCROLL = "minigames/common/images/ui_scroll_medium.webp"
define MG2_HUD_ZOOM   = 0.28
define MG2_HUD_X      = -22
define MG2_HUD_Y      = -22

define MG2_HUD_ICON_ZOOM = 0.6

# 증표별 점수
define MG2_PT_DAGGER  = 1
define MG2_PT_PENDANT = 1
define MG2_PT_CHESS   = 1

# 공주(플레이어) 크기
define MG2_PLAYER_Z     = 0.20
define MG2_PLAYER_SPEED = 1550.0
define MG2_PLAYER_Y     = 830

define MG2_FALL_MIN_V = 750.0
define MG2_FALL_MAX_V = 1150.0

# player hitbox: 상단 15% / 가로 60%
define MG2_HIT_TOP_H    = 0.15
define MG2_HIT_W_FACTOR = 0.60

# item hitbox: 약간 작게
define MG2_ITEM_HIT_F = 0.70

# bomb stun
define MG2_STUN_SEC = 1.0

# bomb flash (무음)
define MG2_FLASH_SEC   = 0.35
define MG2_FLASH_ALPHA = 0.75


# ---------- STATE ----------
default mg2_time_left = MG2_DURATION
default mg2_score = 0

default mg2_schedule = []
default mg2_spawn_i = 0
default mg2_next_spawn = MG2_SPAWN_DT

default mg2_items = []
default mg2_flash = 0.0

default mg2_dagger = 0
default mg2_pendant = 0
default mg2_chess = 0

# mg2_player_x는 "필드 내부 좌표"(0~MG2_FIELD_W)에서의 중심 x
default mg2_player_x = MG2_FIELD_W/2
default mg2_left_down = False
default mg2_right_down = False

default mg2_facing = 0      # -1 L, 0 idle, +1 R
default mg2_facing_t = 0.0

default mg2_stun = 0.0

default mg2_combo_kind = None
default mg2_combo_n = 0

default mg2_show_result = False


init python:
    import random

    def mg2_time_fmt(t):
        t = max(0, int(t))
        m = t // 60
        s = t % 60
        return "%02d:%02d" % (m, s)

    def mg2_clamp(v, a, b):
        return a if v < a else (b if v > b else v)

    def mg2_img_size(path, fallback=(128, 128)):
        try:
            return renpy.image_size(path)
        except:
            return fallback

    def mg2_aabb(ax, ay, aw, ah, bx, by, bw, bh):
        return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

    def mg2_player_hitbox():
        """
        반환:
        - hb_x, hb_y, hb_w, hb_h : 화면좌표 히트박스(바구니 상단 15%)
        - spr_x, spr_y, spr_w, spr_h : 화면좌표 스프라이트 박스(좌상단 기준)
        """
        w0, h0 = mg2_img_size(MG2_P_IDLE, (256, 256))
        spr_w = int(w0 * MG2_PLAYER_Z)
        spr_h = int(h0 * MG2_PLAYER_Z)

        # mg2_player_x는 필드 내부 "중심"
        cx = MG2_FIELD_X + float(store.mg2_player_x)
        spr_x = int(cx - spr_w / 2.0)
        spr_y = int(MG2_PLAYER_Y)

        hb_w = int(spr_w * MG2_HIT_W_FACTOR)
        hb_h = int(spr_h * MG2_HIT_TOP_H)
        hb_x = int(spr_x + (spr_w - hb_w) / 2.0)
        hb_y = int(spr_y)  # 상단

        return hb_x, hb_y, hb_w, hb_h, spr_x, spr_y, spr_w, spr_h

    def mg2_item_hitbox_screen(it):
        """
        it["x"]는 필드 내부 좌표(좌상단 기준).
        화면좌표로 변환해서 판정.
        """
        x = MG2_FIELD_X + float(it["x"])
        y = float(it["y"])

        hb_w = int(it["w"] * MG2_ITEM_HIT_F)
        hb_h = int(it["h"] * MG2_ITEM_HIT_F)
        hb_x = int(x + (it["w"] - hb_w) / 2.0)
        hb_y = int(y + (it["h"] - hb_h) / 2.0)
        return hb_x, hb_y, hb_w, hb_h

    def mg2_make_schedule():
        """
        20회 스폰 슬롯:
        - 7,14 = bomb
        - decor 3개(불꽃/홍매화/달) 랜덤 슬롯
        - token 15개 (dagger/pendant/chess 각 5개)
        """
        sched = [None] * MG2_TOTAL_SPAWN

        sched[MG2_BOMB_I_1 - 1] = ("bomb", None)
        sched[MG2_BOMB_I_2 - 1] = ("bomb", None)

        empty = [i for i in range(MG2_TOTAL_SPAWN) if sched[i] is None]
        random.shuffle(empty)
        for dk in [("decor","fireworks"), ("decor","plum"), ("decor","moon")]:
            sched[empty.pop()] = dk

        tokens = (["dagger"]*5) + (["pendant"]*5) + (["chess"]*5)
        random.shuffle(tokens)

        empty = [i for i in range(MG2_TOTAL_SPAWN) if sched[i] is None]
        for i, t in zip(empty, tokens):
            sched[i] = ("token", t)

        return sched

    def mg2_spawn_from_slot(slot):
        kind, sub = slot

        if kind == "bomb":
            img = MG2_BOMB_128
            it_kind = "bomb"
            score = 0
            store.mg2_flash = MG2_FLASH_SEC

        elif kind == "decor":
            if sub == "fireworks":
                img = MG2_FIREWORKS_128
            elif sub == "plum":
                img = MG2_PLUM_128
            else:
                img = MG2_MOON_128
            it_kind = "decor"
            score = 0

        else:
            if sub == "dagger":
                img = MG2_DAGGER_128
            elif sub == "pendant":
                img = MG2_PENDANT_128
            else:
                img = MG2_CHESS_128
            it_kind = sub
            score = 1

        w0, h0 = mg2_img_size(img, (128, 128))
        w, h = w0, h0

        # 필드 내부 x (좌상단 기준)
        x = random.uniform(0, MG2_FIELD_W - w)
        # y는 위쪽 랜덤
        y = random.uniform(-160, -40)
        vy = random.uniform(MG2_FALL_MIN_V, MG2_FALL_MAX_V)

        store.mg2_items.append({
            "kind": it_kind,  # bomb / decor / dagger / pendant / chess / big_*
            "img": img,
            "x": float(x),    # 필드 내부 좌표(좌상단)
            "y": float(y),
            "vy": float(vy),
            "w": w,
            "h": h,
            "score": score,
        })

    def mg2_spawn_big(kind):
        # 3연속 달성 시 256 큰 증표 추가 낙하
        if kind == "dagger":
            img = MG2_DAGGER_256
        elif kind == "pendant":
            img = MG2_PENDANT_256
        else:
            img = MG2_CHESS_256

        w0, h0 = mg2_img_size(img, (256, 256))
        w, h = w0, h0

        x = random.uniform(0, MG2_FIELD_W - w)
        y = random.uniform(-700, -200)
        vy = random.uniform(MG2_FALL_MIN_V * 0.85, MG2_FALL_MAX_V * 0.95)

        store.mg2_items.append({
            "kind": "big_" + kind,
            "img": img,
            "x": float(x),
            "y": float(y),
            "vy": float(vy),
            "w": w,
            "h": h,
            "score": 3,
        })

    def mg2_on_catch(it):
        # 스턴 중에는 아무것도 못 먹음
        if store.mg2_stun > 0.0:
            return

        k = it["kind"]

        if k == "bomb":
            store.mg2_stun = MG2_STUN_SEC
            store.mg2_combo_kind = None
            store.mg2_combo_n = 0
            renpy.sound.play(MG2_SFX_BOMB)
            return

        # 장식은 무시(카운트/점수 X)
        if k == "decor":
            return

        # 큰 증표: 해당 증표를 "2개 더 먹은 것처럼" 처리 (+2점)
        if k.startswith("big_"):
            base = k[4:]  # "dagger" / "pendant" / "chess"

            if base == "dagger":
                store.mg2_dagger += 2
                store.mg2_score += MG2_PT_DAGGER * 2
            elif base == "pendant":
                store.mg2_pendant += 2
                store.mg2_score += MG2_PT_PENDANT * 2
            elif base == "chess":
                store.mg2_chess += 2
                store.mg2_score += MG2_PT_CHESS * 2

            renpy.sound.play(MG2_SFX_COIN)

            store.mg2_combo_kind = None
            store.mg2_combo_n = 0
            return

        # 일반 증표: 종류별 카운트 + 점수
        if k == "dagger":
            store.mg2_dagger += 1
            store.mg2_score += MG2_PT_DAGGER
        elif k == "pendant":
            store.mg2_pendant += 1
            store.mg2_score += MG2_PT_PENDANT
        elif k == "chess":
            store.mg2_chess += 1
            store.mg2_score += MG2_PT_CHESS

        renpy.sound.play(MG2_SFX_COIN)

        if store.mg2_combo_kind == k:
            store.mg2_combo_n += 1
        else:
            store.mg2_combo_kind = k
            store.mg2_combo_n = 1

        if store.mg2_combo_n >= 3:
            mg2_spawn_big(k)
            store.mg2_combo_kind = None
            store.mg2_combo_n = 0

    def mg2_tick(dt):
        if store.mg2_show_result:
            return

        # time
        store.mg2_time_left -= dt
        if store.mg2_time_left <= 0:
            store.mg2_time_left = 0
            store.mg2_show_result = True
            return

        # flash
        if store.mg2_flash > 0:
            store.mg2_flash -= dt
            if store.mg2_flash < 0:
                store.mg2_flash = 0

        # stun
        if store.mg2_stun > 0:
            store.mg2_stun -= dt
            if store.mg2_stun < 0:
                store.mg2_stun = 0

        # 혹시 둘 다 True로 꼬였으면 정리
        if store.mg2_left_down and store.mg2_right_down:
            store.mg2_left_down = False
            store.mg2_right_down = False

        # move
        if store.mg2_stun <= 0:
            vx = 0.0
            if store.mg2_left_down and not store.mg2_right_down:
                vx = -MG2_PLAYER_SPEED
                store.mg2_facing = -1
                store.mg2_facing_t = 0.05
            elif store.mg2_right_down and not store.mg2_left_down:
                vx = MG2_PLAYER_SPEED
                store.mg2_facing = 1
                store.mg2_facing_t = 0.05
            store.mg2_player_x += vx * dt

        # facing timer
        if store.mg2_facing_t > 0:
            store.mg2_facing_t -= dt
            if store.mg2_facing_t <= 0:
                store.mg2_facing_t = 0
                store.mg2_facing = 0

        # clamp inside field
        _, _, _, _, _, _, spr_w, _ = mg2_player_hitbox()
        half = spr_w / 2.0
        store.mg2_player_x = mg2_clamp(store.mg2_player_x, half + 5, MG2_FIELD_W - half - 5)

        # spawn (20회)
        if store.mg2_spawn_i < MG2_TOTAL_SPAWN:
            store.mg2_next_spawn -= dt
            if store.mg2_next_spawn <= 0:
                slot = store.mg2_schedule[store.mg2_spawn_i]
                store.mg2_spawn_i += 1
                mg2_spawn_from_slot(slot)
                store.mg2_next_spawn += MG2_SPAWN_DT

        # items move + collide
        hb_x, hb_y, hb_w, hb_h, _, _, _, _ = mg2_player_hitbox()
        new_items = []

        for it in store.mg2_items:
            it["y"] += it["vy"] * dt

            # out
            if it["y"] > MG2_SH + 220:
                continue

            # collide (스턴 중엔 먹기 불가)
            ihx, ihy, ihw, ihh = mg2_item_hitbox_screen(it)
            if store.mg2_stun <= 0 and mg2_aabb(hb_x, hb_y, hb_w, hb_h, ihx, ihy, ihw, ihh):
                mg2_on_catch(it)
                continue

            new_items.append(it)

        store.mg2_items = new_items


# ---------- ENTRY ----------
label minigame2_play:
    $ mg2_dagger = 0
    $ mg2_pendant = 0
    $ mg2_chess = 0

    $ mg2_time_left = MG2_DURATION
    $ mg2_score = 0

    $ mg2_schedule = mg2_make_schedule()
    $ mg2_spawn_i = 0
    $ mg2_next_spawn = 0.0

    $ mg2_items = []
    $ mg2_flash = 0.0

    $ mg2_player_x = MG2_FIELD_W / 2.0
    $ mg2_left_down = False
    $ mg2_right_down = False
    $ mg2_facing = 0
    $ mg2_facing_t = 0.0

    $ mg2_stun = 0.0
    $ mg2_combo_kind = None
    $ mg2_combo_n = 0

    $ mg2_show_result = False

    call screen mg2_game
    call screen mg2_result

    return

# ---------- SCREEN (PLAY) ----------
screen mg2_game():
    tag mg2
    modal True

    if mg2_show_result:
        timer 0.01 action Return()

    # tick
    if not mg2_show_result:
        timer (1.0/60.0) repeat True action Function(mg2_tick, (1.0/60.0))

    # input
    key "K_LEFT"  action SetVariable("mg2_left_down", True)
    key "K_RIGHT" action SetVariable("mg2_right_down", True)
    key "keyup_K_LEFT"  action [ SetVariable("mg2_left_down", False),  SetVariable("mg2_facing", 0), SetVariable("mg2_facing_t", 0.0) ]
    key "keyup_K_RIGHT" action [ SetVariable("mg2_right_down", False), SetVariable("mg2_facing", 0), SetVariable("mg2_facing_t", 0.0) ]

    key "K_a"  action SetVariable("mg2_left_down", True)
    key "K_d"  action SetVariable("mg2_right_down", True)
    key "keyup_K_a"     action [ SetVariable("mg2_left_down", False),  SetVariable("mg2_facing", 0), SetVariable("mg2_facing_t", 0.0) ]
    key "keyup_K_d"     action [ SetVariable("mg2_right_down", False), SetVariable("mg2_facing", 0), SetVariable("mg2_facing_t", 0.0) ]

    # BG full
    add MG2_BG_BG:
        fit "cover"

    # 좌/우 영역 살짝 어둡게
    add Solid("#0008") xpos 0 ypos 0 xsize MG2_FIELD_X ysize MG2_SH
    add Solid("#0008") xpos (MG2_FIELD_X + MG2_FIELD_W) ypos 0 xsize (MG2_SW - (MG2_FIELD_X + MG2_FIELD_W)) ysize MG2_SH

    # 폭탄 스폰 flash
    if mg2_flash > 0:
        $ _p = 1.0 - (mg2_flash / MG2_FLASH_SEC)
        $ _wave = abs(__import__("math").sin(_p * 3.141592 * 2))
        $ _a = MG2_FLASH_ALPHA * _wave
        add Solid("#111") alpha _a

    # HUD 두루마리
    add Transform(MG2_HUD_SCROLL, zoom=MG2_HUD_ZOOM) xpos MG2_HUD_X ypos MG2_HUD_Y

    text "[mg2_time_fmt(mg2_time_left)]":
        font MG2_FONT
        size 34
        color "#111111"
        xpos (MG2_HUD_X + 100) ypos (MG2_HUD_Y + 110)

    text "[mg2_dagger]":
        font MG2_FONT
        size 30
        color "#111111"
        xpos (MG2_HUD_X + 165) ypos (MG2_HUD_Y + 170)

    text "[mg2_pendant]":
        font MG2_FONT
        size 30
        color "#111111"
        xpos (MG2_HUD_X + 165) ypos (MG2_HUD_Y + 223)

    text "[mg2_chess]":
        font MG2_FONT
        size 30
        color "#111111"
        xpos (MG2_HUD_X + 165) ypos (MG2_HUD_Y + 275)

    add Transform(MG2_DAGGER_128,  zoom=MG2_HUD_ICON_ZOOM) xpos (MG2_HUD_X + 85) ypos (MG2_HUD_Y + 150)
    add Transform(MG2_PENDANT_128, zoom=MG2_HUD_ICON_ZOOM) xpos (MG2_HUD_X + 85) ypos (MG2_HUD_Y + 200)
    add Transform(MG2_CHESS_128,   zoom=MG2_HUD_ICON_ZOOM) xpos (MG2_HUD_X + 85) ypos (MG2_HUD_Y + 255)

    # falling items
    for it in mg2_items:
        add it["img"] xpos int(MG2_FIELD_X + it["x"]) ypos int(it["y"])

    # player
    $ _hb_x, _hb_y, _hb_w, _hb_h, _spr_x, _spr_y, _spr_w, _spr_h = mg2_player_hitbox()

    # player (폭탄 스턴 중엔 player4 깜빡임)
    $ _blink = (mg2_stun > 0.0 and int(mg2_stun * 10) % 2 == 0)

    if mg2_stun > 0:
        if not _blink:
            add Transform(MG2_P_FALL, zoom=MG2_PLAYER_Z) xpos int(_spr_x) ypos int(_spr_y)
    else:
        if mg2_facing == -1:
            add Transform(MG2_P_L, zoom=MG2_PLAYER_Z) xpos int(_spr_x) ypos int(_spr_y)
        elif mg2_facing == 1:
            add Transform(MG2_P_R, zoom=MG2_PLAYER_Z) xpos int(_spr_x) ypos int(_spr_y)
        else:
            add Transform(MG2_P_IDLE, zoom=MG2_PLAYER_Z) xpos int(_spr_x) ypos int(_spr_y)


# ---------- RESULT ----------
screen mg2_result():
    tag mg2
    modal True
    zorder 200

    default hover_proceed = False

    add MG2_BG_BG:
        fit "cover"

    add Solid("#0008")

    # =========================
    # 결과 패널
    # =========================
    fixed:
        xalign 0.5
        yalign 0.55
        xsize 1200
        ysize 600

        # 두루마리 크기
        add Transform(MG2_UI_SCROLL, zoom=0.88):
            xalign 0.5
            yalign 0.5

        # ----- 타이틀 위치 조정 (조금 위로) -----
        text "게임 결과":
            font MG2_FONT
            size 60
            color "#111111"
            outlines [ (4, "#FFFFFF88", 0, 0) ]
            xalign 0.5
            yalign 0.18

        # =========================
        # 아이콘 + 카운트
        # =========================
        vbox:
            xalign 0.5
            yalign 0.52
            spacing -20

            hbox:
                xalign 0.5
                spacing 2
                add Transform(MG2_DAGGER_128, zoom=0.80)
                text "[mg2_dagger]":
                    font MG2_FONT
                    size 44
                    color "#111111"
                    outlines [ (3, "#FFFFFF88", 0, 0) ]
                    yalign 0.5

            hbox:
                xalign 0.5
                spacing 2
                add Transform(MG2_PENDANT_128, zoom=0.80)
                text "[mg2_pendant]":
                    font MG2_FONT
                    size 44
                    color "#111111"
                    outlines [ (3, "#FFFFFF88", 0, 0) ]
                    yalign 0.5

            hbox:
                xalign 0.5
                spacing 2
                add Transform(MG2_CHESS_128, zoom=0.80)
                text "[mg2_chess]":
                    font MG2_FONT
                    size 44
                    color "#111111"
                    outlines [ (3, "#FFFFFF88", 0, 0) ]
                    yalign 0.5

        # =========================
        # 진행하기 버튼
        # =========================
        fixed:
            xalign 0.5
            yalign 0.84
            xsize 340
            ysize 140

            button:
                xalign 0.5
                yalign 0.5
                xsize 340
                ysize 140

                background Transform(MG2_BTN_IDLE,  zoom=MG2_BTN_ZOOM, xoffset=30, yoffset=55)
                hover_background Transform(MG2_BTN_HOVER, zoom=MG2_BTN_ZOOM, xoffset=30, yoffset=55)
                focus_mask True

                hovered [ Play("sound", MG2_UI_HOVER_SFX), SetScreenVariable("hover_proceed", True) ]
                unhovered SetScreenVariable("hover_proceed", False)

                action Return()

                text "진행하기":
                    font MG2_FONT
                    size 30
                    color (MG2_TXT_HOVER if hover_proceed else MG2_TXT_IDLE)
                    xalign 0.5
                    yalign 0.85
                    yoffset (-MG2_TXT_LIFT if hover_proceed else 0)
