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

Aplikacija koristi PostgreSQL bazu podataka. Modeli su definisani pomoću SQLModel biblioteke, a promene nad strukturom baze vode se pomoću Alembic migracija.

Glavne tabele u sistemu su:

- `notification_types`
- `channel_configs`
- `notification_templates`
- `notification_requests`

### notification_types

Tabela `notification_types` definiše podržane tipove notifikacija.

Njena polja su:

- `id` – jedinstveni identifikator tipa notifikacije.
- `code` – jedinstveni kod tipa notifikacije.
- `is_active` – označava da li je tip notifikacije aktivan.

### channel_config

Tabela `channel config` definiše kanale preko kojih sistem može da šalje notifikacije, 
kao i tehničku konfiguraciju ya svaki od tih kanala.

Njena polja su:

- `id` – jedinstveni identifikator konfiguracije kanala.
- `channel` – naziv kanala.
- `provider` – tehnički provider koji se koristi za slanje.
- `config` – JSONB konfiguracija kanala.
- `is_active` – označava da li je kanal aktivan.


### notification_templates

Tabela `notification_templates` definiše template-e za notifikacije.

Svaki template je vezan za jedinstvenu kombinaciju: 

```text
notification_type + channel
```
Polja ove tabele su:

- `id` - jedinstveni identifikator template-a,
- `notification_type_id` - referenca na tip notifikacije,
- `channel_id` - referenca na kanal,
- `subject_template` - template za naslov poruke (samo kod email notifikacija),
- `body template` - template za telo poruke,
- `required_variables` - JSONB objekat koji definiše obaveyne promenljive koje se koriste za renderovanje template-a,
- `is_active` - označava da li je template aktivan.

### notification_requests

Tabela `notification_requests` čuva konkretne zahteve za slanje notifikacija.

Kada eksterni servis pošalje zahtev za notifikaciju, aplikacija kreira jedan red u ovoj tabeli.

Najvažnija polja:

- `id` - jedinstveni identifikator notification request-a,
- `source_service` - naziv eksternog servisa koji je poslao zahtev,
- `notification_type_id` - tip notifikacije,
- `template_id` - template koji je korišćen za renderovanje poruke,
- `channel` - kanal slanja,
- `recipient` - primalac notifikacije,
- `template_data` - podaci koji se koriste za renderovanje template-a,
- `rendered_subject` - finalni naslov poruke nakon renderovanja,
- `rendered_body` - finalno telo poruke nakon renderovanja,
- `status` - trenutni status notification request-a,
- `error_msg` - poruka o grešci ako slanje nije uspelo,
- `created_at` - vreme kreiranja zahteva,
- `sent_at` - vreme uspešnog slanja,
- `updated_at` - vreme poslednje izmene.

Notification request može imati sledeće statuse:

- `pending` - zahtev je kreiran, ali slanje još nije započeto,
- `processing` - zahtev je u procesu slanja,
- `sent` - notifikacija je uspešno poslata,
- `failed` - slanje notifikacije nije uspelo.

## 5. Notification flow
Glavni endpoint za kreiranje i slanje notifikacije je:

```text
POST /notifications
```
Ovaj endpoint prima yahtev od eksternog servisa, kreira notification request,
renderuje poruku i odmah pokušava da pošalje notifikaciju.

Osnovni tok izvršavanja je:

```text
POST /notifications
        ↓
NotificationRequestRouter
        ↓
NotificationService
        ↓
NotificationRequestRepository
        ↓
NotificationSenderService
        ↓
SenderFactory
        ↓
EmailSender
        ↓
SMTP / Mailtrap
```

### Koraci obrade zahteva

1. Klijent šalje `POST /notification` zahtev sa podacima o notifikaciji.
2. Router prima zahtev i validira osnovnu strukturu podataka pomoću Pzdantic schema.
3. `NotificationOrchestrationService` prima podatke o notifikaciji od rutera i poziva metodu za kreiranje i slanje notifikacije.
4. `NotificationService` proverava da li postoji aktivan `notification_type` na osnovu vrednosti `notification_type` iz request-a, a pomoću `NotificationTypeService`.
5. `NotificationService` proverava da li postoji aktivna konfiguracija kanala u tabeli `channel_configs` pomoću `ChannelConfigService`
6. `NotificationService` pronalazi odgovarajući template u tabeli `notification_templates` za kombinaciju:

```text
notification_type + channel
```

