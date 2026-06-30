# Notification Service

## 1. Opis projekta

Notification Service je je aplikacija za slanje notifikacija razvijena 
pomocu FastAPI framework-a.
Aplikacija omogućava prijem, kreiranje, čuvanje i slanje notifikacija 
različitim kanalima.

Servis funkcioniše tako što primi zahtev od nekog eksternog sistema, 
proverava tip notifikacije i i kanal slanja, pronalazi odgovarajući
template, renderuje sadržaj poruke, čuva zahtev u bazi i pokušava da
pošalje notifikaciju pomoću odgovarajućeg sendera.

Trenutno je implementirano slanje email notifikacija putem SMTP 
protokola, uz korišćenje Mailtrap servisa za testiranje slanja email 
poruka.

## 2. Tehnologije

Pri izradi projekta korišćene su sledeće tehnologije:

- **Python** – programski jezik korišćen za implementaciju aplikacije.
- **FastAPI** – framework za razvoj REST API aplikacije.
- **SQLModel** – biblioteka za definisanje modela i rad sa bazom podataka.
- **PostgreSQL** – relaciona baza podataka.
- **Alembic** – upravljanje migracijama baze podataka.
- **Docker** – kontejnerizacija aplikacije.
- **Docker Compose** – pokretanje aplikacije i baze kroz više povezanih servisa.
- **SMTP** – protokol za slanje email poruka.
- **Mailtrap** – servis za testiranje email slanja u razvojnom okruženju.

## 3. Arhitektura aplikacije

Aplikacija je organiyovana po slojevima kako bi se jasno razdvojile 
odgovornosti izmedju API ruta, poslovne logike, pristupa bazi i 
konkretnih implementacija slanja notifikacija.

Osnovni tok kroz aplikaciju je:

````
Router → Service → Repository → Database
````

Za deo  slanja notifikacija tok je:

````
NotificationSenderService → SenderFactory → konkretan sender 
````

### Struktura projekta

```text
src/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── dependencies/
├── middleware/
├── repositories/
├── routers/
└── services/
    └── senders/
````

Opis glavnih foldera:

- `app/` – osnovna konfiguracija aplikacije, konekcija sa bazom, modeli, Pydantic schemas i seed podaci.
- `routers/` – FastAPI rute koje definišu javni API aplikacije.
- `services/` – poslovna logika aplikacije.
- `repositories/` – sloj za pristup bazi podataka.
- `dependencies/` – FastAPI dependency funkcije za kreiranje servisa i repozitorijuma.
- `middleware/` – middleware komponente, uključujući logovanje notification request-ova.
- `services/senders/` – konkretne implementacije sender-a za slanje notifikacija.

### Slojevi aplikacije

#### Router sloj

Router sloj prima HTTP zahteve, validira ulayne podatke i poyiva odgovarjući servis.

Primeri router-a:

- `notification_request_router.py`
- `notification_sending_router.py`
- `notification_status_router.py`
- `notification_type_router.py`
- `channel_config_router.py`
- `notification_template_router.py`

#### Service sloj

U Service sloju implementirana je poslovna logika aplikacije.

- `notification_service.py` - kreira notification request tako što proverava
da li postoji odgovarajući tip notifikacije, kanal i template, proverava 
required variables, renderuje template, ubacuje notification request u bayu i šalje
njen ID NotificationSenderService-u.

- `notification_sender_service.py` - na osnovu dobijenog ID-a pristupa
odgovarajućem notification request-u i potom na osnovu podataka,a uz
pomoć SenderFactory-a prosledjuje na slanje odgovarajućem senderu.

- `notification_orchestration_service.py` - stoji iznad prethodna dva
servise i služi da brine o redosledu izvršavanja, poziva servis za kreiranje
request-a i potom servis za slanje

- ostali servisi sluze validaciju aktivnosti tipova notifikacija i kanala
za slanje, implementiraju logiku iza svih provera koje se vrše
u NotificationService-u.

#### Repository sloj

Repository sloj je odgovoran za komunikaciju sa bazom. Za svaku tabelu
postoji po jedna klasa u kojoj su implementirane CRUD operacije nad
tom tabelom. Servisi ne komuniciraju direktno sa bazom već preko posrednika
koji predstavljaju repository klase.

#### Sender sloj

Sender sloj sluyi ya konkretno slanje notifikacija. BaseSender je 
apstraktna klasa koju nasledjuje svaki drugi sender. SenderFactory u 
zavisnosti od zahteva koji pročita u NotificationRequest-u,
vraca odgovarajući sender NotificationSenderServiceu koji nakon toga
nad datim senderom poyiva metod send. Sama logika slanja za 
razlicite sendere implementirana je u okviru sender klasa i metoda send.
Za sada je implementirana samo klasa EmailSender ali plan je da se proširi.


## 4. Model podataka

## 5. Notification flow

## 6. Podržani kanali i tipovi notifikacija

## 7. Pokretanje pomoću Docker-a

## 8. Alembic migracije

## 9. Seed podaci

## 10. SMTP / Mailtrap konfiguracija

## 11. API endpoint-i

## 12. Primeri request-ova

## 13. Logging