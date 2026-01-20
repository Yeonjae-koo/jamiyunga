# game/minigames/game1/game1.rpy

##############################################################################
# Minigame 1 : 몽진의 밤
# - Main / Help UI
# - Runner Play (Parallax + Player Anim + Obstacles + Timer + Result)
# - common.rpy 공용 상수 사용 (MG1_*로 매핑)
##############################################################################

# ---------- CHANNELS ----------
# (BGM은 나중에 추가, 지금은 sfx / ui / result만 분리)
init -10 python:
    renpy.music.register_channel("sfx",    "sfx", loop=False)
    renpy.music.register_channel("ui",     "sfx", loop=False)
    renpy.music.register_channel("result", "sfx", loop=False)


# ---------- ASSETS (MAIN/HELP) ----------
define MG1_BG_BG        = "minigames/game1/images/bg_game1_bg.webp"

# 공용 UI 에셋 매핑 (common.rpy)
define MG1_BTN_IDLE     = UI_BTN_IDLE
define MG1_BTN_HOVER    = UI_BTN_HOVER
define MG1_FONT         = UI_FONT

define MG1_REWARD_PANEL = "minigames/game1/images/reward.webp"

# 버튼 크기
define MG1_BTN_ZOOM = 0.55

# 글씨 색(기본/호버)
define MG1_TXT_IDLE  = "#444444"
define MG1_TXT_HOVER = "#FFFFFF"

# 글씨가 떠오르는 정도(px)
define MG1_TXT_LIFT = 2


# ---------- LABELS ----------
label minigame1_main:
    $ _old_quick_menu = quick_menu
    $ quick_menu = False

    call screen mg1_main

    $ quick_menu = _old_quick_menu
    return

label minigame1_help:
    call screen mg1_help
    jump minigame1_main


# ---------- SCREENS (MAIN) ----------
screen mg1_main():
    tag mg1
    modal True

    default hover_help = False
    default hover_start = False

    add MG1_BG_BG:
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

            # 제목
            text "몽진의 밤":
                font MG1_FONT
                size 110
                color "#B3261E"
                outlines [ (7, "#000000", 0, 0) ]
                xalign 0.5
                yalign 0.22
                textalign 0.5

            # 버튼
            hbox:
                spacing 80
                xalign 0.5
                yalign 0.90

                # 왼쪽 : 게임 설명
                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG1_BTN_IDLE,  zoom=MG1_BTN_ZOOM)
                        hover Transform(MG1_BTN_HOVER, zoom=MG1_BTN_ZOOM)
                        hovered [ Play("ui", SFX_UI_HOVER), SetScreenVariable("hover_help", True) ]
                        unhovered SetScreenVariable("hover_help", False)
                        action Jump("minigame1_help")
                        xalign 0.5
                        yalign 0.5

                    text "게임 설명":
                        font MG1_FONT
                        size 30
                        color (MG1_TXT_HOVER if hover_help else MG1_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG1_TXT_LIFT if hover_help else 0)

                # 오른쪽 : 게임 시작
                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG1_BTN_IDLE,  zoom=MG1_BTN_ZOOM)
                        hover Transform(MG1_BTN_HOVER, zoom=MG1_BTN_ZOOM)
                        hovered [ Play("ui", SFX_UI_HOVER), SetScreenVariable("hover_start", True) ]
                        unhovered SetScreenVariable("hover_start", False)

                        action Jump("minigame1_play")
                        xalign 0.5
                        yalign 0.5

                    text "게임 시작":
                        font MG1_FONT
                        size 30
                        color (MG1_TXT_HOVER if hover_start else MG1_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG1_TXT_LIFT if hover_start else 0)


