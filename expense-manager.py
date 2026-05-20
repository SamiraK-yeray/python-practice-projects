from customtkinter import *
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


set_appearance_mode("dark")
window = CTk()
window.title("Gestionnaire de dépenses")
window.geometry("800x700")
window.resizable(False, False)


def ajouter():
    m = champ_montant.get()
    c = champ_categorie.get()
    d = champ_date.get()
    con = sqlite3.connect("expense.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO Expenses (montant,categorie,date)VALUES (?,?,?)",(m,c,d))
    con.commit()
    con.close()
    champ_montant.delete(0, "end")
    champ_categorie.delete(0, "end")
    champ_date.delete(0, "end")

    afficher_depenses()

def afficher_depenses():
    con = sqlite3.connect("expense.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Expenses ")
    texte = cursor.fetchall()
    textbox.delete("1.0", END)
    for ligne in texte:
        textbox.insert(END, f"ID: {ligne[0]} | Montant: {ligne[1]} | Catégorie: {ligne[2]} | Date: {ligne[3]}\n")
    #textbox.delete("1.0", END)
    textbox.configure(state = "normal")
    con.close()

def supprimer_depenses():
    con = sqlite3.connect("expense.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM Expenses WHERE id = ?", (sup.get(),))
    con.commit()
    con.close()
    afficher_depenses()

def analyse_depenses():
    con = sqlite3.connect("expense.db")
    df = pd.read_sql_query("SELECT *FROM Expenses",con)
    print(df)
    print(f"Total : {df["montant"].sum()}")
    print(f"Dépenses maximale  : {df['montant'].max()}")
    print(f"Dépenses minimale : {df['montant'].min()}")
    con.close()

def categorie_depenses():
    con = sqlite3.connect("expense.db")
    df = pd.read_sql_query("SELECT * FROM Expenses", con)
    con.close()
    resultat = df.groupby("categorie")["montant"].sum().plot(kind="pie")
    plt.show()


conn = sqlite3.connect('expense.db')
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


montant = CTkLabel(window, text="Montant")
montant.grid(column=0, row=0, columnspan=2, sticky="nsew",padx = 10)
champ_montant = CTkEntry(window,width=130,height=40)
champ_montant.grid(row=0,column=2,columnspan = 3,padx=50,pady=10)

categorie = CTkLabel(window, text="Catégorie")
categorie.grid(column=0, row=2, columnspan=2,padx = 10)
champ_categorie = CTkEntry(window,width=130,height=40)
champ_categorie.grid(row=2,column=2,columnspan = 3,padx=50,pady=10)

label_date = CTkLabel(window, text="Date")
label_date.grid(column=0, row=4, columnspan=2, sticky="nsew",padx = 10)
champ_date = CTkEntry(window,width=130,height=40)
champ_date.grid(row=4,column=2,columnspan = 3,padx=50,pady=10)


bouton = CTkButton(window,text="Ajouter",command=ajouter)
bouton.grid(column=1,row=6,padx=50,pady=10)

textbox = CTkTextbox(window,width=300, height=150,
                          font=("Courier", 12),
                          fg_color="white", text_color="black")
textbox.grid(column=2,row=10,padx=50,pady=10)

bouton_sup= CTkButton(window,text="Supprimer",command=supprimer_depenses)
bouton_sup.grid(column=2,row=6,padx=50,pady=40)

sup = CTkEntry(window,width=130,height=40,placeholder_text="Entrez l'id de l'élément que vous voulez supprimer.")
sup.grid(column=0,row=7,columnspan=2,sticky="nsew",padx=50,pady=10)


analyse_depenses()
categorie_depenses()


afficher_depenses()
window.mainloop()