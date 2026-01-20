# game/minigames/game4/game4.rpy

##############################################################################
# Minigame 4 : 하나의 진실
# - Main / Help / Game / Result Screen
# - common.rpy 공용 상수 사용 (MG4_*로 매핑)
##############################################################################

# ---------- CHANNELS ----------
init -10 python:
    renpy.music.register_channel("mg4_sfx",    "sfx", loop=False)
    renpy.music.register_channel("mg4_ui",     "sfx", loop=False)
    renpy.music.register_channel("mg4_result", "sfx", loop=False)


# ---------- ASSETS ----------
define MG4_BG_BG     = "minigames/game4/images/bg_game4_bg.webp"

# 공용 UI 에셋 매핑 (common.rpy)
define MG4_BTN_IDLE  = UI_BTN_IDLE
define MG4_BTN_HOVER = UI_BTN_HOVER

define MG4_SPARKLE_0 = UI_SPARKLE_0
define MG4_SPARKLE_1 = UI_SPARKLE_1
define MG4_SPARKLE_2 = UI_SPARKLE_2

define MG4_UI_SCROLL_SHORT  = UI_SCROLL_SHORT
define MG4_UI_SCROLL_MEDIUM = UI_SCROLL_MEDIUM

define MG4_FONT = UI_FONT

# button
define MG4_BTN_ZOOM = 0.55

# text
define MG4_TXT_IDLE  = "#444444"
define MG4_TXT_HOVER = "#FFFFFF"
define MG4_TXT_LIFT  = 2

# theme
define MG4_TITLE_COLOR = "#FFDF6A"

# sfx (game4 전용)
define SFX_MG4_CORRECT = "minigames/game4/sound/correct.mp3"
define SFX_MG4_WRONG   = "minigames/game4/sound/wrong.mp3"

# HUD zoom
define MG4_HUD_SCROLL_Z = 0.35

# 클릭 눌림 연출 유지 시간
define MG4_CLICK_FX_DT = 0.08

# 눌림 연출 강도
define MG4_PRESS_Y = 7
define MG4_PRESS_Z = 0.98


# ---------- TILE FEEL (HOVER ONLY; PRESS IS FORCED BY CLICK_FX) ----------
transform mg4_tile_feel():
    on hover:
        yoffset -2
    on idle:
        yoffset 0
        zoom 1.0
    on insensitive:
        yoffset 0
        zoom 1.0


