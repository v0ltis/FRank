from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class generator:
    def card(pseudo,couleur,xp,reqXp,level,membres,pos,guildId):
        try:
            main_picture = Image.open(f"img/{guildId}.png").convert('RGBA')
            main_picture = main_picture.resize((900, 400))
        except:
            main_picture = Image.open("card.png").convert('RGBA')
        profile_image = Image.open("Avatar.png").convert('RGBA')
        profile_image = profile_image.resize((110,110))
        offset = (75, 90)
        main_picture.paste(profile_image, offset, profile_image)

        drawing = ImageDraw.Draw(main_picture)


        # Change default font following a font file.
        font = ImageFont.truetype("font.ttf", 100)
        # pseudo
        drawing.text((200,70),"{} :".format(pseudo),couleur,font=font)
        font = ImageFont.truetype("font.ttf", 70)
        # niveau

        drawing.text((204,144),"Niveau {}".format(level),(231,231,231),font=font)
        font = ImageFont.truetype("font.ttf", 40)
        # affichage xp
        drawing.text((70,250),"{}/{} xp".format(xp,reqXp),couleur,font=font)
        # classement
        #drawing.text((570,250),"1e place",(77,77,77),font=font)
        #drawing.text((571,251),"1e place",(154,154,154),font=font)
        drawing.text((572,252),f"{pos}e place",(231,231,231),font=font)

        font = ImageFont.truetype("font.ttf", 30)
        # pourcentage xp
        percent = round((xp / reqXp * 100),2)
        drawing.text((70,290),"{}% du niveau accompli".format(percent),couleur,font=font)
        # nombre membres
        drawing.text((570,290),"sur {} membres".format(membres),(231,231,231),font=font)


        #     lignes :
        drawing.line([(50, 350), (850, 350)], fill=(154,154,154), width=9)
        drawing.line([(50, 350), (round(800*(percent/100))+50, 350)], fill=couleur, width=9)

        # level à coté des barres
        drawing.text((38,353),str(level),couleur,font=font)
        drawing.text((850,353),str(level+1),couleur,font=font)

        # Prints the result using your picture explorer and save it as result.png
        main_picture.save('level.png')
