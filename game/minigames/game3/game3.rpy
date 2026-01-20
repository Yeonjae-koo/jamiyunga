# game/minigames/game3/game3.rpy

##############################################################################
# Minigame 3 : 어둠 속 갈림길
# - Main / Help / Play / Result
# - common.rpy 공용 상수 사용 (MG3_*로 매핑)
##############################################################################

# ---------- CHANNELS ----------
init -10 python:
    renpy.music.register_channel("mg3_sfx",    "sfx", loop=False)
    renpy.music.register_channel("mg3_ui",     "sfx", loop=False)
    renpy.music.register_channel("mg3_result", "sfx", loop=False)


# ---------- ASSETS (MAIN/HELP) ----------
define MG3_BG_BG        = "minigames/game3/images/bg_game3_bg.webp"

# 공용 UI 에셋 매핑 (common.rpy)
define MG3_BTN_IDLE     = UI_BTN_IDLE
define MG3_BTN_HOVER    = UI_BTN_HOVER
define MG3_FONT         = UI_FONT

define MG3_BTN_ZOOM = 0.55

define MG3_TXT_IDLE  = "#444444"
define MG3_TXT_HOVER = "#FFFFFF"
define MG3_TXT_LIFT  = 2

define MG3_TITLE_COL = "#9D5E3E"

# reward sparkles (common.rpy)
define MG3_SPARKLE_0 = UI_SPARKLE_0
define MG3_SPARKLE_1 = UI_SPARKLE_1
define MG3_SPARKLE_2 = UI_SPARKLE_2


# ---------- LABELS ----------
label minigame3_main:
    $ _old_quick_menu = quick_menu
    $ quick_menu = False

    call screen mg3_main

    $ quick_menu = _old_quick_menu
    return

label minigame3_help:
    call screen mg3_help
    jump minigame3_main


# ---------- SCREENS (MAIN) ----------
screen mg3_main():
    tag mg3
    modal True

    default hover_help = False
    default hover_start = False

    add MG3_BG_BG:
        fit "cover"

    add Solid("#0007")

    frame:
        xalign 0.5
        yalign 0.55
        xsize 1280
        ysize 640
        background Solid("#FFFFFF33")
        padding (80, 70)

        fixed:
            xfill True
            yfill True

            text "어둠 속 갈림길":
                font MG3_FONT
                size 110
                color MG3_TITLE_COL
                outlines [ (8, "#000000", 0, 0) ]
                xalign 0.5
                yalign 0.28
                textalign 0.5

            hbox:
                spacing 90
                xalign 0.5
                yalign 0.82

                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG3_BTN_IDLE,  zoom=MG3_BTN_ZOOM)
                        hover Transform(MG3_BTN_HOVER, zoom=MG3_BTN_ZOOM)
                        hovered [ Play("mg3_ui", SFX_UI_HOVER), SetScreenVariable("hover_help", True) ]
                        unhovered SetScreenVariable("hover_help", False)
                        action Jump("minigame3_help")
                        xalign 0.5
                        yalign 0.5

                    text "게임 설명":
                        font MG3_FONT
                        size 30
                        color (MG3_TXT_HOVER if hover_help else MG3_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG3_TXT_LIFT if hover_help else 0)

                fixed:
                    xsize 340
                    ysize 140

                    imagebutton:
                        idle Transform(MG3_BTN_IDLE,  zoom=MG3_BTN_ZOOM)
                        hover Transform(MG3_BTN_HOVER, zoom=MG3_BTN_ZOOM)
                        hovered [ Play("mg3_ui", SFX_UI_HOVER), SetScreenVariable("hover_start", True) ]
                        unhovered SetScreenVariable("hover_start", False)
                        action Jump("minigame3_play")
                        xalign 0.5
                        yalign 0.5

                    text "게임 시작":
                        font MG3_FONT
                        size 30
                        color (MG3_TXT_HOVER if hover_start else MG3_TXT_IDLE)
                        xalign 0.5
                        yalign 0.5
                        yoffset (-MG3_TXT_LIFT if hover_start else 0)