# ---------- GAME CONFIG / LOGIC ----------
init -5 python:
    import random

    # 초(float) → "MM:SS"
    def mg4_format_time(t):
        t = int(max(0, t))
        m = t // 60
        s = t % 60
        return "%02d:%02d" % (m, s)

    # 스테이지: 2x2 ~ 6x6
    # 제한 시간:
    # 1: 5s, 2: 8s, 3: 11s, 4: 14s, 5: 17s
    MG4_STAGE_CFG = {
        1: {"rows": 2, "cols": 2, "time": 5.0},
        2: {"rows": 3, "cols": 3, "time": 8.0},
        3: {"rows": 4, "cols": 4, "time": 11.0},
        4: {"rows": 5, "cols": 5, "time": 14.0},
        5: {"rows": 6, "cols": 6, "time": 17.0},
    }

    # 이미지 쌍
    MG4_STAGE_BASE_IMAGES = {
        1: "minigames/game4/images/apple1.webp",
        2: "minigames/game4/images/plumblossom1.webp",
        3: "minigames/game4/images/necklace1.webp",
        4: "minigames/game4/images/waves1.webp",
        5: "minigames/game4/images/leopard1.webp",
    }
    MG4_STAGE_DIFF_IMAGES = {
        1: "minigames/game4/images/apple2.webp",
        2: "minigames/game4/images/plumblossom2.webp",
        3: "minigames/game4/images/necklace2.webp",
        4: "minigames/game4/images/waves2.webp",
        5: "minigames/game4/images/leopard2.webp",
    }

    def mg4_get_cfg(stage):
        return MG4_STAGE_CFG.get(stage, MG4_STAGE_CFG[5])

    def mg4_pick_answer(rows, cols):
        return random.randrange(rows * cols)

    def mg4_setup_stage(stage):
        store.mg4_stage = stage
        cfg = mg4_get_cfg(stage)
        store.mg4_rows = cfg["rows"]
        store.mg4_cols = cfg["cols"]
        store.mg4_time_left = cfg["time"]
        store.mg4_answer_index = mg4_pick_answer(store.mg4_rows, store.mg4_cols)

    def mg4_calc_sparkle(best_stage):
        if best_stage >= 5:
            return 2
        elif best_stage >= 3:
            return 1
        else:
            return 0

    # ---------- 클릭 연출 큐 ----------
    def mg4_queue_click_fx(idx, is_correct):
        # 이미 전환/연출 중이면 무시
        if store.mg4_done or store.mg4_exit_pending or store.mg4_next_stage_pending or store.mg4_click_fx_pending:
            return

        # 즉시 사운드
        if is_correct:
            renpy.sound.play(SFX_MG4_CORRECT, channel="mg4_sfx")
        else:
            renpy.sound.play(SFX_MG4_WRONG, channel="mg4_sfx")

        # 즉시 시간/입력 정지(화면 쪽 조건으로 멈춤)
        store.mg4_click_fx_pending = True
        store.mg4_click_fx_index = idx
        store.mg4_click_fx_correct = is_correct

        renpy.restart_interaction()

    # ---------- 판정/전환 제어 ----------
    def mg4_mark_fail(play_sfx=False):
        if store.mg4_done:
            return
        store.mg4_done = True

        store.mg4_exit_pending = True
        store.mg4_exit_delay = 1.0

        if play_sfx:
            renpy.sound.play(SFX_MG4_WRONG, channel="mg4_sfx")

        # ----- 결과 판정 -----
        store.mg4_result_stage = store.mg4_best_stage
        store.mg4_result_sparkle = mg4_calc_sparkle(store.mg4_best_stage)

    def mg4_mark_timeout():
        # 타임아웃은 즉시 wrong 재생
        mg4_mark_fail(play_sfx=True)

    def mg4_advance_stage(play_sfx=False):
        # play_sfx는 클릭이 아닌 호출에서만. 클릭은 queue에서 이미 재생됨
        if store.mg4_done:
            return

        if play_sfx:
            renpy.sound.play(SFX_MG4_CORRECT, channel="mg4_sfx")

        if store.mg4_stage > store.mg4_best_stage:
            store.mg4_best_stage = store.mg4_stage

        # 최종 스테이지 성공 -> 결과로 나가기
        if store.mg4_stage >= 5:
            store.mg4_done = True
            store.mg4_exit_pending = True
            store.mg4_exit_delay = 1.0

            store.mg4_result_stage = 5
            store.mg4_result_sparkle = mg4_calc_sparkle(5)
            return

        # 다음 스테이지 예약
        store.mg4_next_stage_pending = True


# ---------- RUNTIME VARS ----------
default mg4_stage = 1
default mg4_best_stage = 0
default mg4_time_left = 0.0
default mg4_answer_index = 0
default mg4_rows = 0
default mg4_cols = 0

default mg4_done = False

default mg4_result_stage = 0
default mg4_result_sparkle = 0

# 딜레이 제어 플래그
default mg4_exit_pending = False
default mg4_exit_delay = 0.0
default mg4_next_stage_pending = False

# 클릭 눌림 연출
default mg4_click_fx_pending = False
default mg4_click_fx_index = -1
default mg4_click_fx_correct = False


# ---------- LABELS ----------
label minigame4_main:
    $ _old_quick_menu = quick_menu
    $ quick_menu = False
    call screen mg4_main
    $ quick_menu = _old_quick_menu
    return

label minigame4_help:
    call screen mg4_help
    jump minigame4_main