# ---------- SCREENS (HELP) ----------
screen mg1_help():
    tag mg1
    modal True

    default hover_help_start = False

    add MG1_BG_BG:
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

            # 닫기
            textbutton "X":
                text_font MG1_FONT
                text_size 32
                text_color "#FFFFFF"
                text_hover_color "#DDDDDD"
                hovered Play("ui", SFX_UI_HOVER)
                action Jump("minigame1_main")
                xalign 0.985
                yalign 0.02

            # 설명 텍스트
            vbox:
                xpos 40
                ypos 30
                xmaximum 880
                spacing 18

                text "게임 설명":
                    font MG1_FONT
                    size 70
                    color "#111111"
                    outlines [ (2, "#FFFFFF88", 0, 0) ]

                null height 24

                text "혼란이 휩쓴 밤, 청월국의 수도 '영나성'이 붕괴되고 있다.\n당신은 시위교위 '백담우'와 함께 폐허가 되어가는 궁을 빠져나가야 한다.":
                    font MG1_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

                text "{size=34}게임 규칙{/size}":
                    font MG1_FONT
                    color "#111111"

                text "1. 위/아래 방향키로 캐릭터가 점프/슬라이딩을 합니다.\n2. 붕괴하는 영나성 곳곳에서 낙하/잔해 장애물들이 등장해요.\n3. 장애물을 피하지 못하면 목숨이 1개씩 감소합니다.\n4. 총 3개의 목숨을 가지고 20초 버티면 게임 성공!\n5. 생존 시 남은 목숨에 따라 호감도 보상이 달라집니다.":
                    font MG1_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

                text "{size=34}목표{/size}":
                    font MG1_FONT
                    color "#111111"

                text "폐허 속 장애물을 피하고 끝까지 생존해 호감도를 획득하세요.\n결과 화면에서 이번 플레이로 얻은 총 호감도 보상을 확인할 수 있어요.":
                    font MG1_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

            # 보상 패널
            add MG1_REWARD_PANEL:
                xalign 0.93
                yalign 0.44
                at Transform(zoom=0.45)

            # 시작 버튼
            fixed:
                xalign 0.94
                yalign 0.95
                xsize 340
                ysize 140

                imagebutton:
                    idle Transform(MG1_BTN_IDLE,  zoom=MG1_BTN_ZOOM)
                    hover Transform(MG1_BTN_HOVER, zoom=MG1_BTN_ZOOM)
                    hovered [ Play("ui", SFX_UI_HOVER), SetScreenVariable("hover_help_start", True) ]
                    unhovered SetScreenVariable("hover_help_start", False)

                    action Jump("minigame1_play")
                    xalign 0.5
                    yalign 0.5

                text "게임 시작":
                    font MG1_FONT
                    size 30
                    color (MG1_TXT_HOVER if hover_help_start else MG1_TXT_IDLE)
                    xalign 0.5
                    yalign 0.5
                    yoffset (-MG1_TXT_LIFT if hover_help_start else 0)


##############################################################################
# Game1 PLAY (Runner)
##############################################################################

# ---------- ASSETS (PLAY) ----------
define MG1_BG_BASE = "minigames/game1/images/bg_game1_base.webp"
define MG1_BG_WALL = "minigames/game1/images/bg_game1_wall.webp"
define MG1_BG_ROAD = "minigames/game1/images/bg_game1_stone_road.webp"

# RUN (3프레임)
define MG1_RUN1   = "minigames/game1/images/run1.webp"
define MG1_RUN2   = "minigames/game1/images/run2.webp"
define MG1_RUN3   = "minigames/game1/images/run3.webp"

# JUMP (2프레임)
define MG1_JUMP1  = "minigames/game1/images/jump1.webp"
define MG1_JUMP2  = "minigames/game1/images/jump2.webp"

# SLIDE (2프레임)
define MG1_SLIDE1 = "minigames/game1/images/slide1.webp"
define MG1_SLIDE2 = "minigames/game1/images/slide2.webp"

# OBSTACLES
define MG1_OBS_ARROW   = "minigames/game1/images/obs_arrow.webp"
define MG1_OBS_SPEAR   = "minigames/game1/images/obs_spear.webp"
define MG1_OBS_LANTERN = "minigames/game1/images/obs_lantern.webp"
define MG1_OBS_TILE    = "minigames/game1/images/obs_tile.webp"
define MG1_OBS_ROCK    = "minigames/game1/images/obs_rock.webp"
define MG1_OBS_FIRE    = "minigames/game1/images/obs_fire.webp"

