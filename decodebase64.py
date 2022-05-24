import base64
import quopri
import html
from formatflowed import convertToWrapped

s = b"== Actualit\xc3\xa9s - 10\xc2\xa0nouveaux r\xc3\xa9sultats pour [Android] =\r\nAndroid 13 b\xc3\xaata 1 : Material You int\xc3\xa8gre quatre fois plus de choix de\r\ncouleurs - Frandroid\r\nFrandroid\r\nLe Material You \xc3\xa0 la fa\xc3\xa7on d'Android 13 b\xc3\xaata 1 confirme que Google veut\r\n\xc3\xa9tendre encore les possibilit\xc3\xa9s de jeux de couleurs promis par sa ...\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.frandroid.com/marques/google/1310269_android-13-beta-1-material-you-integre-quatre-fois-plus-de-choix-de-couleurs&ct=ga&cd\xcaEYACoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw0EX44tYkOdEDcQYk3oyKi7>\r\n\r\nAndroid 13 arrive : voici tout ce que nous savons sur le prochain OS de\r\nGoogle - CNET France\r\nCNET France\r\nNous avons fait le point sur la prochaine mise \xc3\xa0 jour d'Android pour\r\nsmartphone et tablette tactile.\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.cnetfrance.fr/news/android-13-arrive-voici-tout-ce-que-nous-savons-sur-le-prochain-os-de-google-39941145.htm&ct=ga&cd\xcaEYASoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw1mjP2S0mi_hKJn8Gxwicpa>\r\n\r\nVous pouvez tester Android 13 d\xc3\xa8s maintenant si vous avez un Google Pixel -\r\nLes Num\xc3\xa9riques\r\nLes Num\xc3\xa9riques\r\nLa nouvelle version d'Android est en approche. La 13e mouture de l'OS de\r\nGoogle vient d'arriver en b\xc3\xaata publique. Les curieux et curieuses peuvent\r\n...\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.lesnumeriques.com/telephone-portable/vous-pouvez-tester-android-13-des-maintenant-si-vous-avez-un-google-pixel-n181577.html&ct=ga&cd\xcaEYAioTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw1SEcc_ns4FmsyL4zfpRFwV>\r\n\r\nAndroid 13 : Google am\xc3\xa9liore le lecteur multim\xc3\xa9dia avec une nouvelle barre\r\nde progression\r\nPhonAndroid\r\nAndroid 13 a droit \xc3\xa0 un lecteur multim\xc3\xa9dia l\xc3\xa9g\xc3\xa8rement revu avec une barre\r\nde progression ondul\xc3\xa9e sur la partie d\xc3\xa9j\xc3\xa0 \xc3\xa9cout\xc3\xa9e.\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.phonandroid.com/android-13-google-ameliore-le-lecteur-multimedia-avec-une-nouvelle-barre-de-progression.html&ct=ga&cd\xcaEYAyoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw0ePFfSBU5UJGky_KQjzpAK>\r\n\r\nAndroid 13 : la premi\xc3\xa8re beta publique est disponible, comment l'installer\r\n? - PhonAndroid\r\nPhonAndroid\r\nGoogle a d\xc3\xa9ploy\xc3\xa9 la premi\xc3\xa8re version beta destin\xc3\xa9e au public d'Android 13.\r\nOn vous explique comment l'installer.\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.phonandroid.com/android-13-la-premiere-beta-publique-est-disponible-comment-linstaller.html&ct=ga&cd\xcaEYBCoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw1Uhx5WnunaBaJxvVgbTdfY>\r\n\r\nLineageOS 19 : voici Android 12 pour plus de 40 smartphones Android -\r\nFrandroid\r\nFrandroid\r\nLineage vient de mettre \xc3\xa0 disposition LineageOS pour 70 appareils Android.\r\nC'est une vraie cure de jouvence pour de vieux smartphones qui ne sont ...\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.frandroid.com/android/rom-custom-2/lineageos/1310505_lineageos-19-voici-android-12-pour-plus-de-40-smartphones-android&ct=ga&cd\xcaEYBSoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw2ARm5_1fCzrDfsVmh0NY-0>\r\n\r\nAndroid Auto 7.6 : quelles sont les nouveaut\xc3\xa9s ? - Autoplus\r\nAutoplus\r\nGoogle pr\xc3\xa9pare la nouvelle version 7.6 d'Android Auto, actuellement\r\npropos\xc3\xa9e aux testeurs en version b\xc3\xaata : voici les principales nouveaut\xc3\xa9s.\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.autoplus.fr/actualite/android-auto-7-6-nouveautes-573930.html&ct=ga&cd\xcaEYBioTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw0VYCEMHf6Isf49KzLACV5s>\r\n\r\nAndroid 14 : Google s'active d\xc3\xa9j\xc3\xa0 autour de la prochaine version -\r\nPresse-citron\r\nPresse-citron\r\nAlors que Android 13 n'arrivera qu'apr\xc3\xa8s l'\xc3\xa9t\xc3\xa9 sur une poign\xc3\xa9e de\r\nsmartphones haut de gamme, Alphabet (Google) commence d\xc3\xa9j\xc3\xa0 \xc3\xa0 pr\xc3\xa9parer\r\nAndroid ...\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.presse-citron.net/android-14-google-sactive-deja-autour-de-la-prochaine-version/&ct=ga&cd\xcaEYByoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw1IyTxmMYkL0-xa5ptccf26>\r\n\r\nAndroid 13 B\xc3\xaata 1 est en cours de d\xc3\xa9ploiement sur les smartphones Google\r\nPixel - CNET France\r\nCNET France\r\nLa prochaine version d'Android devrait \xc3\xaatre pr\xc3\xa9sent\xc3\xa9e lors de la Google I/O\r\nen mai.\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.cnetfrance.fr/news/android-13-beta-1-est-en-cours-de-deploiement-sur-les-smartphones-google-pixel-39941117.htm&ct=ga&cd\xcaEYCCoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw2s_kBcCb7GCbXUvmoZMdG4>\r\n\r\nAndroid 13 n'est plus r\xc3\xa9serv\xc3\xa9 aux d\xc3\xa9veloppeurs, voici la premi\xc3\xa8re version\r\nb\xc3\xaata - Frandroid\r\nFrandroid\r\nContrairement aux versions Developer Preview, Android 13 B\xc3\xaata 1 est\r\nbeaucoup plus simple \xc3\xa0 installer. Si vous poss\xc3\xa9dez un des Pixel compatibles,\r\nvoir ...\r\n<https://www.google.com/url?rct=j&sa=t&url=https://www.frandroid.com/android/1310219_android-13-nest-plus-reserve-aux-developpeurs-voici-la-premiere-version-beta&ct=ga&cd\xcaEYCSoTNzc1ODI4Njk1NTkyMDkxOTI1MjIaYjIyZjE2MDEwYTJhMzUyZjpjb206ZnI6RlI&usg=AOvVaw2E_zEFQvM51cjNtgM9VE5w>\r\n\r\n\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\r\nSe d\xc3\xa9sabonner de cette alerte\xc2\xa0Google:\r\n<https://www.google.com/alerts/remove?source=alertsmail&hl=fr&gl=FR&msgid=Nzc1ODI4Njk1NTkyMDkxOTI1Mg&s\xab2Xq4htQiUtZudfj5aMXl1kUEuuvkYiBO9Wrsc>\r\n\r\nCr\xc3\xa9er une alerte Google suppl\xc3\xa9mentaire:\r\n<https://www.google.com/alerts?source=alertsmail&hl=fr&gl=FR&msgid=Nzc1ODI4Njk1NTkyMDkxOTI1Mg>\r\n\r\nConnectez-vous pour g\xc3\xa9rer vos alertes:\r\n<https://www.google.com/alerts?source=alertsmail&hl=fr&gl=FR&msgid=Nzc1ODI4Njk1NTkyMDkxOTI1Mg>\r\n"