label minigame4_play:
    $ mg4_best_stage = 0
    $ mg4_done = False
    $ mg4_result_stage = 0
    $ mg4_result_sparkle = 0

    $ mg4_exit_pending = False
    $ mg4_exit_delay = 0.0
    $ mg4_next_stage_pending = False

    $ mg4_click_fx_pending = False
    $ mg4_click_fx_index = -1
    $ mg4_click_fx_correct = False

    $ mg4_setup_stage(1)

    # 게임 화면
    call screen mg4_game

    # 결과 화면
    call screen mg4_result

    jump minigame4_main


# ---------- SCREENS (MAIN) ----------
screen mg4_main():
    tag mg4
    modal True

    default hover_help = False
    default hover_start = False

    add MG4_BG_BG:
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

            text "하나의 진실":
                font MG4_FONT
                size 110
                color MG4_TITLE_COLOR
                outlines [ (7, "#000000", 0, 0) ]
                xalign 0.5
                yalign 0.22
                textalign 0.5

            hbox:
                spacing 80
                xalign 0.5
                yalign 0.90

                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG4_BTN_IDLE,  zoom=MG4_BTN_ZOOM)
                        hover Transform(MG4_BTN_HOVER, zoom=MG4_BTN_ZOOM)
                        hovered [ Play("mg4_ui", SFX_UI_HOVER), SetScreenVariable("hover_help", True) ]
                        unhovered SetScreenVariable("hover_help", False)
                        action Jump("minigame4_help")
                        xalign 0.5
                        yalign 0.5

                    text "게임 설명":
                        font MG4_FONT
                        size 30
                        color (MG4_TXT_HOVER if hover_help else MG4_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG4_TXT_LIFT if hover_help else 0)

                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG4_BTN_IDLE,  zoom=MG4_BTN_ZOOM)
                        hover Transform(MG4_BTN_HOVER, zoom=MG4_BTN_ZOOM)
                        hovered [ Play("mg4_ui", SFX_UI_HOVER), SetScreenVariable("hover_start", True) ]
                        unhovered SetScreenVariable("hover_start", False)
                        action Jump("minigame4_play")
                        xalign 0.5
                        yalign 0.5

                    text "게임 시작":
                        font MG4_FONT
                        size 30
                        color (MG4_TXT_HOVER if hover_start else MG4_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG4_TXT_LIFT if hover_start else 0)


# ---------- SCREENS (HELP) ----------
screen mg4_help():
    tag mg4
    modal True

    default hover_help_start = False

    add MG4_BG_BG:
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
                text_font MG4_FONT
                text_size 32
                text_color "#FFFFFF"
                text_hover_color "#DDDDDD"
                hovered Play("mg4_ui", SFX_UI_HOVER)
                action Jump("minigame4_main")
                xalign 0.985
                yalign 0.02

            vbox:
                xpos 40
                ypos 30
                xmaximum 1100
                spacing 18

                text "게임 설명":
                    font MG4_FONT
                    size 70
                    color "#111111"
                    outlines [ (2, "#FFFFFF88", 0, 0) ]

                null height 16

                text "격자 속 여러 그림들 중 단 하나만 다른 그림이 숨어 있어요.\n모양과 색을 꼼꼼히 살펴보고, 유일하게 다른 그 한 칸을 정확하게 찾아 클릭해보세요!":
                    font MG4_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

                text "{size=34}게임 규칙{/size}":
                    font MG4_FONT
                    color "#111111"

                text "1. 똑같아 보이는 그림 중, 미세하게 다른 하나를 찾아 클릭하세요.\n2. 정답을 누르면 즉시 다음 단계로 이동합니다.\n3. 오답을 누르거나 제한 시간이 0초가 되면 즉시 실패합니다.\n4. 단계가 올라갈수록 목패가 증가해 난이도가 상승합니다.\n5. '최종 성공 단계' 기준으로 보상을 획득합니다.":
                    font MG4_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

                text "{size=34}게임 목표{/size}":
                    font MG4_FONT
                    color "#111111"

                text "각 단계에서 하나의 진실을 빠르고 정확하게 찾아 클릭하세요!\n결과 화면에서 진행된 단계 수와 최종 보상을 확인할 수 있어요.\n화야진이 당신을 바라보는 눈빛을 조금씩 바꾸게 되도록 집중해보세요.":
                    font MG4_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

            fixed:
                xalign 0.94
                yalign 0.95
                xsize 340
                ysize 140

                imagebutton:
                    idle Transform(MG4_BTN_IDLE,  zoom=MG4_BTN_ZOOM)
                    hover Transform(MG4_BTN_HOVER, zoom=MG4_BTN_ZOOM)
                    hovered [ Play("mg4_ui", SFX_UI_HOVER), SetScreenVariable("hover_help_start", True) ]
                    unhovered SetScreenVariable("hover_help_start", False)
                    action Jump("minigame4_play")
                    xalign 0.5
                    yalign 0.5

                text "게임 시작":
                    font MG4_FONT
                    size 30
                    color (MG4_TXT_HOVER if hover_help_start else MG4_TXT_IDLE)
                    xalign 0.5
                    yalign 0.5
                    yoffset (-MG4_TXT_LIFT if hover_help_start else 0)