# SFX (game1 전용)
define SFX_MG1_JUMP  = "minigames/game1/sound/jump.mp3"
define SFX_MG1_SLIDE = "minigames/game1/sound/slide.mp3"
define SFX_MG1_CRASH = "minigames/game1/sound/crash.mp3"

# 공용 Result SFX 매핑 (common.rpy)
define SFX_MG1_WIN   = SFX_COMMON_WIN
define SFX_MG1_CLEAR = SFX_COMMON_CLEAR
define SFX_MG1_FAIL  = SFX_COMMON_FAIL
# SFX_UI_HOVER는 common.rpy 전역 사용

# HUD UI (COMMON) 매핑 (common.rpy)
define MG1_UI_SCROLL      = UI_SCROLL_SHORT
define MG1_UI_HEART       = UI_HEART
define MG1_UI_BROKEN      = UI_BROKEN_HEART
define MG1_UI_SCROLL_MED  = UI_SCROLL_MEDIUM

define MG1_UI_SCROLL_Z = 0.38
define MG1_UI_HEART_Z  = 0.07

# ---------- SCREEN ----------
define MG1_SW = 1920
define MG1_SH = 1080

# ---------- GAME CONST ----------
define MG1_DURATION = 20.0

# 속도
define MG1_WALL_SPEED = 90.0
define MG1_ROAD_SPEED = 360.0
define MG1_OBS_SPEED  = 700.0

# 스폰
define MG1_SPAWN_MIN = 1.50
define MG1_SPAWN_MAX = 2.00

# 스케일
define MG1_Z_BASE = 0.5
define MG1_Z_WALL = 0.5
define MG1_Z_ROAD = 0.5

define MG1_Z_PLAYER = 0.35
define MG1_Z_OBS_TOP = 0.16
define MG1_Z_OBS_BOTTOM = 0.16

define MG1_WALL_BAND_H = 648
define MG1_WALL_Y = 216
define MG1_ROAD_Y = 864

define MG1_PLAYER_X = 220
define MG1_GROUND_Y = 650

define MG1_JUMP_V0 = -980.0
define MG1_GRAVITY = 2600.0

define MG1_SLIDE_Y_EXTRA = 36

# ---------- HITBOX ----------
# RUN: 상단/하단 둘 다 닿게
define MG1_RUN_HIT_W = 360
define MG1_RUN_HIT_H = 620
define MG1_RUN_HIT_Y_OFFSET = 60

# SLIDE: 아래로 + 상단 안맞게
define MG1_SLIDE_HIT_W = 520
define MG1_SLIDE_HIT_H = 220
define MG1_SLIDE_HIT_Y_OFFSET = 210

# JUMP: 하단 안맞게
define MG1_JUMP_HIT_W = 360
define MG1_JUMP_HIT_H = 320
define MG1_JUMP_HIT_Y_OFFSET = 150

# 장애물 히트박스 비율
define MG1_OBS_HIT_FACTOR = 0.48


# ---------- ANIM CONST ----------
define MG1_RUN_FRAME_DT  = 0.10
define MG1_JUMP_FRAME_DT = 0.10

define MG1_SLIDE_ENTER_DT = 0.15
define MG1_SLIDE_EXIT_DT  = 0.25

# ---------- STATE ----------
default mg1_time_left = MG1_DURATION
default mg1_life = 3
default mg1_result = None
default mg1_show_result = False

default mg1_state = "run"         # "run" / "jump" / "slide"
default mg1_player_y = MG1_GROUND_Y
default mg1_vy = 0.0

default mg1_wall_off = 0.0
default mg1_road_off = 0.0

default mg1_obstacles = []
default mg1_next_spawn = 1.0
default mg1_invuln = 0.0