# ---------- SCREENS (HELP) ----------
screen mg3_help():
    tag mg3
    modal True

    default hover_start = False

    add MG3_BG_BG:
        fit "cover"

    add Solid("#0007")

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
                text_font MG3_FONT
                text_size 32
                text_color "#FFFFFF"
                text_hover_color "#DDDDDD"
                hovered Play("mg3_ui", SFX_UI_HOVER)
                action Jump("minigame3_main")
                xalign 0.985
                yalign 0.02

            vbox:
                xpos 40
                ypos 30
                xmaximum 1000
                spacing 18

                text "게임 설명":
                    font MG3_FONT
                    size 70
                    color "#111111"
                    outlines [ (2, "#FFFFFF88", 0, 0) ]

                null height 20

                text (
                    "어둠이 짙게 내려앉은 복도, 두 개의 문이 당신을 기다리고 있습니다.\n"
                    "두 문은 거의 똑같아 보이지만 그 중 하나는 어딘가 미묘하게 이상한 문.\n"
                    "세 번의 갈림길 중 단 한 번이라도 올바른 문을 고른다면 무사히 나아갈 수 있어요.\n\n"
                    "{size=34}게임 규칙{/size}\n"
                    "1. 매 라운드 두 개의 문이 등장하며, 그중 하나만 자연스러운 '정상 문'이에요.\n"
                    "2. 총 3라운드를 진행하며, 3번 모두 잘못 고른 경우 화야진에게 들켜 실패해요.\n"
                    "3. 라운드가 올라갈수록 차이가 점점 교묘해지고 눈썰미가 더 필요해져요.\n\n"
                    "{size=34}목표{/size}\n"
                    "3번의 선택을 끝까지 버티고 단 한 번이라도 올바른 문을 찾아 생존하세요.\n"
                    "혹은… 잘못된 문만 골라 어둠에 잠기게 될 수도 있겠죠.\n"
                    "그가 당신을 '어떻게 평가할지'… 선택의 결과에 따라 달라질 거예요.\n"
                ):
                    font MG3_FONT
                    size 26
                    color "#111111"
                    line_spacing 10

            fixed:
                xalign 0.94
                yalign 0.95
                xsize 340
                ysize 140

                imagebutton:
                    idle Transform(MG3_BTN_IDLE,  zoom=MG3_BTN_ZOOM)
                    hover Transform(MG3_BTN_HOVER, zoom=MG3_BTN_ZOOM)
                    hovered [ Play("mg3_ui", SFX_UI_HOVER), SetScreenVariable("hover_start", True) ]
                    unhovered SetScreenVariable("hover_start", False)
                    action Jump("minigame3_play")
                    xalign 0.5
                    yalign 0.5

                text "게임 시작":
                    font MG3_FONT
                    size 30
                    color (MG3_TXT_HOVER if hover_start else MG3_TXT_IDLE)
                    xalign 0.5
                    yalign 0.5
                    yoffset (-MG3_TXT_LIFT if hover_start else 0)


##############################################################################
# Game3 PLAY
##############################################################################

# ---------- ASSETS (PLAY) ----------
define MG3_DOOR_NORMAL         = "minigames/game3/images/door1.webp"
define MG3_DOOR_HANDLE_REVERSE = "minigames/game3/images/door2.webp"
define MG3_DOOR_NO_HINGE       = "minigames/game3/images/door3.webp"
define MG3_DOOR_SHADOW_REVERSE = "minigames/game3/images/door4.webp"

# 공용 UI 에셋 매핑 (common.rpy)
define MG3_UI_SCROLL     = UI_SCROLL_SHORT
define MG3_UI_HEART      = UI_HEART
define MG3_UI_BROKEN     = UI_BROKEN_HEART

define SFX_MG3_DOOR1 = "minigames/game3/sound/door1.mp3"
define SFX_MG3_DOOR2 = "minigames/game3/sound/door2.mp3"
define SFX_MG3_DOOR3 = "minigames/game3/sound/door3.mp3"
define SFX_MG3_DOOR4 = "minigames/game3/sound/door4.mp3"

