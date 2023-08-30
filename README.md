# Azil-projekt
Azil je web aplikacija koji omogućuje praćenje života psa u azilu. Imamo 4 mogućnosti na kojima se bazira ovaj web servis.
## Mogućnosti
1. Create Pas
2. Read Pas
3. Update Pas
4. Delete Pas
## Rad servisa
Web aplikacija se sastoji od jedne klase Pas. Kad pas dođe u azil, korisnik prvo ispunjava obrazac u koji unosi: pasminu, dob, spol, ime, boju, datum dolaska, zdravstveno stanje i težinu.
Osim toga korisnik može vidjeti sve pse koji su u azilu. Ako se nešto promijeni, korisnik update-a podatke ili ako je pas usvojen, korisnik ga briše iz baze podataka.
## Pokretanje
Preuzmite datoteke s Github-a i spremite ih u mapu.
Pomoću naredbe docker build -t projekt:latest - izradite image.
Kako bi pokrenuli docker container, koristite ovu naredbu: docker run -p 5000:8080 projekt:latest.
I na kraju kako bi pristupili aplikaciji, otvaramo preglednik na http://localhost:5000