# 폭 캐시(1회 계산)
default mg1_bw = 0
default mg1_ww = 0
default mg1_rw = 0

# 애니 상태
default mg1_anim_t = 0.0
default mg1_run_i = 0
default mg1_jump_i = 0
default mg1_slide_phase = "none"
default mg1_slide_t = 0.0


# ---------- PYTHON ----------
init python:
    import random

    def mg1_fmt_time(t):
        s = int(max(0, t))
        mm = s // 60
        ss = s % 60
        return "%02d:%02d" % (mm, ss)

    def mg1_scaled_w(path, zoom, fallback=1920):
        try:
            w, h = renpy.image_size(path)
            return int(w * zoom)
        except:
            return fallback

    def mg1_aabb(ax, ay, aw, ah, bx, by, bw, bh):
        return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

    def mg1_player_hitbox():
        z = MG1_Z_PLAYER
        x = MG1_PLAYER_X

        if store.mg1_state == "slide":
            y = store.mg1_player_y + MG1_SLIDE_Y_EXTRA + int(MG1_SLIDE_HIT_Y_OFFSET * z)
            return (x, y, int(MG1_SLIDE_HIT_W * z), int(MG1_SLIDE_HIT_H * z))

        if store.mg1_state == "jump":
            y = store.mg1_player_y + int(MG1_JUMP_HIT_Y_OFFSET * z)
            return (x, y, int(MG1_JUMP_HIT_W * z), int(MG1_JUMP_HIT_H * z))

        y = store.mg1_player_y + int(MG1_RUN_HIT_Y_OFFSET * z)
        return (x, y, int(MG1_RUN_HIT_W * z), int(MG1_RUN_HIT_H * z))

    # 실제 이미지 크기 기반 + 상단 bottom-left 기준 히트박스
    def mg1_spawn():
        lane = random.choice(["top", "bottom"])

        if lane == "top":
            img = random.choice([MG1_OBS_ARROW, MG1_OBS_SPEAR, MG1_OBS_LANTERN])
            z = MG1_Z_OBS_TOP
            img_y = MG1_WALL_Y + 320
        else:
            img = random.choice([MG1_OBS_TILE, MG1_OBS_ROCK, MG1_OBS_FIRE])
            z = MG1_Z_OBS_BOTTOM
            img_y = MG1_ROAD_Y - int(1024 * z * 0.40)

        # 실제 원본 이미지 크기
        try:
            iw0, ih0 = renpy.image_size(img)
        except:
            iw0, ih0 = 1024, 1024

        # 스케일된 이미지 크기(디버그/기준용)
        img_w = int(iw0 * z)
        img_h = int(ih0 * z)

        # 히트박스 크기(원본 크기 기준)
        hit_w = int(iw0 * z * MG1_OBS_HIT_FACTOR)
        hit_h = int(ih0 * z * MG1_OBS_HIT_FACTOR)

        # 히트박스 y 배치
        if lane == "top":
            hit_y = img_y + img_h - hit_h   # bottom-left anchor
        else:
            hit_y = img_y                   # top-left anchor

        store.mg1_obstacles.append({
            "lane": lane,
            "img": img,
            "x": 2000,

            "img_y": img_y,   # 화면 표시용 y
            "y": hit_y,       # 판정용 y

            "z": z,
            "w": hit_w,
            "h": hit_h,
        })

    def mg1_do_jump():
        if store.mg1_state == "run":
            renpy.music.play(SFX_MG1_JUMP, channel="sfx")
            store.mg1_state = "jump"
            store.mg1_vy = MG1_JUMP_V0
            store.mg1_jump_i = 0
            store.mg1_anim_t = 0.0

    def mg1_slide_on():
        if store.mg1_state == "jump":
            return

        if store.mg1_state != "slide":
            renpy.music.play(SFX_MG1_SLIDE, channel="sfx")
            store.mg1_state = "slide"

        store.mg1_slide_phase = "enter"
        store.mg1_slide_t = 0.0

    def mg1_slide_off():
        if store.mg1_state != "slide":
            return

        store.mg1_slide_phase = "exit"
        store.mg1_slide_t = 0.0

    def mg1_tick(dt):
        if store.mg1_show_result:
            return

        store.mg1_anim_t += dt

        if store.mg1_state == "run":
            if store.mg1_anim_t >= MG1_RUN_FRAME_DT:
                store.mg1_anim_t -= MG1_RUN_FRAME_DT
                store.mg1_run_i = (store.mg1_run_i + 1) % 3

        elif store.mg1_state == "jump":
            if store.mg1_anim_t >= MG1_JUMP_FRAME_DT:
                store.mg1_anim_t -= MG1_JUMP_FRAME_DT
                store.mg1_jump_i = 1 - store.mg1_jump_i

        elif store.mg1_state == "slide":
            store.mg1_slide_t += dt

            if store.mg1_slide_phase == "enter":
                if store.mg1_slide_t >= MG1_SLIDE_ENTER_DT:
                    store.mg1_slide_phase = "hold"
                    store.mg1_slide_t = 0.0

            elif store.mg1_slide_phase == "exit":
                if store.mg1_slide_t >= MG1_SLIDE_EXIT_DT:
                    store.mg1_state = "run"
                    store.mg1_slide_phase = "none"
                    store.mg1_slide_t = 0.0
                    store.mg1_anim_t = 0.0

        # 무적시간
        if store.mg1_invuln > 0:
            store.mg1_invuln -= dt
            if store.mg1_invuln < 0:
                store.mg1_invuln = 0

        # 타이머
        store.mg1_time_left -= dt

        # 패럴럭스 이동
        store.mg1_wall_off += MG1_WALL_SPEED * dt
        store.mg1_road_off += MG1_ROAD_SPEED * dt

        # 점프 물리
        if store.mg1_state == "jump":
            store.mg1_vy += MG1_GRAVITY * dt
            store.mg1_player_y += store.mg1_vy * dt
            if store.mg1_player_y >= MG1_GROUND_Y:
                store.mg1_player_y = MG1_GROUND_Y
                store.mg1_state = "run"
                store.mg1_anim_t = 0.0

        # 스폰
        store.mg1_next_spawn -= dt
        if store.mg1_next_spawn <= 0:
            mg1_spawn()
            store.mg1_next_spawn = random.uniform(MG1_SPAWN_MIN, MG1_SPAWN_MAX)

        # 장애물 이동/충돌
        new_obs = []
        px, py, pw, ph = mg1_player_hitbox()

        for o in store.mg1_obstacles:
            o["x"] -= MG1_OBS_SPEED * dt
            if o["x"] > -300:
                if store.mg1_invuln <= 0 and mg1_aabb(px, py, pw, ph, o["x"], o["y"], o["w"], o["h"]):
                    renpy.music.play(SFX_MG1_CRASH, channel="sfx")
                    store.mg1_life -= 1
                    store.mg1_invuln = 0.8
                else:
                    new_obs.append(o)

        store.mg1_obstacles = new_obs

        # 종료
        if store.mg1_life <= 0:
            store.mg1_result = "fail"
            store.mg1_show_result = True
        elif store.mg1_time_left <= 0:
            store.mg1_result = "success"
            store.mg1_show_result = True