7. `NotificationService` proverava da li su u `template_data` poslati svi podaci koji su definisani u `required_variables` pomoću `NotificationTemplateService`
8. Kreira se zapis u tabeli `notification_requests` sa početnim statusom:

```text
pending
```
9. Nakon kreiranja request-a, `NotificationSenderService` odmah pokreće proces slanja.
10. Status notification request-a se menja:

```text
pending → processing
```
11. `NotificationSenderService` uzima aktivnu konfiguraciju kanala iz `channel_configs`.
12. `SenderFactory` bira odgovarajući sender na osnovu kanala.

13. Za `email` kanal koristi se `EmailSender`.

14. `EmailSender` čita SMTP konfiguraciju iz `channel_configs.config`.

15. SMTP username i password se ne čuvaju direktno u bazi, već se čitaju iz environment promenljivih.

16. `EmailSender` šalje email poruku preko SMTP servera.

17. Ako je slanje uspešno, status notification request-a se menja u:

```text
sent
```

18. Ako slanje nije uspešno, status notification request-a se menja u:

```text
failed
```

i u polje `error_msg` se upisuje opis greške.

### Uspešan tok

Kod uspešnog slanja email notifikacije, statusi se menjaju sledećim redosledom:

```text
pending → processing → sent
```

Primer uspešnog odgovora:

```json
{
  "id": 1,
  "source_service": "user-service",
  "notification_type_id": 1,
  "template_id": 1,
  "channel": "email",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija",
    "activation_link": "https://example.com/activate/123"
  },
  "rendered_subject": "Dobrodošao, Matija!",
  "rendered_body": "Zdravo Matija, dobrodošao u naš sistem. Aktiviraj nalog klikom na sledeći link: https://example.com/activate/123.",
  "status": "sent",
  "error_msg": null,
  "sent_at": "2026-06-29T07:04:35.956479"
}
```

### Neuspešan tok

Ako dođe do greške prilikom slanja, notification request se i dalje kreira, ali završava sa statusom:

```text
failed
```

Primer:

```json
{
  "id": 2,
  "channel": "email",
  "recipient": "matija@example.com",
  "status": "failed",
  "error_msg": "Connection unexpectedly closed"
}
```
### Validacione greške

Ako zahtev nije ispravan, notification request se ne kreira.

Primeri validacionih grešaka:

- nepostojeći `notification_type`
- nepostojeći kanal
- neaktivan kanal
- nedostaju obavezne promenljive iz `template_data`
- nevalidan email format

Primer greške kada nedostaje obavezna promenljiva:

```json
{
  "detail": "Missing required variables: ['activation_link']"
}
```

U ovom slučaju API vraća HTTP status:

```text
400 Bad Request
```

Za greške Pydantic validacije, na primer nevalidan email format, API vraća:

```text
422 Unprocessable Entity
```

## 6. Podržani kanali i tipovi notifikacija

### Podržani tipovi notifikacija
Trenutno su definisani sledeći tipovi notifikacija:

| Code | Opis |
|---|---|
| `welcome_user` | Notifikacija dobrodošlice novom korisniku. |
| `password_reset` | Notifikacija za resetovanje lozinke. |
| `payment_success` | Notifikacija o uspešnoj uplati. |
| `appointment_reminder` | Podsetnik za zakazani termin. |
| `system_alert` | Sistemsko upozorenje. |

### Podržani kanali

Trenutno su u konfiguraciji definisani sledeći kanali:

| Channel | Provider | Status implementacije |
|---|--|---|
| `email` | `smtp` | Implementirano slanje putem SMTP protokola. |
| `teams` |  | Kanal postoji u konfiguraciji, ali sender trenutno nije implementiran. |
| `viber` |  | Kanal postoji u konfiguraciji, ali sender trenutno nije implementiran. |
| `whatsapp` |  | Kanal postoji u konfiguraciji, ali sender trenutno nije implementiran. |

Trenutno je potpuno implementirano slanje samo za `email` kanal.  
Ostali kanali su deo konfiguracije sistema i mogu se implementirati naknadno dodavanjem odgovarajućih sender klasa.

## 7. Alembic migracije
Aplikacija koristi Alembic za upravljanje promenama nad bazom podataka.

Promene nad bazom ne izvršavaju se direktno kroz aplikaciju, već se vode kroz migracione fajlove. Na taj način se svaka promena strukture baze ili važnih konfiguracionih podataka može pratiti, verzionisati i ponoviti u drugom okruženju.