# ---------- TUNING ----------
define MG3_DOOR_Z        = 0.95
define MG3_DOOR_Z_HOVER  = 0.96
define MG3_DOOR_Y        = 280
define MG3_DOOR_LEFT_X   = 565
define MG3_DOOR_RIGHT_X  = 960

define MG3_HUD_SCROLL_Z  = 0.35
define MG3_HUD_HEART_Z   = 0.06

define MG3_ADVANCE_DELAY = 0.45
define MG3_FINAL_DELAY   = 2.2

# 연타 방지 잠금 해제 시간(스테이지 전환 직후)
define MG3_TRANSITION_UNLOCK_DT = 0.20

# ---------- STATE ----------
default mg3_stage = 1
default mg3_life = 3
default mg3_result = None

default mg3_has_correct = False
default mg3_locked = False
default mg3_disabled = set()
default mg3_last_fail_toast = ""
default mg3_dim_alpha = 0.55
default mg3_final_wait = False

# 전환/연타 방지 잠금
default mg3_transition_lock = False

# 커스텀 토스트(위치/크기 제어)
default mg3_toast_msg = ""
default mg3_toast_t = 0.0


# ---------- PYTHON ----------
init python:
    MG3_STAGE_DATA = {
        1: {
            "left_img":  MG3_DOOR_NORMAL,
            "left_sfx":  SFX_MG3_DOOR1,
            "right_img": MG3_DOOR_HANDLE_REVERSE,
            "right_sfx": SFX_MG3_DOOR2,
            "answer": "left",
            "fail_toast": "문이 열리지 않는다…",
        },
        2: {
            "left_img":  MG3_DOOR_NO_HINGE,
            "left_sfx":  SFX_MG3_DOOR3,
            "right_img": MG3_DOOR_NORMAL,
            "right_sfx": SFX_MG3_DOOR1,
            "answer": "right",
            "fail_toast": "문이 부서질 것 같은 기분에 황급히 물러섰다.",
        },
        3: {
            "left_img":  MG3_DOOR_NORMAL,
            "left_sfx":  SFX_MG3_DOOR1,
            "right_img": MG3_DOOR_SHADOW_REVERSE,
            "right_sfx": SFX_MG3_DOOR4,
            "answer": "left",
            "fail_toast": "섬뜩한 시선이 느껴진다.",
        },
    }

    def mg3_update_dim():
        a = 0.55 + 0.07 * (store.mg3_stage - 1)
        store.mg3_dim_alpha = min(0.75, a)

    # 커스텀 토스트 함수
    def mg3_show_toast(msg, dur=1.0):
        store.mg3_toast_msg = msg
        store.mg3_toast_t = float(dur)

    def mg3_toast_tick(dt):
        if store.mg3_toast_t > 0:
            store.mg3_toast_t -= dt
            if store.mg3_toast_t <= 0:
                store.mg3_toast_t = 0
                store.mg3_toast_msg = ""

    def mg3_choose(side):
        if store.mg3_result is not None:
            return
        if store.mg3_locked:
            return
        if store.mg3_final_wait:
            return
        if store.mg3_transition_lock:
            return
        if side in store.mg3_disabled:
            return

        data = MG3_STAGE_DATA[store.mg3_stage]

        # 문 클릭 = 해당 문 사운드
        if side == "left":
            renpy.music.play(data["left_sfx"], channel="mg3_sfx")
        else:
            renpy.music.play(data["right_sfx"], channel="mg3_sfx")

        # 정답
        if side == data["answer"]:
            store.mg3_has_correct = True
            store.mg3_locked = True
            store.mg3_transition_lock = True   # 전환 중 입력 잠금
            return

        # 오답: 해당 문만 비활성 + 하트 -1
        store.mg3_disabled.add(side)
        store.mg3_life -= 1
        store.mg3_last_fail_toast = data["fail_toast"]

        mg3_show_toast(store.mg3_last_fail_toast, 1.5)

        if store.mg3_life <= 0:
            store.mg3_final_wait = True
            store.mg3_transition_lock = True   # 최종 대기에서도 잠금

    def mg3_advance():
        if store.mg3_result is not None:
            return

        # 스테이지 전환 직후 연타 방지 유지
        store.mg3_transition_lock = True

        if store.mg3_stage >= 3:
            store.mg3_locked = False
            store.mg3_final_wait = True
            return

        store.mg3_stage += 1
        store.mg3_disabled = set()
        store.mg3_locked = False
        store.mg3_last_fail_toast = ""
        mg3_update_dim()

        renpy.restart_interaction()

    def mg3_finish():
        if store.mg3_result is not None:
            return

        if store.mg3_has_correct and store.mg3_life > 0:
            store.mg3_result = "success"
        else:
            store.mg3_result = "fail"

        store.mg3_final_wait = False
        store.mg3_transition_lock = True  # 결과 화면 넘어가기 직전 잠금