# ---------- ENTRY ----------
label minigame1_play:
    $ mg1_time_left = MG1_DURATION
    $ mg1_life = 3
    $ mg1_result = None
    $ mg1_show_result = False

    $ mg1_state = "run"
    $ mg1_player_y = MG1_GROUND_Y
    $ mg1_vy = 0.0

    $ mg1_wall_off = 0.0
    $ mg1_road_off = 0.0

    $ mg1_obstacles = []
    $ mg1_next_spawn = 0.75
    $ mg1_invuln = 0.0

    $ mg1_anim_t = 0.0
    $ mg1_run_i = 0
    $ mg1_jump_i = 0
    $ mg1_slide_phase = "none"
    $ mg1_slide_t = 0.0

    $ mg1_bw = mg1_scaled_w(MG1_BG_BASE, MG1_Z_BASE, 1920)
    $ mg1_ww = mg1_scaled_w(MG1_BG_WALL, MG1_Z_WALL, 1152)
    $ mg1_rw = mg1_scaled_w(MG1_BG_ROAD, MG1_Z_ROAD, 1487)

    call screen mg1_game
    call screen mg1_result_popup
    return


# ---------- SCREEN (PLAY) ----------
screen mg1_game():
    tag mg1
    modal True

    if mg1_show_result:
        timer 0.01 action Return()

    # 안정적인 60fps 업데이트
    if not mg1_show_result:
        timer (1.0/60.0) repeat True action Function(mg1_tick, (1.0/60.0))

    # 입력
    key "K_UP" action Function(mg1_do_jump)
    key "K_w"  action Function(mg1_do_jump)

    key "K_DOWN" action Function(mg1_slide_on)
    key "K_s"    action Function(mg1_slide_on)
    key "keyup_K_DOWN" action Function(mg1_slide_off)
    key "keyup_K_s"    action Function(mg1_slide_off)

    # BASE
    add Transform(MG1_BG_BASE, zoom=MG1_Z_BASE) xoffset 0

    # WALL (4장)
    $ ww = (mg1_ww if mg1_ww > 0 else 1152)
    $ wx = int(mg1_wall_off) % ww
    viewport:
        xpos 0 ypos MG1_WALL_Y
        xsize MG1_SW ysize MG1_WALL_BAND_H
        clipping True
        add Transform(MG1_BG_WALL, zoom=MG1_Z_WALL) xoffset -wx
        add Transform(MG1_BG_WALL, zoom=MG1_Z_WALL) xoffset -wx + ww
        add Transform(MG1_BG_WALL, zoom=MG1_Z_WALL) xoffset -wx + ww * 2
        add Transform(MG1_BG_WALL, zoom=MG1_Z_WALL) xoffset -wx + ww * 3

    # ROAD (4장)
    $ rw = (mg1_rw if mg1_rw > 0 else 1487)
    $ rx = int(mg1_road_off) % rw
    add Transform(MG1_BG_ROAD, zoom=MG1_Z_ROAD) xoffset -rx ypos MG1_ROAD_Y
    add Transform(MG1_BG_ROAD, zoom=MG1_Z_ROAD) xoffset -rx + rw ypos MG1_ROAD_Y
    add Transform(MG1_BG_ROAD, zoom=MG1_Z_ROAD) xoffset -rx + rw * 2 ypos MG1_ROAD_Y
    add Transform(MG1_BG_ROAD, zoom=MG1_Z_ROAD) xoffset -rx + rw * 3 ypos MG1_ROAD_Y

    # HUD (Scroll + Hearts) - left top
    fixed:
        xpos 20
        ypos 18

        # 두루마리
        add Transform(MG1_UI_SCROLL, zoom=MG1_UI_SCROLL_Z)

        # TIME (두루마리 안)
        text "[mg1_fmt_time(mg1_time_left)]":
            font MG1_FONT
            size 55
            color "#111111"
            outlines [ (3, "#FFFFFF88", 0, 0) ]
            xpos 70
            ypos 70

        # HEARTS (두루마리 안, 3개 고정)
        hbox:
            xpos 46
            ypos 140
            spacing -8

            for i in range(3):
                if i < mg1_life:
                    add Transform(MG1_UI_HEART, zoom=MG1_UI_HEART_Z)
                else:
                    add Transform(MG1_UI_BROKEN, zoom=MG1_UI_HEART_Z)

    # OBSTACLES (그림은 img_y 기준)
    for o in mg1_obstacles:
        add Transform(o["img"], zoom=o["z"]) xpos int(o["x"]) ypos int(o.get("img_y", o["y"]))

    # PLAYER
    # 무적 중이면 0.1초 간격으로 표시/숨김
    $ _blink = (mg1_invuln > 0.0 and int(mg1_invuln * 10) % 2 == 0)

    if not _blink:

        if mg1_state == "run":
            $ run_img = (MG1_RUN1 if mg1_run_i == 0 else (MG1_RUN2 if mg1_run_i == 1 else MG1_RUN3))
            add Transform(run_img, zoom=MG1_Z_PLAYER) xpos MG1_PLAYER_X ypos int(mg1_player_y)

        elif mg1_state == "jump":
            $ jump_img = (MG1_JUMP1 if mg1_jump_i == 0 else MG1_JUMP2)
            add Transform(jump_img, zoom=MG1_Z_PLAYER) xpos MG1_PLAYER_X ypos int(mg1_player_y)

        else:
            if mg1_slide_phase == "enter":
                $ slide_img = MG1_SLIDE1
            else:
                $ slide_img = MG1_SLIDE2
            add Transform(slide_img, zoom=MG1_Z_PLAYER) xpos MG1_PLAYER_X ypos int(mg1_player_y + MG1_SLIDE_Y_EXTRA + 55)