# ---------- SCREENS (GAME) ----------
screen mg4_game():
    tag mg4
    modal True
    zorder 100

    add MG4_BG_BG:
        fit "cover"
    add Solid("#0006")

    # CLICK FX
    if mg4_click_fx_pending:
        timer MG4_CLICK_FX_DT action [
            SetVariable("mg4_click_fx_pending", False),
            If(mg4_click_fx_correct, Function(mg4_advance_stage, False), Function(mg4_mark_fail, False)),
            SetVariable("mg4_click_fx_index", -1)
        ]

    # EXIT / NEXT STAGE TIMERS
    if mg4_exit_pending:
        timer mg4_exit_delay action Return()

    if mg4_next_stage_pending:
        timer 0.7 action [
            SetVariable("mg4_next_stage_pending", False),
            Function(mg4_setup_stage, mg4_stage + 1),
            Function(renpy.restart_interaction)
        ]

    # ========== 타이머 ==========
    # 클릭 연출 중에도 시간 멈춤
    if (not mg4_done) and (not mg4_exit_pending) and (not mg4_next_stage_pending) and (not mg4_click_fx_pending):
        timer 0.1 repeat True action [
            SetVariable("mg4_time_left", max(0.0, mg4_time_left - 0.1)),
            If(mg4_time_left <= 0.0, Function(mg4_mark_timeout))
        ]

    # =========================
    # HUD
    # =========================
    fixed:
        xpos 30
        ypos 20

        add Transform(MG4_UI_SCROLL_SHORT, zoom=MG4_HUD_SCROLL_Z)

        text "[mg4_stage] 단계":
            font MG4_FONT
            size 32
            color "#111111"
            outlines [ (2, "#FFFFFF88", 0, 0) ]
            xpos 88
            ypos 70

        text "[mg4_format_time(mg4_time_left)]":
            font MG4_FONT
            size 40
            color "#111111"
            outlines [ (2, "#FFFFFF88", 0, 0) ]
            xpos 76
            ypos 125

    # =========================
    # 보드
    # =========================
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1080
        ysize 1080
        background Solid("#FFFFFF22")
        padding (30, 30)

        $ board_w = 1080 - 60
        $ board_h = 1080 - 60
        $ gap = 6

        $ cell_size_w = int((board_w - (mg4_cols - 1) * gap) / float(mg4_cols))
        $ cell_size_h = int((board_h - (mg4_rows - 1) * gap) / float(mg4_rows))
        $ cell_size = min(cell_size_w, cell_size_h)
        $ cell_size = max(64, min(cell_size, 400))

        vpgrid:
            rows mg4_rows
            cols mg4_cols
            spacing gap
            xalign 0.5
            yalign 0.5

            for i in range(mg4_rows * mg4_cols):
                $ base_img = MG4_STAGE_BASE_IMAGES[mg4_stage]
                $ diff_img = MG4_STAGE_DIFF_IMAGES[mg4_stage]

                $ locked = (mg4_done or mg4_exit_pending or mg4_next_stage_pending or mg4_click_fx_pending)
                $ is_pressed_fx = (mg4_click_fx_pending and mg4_click_fx_index == i)

                if i == mg4_answer_index:
                    button:
                        xysize (cell_size, cell_size)
                        focus_mask True
                        at mg4_tile_feel()
                        sensitive not locked

                        action Function(mg4_queue_click_fx, i, True)

                        add Transform(
                            diff_img,
                            xysize=(cell_size, cell_size),
                            fit="cover",
                            yoffset=(MG4_PRESS_Y if is_pressed_fx else 0),
                            zoom=(MG4_PRESS_Z if is_pressed_fx else 1.0)
                        )

                else:
                    button:
                        xysize (cell_size, cell_size)
                        focus_mask True
                        at mg4_tile_feel()
                        sensitive not locked

                        action Function(mg4_queue_click_fx, i, False)

                        add Transform(
                            base_img,
                            xysize=(cell_size, cell_size),
                            fit="cover",
                            yoffset=(MG4_PRESS_Y if is_pressed_fx else 0),
                            zoom=(MG4_PRESS_Z if is_pressed_fx else 1.0)
                        )