text = convertToWrapped(s, character_set="ISO-8859-2")
print(text)

s = """PGh0bWwgeG1sbnM6dj0idXJuOnNjaGVtYXMtbWljcm9zb2Z0LWNvbTp2bWwiIHhtbG5zOm89InVy
bjpzY2hlbWFzLW1pY3Jvc29mdC1jb206b2ZmaWNlOm9mZmljZSIgeG1sbnM6dz0idXJuOnNjaGVt
YXMtbWljcm9zb2Z0LWNvbTpvZmZpY2U6d29yZCIgeG1sbnM6eD0idXJuOnNjaGVtYXMtbWljcm9z
b2Z0LWNvbTpvZmZpY2U6ZXhjZWwiIHhtbG5zOm09Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5j
b20vb2ZmaWNlLzIwMDQvMTIvb21tbCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnL1RSL1JFQy1o
dG1sNDAiPg0KPGhlYWQ+DQo8bWV0YSBodHRwLWVxdWl2PSJDb250ZW50LVR5cGUiIGNvbnRlbnQ9
InRleHQvaHRtbDsgY2hhcnNldD11dGYtOCI+DQo8bWV0YSBuYW1lPSJHZW5lcmF0b3IiIGNvbnRl
bnQ9Ik1pY3Jvc29mdCBXb3JkIDE1IChmaWx0ZXJlZCBtZWRpdW0pIj4NCjxzdHlsZT48IS0tDQov
KiBGb250IERlZmluaXRpb25zICovDQpAZm9udC1mYWNlDQoJe2ZvbnQtZmFtaWx5OiJDYW1icmlh
IE1hdGgiOw0KCXBhbm9zZS0xOjIgNCA1IDMgNSA0IDYgMyAyIDQ7fQ0KQGZvbnQtZmFjZQ0KCXtm
b250LWZhbWlseTpDYWxpYnJpOw0KCXBhbm9zZS0xOjIgMTUgNSAyIDIgMiA0IDMgMiA0O30NCkBm
b250LWZhY2UNCgl7Zm9udC1mYW1pbHk6VmVyZGFuYTsNCglwYW5vc2UtMToyIDExIDYgNCAzIDUg
NCA0IDIgNDt9DQpAZm9udC1mYWNlDQoJe2ZvbnQtZmFtaWx5OiJTZWdvZSBVSSI7DQoJcGFub3Nl
LTE6MiAxMSA1IDIgNCAyIDQgMiAyIDM7fQ0KLyogU3R5bGUgRGVmaW5pdGlvbnMgKi8NCnAuTXNv
Tm9ybWFsLCBsaS5Nc29Ob3JtYWwsIGRpdi5Nc29Ob3JtYWwNCgl7bWFyZ2luOjBjbTsNCglmb250
LXNpemU6MTEuMHB0Ow0KCWZvbnQtZmFtaWx5OiJDYWxpYnJpIixzYW5zLXNlcmlmO30NCmE6bGlu
aywgc3Bhbi5Nc29IeXBlcmxpbmsNCgl7bXNvLXN0eWxlLXByaW9yaXR5Ojk5Ow0KCWNvbG9yOmJs
dWU7DQoJdGV4dC1kZWNvcmF0aW9uOnVuZGVybGluZTt9DQouTXNvQ2hwRGVmYXVsdA0KCXttc28t
c3R5bGUtdHlwZTpleHBvcnQtb25seTsNCglmb250LXNpemU6MTAuMHB0O30NCkBwYWdlIFdvcmRT
ZWN0aW9uMQ0KCXtzaXplOjYxMi4wcHQgNzkyLjBwdDsNCgltYXJnaW46NzAuODVwdCA3MC44NXB0
IDcwLjg1cHQgNzAuODVwdDt9DQpkaXYuV29yZFNlY3Rpb24xDQoJe3BhZ2U6V29yZFNlY3Rpb24x
O30NCi0tPjwvc3R5bGU+PCEtLVtpZiBndGUgbXNvIDldPjx4bWw+DQo8bzpzaGFwZWRlZmF1bHRz
IHY6ZXh0PSJlZGl0IiBzcGlkbWF4PSIxMDI2IiAvPg0KPC94bWw+PCFbZW5kaWZdLS0+PCEtLVtp
ZiBndGUgbXNvIDldPjx4bWw+DQo8bzpzaGFwZWxheW91dCB2OmV4dD0iZWRpdCI+DQo8bzppZG1h
cCB2OmV4dD0iZWRpdCIgZGF0YT0iMSIgLz4NCjwvbzpzaGFwZWxheW91dD48L3htbD48IVtlbmRp
Zl0tLT4NCjwvaGVhZD4NCjxib2R5IGxhbmc9IkZSIiBsaW5rPSJibHVlIiB2bGluaz0icHVycGxl
IiBzdHlsZT0id29yZC13cmFwOmJyZWFrLXdvcmQiPg0KPGRpdiBjbGFzcz0iV29yZFNlY3Rpb24x
Ij4NCjxwIGNsYXNzPSJNc29Ob3JtYWwiPjxzcGFuIHN0eWxlPSJtc28tZmFyZWFzdC1sYW5ndWFn
ZTpFTi1VUyI+Qm9uam91ciBDaHJpc3RvcGhlLDxvOnA+PC9vOnA+PC9zcGFuPjwvcD4NCjxwIGNs
YXNzPSJNc29Ob3JtYWwiPjxzcGFuIHN0eWxlPSJtc28tZmFyZWFzdC1sYW5ndWFnZTpFTi1VUyI+
PG86cD4mbmJzcDs8L286cD48L3NwYW4+PC9wPg0KPHAgY2xhc3M9Ik1zb05vcm1hbCI+PHNwYW4g
c3R5bGU9Im1zby1mYXJlYXN0LWxhbmd1YWdlOkVOLVVTIj5Ob3RyZSBzZXJ2aWNlIFBhaWUgw6l0
YWl0IHVuIHBldSBzdXJtZW7DqSBjZXMgZGVybmnDqHJlcyBzZW1haW5lcywgYXVzc2kgbOKAmWVu
dm9pIGRlcyBkb2N1bWVudHMgbGnDqSDDoCB0b24gc29sZGUgZGUgdG91dCBjb21wdGUgZXN0IHBy
w6l2dSBwb3VyIGZpbiBkZSBzZW1haW5lIHByb2NoYWluZSZuYnNwOzwvc3Bhbj48c3BhbiBzdHls
ZT0iZm9udC1mYW1pbHk6JnF1b3Q7U2Vnb2UgVUkgRW1vamkmcXVvdDssc2Fucy1zZXJpZjttc28t
ZmFyZWFzdC1sYW5ndWFnZTpFTi1VUyI+JiMxMjg1MjI7PC9zcGFuPjxzcGFuIHN0eWxlPSJtc28t
ZmFyZWFzdC1sYW5ndWFnZTpFTi1VUyI+PG86cD48L286cD48L3NwYW4+PC9wPg0KPHAgY2xhc3M9
Ik1zb05vcm1hbCI+PHNwYW4gc3R5bGU9Im1zby1mYXJlYXN0LWxhbmd1YWdlOkVOLVVTIj48bzpw
PiZuYnNwOzwvbzpwPjwvc3Bhbj48L3A+DQo8cCBjbGFzcz0iTXNvTm9ybWFsIj48c3BhbiBzdHls
ZT0ibXNvLWZhcmVhc3QtbGFuZ3VhZ2U6RU4tVVMiPk1lcmNpLDxvOnA+PC9vOnA+PC9zcGFuPjwv
cD4NCjxwIGNsYXNzPSJNc29Ob3JtYWwiPjxzcGFuIHN0eWxlPSJtc28tZmFyZWFzdC1sYW5ndWFn
ZTpFTi1VUyI+Q2R0LDxvOnA+PC9vOnA+PC9zcGFuPjwvcD4NCjxwIGNsYXNzPSJNc29Ob3JtYWwi
PjxzcGFuIHN0eWxlPSJtc28tZmFyZWFzdC1sYW5ndWFnZTpFTi1VUyI+TWFyaW5lLjxvOnA+PC9v
OnA+PC9zcGFuPjwvcD4NCjxkaXY+DQo8ZGl2IHN0eWxlPSJib3JkZXI6bm9uZTtib3JkZXItdG9w
OnNvbGlkICNFMUUxRTEgMS4wcHQ7cGFkZGluZzozLjBwdCAwY20gMGNtIDBjbSI+DQo8cCBjbGFz
cz0iTXNvTm9ybWFsIj48Yj5EZSZuYnNwOzo8L2I+IEdvb2dsZSAmbHQ7PGEgaHJlZj0ibWFpbHRv
OmNocmlzdG9waGUubWljaGFlbC5qYWNxdWVzQGdtYWlsLmNvbSI+Y2hyaXN0b3BoZS5taWNoYWVs
LmphY3F1ZXNAZ21haWwuY29tPC9hPiZndDsNCjxicj4NCjxiPkVudm95w6kmbmJzcDs6PC9iPiB2
ZW5kcmVkaSAxOCBmw6l2cmllciAyMDIyIDA5OjU0PGJyPg0KPGI+w4AmbmJzcDs6PC9iPiBEdWd1
YXksIFBhdHJpY2sgJmx0OzxhIGhyZWY9Im1haWx0bzpwYXRyaWNrLmR1Z3VheUBjYXBnZW1pbmku
Y29tIj5wYXRyaWNrLmR1Z3VheUBjYXBnZW1pbmkuY29tPC9hPiZndDs8YnI+DQo8Yj5PYmpldCZu
YnNwOzo8L2I+IEZhY3R1cmUgVmluY2kgKyBTb2xkZSBkw6lwYXJ0IENhcGfDqW1pbmk8bzpwPjwv
bzpwPjwvcD4NCjwvZGl2Pg0KPC9kaXY+DQo8cCBjbGFzcz0iTXNvTm9ybWFsIj48bzpwPiZuYnNw
OzwvbzpwPjwvcD4NCjxkaXYgYWxpZ249ImNlbnRlciI+DQo8dGFibGUgY2xhc3M9Ik1zb05vcm1h
bFRhYmxlIiBib3JkZXI9IjAiIGNlbGxzcGFjaW5nPSIwIiBjZWxscGFkZGluZz0iMCIgd2lkdGg9
IjEwMCUiIHN0eWxlPSJ3aWR0aDoxMDAuMCU7YmFja2dyb3VuZDojMkIwQTNEIj4NCjx0Ym9keT4N
Cjx0cj4NCjx0ZCBzdHlsZT0icGFkZGluZzo0LjVwdCA0LjVwdCA0LjVwdCA0LjVwdCI+DQo8cCBj
bGFzcz0iTXNvTm9ybWFsIiBhbGlnbj0iY2VudGVyIiBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7
bGluZS1oZWlnaHQ6MTEuMjVwdCI+DQo8c3BhbiBzdHlsZT0iZm9udC1zaXplOjkuMHB0O2ZvbnQt
ZmFtaWx5OiZxdW90O1ZlcmRhbmEmcXVvdDssc2Fucy1zZXJpZjtjb2xvcjp3aGl0ZSI+VGhpcyBt
YWlsIGhhcyBiZWVuIHNlbnQgZnJvbSBhbiBleHRlcm5hbCBzb3VyY2U8bzpwPjwvbzpwPjwvc3Bh
bj48L3A+DQo8L3RkPg0KPC90cj4NCjwvdGJvZHk+DQo8L3RhYmxlPg0KPC9kaXY+DQo8cCBjbGFz
cz0iTXNvTm9ybWFsIj48c3BhbiBzdHlsZT0iZm9udC1zaXplOjEwLjBwdDtmb250LWZhbWlseTom
cXVvdDtTZWdvZSBVSSZxdW90OyxzYW5zLXNlcmlmIj48bzpwPiZuYnNwOzwvbzpwPjwvc3Bhbj48
L3A+DQo8cD48c3BhbiBzdHlsZT0iZm9udC1zaXplOjEwLjBwdDtmb250LWZhbWlseTomcXVvdDtT
ZWdvZSBVSSZxdW90OyxzYW5zLXNlcmlmIj5Cb25qb3VyIFBhdHJpY2ssPG86cD48L286cD48L3Nw
YW4+PC9wPg0KPHA+PHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxMC4wcHQ7Zm9udC1mYW1pbHk6JnF1
b3Q7U2Vnb2UgVUkmcXVvdDssc2Fucy1zZXJpZiI+Jm5ic3A7IGNvbW1lIHN1aXRlIMOgIG5vdHJl
IGRpc2N1c3Npb24gdMOpbMOpcGhvbmlxdWUsPG86cD48L286cD48L3NwYW4+PC9wPg0KPHA+PHNw
YW4gc3R5bGU9ImZvbnQtc2l6ZToxMC4wcHQ7Zm9udC1mYW1pbHk6JnF1b3Q7U2Vnb2UgVUkmcXVv
dDssc2Fucy1zZXJpZiI+amUgdGUgZmFpcyBzdWl2cmUgbW9uIGp1c3RpZmljYXRpZiBkZSBww6lh
Z2UgcG91ciBsZSBtb2lzIGRlIEphbnZpZXIgMjAyMjxvOnA+PC9vOnA+PC9zcGFuPjwvcD4NCjxw
PjxzcGFuIHN0eWxlPSJmb250LXNpemU6MTAuMHB0O2ZvbnQtZmFtaWx5OiZxdW90O1NlZ29lIFVJ
JnF1b3Q7LHNhbnMtc2VyaWYiPkonZW4gcHJvZml0ZSwgcG91ciB0J2luZm9ybWVyIHF1ZSBqJ2Fp
IGJpZW4gcmXDp3UgdW4gdmlyZW1lbnQgZHUgJnF1b3Q7c29sZGUgZGUgdG91dCBjb21wdGUmcXVv
dDsgc3VyIG1vbiBjb21wdGUgYmFuY2FpcmUsPG86cD48L286cD48L3NwYW4+PC9wPg0KPHAgY2xh
c3M9Ik1zb05vcm1hbCI+PHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxMC4wcHQ7Zm9udC1mYW1pbHk6
JnF1b3Q7U2Vnb2UgVUkmcXVvdDssc2Fucy1zZXJpZiI+amUgbidhaSBwYXIgY29udHJlIHJlw6d1
IGF1Y3VuIG1lc3NhZ2UgKG1haWwpIG0naW5kaXF1YW50IGxlIGTDqXRhaWwgZGUgY2UgdmlyZW1l
bnQsIG5pIGxlcyBwacOoY2VzIG91IGp1c3RpZmljYXRpZnMNCjxicj4NCmR1cyDDoCBtb24gZMOp
cGFydCBkZSBDYXBnZW1pbmkgKGRvbnQgYXUgbW9pbnMgbW9uIGNlcnRpZmljYXQgZGUgdHJhdmFp
bCBxdWkgbSdlc3QgZGVtYW5kw6kpLjxvOnA+PC9vOnA+PC9zcGFuPjwvcD4NCjxkaXY+DQo8cCBj
bGFzcz0iTXNvTm9ybWFsIj48c3BhbiBzdHlsZT0iZm9udC1zaXplOjEwLjBwdDtmb250LWZhbWls
eTomcXVvdDtTZWdvZSBVSSZxdW90OyxzYW5zLXNlcmlmIj48YnI+DQo8YnI+DQotLS0tLS0tLSBN
ZXNzYWdlIHRyYW5zZsOpcsOpIC0tLS0tLS0tIDxvOnA+PC9vOnA+PC9zcGFuPjwvcD4NCjx0YWJs
ZSBjbGFzcz0iTXNvTm9ybWFsVGFibGUiIGJvcmRlcj0iMCIgY2VsbHNwYWNpbmc9IjAiIGNlbGxw
YWRkaW5nPSIwIj4NCjx0Ym9keT4NCjx0cj4NCjx0ZCBub3dyYXA9IiIgdmFsaWduPSJ0b3AiIHN0
eWxlPSJwYWRkaW5nOjBjbSAwY20gMGNtIDBjbSI+DQo8cCBjbGFzcz0iTXNvTm9ybWFsIiBhbGln
bj0icmlnaHQiIHN0eWxlPSJ0ZXh0LWFsaWduOnJpZ2h0Ij48Yj5TdWpldCZuYnNwOzogPG86cD48
L286cD48L2I+PC9wPg0KPC90ZD4NCjx0ZCBzdHlsZT0icGFkZGluZzowY20gMGNtIDBjbSAwY20i
Pg0KPHAgY2xhc3M9Ik1zb05vcm1hbCI+RmFjdHVyZSBWaW5jaTxvOnA+PC9vOnA+PC9wPg0KPC90
ZD4NCjwvdHI+DQo8dHI+DQo8dGQgbm93cmFwPSIiIHZhbGlnbj0idG9wIiBzdHlsZT0icGFkZGlu
ZzowY20gMGNtIDBjbSAwY20iPg0KPHAgY2xhc3M9Ik1zb05vcm1hbCIgYWxpZ249InJpZ2h0IiBz
dHlsZT0idGV4dC1hbGlnbjpyaWdodCI+PGI+RGF0ZSZuYnNwOzogPG86cD48L286cD48L2I+PC9w
Pg0KPC90ZD4NCjx0ZCBzdHlsZT0icGFkZGluZzowY20gMGNtIDBjbSAwY20iPg0KPHAgY2xhc3M9
Ik1zb05vcm1hbCI+RnJpLCAxOCBGZWIgMjAyMiAwOTo0NToyNiArMDEwMDxvOnA+PC9vOnA+PC9w
Pg0KPC90ZD4NCjwvdHI+DQo8dHI+DQo8dGQgbm93cmFwPSIiIHZhbGlnbj0idG9wIiBzdHlsZT0i
cGFkZGluZzowY20gMGNtIDBjbSAwY20iPg0KPHAgY2xhc3M9Ik1zb05vcm1hbCIgYWxpZ249InJp
Z2h0IiBzdHlsZT0idGV4dC1hbGlnbjpyaWdodCI+PGI+RGUmbmJzcDs6IDxvOnA+PC9vOnA+PC9i
PjwvcD4NCjwvdGQ+DQo8dGQgc3R5bGU9InBhZGRpbmc6MGNtIDBjbSAwY20gMGNtIj4NCjxwIGNs
YXNzPSJNc29Ob3JtYWwiPkNocmlzdG9waGUgSkFDUVVFUyA8bzpwPjwvbzpwPjwvcD4NCjwvdGQ+
DQo8L3RyPg0KPHRyPg0KPHRkIG5vd3JhcD0iIiB2YWxpZ249InRvcCIgc3R5bGU9InBhZGRpbmc6
MGNtIDBjbSAwY20gMGNtIj4NCjxwIGNsYXNzPSJNc29Ob3JtYWwiIGFsaWduPSJyaWdodCIgc3R5
bGU9InRleHQtYWxpZ246cmlnaHQiPjxiPlBvdXImbmJzcDs6IDxvOnA+PC9vOnA+PC9iPjwvcD4N
CjwvdGQ+DQo8dGQgc3R5bGU9InBhZGRpbmc6MGNtIDBjbSAwY20gMGNtIj4NCjxwIGNsYXNzPSJN
c29Ob3JtYWwiPjxhIGhyZWY9Im1haWx0bzpjaHJpc3RvcGhlLm1pY2hhZWwuamFjcXVlc0BnbWFp
bC5jb20iPmNocmlzdG9waGUubWljaGFlbC5qYWNxdWVzQGdtYWlsLmNvbTwvYT48bzpwPjwvbzpw
PjwvcD4NCjwvdGQ+DQo8L3RyPg0KPC90Ym9keT4NCjwvdGFibGU+DQo8cCBjbGFzcz0iTXNvTm9y
bWFsIiBzdHlsZT0ibWFyZ2luLWJvdHRvbToxMi4wcHQiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6
MTAuMHB0O2ZvbnQtZmFtaWx5OiZxdW90O1NlZ29lIFVJJnF1b3Q7LHNhbnMtc2VyaWYiPjxvOnA+
Jm5ic3A7PC9vOnA+PC9zcGFuPjwvcD4NCjwvZGl2Pg0KPC9kaXY+DQo8c3BhbiBzdHlsZT0iZm9u
dC1zaXplOiA5cHg7IGxpbmUtaGVpZ2h0OiAxMHB4OyI+VGhpcyBtZXNzYWdlIGNvbnRhaW5zIGlu
Zm9ybWF0aW9uIHRoYXQgbWF5IGJlIHByaXZpbGVnZWQgb3IgY29uZmlkZW50aWFsIGFuZCBpcyB0
aGUgcHJvcGVydHkgb2YgdGhlIENhcGdlbWluaSBHcm91cC4gSXQgaXMgaW50ZW5kZWQgb25seSBm
b3IgdGhlIHBlcnNvbiB0byB3aG9tIGl0IGlzIGFkZHJlc3NlZC4gSWYgeW91IGFyZSBub3QgdGhl
IGludGVuZGVkIHJlY2lwaWVudCwgeW91IGFyZSBub3QgYXV0aG9yaXplZCB0byByZWFkLCBwcmlu
dCwgcmV0YWluLCBjb3B5LCBkaXNzZW1pbmF0ZSwgZGlzdHJpYnV0ZSwgb3IgdXNlIHRoaXMgbWVz
c2FnZSBvciBhbnkgcGFydCB0aGVyZW9mLiBJZiB5b3UgcmVjZWl2ZSB0aGlzIG1lc3NhZ2UgaW4g
ZXJyb3IsIHBsZWFzZSBub3RpZnkgdGhlIHNlbmRlciBpbW1lZGlhdGVseSBhbmQgZGVsZXRlIGFs
bCBjb3BpZXMgb2YgdGhpcyBtZXNzYWdlLjwvc3Bhbj48L2JvZHk+DQo8L2h0bWw+DQo="""

