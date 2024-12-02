**ACTIVATE VIRTUAL ENVIROMENT**

commands to terminal 

``` ./Scripts/Activate.ps1 ```

```pip install flask etc.```

```docker-compose build --no-cache```

```docker-compose up```


# Sociální síť pro alkoholiky

Projekt sociální sítě zaměřené na alkoholiky s využitím Python-Flask a Neo4j databáze. Součástí aplikace bude messenger a další klíčové funkcionality.

## Funkcionality

### 1. Registrace a přihlášení uživatelů
- Ukládání informací o uživatelích do databáze Neo4j (např. uživatelské jméno, email, heslo).
- Možnost registrace přes email nebo sociální sítě.

### 2. Uživatelské profily
- Možnost přidávat osobní informace (např. věk, záliby, preferované nápoje).
- Profilová fotka.

### 3. Komunity a skupiny
- Tvorba komunit zaměřených na různé druhy alkoholu nebo sdílené zájmy.
- Členství ve skupinách.

### 4. Přátelé a sledování
- Uživatelé mohou navazovat přátelství nebo sledovat ostatní uživatele.
- Návrhy přátel na základě podobných zájmů (využití grafové databáze Neo4j pro doporučení).

### 5. Příspěvky a komentáře
- Uživatelé mohou přidávat příspěvky, fotky a komentáře.
- Lajkování a sdílení obsahu.

### 6. Messenger
- Real-time chat mezi uživateli (např. přes WebSockets).
- Skupinové chaty.

### 7. Události a setkání
- Možnost vytvoření a účast na událostech (např. ochutnávky nebo setkání fanoušků určitého druhu alkoholu).
- Kalendář událostí.

### 8. Moderace a bezpečnost
- Nahlášení nevhodného obsahu.
- Ověření věku.

---

## Jak začít?
1. Návrh datového modelu v Neo4j.
2. Vytvoření základních endpointů pro registraci a přihlášení uživatelů.
3. Postupné přidávání dalších funkcionalit (messenger, skupiny, události).

---
