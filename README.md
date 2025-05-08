# OOP Kursinis – Žaidimas su trimis lygiais

**Autorė:** Greta Garnytė  
**Grupė:** EAf-24  
**Tema:** Platformų, galvosūkių ir dėlionių žaidimas  
**Technologijos:** Python, Pygame, OOP, unittest

---

## 🎮 Aprašymas

Tai objektinio programavimo kursinis darbas, kuriame sukurtas žaidimas su trimis skirtingais lygiais:

1. **Platforminis lygis:** žaidėjas šokinėja tarp platformų ir renka žvaigždes.
2. **Labirinto lygis:** žaidėjas keliauja per tekstu aprašytą labirintą (`maze1.txt`), ieško žvaigždžių.
3. **Dėlionės/reakcijos lygis:** krenta žvaigždės ir kliūtys – reikia rinkti, vengti, išlikti.

Žaidimas sukurtas naudojant **modulinę struktūrą**, atskirus `.py` failus ir **objektinio programavimo principus**.

---

## 📁 Struktūra

```
├── main.py              # Pagrindinis žaidimo paleidimas
├── config.py            # Nustatymai (dydžiai, greičiai, keliai)
├── levels.py            # Visi trys žaidimo lygiai
├── components.py        # Objektai: platformos, žvaigždės, portalai, kliūtys
├── player.py            # Žaidėjo logika
├── maze1.txt            # Labirinto planas
├── player_image.png     # Žaidėjo paveikslėlis 
├── star_image.png       # Žvaigždės paveikslėlis
```

---

## 🧪 Testavimas

Projektas testuotas su `unittest`:
- `test_player.py` – tikrina šuolį ir poziciją
- `test_components.py` – testuoja komponentus
- `test_levels.py` – tikrina `LevelFactory`
- `main.py` nėra testuojamas, nes jame nėra loginės grąžinamos informacijos

---

## 💡 OOP principai

- Paveldėjimas: klasės paveldi iš `Component` ar `pygame.sprite.Sprite`
- Inkapsuliacija: objektai tvarko savo logiką (pvz. `Player`)
- Polimorfizmas: `update()` naudojamas skirtingiems objektams
- Kompozicija: `Level` turi `Player`, `Platform`, `Star` objektus

---

## 🏁 Paleidimas

1. Įsitikink, kad įdiegta `pygame`:  
```
pip install pygame
```

2. Paleisk žaidimą:  
```
python main.py
```

---



