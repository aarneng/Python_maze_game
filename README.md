1. Mitä ominaisuuksia olet jo toteuttanut projektiisi?

koodi voi tällä hetkellä luoda labyrintin jonka kokoa voi muuttaa NxN kokoiseksi.
Labyrintillä on myös on useampia kerroksia ja maali,
ja koodi luo myös pelaajan jota voi liikuttaa ja "lennättää".
Pelaaja ei pääse menemään muurien yli, ellei kyseessä ole
erikoistilanne (kts. 2: käyttöohje)

solve_maze on vielä keskeneräinen, mutta algoritmi löytää kyllä maaliruudun 
(reitin tallennus on pielessä)

Tämän lisäksi ruudukon luonnin voi "animoida" vaihtamalla
mane.Mane():in __init__ funtiossa olevan self.show_animation True:ksi
Ruudokon kokoa voi muuttaa vaihtamalla self.grid:in NewGrid(width=N, height=N)

2. Käyttöohje

  - Voiko ohjelmaa jo ajaa? (kyllä/ei)
  - Kuinka ohjelma käynnistetään?
  - Mitä sillä voi tässä vaiheessa tehdä?
  
  ohjelmaa voi ajaa!
  
  ohjelma käynnistetään pyörittämällä mane.py.
  
  pelaajaa ohjataan WASD näppäimillä, jotka ohjaavat miten pelaaja liikkuu
  ja välilyönnillä, joka muuttaa pelaajan statuksen (on maassa / lentääkö). 
  kun pelaaja lentää se on hieman suurempi kuin sen ollessa maassa, ja suu avautuu.
  
  Kun pelaaja on maassa se voi kävellä vihreiden muurien yli, 
  kun se on ilmassa pelaaja voi lentää sinisten muurien yli. pelaaja ei voi mennä 
  (mustien) muurien yli tai reunojen yli vaikka ne olisivat mitä väriä tahansa
  labyrintin vastauksen saa painamalla 0, joka tässä vaiheessa heittää melkein
  aina pelkän suoran viivan maaliruutuun
  
  joitain pikkujuttuja on voinut unohtua
 

3. Aikataulu

  - Kuinka paljon olet jo käyttänyt aikaa projektiin?
  - Onko ilmennyt muutoksia suunnitelman aikatauluun?
  
  en tiedä paljonko aikaa tävän on mennyt. parisenkymmentä tuntia kai
  Taidan olla aikataulua edellä, en ole ihan varma. jatkan näillä näkymin samaa
  tahtia eteenpäin

4. Muuta

  - Onko ilmaantunut erityisiä ongelmia?
  - Oletko joutunut tekemään muutoksia suunnitelmaasi?
  
  solve_maze() funktio on tuottanut paljon hankaluuksia. 