# ---------- RESULT ----------
screen mg4_result():
    tag mg4
    modal True
    zorder 200

    # 결과 화면 진입 시 사운드 재생 (common.rpy)
    on "show" action If(
        mg4_result_stage >= 5,
        Play("mg4_result", SFX_COMMON_WIN),
        If(
            mg4_result_stage >= 3,
            Play("mg4_result", SFX_COMMON_CLEAR),
            Play("mg4_result", SFX_COMMON_FAIL)
        )
    )

    default hover_proceed = False

    add MG4_BG_BG:
        fit "cover"
    add Solid("#0008")

    fixed:
        xalign 0.5
        yalign 0.55
        xsize 1200
        ysize 600

        add Transform(MG4_UI_SCROLL_MEDIUM, zoom=0.88):
            xalign 0.5
            yalign 0.5

        text "게임 결과":
            font MG4_FONT
            size 60
            color "#111111"
            outlines [ (4, "#FFFFFF88", 0, 0) ]
            xalign 0.5
            yalign 0.24

        text "최종 성공 단계: [mg4_result_stage]":
            font MG4_FONT
            size 34
            color "#111111"
            outlines [ (2, "#FFFFFF88", 0, 0) ]
            xalign 0.5
            yalign 0.40

        fixed:
            xalign 0.5
            yalign 0.65
            xsize 260
            ysize 260

            if mg4_result_sparkle <= 0:
                add Transform(MG4_SPARKLE_0, zoom=0.9) xalign 0.5 yalign 0.5
            elif mg4_result_sparkle == 1:
                add Transform(MG4_SPARKLE_1, zoom=0.9) xalign 0.5 yalign 0.5
            else:
                add Transform(MG4_SPARKLE_2, zoom=0.9) xalign 0.5 yalign 0.5

        fixed:
            xalign 0.5
            yalign 0.80
            xsize 340
            ysize 140

            button:
                xalign 0.5
                yalign 0.5
                xsize 340
                ysize 140

                background Transform(MG4_BTN_IDLE,  zoom=MG4_BTN_ZOOM,  xoffset=30, yoffset=55)
                hover_background Transform(MG4_BTN_HOVER, zoom=MG4_BTN_ZOOM, xoffset=30, yoffset=55)
                focus_mask True

                hovered [ Play("mg4_ui", SFX_UI_HOVER), SetScreenVariable("hover_proceed", True) ]
                unhovered SetScreenVariable("hover_proceed", False)

                action Return()

                text "진행하기":
                    font MG4_FONT
                    size 30
                    color (MG4_TXT_HOVER if hover_proceed else MG4_TXT_IDLE)
                    xalign 0.5
                    yalign 0.85
                    yoffset (-MG4_TXT_LIFT if hover_proceed else 0)