Alembic migracije se nalaze u folderu:

```text
alembic/versions/
```

### Tipovi migracija

U projektu se koriste dve vrste migracija:

1. **Schema migracije**  
   Koriste se kada se menja struktura baze.

   Primeri:

   - dodavanje nove tabele
   - dodavanje nove kolone
   - promena tipa kolone
   - dodavanje constraint-a
   - dodavanje indeksa

2. **Data migracije**  
   Koriste se kada treba promeniti postojeće podatke koji predstavljaju konfiguraciju sistema.

   Primer:

   - izmena SMTP konfiguracije za `email` kanal u tabeli `channel_configs`
   - promena vrednosti u `config` JSONB polju
   - aktiviranje ili deaktiviranje određenog kanala

Svaka migracija predstavlja jednu verzionisanu promenu nad bazom.

### Primena migracija

Kada je aplikacija pokrenuta kroz Docker, migracije se primenjuju komandom:

```bash
docker compose exec app alembic upgrade head
```

Ova komanda primenjuje sve migracije koje još nisu izvršene nad bazom.

Trenutna verzija baze može se proveriti komandom:

```bash
docker compose exec app alembic current
```

Istorija migracija može se prikazati komandom:

```bash
docker compose exec app alembic history
```

Ako `app` container nije pokrenut, migracije se mogu pokrenuti kroz privremeni container:

```bash
docker compose run --rm app alembic upgrade head
```
## 8. Seed podaci
Seed podaci se nalaze u fajlu:

```text
src/app/seed.py
```

Seed proces se pokreće prilikom startovanja aplikacije i popunjava osnovne konfiguracione tabele ako podaci ne postoje.

Seed trenutno dodaje:

- osnovne tipove notifikacija
- konfiguracije kanala
- template-e za podržane kombinacije tipova notifikacija i kanala

Seed je napravljen tako da bude idempotentan, odnosno ponovno pokretanje aplikacije ne bi trebalo da duplira postojeće podatke.

### Pregled seed podataka kroz API

Konfiguracioni podaci mogu se pregledati kroz sledeće endpoint-e:

```text
GET /notification-types
GET /channel-configs
GET /notification-templates
```

Pojedinačni zapisi se mogu dobiti pomoću:

```text
GET /notification-types/{id}
GET /channel-configs/{id}
GET /notification-templates/{id}
```

## 9. Pokretanje pomoću Docker-a

Aplikacija se pokree pomoću Docker Compose-a.

Docker Compose pokreće dva glavna servisa:

```text
db   → PostgreSQL baza podataka
app  → FastAPI aplikacija
```

FastAPI apliacija se pokreće u posebnom Docker container-u i poveyuje se sa PostgreSQL
bazon, koja je podignuta u drugom Docker container-u, preko Docker mreže.

### Environment konfiguracija za Docker

Za pokretanje aplikacije u Docker okruženju koristi se fajl:

```text
.env.docker
```

Primer konfiguracije nalazi se u fajlu:

```text
.env.docker.example
```

Primer sadržaja:

```env
APP_NAME=Notification Service
APP_VERSION=0.1.0
DEBUG=True

DATABASE_URL=postgresql://postgres:postgres@db:5432/notification_db

MAILTRAP_USERNAME=your_mailtrap_username
MAILTRAP_PASSWORD=your_mailtrap_password
```

Važno je da se u Docker okruženju za bazu koristi hostname `db`, jer je `db` naziv PostgreSQL servisa u `docker-compose.yml` fajlu.

Zato se koristi:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/notification_db
```

a ne:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/notification_db
```

### Pokretanje servisa

Za pokretanje aplikacije i baze koristi se komanda:

```bash
docker compose up --build
```

Nakon pokretanja, aplikacija je dostupna na:

```text
http://localhost:8000
```

Swagger dokumentacija dostupna je na:

```text
http://localhost:8000/docs
```

### Docker logovi

Logovi FastAPI aplikacije mogu se pregledati komandom:

```bash
docker compose logs app
```

Za praćenje logova uživo koristi se:

```bash
docker compose logs -f app
```

Za prikaz poslednjih 100 linija loga:

```bash
docker compose logs --tail=100 app
```

Logovi baze mogu se pregledati pomoću:

```bash
docker compose logs db
```

## 10. SMTP / Mailtrap konfiguracija

Trenutno je implementirano slanje notifikacija za `email` kanal.

Email notifikacije se šalju preko SMTP protokola, adok se u razvojnom okruženju za testiranje
koristi Mailtrap.

