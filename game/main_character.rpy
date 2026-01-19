#캐릭터 나레이션 정의
define princess = Character('장희공주', color="#e991ff", image="princess")
define back = Character('백담우', color="#566e92")
define anonymous = Character('???', color="#ffe989" )
define Jinhyo = Character('진효', color="#ffe989" )
define Hwayajin = Character('화야진', color = "#943636" )

define JinhyoShowCharacter = Position(xalign = 0.9, yalign = 0.0)
define JinhyoLeftCharacter = Position(xalign = 0.98, yalign = 0.0)
define JinhyoRightCharacter = Position(xalign = 0.95, yalign = -0.1)

define backShowCharacter = Position(xalign = 0.85, yalign = -0.02)

define ShowCharacter = Position(xalign = 0.98, yalign = 0.02)
define RightCharacter = Position(xalign = 0.95, yalign = 0.02)
define LeftCharacter = Position (xalign = 0.25, yalign = 0.02)

#캐릭터 이미지 정의
image side princess = Transform("images/character/월영.webp", zoom=0.17)
image back = Transform("images/character/백담우전신최종.webp", zoom=0.43 )
image back2 = Transform("images/character/백담우전신최종2.webp", zoom=0.43)
image backSword = Transform("images/character/백담우칼최종.webp", zoom=0.3)
image backNerveous = Transform("images/character/백담우긴장.webp", zoom=0.3)
image Jinhyo = Transform("images/character/진효반신.webp", zoom=0.4)
image Hwayajin = Transform("images/character/화야진.webp", zoom=0.4)

define scene_fade = Fade(0.5, 0.2, 0.5)