# ---------- ENTRY ----------
label minigame3_play:
    $ mg3_stage = 1
    $ mg3_life = 3
    $ mg3_result = None

    $ mg3_has_correct = False
    $ mg3_locked = False
    $ mg3_disabled = set()
    $ mg3_last_fail_toast = ""
    $ mg3_dim_alpha = 0.55
    $ mg3_final_wait = False

    $ mg3_transition_lock = False

    # 토스트 초기화
    $ mg3_toast_msg = ""
    $ mg3_toast_t = 0.0

    call screen mg3_game
    call screen mg3_result_popup
    return


# ---------- SCREEN (PLAY) ----------
screen mg3_game():
    tag mg3
    modal True

    # 결과가 결정되면 화면 종료 (입력 꼬임 방지)
    if mg3_result is not None:
        timer 0.2 action Return()

    # 정답 후 다음 스테이지로
    if mg3_locked and mg3_result is None:
        timer MG3_ADVANCE_DELAY action Function(mg3_advance)

    # 최종 판정(승/패)로
    if mg3_final_wait and mg3_result is None:
        timer MG3_FINAL_DELAY action Function(mg3_finish)

    # 전환 잠금 해제 (새 스테이지 진입 직후 연타 방지)
    if mg3_transition_lock and (not mg3_locked) and (not mg3_final_wait) and mg3_result is None:
        timer MG3_TRANSITION_UNLOCK_DT action SetVariable("mg3_transition_lock", False)

    # 토스트 시간 감소
    if mg3_toast_t > 0:
        timer 0.05 repeat True action Function(mg3_toast_tick, 0.05)

    add MG3_BG_BG:
        fit "cover"

    add Solid("#000"):
        alpha mg3_dim_alpha

    # HUD
    fixed:
        xpos 30
        ypos 20

        add Transform(MG3_UI_SCROLL, zoom=MG3_HUD_SCROLL_Z)

        text "[mg3_stage] 단계":
            font MG3_FONT
            size 32
            color "#111111"
            outlines [ (2, "#FFFFFF88", 0, 0) ]
            xpos 88
            ypos 70

        hbox:
            xpos 50
            ypos 125
            spacing -6

            for i in range(3):
                if i < mg3_life:
                    add Transform(MG3_UI_HEART, zoom=MG3_HUD_HEART_Z)
                else:
                    add Transform(MG3_UI_BROKEN, zoom=MG3_HUD_HEART_Z)

    # 커스텀 토스트
    if mg3_toast_t > 0 and mg3_toast_msg != "":
        frame:
            xalign 0.5
            yalign 0.10
            xsize 980
            background Solid("#000A")
            padding (28, 18)

            text "[mg3_toast_msg]":
                font MG3_FONT
                size 42
                color "#FFFFFF"
                outlines [ (3, "#000000", 0, 0) ]
                xalign 0.5
                yalign 0.5
                textalign 0.5

    $ _d = MG3_STAGE_DATA[mg3_stage]

    # 클릭 잠금 상태
    $ _input_locked = (mg3_locked or mg3_final_wait or mg3_transition_lock)

    # 왼쪽 문
    if "left" in mg3_disabled:
        add Transform(_d["left_img"], zoom=MG3_DOOR_Z, matrixcolor=BrightnessMatrix(-0.15)) xpos MG3_DOOR_LEFT_X ypos MG3_DOOR_Y
    else:
        imagebutton:
            idle Transform(_d["left_img"], zoom=MG3_DOOR_Z)
            hover Transform(_d["left_img"], zoom=MG3_DOOR_Z_HOVER)
            action Function(mg3_choose, "left")
            xpos MG3_DOOR_LEFT_X
            ypos MG3_DOOR_Y
            sensitive (not _input_locked)

    # 오른쪽 문
    if "right" in mg3_disabled:
        add Transform(_d["right_img"], zoom=MG3_DOOR_Z, matrixcolor=BrightnessMatrix(-0.15)) xpos MG3_DOOR_RIGHT_X ypos MG3_DOOR_Y
    else:
        imagebutton:
            idle Transform(_d["right_img"], zoom=MG3_DOOR_Z)
            hover Transform(_d["right_img"], zoom=MG3_DOOR_Z_HOVER)
            action Function(mg3_choose, "right")
            xpos MG3_DOOR_RIGHT_X
            ypos MG3_DOOR_Y
            sensitive (not _input_locked)


