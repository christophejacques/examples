
with open("D:\\Mes Documents\\Tel\\jufe.html", "w") as fichier:

    fichier.write("<!DOCTYPE html>")
    fichier.write("""
    <HTML>
    <HEAD>
      <TITLE>Images JUFE</TITLE>
    </HEAD>
    <BODY>
      <TABLE>
    """)
    for i in range(20, 50):
        fichier.write(f"  <TR>\n")
        for j in range(2):
            chaine = ""
            chaine += f"JUFE-"
            chaine += f"00{j+2*i}"[-3:]
            url = f"https://img2.javmost.com/file_image/{chaine}.jpg"

            fichier.write(f"    <TD>\n")
            fichier.write(f"      <A HREF={url}>{chaine}</A><BR />\n")
            fichier.write(f'      <IMG SRC="{url}" /><BR />\n')
            fichier.write(f"    </TD>\n")

        fichier.write(f"  </TR>\n")
    fichier.write("""
        </TABLE>
    </BODY>
    </HTML>
    """)
