#캐릭터 나레이션 정의
define princess = Character('장희공주', color="#e991ff", image="princess")
define back = Character('백담우', color="#566e92")
define anonymous = Character('???', color="#ffe989" )
define Jinhyo = Character('진효', color="#ffe989" )
define Hwayajin = Character('화야진', color = "#943636" )
define ShowCharacter = Position(xalign = 0.8, yalign = 0.2)
define RightCharacter = Position(xalign = 0.95, yalign = 0.2)
define LeftCharacter = Position (xalign = 0.25, yalign = 0.2)

#캐릭터 이미지 정의
image side princess = Transform("images/character/월영.webp", zoom=0.17)
image back = Transform("images/character/백담우.webp", zoom=0.38)
image Jinhyo = Transform("images/character/진효.webp", zoom=0.35)
image Hwayajin = Transform("images/character/화야진.webp", zoom=0.35)

define scene_fade = Fade(0.5, 0.2, 0.5)