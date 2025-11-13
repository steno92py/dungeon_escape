# Dungeon Escape - Roguelike Game

Un gioco roguelike creato con PgZero per l'insegnamento di Python e dei principi di game development.

## 🎮 Descrizione del Gioco

**Dungeon Escape** è un roguelike minimalista dove il giocatore deve:
- Esplorare dungeon generati proceduralmente
- Evitare nemici con comportamenti AI unici
- Raccogliere la chiave dorata in ogni livello
- Raggiungere la porta di uscita per avanzare
- Sopravvivere attraverso 5 livelli di difficoltà crescente

### Obiettivo
Scappare dal dungeon completando tutti e 5 i livelli. Perdi se i tuoi 3 punti vita si esauriscono!

## 📋 Requisiti Soddisfatti

✅ **Librerie utilizzate:** Solo PgZero, math, random (+ Rect da pygame come eccezione consentita)
✅ **Genere:** Roguelike con generazione procedurale
✅ **Menu principale** con pulsanti chiari:
   - Avvia partita
   - Toggle Music (solo musica di sottofondo)
   - Toggle Sound (solo effetti sonori)
   - Esci

✅ **Audio completo:** Musica di sottofondo in loop + 7 effetti sonori
✅ **Nemici multipli:** 4 tipi di slime con comportamenti AI distinti
✅ **Movimento nemici:** Ogni nemico ha pattern di movimento unico e intelligenza artificiale
✅ **Classi con animazioni:** Sistema completo di animazioni frame-based
✅ **Animazioni idle e walk:** Per personaggio principale e tutti i nemici
✅ **Naming PEP8:** Nomi in inglese seguendo le convenzioni Python
✅ **Meccaniche roguelike:** Generazione procedurale, permadeath, difficoltà progressiva
✅ **Codice originale:** Completamente scritto da zero con architettura OOP pulita

## 🚀 Come Eseguire il Gioco

### Installazione dipendenze:
```bash
pip install pgzero
# oppure
python -m pip install pgzero
```

### Esecuzione (metodo consigliato e stabile):
```bash
# Dalla cartella del progetto
python -m pgzero main.py

# Oppure, se disponibile
pgzrun main.py
```

**Nota importante:** Su alcuni ambienti macOS/Conda, l'avvio con `python main.py` può non aprire la finestra di gioco. Usa i comandi sopra (metodi ufficiali di PgZero) per un avvio affidabile.

### Audio
- Tutti gli audio sono in formato WAV e funzionano senza conversioni aggiuntive
- La musica di sottofondo parte automaticamente e va in loop
- Non sono necessari strumenti esterni: avvia il gioco e basta!

## 🎮 Controlli di Gioco

### Durante il gioco
- **WASD** o **Frecce direzionali**: Movimento del personaggio (8 direzioni)
- Il movimento diagonale è normalizzato (stessa velocità del movimento retto)

### Menu
- **Mouse**: Navigazione e hover sui pulsanti
- **Click sinistro**: Selezione opzioni

### Schermate Game Over / Vittoria
- **SPAZIO**: Ritorna al menu principale

## 🏗️ Struttura del Progetto

```
dungeon_escape/
│
├── main.py                          # File principale del gioco (27 KB)
├── README.md                        # Questa documentazione
├── .gitignore                       # Esclude file Python generati e IDE
│
├── images/                          # Sprite del gioco (24 file PNG)
│   ├── Characters/                  # 9 sprite del personaggio principale
│   │   ├── character_beige_idle.png
│   │   ├── character_beige_walk_a.png
│   │   ├── character_beige_walk_b.png
│   │   ├── character_beige_climb_a.png
│   │   ├── character_beige_climb_b.png
│   │   ├── character_beige_duck.png
│   │   ├── character_beige_front.png
│   │   ├── character_beige_hit.png
│   │   └── character_beige_jump.png
│   │
│   ├── Enemies/                     # 16 sprite nemici (4 tipi)
│   │   ├── slime_normal_*.png      # Slime verde (rest, walk_a/b, flat)
│   │   ├── slime_fire_*.png        # Slime fuoco (rest, walk_a/b, flat)
│   │   ├── slime_block_*.png       # Slime block (rest, walk_a/b, jump)
│   │   └── slime_spike_*.png       # Slime spike (rest, walk_a/b, flat)
│   │
│   ├── door_closed.png              # Porta chiusa
│   ├── door_open.png                # Porta aperta
│   ├── floor.png                    # Pavimento
│   ├── wall.png                     # Muro
│   ├── key_yellow.png               # Chiave dorata
│   ├── hud_heart.png                # Cuore pieno (vita)
│   └── hud_heart_empty.png          # Cuore vuoto
│
└── sounds/                          # Audio (8 file WAV, ~1.8 MB totali)
    ├── background.wav               # Musica di sottofondo (loop infinito)
    ├── hit.wav                      # Suono danno al giocatore
    ├── pickup.wav                   # Raccolta chiave
    ├── start.wav                    # Inizio gioco
    ├── gameover.wav                 # Game over
    ├── victory.wav                  # Vittoria
    ├── nextlevel.wav                # Passaggio di livello
    └── toggle.wav                   # Toggle opzioni audio
```