# ---------- RESULT ----------
screen mg3_result_popup():
    tag mg3
    modal True
    zorder 200

    default hover_proceed = False

    # 스파클 계산
    $ _sparkle = 0
    if mg3_life >= 3:
        $ _sparkle = 2
    elif mg3_life == 2:
        $ _sparkle = 1
    else:
        $ _sparkle = 0

    # 결과 사운드
    on "show" action If(
        mg3_life <= 0,
        Play("mg3_result", SFX_COMMON_FAIL),
        If(
            _sparkle >= 2,
            Play("mg3_result", SFX_COMMON_WIN),
            Play("mg3_result", SFX_COMMON_CLEAR)
        )
    )

    add MG3_BG_BG:
        fit "cover"
    add Solid("#0008")

    fixed:
        xalign 0.5
        yalign 0.55
        xsize 1200
        ysize 600

        add Transform(MG3_UI_SCROLL, zoom=0.75):
            xalign 0.5
            yalign 0.5

        text "게임 결과":
            font MG3_FONT
            size 60
            color "#111111"
            outlines [ (4, "#FFFFFF88", 0, 0) ]
            xalign 0.5
            yalign 0.32

        if mg3_life <= 0:
            text "탈출 실패":
                font MG3_FONT
                size 50
                color "#E53935"
                outlines [ (4, "#FFFFFF88", 0, 0) ]
                xalign 0.5
                yalign 0.5
                textalign 0.5
        else:
            fixed:
                xalign 0.5
                yalign 0.52
                xsize 260
                ysize 260

                if _sparkle <= 0:
                    add Transform(MG3_SPARKLE_0, zoom=0.9) xalign 0.5 yalign 0.5
                elif _sparkle == 1:
                    add Transform(MG3_SPARKLE_1, zoom=0.9) xalign 0.5 yalign 0.5
                else:
                    add Transform(MG3_SPARKLE_2, zoom=0.9) xalign 0.5 yalign 0.5

        fixed:
            xalign 0.5
            yalign 0.65
            xsize 340
            ysize 140

            button:
                xalign 0.5
                yalign 0.5
                xsize 340
                ysize 140

                background Transform(MG3_BTN_IDLE,  zoom=MG3_BTN_ZOOM,  xoffset=30, yoffset=55)
                hover_background Transform(MG3_BTN_HOVER, zoom=MG3_BTN_ZOOM, xoffset=30, yoffset=55)
                focus_mask True

                hovered [ Play("mg3_ui", SFX_UI_HOVER), SetScreenVariable("hover_proceed", True) ]
                unhovered SetScreenVariable("hover_proceed", False)

                action Return()

                text "진행하기":
                    font MG3_FONT
                    size 30
                    color (MG3_TXT_HOVER if hover_proceed else MG3_TXT_IDLE)
                    xalign 0.5
                    yalign 0.85
                    yoffset (-MG3_TXT_LIFT if hover_proceed else 0)