Konfiguracija email kanala čuva se u tabeli `channel_configs`, u JSONB koloni `config`.

Primer konfiguracije za email kanal:

```json
{
  "host": "sandbox.smtp.mailtrap.io",
  "port": 587,
  "username_env": "MAILTRAP_USERNAME",
  "password_env": "MAILTRAP_PASSWORD",
  "from_email": "noreply@notification-service.local",
  "use_tls": true
}
```

U bazi se ne čuvaju stvarni SMTP kredencijali.  
Umesto toga, u bazi se čuvaju nazivi environment promenljivih:

```text
MAILTRAP_USERNAME
MAILTRAP_PASSWORD
```

Stvarne vrednosti se definišu u `.env` ili `.env.docker` fajlu:

```env
MAILTRAP_USERNAME=your_mailtrap_username
MAILTRAP_PASSWORD=your_mailtrap_password
```

Ovi fajlovi se ne commituju na GitHub.

Za slanje email poruka koristi se `EmailSender`, koji čita SMTP konfiguraciju iz `channel_configs`, uzima kredencijale iz environment promenljivih i šalje poruku preko SMTP servera.

Poruke poslate kroz Mailtrap ne stižu u pravi inbox korisnika, već se prikazuju u Mailtrap test inbox-u.

## 11. Logging
## Logging

Aplikacija koristi middleware za logovanje zahteva za kreiranje notifikacija.

Middleware se nalazi u fajlu:

```text
src/middleware/notification_logging_middleware.py
```

Trenutno se loguju `POST /notifications` zahtevi, jer je to glavni endpoint kroz koji prolazi kreiranje i slanje notifikacija.

Za svaki obrađeni notification request loguju se osnovne informacije:

- HTTP metoda
- path
- HTTP status code
- trajanje obrade
- IP adresa klijenta
- source service
- kanal slanja
- tip notifikacije
- primalac
- ID kreirane notifikacije
- finalni status notifikacije
- poruka o grešci, ako postoji

Primer log zapisa:

```text
Notification request completed | method=POST / path=/notifications/ / status_code=200 / duration_ms=120.45 / client_ip=172.18.0.1 / source_service=user-service / channel=email / notification_type=welcome_user / recipient=matija@example.com / notification_id=1 / final_status=sent / error_msg=None
```

Logovi se ispisuju na standardni output aplikacije.  
Pošto aplikacija radi u Docker container-u, logovi se mogu pratiti pomoću:

```bash
docker compose logs -f app
```

Middleware omogućava lakše praćenje notification flow-a, posebno u slučajevima kada slanje notifikacije ne uspe ili kada API vrati validacionu grešku.

Važno je razlikovati HTTP status code od statusa notifikacije.  
HTTP status code opisuje rezultat API zahteva, dok `final_status` opisuje rezultat procesa slanja notifikacije.

## 12. API endpoint-i

Aplikacija izlaže REST API endpoint-e za kreiranje, slanje, pregled i upravljanje notification request-ovima, kao i za pregled konfiguracionih podataka.



### Notification request endpoint-i

| Metoda | Endpoint | Opis |
|---|---|---|
| `POST` | `/notifications` | Kreira notification request i odmah pokušava da pošalje notifikaciju. |
| `GET` | `/notifications/{id}` | Vraća detalje jednog notification request-a. |
| `GET` | `/notifications/pending` | Vraća notification request-ove sa statusom `pending`. |
| `DELETE` | `/notifications/{id}` | Briše jedan notification request. |
| `DELETE` | `/notifications` | Briše sve notification request-ove. |

### Slanje notifikacija

| Metoda | Endpoint | Opis |
|---|---|---|
| `POST` | `/notifications/{id}/send` | Pokreće slanje postojeće notifikacije. |
| `POST` | `/notifications/process-pending` | Pokreće obradu pending notifikacija. |

### Status endpoint-i

| Metoda | Endpoint | Opis |
|---|---|---|
| `PATCH` | `/notifications/{id}/processing` | Menja status notification request-a u `processing`. |
| `PATCH` | `/notifications/{id}/sent` | Menja status notification request-a u `sent`. |
| `PATCH` | `/notifications/{id}/failed` | Menja status notification request-a u `failed`. |

### Konfiguracioni endpoint-i