s64 = base64.b64decode(s)
res = html.unescape(quopri.decodestring(s64).decode())
print()
print(res)


s = """
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div dir=3D"ltr">Bonjour MR JACQUES,<div><br></div><div>Je reviens vers vou=
s juste pour vous informer que l&#39;acompte de 1950 euros est bien arriv=
=C3=A9 sur notre compte.</div><div><br></div><div>Je vous tiendrai inform=
=C3=A9 de l&#39;=C3=A9volution de votre commande au fur et =C3=A0 mesure.</=
div><div><br></div><div>Bonne journ=C3=A9e =C3=A0 vous</div><div><br></div>=
<div>=C3=A0 bient=C3=B4t</div><div><br></div><div>cdt,</div><div><br clear=
=3D"all"><div><div dir=3D"ltr" class=3D"gmail_signature" data-smartmail=3D"=
gmail_signature"><div dir=3D"ltr"><img width=3D"420" height=3D"210" src=3D"=
https://docs.google.com/uc?export=3Ddownload&amp;id=3D1YI6LCtxWfSV4hRpukSPy=
PR2DCZ2qTlcA&amp;revid=3D0B32WcwVb_kA4bDBpcTU0TUNtdXpNNmJjaVRlN2JnWTJSVmlBP=
Q"></div></div></div></div></div>
"""

s = "=?windows-1252?Q?APE_sign=E9e.pdf?="
s = "APE_sign=E9e.pdf"

res = html.unescape(quopri.decodestring(s).decode("windows-1252"))
print()
print(res)

s = "Alerte_Google=C2=A0=3A_Android="

res = html.unescape(quopri.decodestring(s).decode())
print()
print(res)