## 🎯 Caratteristiche del Gioco

### Personaggio Principale (Player)
- **Vita:** 3 cuori (3 HP)
- **Velocità:** 150 pixel/secondo
- **Movimento:** 8 direzioni (WASD o frecce direzionali)
- **Animazioni:**
  - Idle (2 frame - respirazione)
  - Walk (2 frame - camminata)
- **Invulnerabilità:** 1.5 secondi dopo essere colpito (effetto flash)
- **Hitbox:** 30x30 pixel per collision detection

### Nemici - I Quattro Slime

Tutti i nemici hanno animazioni (idle + walk) e comportamenti AI unici:

#### 🟢 Slime Normal (Verde)
- **Comportamento:** Vaga casualmente, insegue se il player è entro 120 pixel
- **Velocità:** 50 pixel/secondo (lento)
- **AI:** Cambia direzione random ogni 1-2 secondi
- **Strategia:** Facile da evitare, pericoloso in gruppo

#### 🔥 Slime Fire (Fuoco)
- **Comportamento:** Caccia attivamente il giocatore
- **Velocità:** 80 pixel/secondo (veloce!)
- **AI:** Percepisce il player da 200 pixel di distanza
- **Strategia:** Nemico più pericoloso, insegue aggressivamente

#### 🟦 Slime Block (Blocco)
- **Comportamento:** Pattuglia tra 2 punti fissi (difesa area)
- **Velocità:** 60 pixel/secondo (media)
- **AI:** Attacca se player entro 100 pixel, altrimenti pattuglia
- **Strategia:** Controlla zone specifiche, tipo "tank"

#### ⚡ Slime Spike (Spike)
- **Comportamento:** Movimento erratico e imprevedibile
- **Velocità:** 70 pixel/secondo (medio-veloce)
- **AI:** Random movement, insegue entro 150 pixel
- **Strategia:** Difficile da predire, aggressivo quando vicino

### Sistema di Livelli

**Progressione:** 5 livelli totali prima della vittoria

**Difficoltà crescente:**
- **Livello 1:** 7 muri interni, 3 nemici
- **Livello 2:** 9 muri interni, 4 nemici
- **Livello 3:** 12 muri interni, 6 nemici
- **Livello 4:** 15 muri interni, 7 nemici
- **Livello 5:** 18 muri interni, 9 nemici

**Generazione procedurale:**
- Ogni livello è generato casualmente
- Muri perimetrali fissi + muri interni random
- Spawn garantiti per: Player, Chiave, Porta, Nemici
- Chiave spawna sempre a distanza di almeno 6 tile dal player
- Nessun seed fisso: ogni partita è unica

### Meccaniche di Gioco

#### Sistema Vita
- Inizi con 3 cuori
- Ogni collisione con un nemico toglie 1 cuore
- Dopo il danno: 1.5 secondi di invulnerabilità (effetto flash)
- Se vita = 0: Game Over

#### Raccolta Oggetti
- **Chiave Dorata:** Deve essere raccolta prima di aprire la porta
- **Porta:** Aperta solo se hai la chiave, poi puoi avanzare al livello successivo
- Hitbox chiave: 40x40 pixel
- Hitbox porta: 40x80 pixel

#### Collisioni
- I muri bloccano player e nemici
- I nemici non si bloccano tra loro
- Collision detection basata su Rect di pygame
- Movimento normalizzato per velocità costante