| Metoda | Endpoint | Opis |
|---|---|---|
| `GET` | `/notification-types` | Vraća sve definisane tipove notifikacija. |
| `GET` | `/notification-types/{id}` | Vraća jedan tip notifikacije. |
| `GET` | `/channel-configs` | Vraća sve konfiguracije kanala. |
| `GET` | `/channel-configs/{id}` | Vraća jednu konfiguraciju kanala. |
| `GET` | `/notification-templates` | Vraća sve definisane template-e. |
| `GET` | `/notification-templates/{id}` | Vraća jedan template. |

Detaljna interaktivna API dokumentacija dostupna je kroz Swagger UI:

```text
http://localhost:8000/docs
```

## 13. Primeri request-ova

## Primeri zahteva

U nastavku su prikazani primeri zahteva za glavni endpoint:

```text
POST /notifications
```

### Welcome user

```json
{
  "source_service": "user-service",
  "channel": "email",
  "notification_type": "welcome_user",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija",
    "activation_link": "https://example.com/activate/123"
  }
}
```

Primer uspešnog odgovora:

```json
{
  "id": 1,
  "source_service": "user-service",
  "notification_type_id": 1,
  "template_id": 1,
  "channel": "email",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija",
    "activation_link": "https://example.com/activate/123"
  },
  "rendered_subject": "Dobrodošao, Matija!",
  "rendered_body": "Zdravo Matija, dobrodošao u naš sistem. Aktiviraj nalog klikom na sledeći link: https://example.com/activate/123.",
  "status": "sent",
  "error_msg": null,
  "created_at": "2026-06-29T10:00:00",
  "sent_at": "2026-06-29T10:00:01",
  "updated_at": "2026-06-29T10:00:01"
}
```

### Password reset

```json
{
  "source_service": "auth-service",
  "channel": "email",
  "notification_type": "password_reset",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija",
    "reset_link": "https://example.com/reset-password/token123",
    "expiration_minutes": "15"
  }
}
```

### Payment success

```json
{
  "source_service": "payment-service",
  "channel": "email",
  "notification_type": "payment_success",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija",
    "amount": "2500",
    "currency": "RSD",
    "transaction_id": "TX-2026-001"
  }
}
```

### Appointment reminder

```json
{
  "source_service": "appointment-service",
  "channel": "email",
  "notification_type": "appointment_reminder",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija",
    "appointment_date": "2026-06-30",
    "appointment_time": "14:30",
    "location": "Beograd, Bulevar kralja Aleksandra 73"
  }
}
```

### System alert

```json
{
  "source_service": "monitoring-service",
  "channel": "email",
  "notification_type": "system_alert",
  "recipient": "admin@example.com",
  "template_data": {
    "service_name": "payment-service",
    "severity": "HIGH",
    "timestamp": "2026-06-29T12:45:00",
    "message": "Database connection timeout"
  }
}
```

## Primeri grešaka

### Nedostaju obavezne promenljive

Ako se ne pošalje neka od promenljivih koje template zahteva, API vraća grešku.

Primer neispravnog zahteva:

```json
{
  "source_service": "user-service",
  "channel": "email",
  "notification_type": "welcome_user",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija"
  }
}
```

Primer odgovora:

```json
{
  "detail": "Missing required variables: ['activation_link']"
}
```

HTTP status:

```text
400 Bad Request
```

### Nepostojeći tip notifikacije

```json
{
  "source_service": "user-service",
  "channel": "email",
  "notification_type": "unknown_type",
  "recipient": "matija@example.com",
  "template_data": {
    "first_name": "Matija"
  }
}
```

Primer odgovora:

```json
{
  "detail": "Notification type does not exist"
}
```

HTTP status:

```text
400 Bad Request
```

### Nevalidan email format

```json
{
  "source_service": "user-service",
  "channel": "email",
  "notification_type": "welcome_user",
  "recipient": "nije-email",
  "template_data": {
    "first_name": "Matija",
    "activation_link": "https://example.com/activate/123"
  }
}
```

U ovom slučaju validacija se izvršava na nivou Pydantic schema i API vraća:

```text
422 Unprocessable Entity
```

## Napomena

Primeri koriste `email` kanal jer je trenutno za njega implementirano stvarno slanje preko SMTP protokola.  
Ostali kanali postoje u konfiguraciji sistema, ali nemaju implementirane sender-e.

## 14. Planirana unapredjenja

Planirana unapredjenja projekata:

- implementacija dodatnih sendera za Teams, Viber i Whatsapp
- unapredjenje `SenderFactory` mehanizma