# ---------- RESULT ----------
screen mg1_result_popup():
    tag mg1
    modal True
    zorder 200

    default hover_proceed = False

    # 점수 계산
    $ _reward = (5 if mg1_life >= 3 else (3 if mg1_life >= 1 else 0))
    if mg1_result != "success":
        $ _reward = 0

    $ _result_sfx = (
        SFX_MG1_WIN   if _reward == 5 else
        SFX_MG1_CLEAR if _reward > 0 else
        SFX_MG1_FAIL
    )

    on "show" action Play("result", _result_sfx)

    add MG1_BG_BG:
        fit "cover"

    add Solid("#0008")

    # =========================
    # 결과 패널 (두루마리)
    # =========================
    fixed:
        xalign 0.5
        yalign 0.55
        xsize 1200
        ysize 600

        add Transform(MG1_UI_SCROLL_MED, zoom=0.75):
            xalign 0.5
            yalign 0.5

        # ----- 내용 -----
        text "게임 결과":
            font MG1_FONT
            size 60
            color "#111111"
            outlines [ (4, "#FFFFFF88", 0, 0) ]
            xalign 0.5
            yalign 0.24

        text "+[_reward]":
            font MG1_FONT
            size 80
            color "#E53935"
            outlines [ (4, "#FFFFFF88", 0, 0) ]
            xalign 0.5
            yalign 0.44

        # 하트
        hbox:
            xalign 0.5
            yalign 0.63
            spacing -8

            for i in range(3):
                if i < mg1_life and mg1_result == "success":
                    add Transform(MG1_UI_HEART, zoom=MG1_UI_HEART_Z + 0.03)
                else:
                    add Transform(MG1_UI_BROKEN, zoom=MG1_UI_HEART_Z + 0.03)

        # =========================
        # 진행하기 버튼
        # =========================
        fixed:
            xalign 0.5
            yalign 0.78
            xsize 340
            ysize 140

            button:
                xalign 0.5
                yalign 0.5
                xsize 340
                ysize 140

                background Transform(MG1_BTN_IDLE,  zoom=MG1_BTN_ZOOM,  xoffset=30, yoffset=55)
                hover_background Transform(MG1_BTN_HOVER, zoom=MG1_BTN_ZOOM,  xoffset=30,   yoffset=55)
                focus_mask True

                hovered [ Play("ui", SFX_UI_HOVER), SetScreenVariable("hover_proceed", True) ]
                unhovered SetScreenVariable("hover_proceed", False)

                action Return()

                text "진행하기":
                    font MG1_FONT
                    size 30
                    color (MG1_TXT_HOVER if hover_proceed else MG1_TXT_IDLE)
                    xalign 0.5
                    yalign 0.85
                    yoffset (-MG1_TXT_LIFT if hover_proceed else 0)
