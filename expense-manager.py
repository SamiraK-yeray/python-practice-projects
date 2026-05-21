from customtkinter import *
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry



set_appearance_mode("dark")
window = CTk()
window.title("Gestionnaire de dépenses")
window.geometry("1100x700")
window.resizable(False, False)


conn = sqlite3.connect("expense.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS Expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    montant REAL NOT NULL,
    categorie TEXT NOT NULL,
    date TEXT NOT NULL)
""")
conn.commit()
conn.close()


CATEGORIES = ["Nourriture", "Transport", "Loisirs", "Logement", "Santé", "Autre"]


def ajouter():
    m = champ_montant.get()
    c = champ_categorie.get()
    d = champ_date.get()

    if m == "" or c == "" or d == "":
        label_message.configure(text="Remplissez tous les champs !", text_color="red")
        return

    try:
        float(m)
    except ValueError:
        label_message.configure(text="Le montant doit être un nombre !", text_color="red")
        return

    con = sqlite3.connect("expense.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO Expenses (montant, categorie, date) VALUES (?,?,?)", (m, c, d))
    con.commit()
    con.close()

    champ_montant.delete(0, "end")
    champ_date.delete(0, "end")
    champ_categorie.set(CATEGORIES[0])

    label_message.configure(text="Dépense ajoutée !", text_color="green")
    afficher_depenses()
    afficher_analyses()


def afficher_depenses():
    con = sqlite3.connect("expense.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Expenses")
    lignes = cursor.fetchall()
    con.close()

    textbox.configure(state="normal")
    textbox.delete("1.0", END)
    if not lignes:
        textbox.insert(END, "Aucune dépense enregistrée.")
    for ligne in lignes:
        textbox.insert(END, f"  ID: {ligne[0]}  |  {ligne[1]}€  |  {ligne[2]}  |  {ligne[3]}\n")
    textbox.configure(state="disabled")


def supprimer():
    id_val = champ_sup.get()
    if id_val == "":
        label_message.configure(text="Entrez un ID à supprimer !", text_color="red")
        return

    con = sqlite3.connect("expense.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM Expenses WHERE id = ?", (id_val,))
    con.commit()
    con.close()

    champ_sup.delete(0, "end")
    label_message.configure(text=f"ID {id_val} supprimé !", text_color="green")
    afficher_depenses()
    afficher_analyses()


def afficher_analyses():
    con = sqlite3.connect("expense.db")
    df = pd.read_sql_query("SELECT * FROM Expenses", con)
    con.close()

    if df.empty:
        label_total.configure(text="Total : 0 €")
        label_max.configure(text="Maximum : 0 €")
        label_min.configure(text="Minimum : 0 €")
        label_nb.configure(text="Nombre : 0")
        return

    label_total.configure(text=f"Total : {df['montant'].sum():.2f} €")
    label_max.configure(text=f"Maximum : {df['montant'].max():.2f} €")
    label_min.configure(text=f"Minimum : {df['montant'].min():.2f} €")
    label_nb.configure(text=f"Nombre : {len(df)}")

    afficher_graphique(df)


def afficher_graphique(df):
    for widget in frame_graph.winfo_children():
        widget.destroy()

    if df.empty:
        return

    groupe = df.groupby("categorie")["montant"].sum()

    fig, ax = plt.subplots(figsize=(4, 3), facecolor="#2b2b2b")
    ax.set_facecolor("#2b2b2b")
    groupe.plot(kind="bar", ax=ax, color=["#4e9af1", "#f1714e", "#4ef1a0", "#f1d84e", "#d44ef1", "#f14e8a"])
    ax.set_title("Dépenses par catégorie", color="white", fontsize=10)
    ax.tick_params(colors="white", labelsize=7)
    ax.set_xlabel("")
    for spine in ax.spines.values():
        spine.set_edgecolor("#555")
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)


frame_gauche = CTkFrame(window, width=350, fg_color="#1e1e1e", corner_radius=0)
frame_gauche.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
frame_gauche.grid_propagate(False)

frame_droite = CTkFrame(window, fg_color="#1e1e1e", corner_radius=0)
frame_droite.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)


CTkLabel(frame_gauche, text="Gestionnaire de dépenses",
         font=("Arial", 16, "bold"), text_color="white").pack(pady=(20, 15))

CTkLabel(frame_gauche, text="Montant (€)", anchor="w").pack(fill="x", padx=20)
champ_montant = CTkEntry(frame_gauche, width=300, height=38, placeholder_text="ex: 25.50")
champ_montant.pack(padx=20, pady=(3, 10))

CTkLabel(frame_gauche, text="Catégorie", anchor="w").pack(fill="x", padx=20)
champ_categorie = CTkOptionMenu(frame_gauche, width=300, height=38, values=CATEGORIES)
champ_categorie.pack(padx=20, pady=(3, 10))

CTkLabel(frame_gauche, text="Date", anchor="w").pack(fill="x", padx=20)
champ_date =DateEntry(frame_gauche, date_pattern="dd/mm/yyyy")
champ_date.pack(padx=20, pady=(3, 10))

CTkButton(frame_gauche, text="Ajouter la dépense", height=40,
          fg_color="#4e9af1", hover_color="#2c7de0", command=ajouter).pack(padx=20, pady=(10, 5), fill="x")

CTkLabel(frame_gauche, text="ID à supprimer", anchor="w").pack(fill="x", padx=20, pady=(15, 0))
champ_sup = CTkEntry(frame_gauche, width=300, height=38, placeholder_text="ex: 1")
champ_sup.pack(padx=20, pady=(3, 5))

CTkButton(frame_gauche, text="Supprimer", height=40,
          fg_color="#e05252", hover_color="#b83232", command=supprimer).pack(padx=20, pady=5, fill="x")

label_message = CTkLabel(frame_gauche, text="", font=("Arial", 12))
label_message.pack(pady=5)


CTkLabel(frame_droite, text="Liste des dépenses",
         font=("Arial", 14, "bold")).pack(pady=(15, 5))

textbox = CTkTextbox(frame_droite, height=180, font=("Courier", 12),
                     fg_color="#2b2b2b", text_color="white", state="disabled")
textbox.pack(padx=15, pady=(0, 10), fill="x")

frame_stats = CTkFrame(frame_droite, fg_color="#2b2b2b", corner_radius=10)
frame_stats.pack(padx=15, pady=(0, 10), fill="x")

CTkLabel(frame_stats, text="Analyses", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=4, pady=8)

label_total = CTkLabel(frame_stats, text="Total : 0 €", font=("Arial", 12), text_color="#4e9af1")
label_total.grid(row=1, column=0, padx=15, pady=5)

label_max = CTkLabel(frame_stats, text="Maximum : 0 €", font=("Arial", 12), text_color="#f1714e")
label_max.grid(row=1, column=1, padx=15, pady=5)

label_min = CTkLabel(frame_stats, text="Minimum : 0 €", font=("Arial", 12), text_color="#4ef1a0")
label_min.grid(row=1, column=2, padx=15, pady=5)

label_nb = CTkLabel(frame_stats, text="Nombre : 0", font=("Arial", 12), text_color="#f1d84e")
label_nb.grid(row=1, column=3, padx=15, pady=5)

CTkLabel(frame_droite, text="Graphique par catégorie",
         font=("Arial", 13, "bold")).pack(pady=(5, 3))

frame_graph = CTkFrame(frame_droite, fg_color="#2b2b2b", corner_radius=10)
frame_graph.pack(padx=15, pady=(0, 15), fill="both", expand=True)


afficher_depenses()
afficher_analyses()

try:
    window.mainloop()
except KeyboardInterrupt:
    pass