## 🔧 Dettagli Tecnici

### Configurazione Finestra
```python
WIDTH = 800              # Larghezza finestra
HEIGHT = 600             # Altezza finestra
TILE_SIZE = 40           # Dimensione cella griglia
GRID_WIDTH = 20          # 20 celle orizzontali
GRID_HEIGHT = 14         # 14 celle verticali (incluso HUD)
HUD_HEIGHT = 40          # Altezza barra HUD inferiore
```

### Classi Principali

#### `Animation`
Gestisce animazioni sprite frame-based.
```python
- frames: lista di frame (immagini)
- fps: frame per secondo (default: 8)
- update(dt): avanza frame in base al tempo
- get_current_frame(): ritorna frame corrente
- reset(): riporta alla prima frame
```

#### `Character` (Classe Base)
Classe astratta per tutti i personaggi con:
- Sistema di movimento con normalizzazione diagonale
- Collision detection con muri
- Gestione stati (idle, move)
- Sistema animazioni integrato
- Hitbox 30x30 pixel per collisioni

#### `Player(Character)`
Estende Character con:
- Gestione input tastiera (WASD/Frecce)
- Sistema vita e danno (health, max_health)
- Timer invulnerabilità con effetto visuale
- Velocità: 150 px/sec

#### `Enemy(Character)` (Classe Base Astratta)
Base per tutti i nemici con:
- Metodo `think(player_pos, dt)` per AI (implementato in sottoclassi)
- Metodo `update(dt, player_pos)` per update
- Behavior timer per comportamenti temporizzati

#### Sottoclassi Enemy
- `SlimeNormal`: Vaga e insegue (120px detection)
- `SlimeFire`: Caccia aggressiva (200px detection)
- `SlimeBlock`: Pattuglia area fissa (100px detection)
- `SlimeSpike`: Movimento erratico (150px detection)

#### `MenuButton`
Gestione pulsanti interattivi del menu:
- Testo, posizione, azione
- Hover effect (cambio colore)
- Click detection

### Funzioni Principali

#### `generate_level(level_num)`
Genera dungeon procedurali:
1. Crea bordi perimetrali (muri)
2. Aggiunge muri interni random
3. Identifica tile libere (pavimento)
4. Spawn: Player → Chiave (min 6 tile away) → Porta → Nemici

#### `update(dt)`
Game loop principale:
- Gestisce input per stati diversi
- Update player (movimento, animazioni, invulnerabilità)
- Update nemici (AI, movimento, collision con player)
- Check raccolta chiave
- Check interazione porta → next_level()
- Check game over

#### `draw()`
Rendering grafico a layer:
1. Background (colore sfondo)
2. Pavimento (tile floor)
3. Muri (sprite wall)
4. Chiave e Porta
5. Nemici
6. Player (con flash se invulnerabile)
7. HUD (cuori, livello, key indicator)

#### `draw_hud()`
Interfaccia utente inferiore:
- Cuori vita (pieni/vuoti)
- Numero livello attuale
- Indicatore chiave raccolta

### Stati di Gioco

```python
STATE_MENU = "menu"           # Menu principale
STATE_PLAYING = "playing"     # Gameplay attivo
STATE_GAME_OVER = "game_over" # Sconfitta
STATE_VICTORY = "victory"     # Vittoria (5 livelli completati)
```

### Sistema Audio

**Musica di sottofondo:**
```python
sounds.background.play(-1)    # -1 = loop infinito
```

**Effetti sonori:**
- `sounds.hit.play()` - Danno al player
- `sounds.pickup.play()` - Raccolta chiave
- `sounds.start.play()` - Inizio gioco
- `sounds.gameover.play()` - Game over
- `sounds.victory.play()` - Vittoria
- `sounds.nextlevel.play()` - Prossimo livello
- `sounds.toggle.play()` - Toggle audio

**Controlli audio:**
- `music_enabled` - Toggle musica di sottofondo
- `sound_enabled` - Toggle effetti sonori
- Separati per permettere controllo granulare

## 🎓 Note per l'Insegnamento

Questo progetto è ideale per insegnare:

### Concetti di Programmazione
1. **OOP in Python:**
   - Classi e oggetti
   - Ereditarietà (Character → Player/Enemy)
   - Polimorfismo (metodo think() diverso per ogni nemico)
   - Incapsulamento (attributi privati, metodi pubblici)

