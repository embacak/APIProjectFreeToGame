
import io
import tkinter as tk
from PIL import Image, ImageTk
import requests

# Spieledaten von der API laden und als JSON speichern
URL = "https://www.freetogame.com/api/games"
data = requests.get(URL)
data = data.json()


# Liste beim Tippen nach dem Suchbegriff filtern
def vorschlaege_aktualisieren(event=None):
  suche = eingabe.get().strip().lower()
  vorschlag_liste.delete(0, tk.END)

  for spiel in data:
    if suche in spiel["title"].lower():
      vorschlag_liste.insert(tk.END, spiel["title"])


# Infos und Cover-Bild für das ausgewählte Spiel laden
def spiel_auswaehlen(event=None):
  auswahl = vorschlag_liste.curselection()
  if auswahl:
    gesuchter_titel = vorschlag_liste.get(auswahl[0])
    eingabe.delete(0, tk.END)
    eingabe.insert(0, gesuchter_titel)
  else:
    gesuchter_titel = eingabe.get().strip()

  for spiel in data:
    if gesuchter_titel.lower() in spiel["title"].lower():
      # Textfelder mit den Spieledaten füllen
      titel_var.set(spiel["title"])
      meta_var.set(
          f"Genre: {spiel['genre']}   |   Plattform: {spiel['platform']}\n"
          f"Publisher: {spiel['publisher']}   |   Release:"
          f" {spiel['release_date']}"
      )
      beschreibung_var.set(spiel["short_description"])

      # Cover-Bild herunterladen und anzeigen
      bild_daten = requests.get(spiel["thumbnail"]).content
      pil_bild = Image.open(io.BytesIO(bild_daten))
      pil_bild = pil_bild.resize((540, 305), Image.Resampling.LANCZOS)
      tk_bild = ImageTk.PhotoImage(pil_bild)

      bild_label.config(image=tk_bild, text="")
      bild_label.image = tk_bild
      return


# Hauptfenster erstellen
fenster = tk.Tk()
fenster.title("FreeToGame Explorer")
fenster.state("zoomed")
fenster.configure(bg="#1e1e2e")

# Linke Seite: Suchfeld, Button und Vorschlagsliste
links_frame = tk.Frame(fenster, bg="#252538", width=420, padx=25, pady=25)
links_frame.pack(side="left", fill="y")
links_frame.pack_propagate(False)

tk.Label(
    links_frame,
    text="Game Explorer",
    font=("Segoe UI", 22, "bold"),
    bg="#252538",
    fg="#ffffff",
).pack(anchor="w", pady=(0, 20))

tk.Label(
    links_frame,
    text="Spielname eingeben:",
    font=("Segoe UI", 11),
    bg="#252538",
    fg="#a6adc8",
).pack(anchor="w", pady=(0, 5))

eingabe = tk.Entry(
    links_frame,
    font=("Segoe UI", 13),
    bg="#313244",
    fg="#ffffff",
    insertbackground="white",
    relief="flat",
)
eingabe.pack(fill="x", ipady=8, pady=(0, 12))
eingabe.bind("<KeyRelease>", vorschlaege_aktualisieren)
eingabe.bind("<Return>", spiel_auswaehlen)

btn_suchen = tk.Button(
    links_frame,
    text="Details anzeigen",
    command=spiel_auswaehlen,
    font=("Segoe UI", 11, "bold"),
    bg="#89b4fa",
    fg="#11111b",
    activebackground="#74c7ec",
    relief="flat",
    cursor="hand2",
)
btn_suchen.pack(fill="x", ipady=6, pady=(0, 20))

tk.Label(
    links_frame,
    text="Vorschläge (Anklicken zum Laden):",
    font=("Segoe UI", 10),
    bg="#252538",
    fg="#a6adc8",
).pack(anchor="w", pady=(0, 5))

liste_frame = tk.Frame(links_frame, bg="#313244")
liste_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(liste_frame)
scrollbar.pack(side="right", fill="y")

vorschlag_liste = tk.Listbox(
    liste_frame,
    font=("Segoe UI", 11),
    bg="#313244",
    fg="#cdd6f4",
    selectbackground="#89b4fa",
    selectforeground="#11111b",
    relief="flat",
    highlightthickness=0,
    yscrollcommand=scrollbar.set,
)
vorschlag_liste.pack(side="left", fill="both", expand=True, padx=5, pady=5)
scrollbar.config(command=vorschlag_liste.yview)
vorschlag_liste.bind("<<ListboxSelect>>", spiel_auswaehlen)

# Rechte Seite: Titel, Infos, Cover-Bild und Beschreibung
rechts_frame = tk.Frame(fenster, bg="#1e1e2e", padx=50, pady=40)
rechts_frame.pack(side="right", fill="both", expand=True)

titel_var = tk.StringVar(value="Wähle links ein Spiel aus")
tk.Label(
    rechts_frame,
    textvariable=titel_var,
    font=("Segoe UI", 26, "bold"),
    bg="#1e1e2e",
    fg="#cdd6f4",
    anchor="w",
).pack(fill="x", pady=(0, 10))

meta_var = tk.StringVar(value="")
tk.Label(
    rechts_frame,
    textvariable=meta_var,
    font=("Segoe UI", 12),
    bg="#1e1e2e",
    fg="#89b4fa",
    justify="left",
    anchor="w",
).pack(fill="x", pady=(0, 25))

bild_label = tk.Label(
    rechts_frame,
    bg="#181825",
    fg="#6c7086",
    text="[Kein Bild geladen]",
    font=("Segoe UI", 12),
)
bild_label.pack(anchor="w", pady=(0, 25))

beschreibung_var = tk.StringVar(
    value="Tippe links einen Namen ein, um die Vorschläge zu filtern."
)
tk.Label(
    rechts_frame,
    textvariable=beschreibung_var,
    font=("Segoe UI", 13),
    bg="#1e1e2e",
    fg="#bac2de",
    wraplength=750,
    justify="left",
    anchor="w",
).pack(fill="x")

# Liste beim Programmstart füllen und Fenster starten
vorschlaege_aktualisieren()
fenster.mainloop()