2. **Design Patterns:**
   - State pattern (menu, playing, game over, victory)
   - Update/Draw pattern (game loop)
   - Component pattern (Animation come componente)

3. **Algoritmi:**
   - Collision detection (AABB con Rect)
   - Pathfinding semplice (inseguimento diretto)
   - Normalizzazione vettori (movimento diagonale)
   - Distance calculation (hypot per detection range)

4. **Strutture Dati:**
   - Liste (walls, enemies, free_tiles)
   - Dizionari (animations per stato)
   - Tuple (posizioni x,y)

### Concetti di Game Development
1. **Game Loop:** Update (logica) → Draw (rendering)
2. **Delta Time:** Movimento frame-independent
3. **Animation System:** Frame-based animations
4. **Collision Detection:** Hitbox e Rect
5. **Procedural Generation:** Dungeon random
6. **AI semplice:** Pattern di movimento e detection range
7. **State Management:** FSM (Finite State Machine)
8. **HUD e UI:** Rendering informazioni player

### Best Practices
1. **PEP8:** Naming conventions, snake_case
2. **Commenti:** Codice ben documentato in italiano
3. **Separation of Concerns:** Classi con responsabilità singole
4. **DRY (Don't Repeat Yourself):** Ereditarietà per riutilizzo codice
5. **Readability:** Nomi variabili chiari e descrittivi

## 🎨 Personalizzazioni e Espansioni Possibili

Per espandere il progetto, si potrebbero aggiungere:

### Gameplay
- **Power-up:** Scudo temporaneo, velocità aumentata, vita extra
- **Armi/Attacco:** Permettere al player di eliminare nemici
- **Boss Fight:** Boss speciale ogni 5 livelli
- **Trappole:** Spike trap, buchi, lave
- **Tesori:** Monete per sistema di punteggio
- **Timer:** Completare livello entro tempo limite

### Meccaniche
- **Sistema di punteggio:** Punti per livello, nemici evitati, tempo
- **Salvataggio progressi:** Persistenza tra sessioni
- **Seed-based generation:** Livelli riproducibili
- **Minimap:** Mappa del dungeon nell'HUD
- **Oggetti consumabili:** Pozioni, pergamene
- **Stanze speciali:** Shop, stanza tesoro, stanza puzzle

### Nemici e AI
- **Nuovi tipi nemici:** Boss, volanti, ranged
- **AI più complessa:** A* pathfinding, cooperative behavior
- **Nemici con pattern:** Movimento a zig-zag, circolare
- **Nemici con abilità:** Teletrasporto, invisibilità

### Tecnici
- **Effetti particellari:** Esplosioni, polvere
- **Screenshake:** Camera shake per impatti
- **Lighting system:** Torce, aree buie
- **Parallax background:** Sfondo a layer multipli
- **Transizioni:** Fade in/out tra livelli
- **Particle trails:** Scie dietro player/nemici

### Audio/Visuale
- **Più musiche:** Musica diversa per livello
- **Ambient sounds:** Passi, porte, vento
- **Sprite variations:** Palette swap per nemici
- **Tile variations:** Più varianti floor/wall

## 📊 Statistiche Progetto

### Analisi Righe di Codice (main.py)
- **Totale righe:** 1037
- **Codice puro:** 401 righe (38.7%)
- **Codice + commento inline:** 2 righe (0.2%)
- **Commenti (#):** 52 righe (5.0%)
- **Docstring ("""..."""):** 399 righe (38.5%)
- **Righe vuote:** 183 righe (17.6%)

**Rapporto Documentazione/Codice:** ~1:1 (eccellente per progetto didattico)

### Componenti Codice
- **Classi:** 9 (Animation, Character, Player, Enemy, SlimeNormal, SlimeFire, SlimeBlock, SlimeSpike, MenuButton)
- **Funzioni globali:** 15
- **Metodi di classe:** 30+
- **Costanti globali:** 11

### Asset
- **Asset grafici:** 24 file PNG (~25 KB totali)
  - 9 sprite personaggio principale
  - 16 sprite nemici (4 tipi × 4 frame ciascuno)
  - 7 sprite ambiente/oggetti
  - 2 sprite HUD
- **Asset audio:** 8 file WAV (~1.8 MB totali)
  - 1 musica di sottofondo (loop)
  - 7 effetti sonori

### Dimensioni File
- **main.py:** 33.2 KB (1037 righe)
- **Progetto totale:** ~2 MB

## 📚 Documentazione Codice Completa

### Costanti Globali
```python
WIDTH = 800                    # Larghezza finestra di gioco
HEIGHT = 600                   # Altezza finestra di gioco
TILE_SIZE = 40                 # Dimensione di ogni tile (40x40 pixel)
GRID_WIDTH = 20                # Numero di tile in orizzontale
GRID_HEIGHT = 14               # Numero di tile in verticale
HUD_HEIGHT = 40                # Altezza barra HUD inferiore
HUD_ICON_PX = 32               # Dimensione icone HUD (cuori, chiave)

STATE_MENU = "menu"            # Stato: menu principale
STATE_PLAYING = "playing"      # Stato: gameplay attivo
STATE_GAME_OVER = "game_over"  # Stato: schermata game over
STATE_VICTORY = "victory"      # Stato: schermata vittoria
STATE_PAUSED = "paused"        # Stato: gioco in pausa
```

### Variabili Globali
```python
game_state                     # Stato corrente del gioco
current_level                  # Livello attuale (1-5)
player                         # Istanza del giocatore
enemies = []                   # Lista di tutti i nemici nel livello
walls = []                     # Lista di Rect rappresentanti i muri
floor_tiles = []               # Lista di tuple (x, y) per le tile pavimento
key_collected                  # Bool: chiave raccolta o no
door_position                  # Tuple (x, y) posizione porta
key_position                   # Tuple (x, y) posizione chiave
key_actor                      # Actor PgZero per sprite chiave
door_actor                     # Actor PgZero per sprite porta
music_enabled                  # Bool: musica abilitata
sound_enabled                  # Bool: effetti sonori abilitati
menu_buttons = []              # Lista pulsanti menu principale
pause_buttons = []             # Lista pulsanti menu pausa
level_time_accum               # Float: tempo accumulato nel livello corrente
level_times = []               # Lista: tempi di completamento di ogni livello
```

---

### Classe: `Animation`
**Descrizione:** Gestisce animazioni sprite frame-based con timing automatico

#### Attributi
- `frames` (list): Lista di nomi frame (stringhe)
- `fps` (int): Frame per secondo (velocità animazione)
- `current_frame` (int): Indice frame corrente
- `time_accumulated` (float): Tempo accumulato per cambio frame

#### Metodi
```python
__init__(self, frames, fps=8)
    """Inizializza animazione con lista frame e velocità"""

update(self, dt)
    """Avanza animazione in base al tempo trascorso (dt in secondi)"""

get_current_frame(self)
    """Ritorna il nome del frame corrente da visualizzare"""

reset(self)
    """Reset animazione: torna al primo frame e azzera tempo"""
```

---

### Classe: `Character` (Base Class)
**Descrizione:** Classe base per tutti i personaggi con movimento, collisioni e animazioni

#### Attributi
- `x, y` (float): Coordinate pixel del centro del personaggio
- `speed` (float): Velocità movimento in pixel/secondo
- `dx, dy` (float): Direzione movimento normalizzata (-1 a 1)
- `state` (str): Stato corrente ("idle" o "move")
- `animations` (dict): Dizionario {stato: Animation}
- `actor` (Actor): Actor PgZero per rendering
- `hitbox` (Rect): Rectangle per collision detection

#### Metodi
```python
__init__(self, x, y, speed, hitbox_size=20)
    """Inizializza personaggio con posizione, velocità e hitbox"""

setup_animations(self, idle_frames, move_frames)
    """Registra animazioni idle e move, crea Actor"""

move(self, dt)
    """Aggiorna posizione con normalizzazione e collision detection.
    - Normalizza movimento diagonale
    - Controlla collisioni con muri
    - Mantiene personaggio dentro i bordi schermo"""

update_animation(self, dt)
    """Avanza animazione corrente e aggiorna sprite Actor"""

draw(self)
    """Disegna lo sprite sullo schermo"""
```

---

### Classe: `Player(Character)`
**Descrizione:** Personaggio giocabile con input, vita e invulnerabilità

#### Attributi (oltre a Character)
- `health` (int): Vita corrente (0-3)
- `max_health` (int): Vita massima (3)
- `invulnerable_timer` (float): Timer invulnerabilità (1.5s dopo danno)

#### Metodi
```python
__init__(self, x, y)
    """Crea player con animazioni, velocità 150 px/s, hitbox 22px"""

handle_input(self)
    """Legge input tastiera (WASD/Frecce) e imposta dx, dy"""

take_damage(self, amount=1)
    """Applica danno se non invulnerabile.
    - Toglie vita
    - Attiva invulnerabilità 1.5s
    - Suona effetto hit
    - Chiama game_over() se vita = 0"""

update(self, dt)
    """Update completo player:
    - Decrementa timer invulnerabilità
    - Legge input
    - Muove personaggio
    - Aggiorna animazione"""
```

---

### Classe: `Enemy(Character)` (Base Class)
**Descrizione:** Classe base per tutti i nemici con AI

#### Attributi (oltre a Character)
- `behavior_timer` (float): Timer per comportamenti temporizzati

#### Metodi
```python
__init__(self, x, y, speed)
    """Inizializza nemico con velocità e hitbox 20px"""

think(self, player_pos, dt)
    """Metodo astratto: implementato nelle sottoclassi.
    Decide movimento (dx, dy) in base a posizione player e AI"""

update(self, dt, player_pos)
    """Update completo nemico:
    - Esegue AI (think)
    - Muove nemico
    - Aggiorna animazione"""
```

---

### Classe: `SlimeNormal(Enemy)`
**Descrizione:** Slime verde che vaga e insegue quando vicino

#### Parametri
- Velocità: 50 px/s (lento)
- Detection range: 120 pixel
- Animazioni: idle (rest × 2), walk (walk_a, walk_b)

#### Metodi
```python
__init__(self, x, y)
    """Crea slime normale con animazioni verde"""

wander_direction(self)
    """Sceglie direzione casuale per vagare (1-2 secondi)"""

think(self, player_pos, dt)
    """AI: Insegue se player < 120px, altrimenti vaga casualmente"""
```

---

### Classe: `SlimeFire(Enemy)`
**Descrizione:** Slime fuoco veloce che caccia aggressivamente

#### Parametri
- Velocità: 80 px/s (veloce)
- Detection range: 200 pixel
- Animazioni: idle (rest × 2), walk (walk_a, walk_b)

#### Metodi
```python
__init__(self, x, y)
    """Crea slime fuoco con animazioni rosse"""

think(self, player_pos, dt)
    """AI: Insegue direttamente se player < 200px, altrimenti pattuglia"""
```

---

### Classe: `SlimeBlock(Enemy)`
**Descrizione:** Slime blocco che pattuglia tra punti fissi

#### Parametri
- Velocità: 60 px/s (media)
- Detection range: 100 pixel
- Patrol points: ±80px dalla posizione spawn
- Animazioni: idle (rest × 2), walk (walk_a, walk_b)

#### Attributi Extra
- `patrol_points` (list): Lista di 2 punti di pattuglia
- `current_target` (int): Indice punto target corrente

#### Metodi
```python
__init__(self, x, y)
    """Crea slime block con pattuglia orizzontale"""

think(self, player_pos, dt)
    """AI: Attacca se player < 100px, altrimenti pattuglia tra punti"""
```

---

### Classe: `SlimeSpike(Enemy)`
**Descrizione:** Slime spike con movimento erratico e imprevedibile

#### Parametri
- Velocità: 70 px/s (medio-veloce)
- Detection range: 150 pixel
- Animazioni: idle (rest × 2), walk (walk_a, walk_b)

#### Attributi Extra
- `change_direction_timer` (float): Timer cambio direzione casuale
- `is_aggressive` (bool): Flag modalità aggressiva

#### Metodi
```python
__init__(self, x, y)
    """Crea slime spike con movimento erratico"""

think(self, player_pos, dt)
    """AI: Insegue aggressivamente se < 150px,
    altrimenti movimento random ogni 0.5-1.5s"""
```

---

### Classe: `MenuButton`
**Descrizione:** Pulsante cliccabile per menu con hover effect

#### Attributi
- `text` (str): Etichetta pulsante
- `rect` (Rect): Rectangle per area cliccabile
- `action` (str): Identificatore azione ("start", "toggle_music", etc.)
- `hovered` (bool): Stato hover (mouse sopra)

#### Metodi
```python
__init__(self, text, x, y, width, height, action)
    """Crea pulsante centrato in (x, y) con dimensioni e azione"""

check_hover(self, mouse_pos)
    """Aggiorna stato hover in base a posizione mouse"""

draw(self)
    """Disegna pulsante con effetto hover (colore diverso se hovered)"""
```

---

## 🎯 Funzioni Globali

### Generazione e Gestione Livelli

```python
generate_level(level_num)
    """Genera dungeon procedurale per livello specificato.

    Processo:
    1. Crea muri perimetrali (bordo fisso)
    2. Aggiunge muri interni casuali (quantità basata su level_num)
    3. Identifica tutte le tile libere (pavimento)
    4. Posiziona player su tile libera
    5. Posiziona chiave lontano dal player (min 6 tile)
    6. Posiziona porta su tile libera (preferenza: destra)
    7. Spawn nemici su tile libere (tipo/quantità basati su level_num)

    Parametri:
    - level_num (int): 1-5, determina difficoltà (muri, nemici)

    Modifica globali: walls, floor_tiles, enemies, player,
                       key_position, door_position, key_actor, door_actor"""

choose_enemy_type(level_num)
    """Sceglie tipo nemico casuale in base a livello.

    Distribuzione per livello:
    - Livello 1: 100% SlimeNormal
    - Livello 2: 70% Normal, 30% Fire
    - Livello 3: 40% Normal, 35% Fire, 25% Block
    - Livello 4: 25% Normal, 35% Fire, 25% Block, 15% Spike
    - Livello 5: 15% Normal, 30% Fire, 30% Block, 25% Spike

    Return: int (0=Normal, 1=Fire, 2=Block, 3=Spike)"""

next_level()
    """Avanza al livello successivo.
    - Salva tempo livello completato
    - Incrementa current_level
    - Reset key_collected
    - Se livello > 5: chiama victory()
    - Altrimenti: genera nuovo livello e suona nextlevel.wav"""
```

---

### Menu e Navigazione

```python
create_menu()
    """Crea pulsanti menu principale.
    Pulsanti: Avvia Partita, Musica ON/OFF, Suoni ON/OFF, Esci"""

create_pause_menu()
    """Crea pulsanti menu pausa.
    Pulsanti: Riprendi Partita, Esci"""

pause_game()
    """Mette il gioco in pausa (STATE_PAUSED)"""

resume_game()
    """Riprende il gioco da pausa (STATE_PLAYING)"""

quit_to_menu()
    """Esce dalla partita e torna al menu principale.
    Ferma musica di sottofondo"""
```

---

### Gestione Gioco

```python
start_game()
    """Inizia nuova partita.
    - Reset: livello 1, vita piena, key_collected = False
    - Reset player (None per ricreare con vita piena)
    - Azzera timer e tempi livelli
    - Genera primo livello
    - Avvia musica e suono start"""

game_over()
    """Gestisce sconfitta giocatore.
    - Salva tempo livello corrente
    - Cambia stato a STATE_GAME_OVER
    - Ferma musica
    - Suona effetto gameover"""

victory()
    """Gestisce vittoria (5 livelli completati).
    - Cambia stato a STATE_VICTORY
    - Suona effetto victory"""

toggle_music()
    """Toggle musica di sottofondo on/off.
    Avvia/ferma loop background.wav"""

toggle_sound()
    """Toggle effetti sonori on/off.
    Non influenza musica di sottofondo"""
```

---

### Audio

```python
start_background_music()
    """Avvia musica di sottofondo in loop infinito.
    sounds.background.play(-1)"""

stop_background_music()
    """Ferma musica di sottofondo.
    Ignora errori se non attiva"""
```

---

### Game Loop (PgZero Callbacks)

```python
update(dt)
    """Game loop principale - chiamato ogni frame da PgZero.

    Parametri:
    - dt (float): Delta time in secondi dall'ultimo frame

    Comportamento per stato:

    STATE_MENU:
      - Nessun update (hover gestito da on_mouse_move)

    STATE_PLAYING:
      - Accumula tempo livello
      - Update player (input, movimento, animazioni)
      - Update nemici (AI, movimento, animazioni)
      - Check collisioni player-nemici → take_damage()
      - Check raccolta chiave → key_collected = True
      - Check porta (se key_collected) → next_level()

    Altri stati: nessun update"""

draw()
    """Rendering - chiamato ogni frame da PgZero dopo update().

    Delega rendering allo stato corrente:
    - STATE_MENU: draw_menu()
    - STATE_PLAYING: draw_game()
    - STATE_GAME_OVER: draw_game_over()
    - STATE_VICTORY: draw_victory()
    - STATE_PAUSED: draw_game() + draw_pause()"""
```

---

### Rendering

```python
draw_menu()
    """Disegna menu principale.
    - Titolo "DUNGEON ESCAPE"
    - Stato audio (Musica ON/OFF | Suoni ON/OFF)
    - Pulsanti menu (menu_buttons)"""

draw_game()
    """Disegna schermata di gioco (layer multipli).

    Ordine rendering:
    1. Background (colore riempimento)
    2. Tile pavimento (floor_tiles)
    3. Muri (walls)
    4. Chiave (se non raccolta)
    5. Porta
    6. Nemici
    7. Player (con effetto flash se invulnerabile)
    8. HUD (draw_hud)"""

draw_pause()
    """Disegna overlay menu pausa.
    - Pannello centrale semi-trasparente
    - Titolo "PAUSA"
    - Pulsanti pausa (pause_buttons)"""

draw_hud()
    """Disegna barra HUD inferiore.
    - Background HUD (40px altezza)
    - Cuori vita (pieni/vuoti)
    - Indicatore chiave (se raccolta)
    - Numero livello corrente"""

draw_game_over()
    """Disegna schermata game over.
    - Titolo "FINE PARTITA"
    - Livello raggiunto
    - Tempo totale partita (mm:ss.ms)
    - Istruzioni (SPAZIO per menu)"""

draw_victory()
    """Disegna schermata vittoria.
    - Titolo "VITTORIA!"
    - Messaggio vittoria
    - Tempo totale partita (mm:ss.ms)
    - Istruzioni (SPAZIO per menu)"""
```

---

### Input Handling (PgZero Callbacks)

```python
on_mouse_down(pos, button)
    """Gestisce click mouse.

    STATE_MENU:
      - Check click su menu_buttons
      - Esegue azione pulsante cliccato
        (start, toggle_music, toggle_sound, exit)

    STATE_PAUSED:
      - Check click su pause_buttons
      - Esegue azione (resume, quit_to_menu)"""

on_mouse_move(pos)
    """Aggiorna hover effect pulsanti.

    STATE_MENU: aggiorna hover su menu_buttons
    STATE_PAUSED: aggiorna hover su pause_buttons"""

on_key_down(key)
    """Gestisce pressione tasti.

    SPACE:
      - Da STATE_GAME_OVER/VICTORY: torna a STATE_MENU

    ESC o P:
      - Da STATE_PLAYING: pause_game()
      - Da STATE_PAUSED: resume_game()"""
```

---

### Funzioni di Inizializzazione

```python
create_menu()
    """Chiamata all'avvio per creare menu iniziale"""

# Entry point
if __name__ == '__main__':
    """Stampa istruzioni esecuzione (python -m pgzero main.py)"""
```

---

## 🐛 Note Tecniche

### Normalizzazione Movimento
Il movimento diagonale è normalizzato per evitare velocità √2 maggiore:
```python
mag = hypot(self.dx, self.dy)
if mag > 0:
    self.dx /= mag
    self.dy /= mag
```

### Invulnerabilità Visuale
Effetto flash durante invulnerabilità:
```python
if player.invulnerable_timer <= 0 or int(player.invulnerable_timer * 10) % 2 == 0:
    player.draw()  # Disegna solo su frame pari = effetto lampeggio
```

### Spawn Sicuro
Il gioco garantisce che chiave, porta e nemici spawnino su tile libere (non su muri) e che la chiave sia lontana almeno 6 tile dal player.

## 📄 Licenza

Progetto educativo - Libero uso per insegnamento e apprendimento.

---

**Creato per l'insegnamento di Python e Game Development** 🎮🐍
**Buon divertimento e buon apprendimento!**

**Stefano Nocco**
