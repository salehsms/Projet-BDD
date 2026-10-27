import tkinter as tk
from tkinter import ttk, messagebox
import sys

sys.path.append("data_base")
from connexion import get_connection

BG     = "#0e1118"
SURF   = "#141926"
PANEL  = "#1a2035"
CARD   = "#1f2640"
CARD_H = "#28305a"
BORDER = "#2d3660"
GOLD   = "#d4a843"
GOLD_L = "#f0c96a"
GOLD_D = "#a07828"
TEAL   = "#3ecfcf"
TEAL_D = "#1a9999"
RED    = "#c0392b"
GREEN  = "#27ae60"
TEXT   = "#e8ecf8"
DIM    = "#4a5580"
MED    = "#7a86b0"
WHITE  = "#ffffff"


def apply_style():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=[0, 0, 0, 0])
    s.configure("TNotebook.Tab", font=("Georgia", 11), padding=[20, 10],
                background=SURF, foreground=DIM, borderwidth=0)
    s.map("TNotebook.Tab",
          background=[("selected", PANEL), ("active", CARD)],
          foreground=[("selected", GOLD), ("active", MED)])
    s.configure("TScrollbar", background=PANEL, troughcolor=BG, borderwidth=0, arrowsize=13)
    s.configure("TCombobox", fieldbackground=CARD, background=CARD,
                foreground=TEXT, selectbackground=CARD, selectforeground=GOLD,
                borderwidth=0, relief="flat")
    s.map("TCombobox", fieldbackground=[("readonly", CARD)], foreground=[("readonly", TEXT)])


def mk_btn(parent, text, cmd, bg=GOLD, fg=BG, small=False):
    return tk.Button(
        parent, text=text, command=cmd,
        font=("Georgia", 9 if small else 10, "bold"),
        bg=bg, fg=fg, activebackground=GOLD_L, activeforeground=BG,
        relief="flat", cursor="hand2",
        padx=10 if small else 20, pady=5 if small else 9, bd=0
    )


def mk_entry(parent, var, width=24):
    f = tk.Frame(parent, bg=CARD, highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=GOLD)
    tk.Entry(f, textvariable=var, width=width, font=("Helvetica", 10),
             bg=CARD, fg=TEXT, insertbackground=GOLD, relief="flat", bd=6).pack()
    return f


def mk_combo(parent, var, values, width=16):
    return ttk.Combobox(parent, textvariable=var, values=values,
                        state="readonly", width=width, font=("Helvetica", 10))


def scrollable(parent, bg=BG):
    c = tk.Canvas(parent, bg=bg, highlightthickness=0)
    vsb = ttk.Scrollbar(parent, orient="vertical", command=c.yview)
    c.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    c.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(c, bg=bg)
    wid = c.create_window((0, 0), window=inner, anchor="nw")
    c.bind("<Configure>", lambda e: c.itemconfig(wid, width=e.width))
    inner.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
    def on_scroll(e):
        try:
            c.yview_scroll(int(-1 * (e.delta / 120)), "units")
        except Exception:
            pass

    c.bind("<MouseWheel>", on_scroll)       
    inner.bind("<MouseWheel>", on_scroll)   

    return c, inner


def set_bg(w, color):
    try:
        w.configure(bg=color)
    except:
        pass
    for ch in w.winfo_children():
        set_bg(ch, color)


def all_children(w):
    kids = list(w.winfo_children())
    for k in list(kids):
        kids += all_children(k)
    return kids


def win_header(win, icon, titre, sous=""):
    h = tk.Frame(win, bg=PANEL)
    h.pack(fill="x")
    inn = tk.Frame(h, bg=PANEL)
    inn.pack(fill="x", padx=24, pady=16)
    tk.Label(inn, text=icon, font=("Helvetica", 22), bg=PANEL).pack(side="left", padx=(0, 14))
    b = tk.Frame(inn, bg=PANEL)
    b.pack(side="left")
    tk.Label(b, text=titre, font=("Georgia", 17, "bold"), bg=PANEL, fg=TEXT).pack(anchor="w")
    if sous:
        tk.Label(b, text=sous, font=("Helvetica", 9, "italic"), bg=PANEL, fg=MED).pack(anchor="w")
    tk.Frame(win, bg=GOLD, height=2).pack(fill="x")


def section_sep(parent, icon, titre, color=GOLD_L):
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", padx=20, pady=(18, 6))
    tk.Label(f, text=f"{icon}  {titre}", font=("Georgia", 11, "bold"),
             bg=BG, fg=color).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(12, 0), pady=5)


def badge(parent, text, bg_c, fg_c=WHITE, size=8):
    tk.Label(parent, text=text, font=("Helvetica", size, "bold"),
             bg=bg_c, fg=fg_c, padx=8, pady=3).pack(side="left", padx=2, pady=2)


def charger():
    d = {}
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_menu, nom_menu FROM Menu
            WHERE LOWER(TRIM(nom_menu)) != 'menu test'
            ORDER BY nom_menu
        """)
        d["menus"] = [{"id": r[0], "nom": r[1]} for r in cur.fetchall()]

        cur.execute("""
            SELECT a.id_menu, r.id_recette, r.nom_recette,
                   c.nom_catgorie, r.temps_preparation, r.temps_cuisson
            FROM appartient a
            JOIN recette r ON r.id_recette = a.id_recette
            LEFT JOIN categorie c ON c.id_categorie = r.id_categorie
            ORDER BY r.nom_recette
        """)
        d["menu_recettes"] = {}
        for id_m, id_r, nom, cat, prep, cuis in cur.fetchall():
            d["menu_recettes"].setdefault(id_m, []).append({
                "id": id_r, "nom": nom,
                "categorie": cat or "—",
                "prep": str(prep) if prep else "—",
                "cuisson": str(cuis) if cuis else "—",
            })

        cur.execute("""
            SELECT id_recette, numero_ordre, descrption_etape
            FROM Etape ORDER BY id_recette, numero_ordre
        """)
        d["etapes"] = {}
        for id_r, ordre, desc in cur.fetchall():
            d["etapes"].setdefault(id_r, []).append({"ordre": ordre, "desc": desc or ""})

        cur.execute("""
            SELECT n.id_recette, u.nom_ustensile, u.type_ustensile
            FROM necessite n
            JOIN ustensile u ON u.id_ustensile = n.id_ustensile
            ORDER BY u.nom_ustensile
        """)
        d["ustensiles"] = {}
        for id_r, nom_u, type_u in cur.fetchall():
            d["ustensiles"].setdefault(id_r, []).append({"nom": nom_u, "type": type_u or ""})

        cur.execute("""
            SELECT co.id_recette, i.id_ingredient, i.nom_ingredient, i.unite_mesure_defaut
            FROM compose co
            JOIN ingredient i ON i.id_ingredient = co.id_ingredient
            ORDER BY i.nom_ingredient
        """)
        d["ingredients"] = {}
        for id_r, id_i, nom_i, unite in cur.fetchall():
            d["ingredients"].setdefault(id_r, []).append({
                "id": id_i, "nom": nom_i, "unite": unite or ""
            })

        cur.execute("""
            SELECT ct.id_ingredient, a.nom_allergene
            FROM contient2 ct
            JOIN allergien a ON a.id_allergene = ct.id_allergene
        """)
        d["allergenes_ing"] = {}
        for id_i, nom_a in cur.fetchall():
            d["allergenes_ing"].setdefault(id_i, []).append(nom_a)

        cur.execute("""
            SELECT ip.id_ingredient, p.id_produit, p.nom_produit, p.marques, p.disponiblite
            FROM IngredientProduit ip
            JOIN produit p ON p.id_produit = ip.id_produit
            ORDER BY p.nom_produit
        """)
        d["produits_ing"] = {}
        for id_i, id_p, nom_p, marque, dispo in cur.fetchall():
            d["produits_ing"].setdefault(id_i, []).append({
                "id": id_p, "nom": nom_p, "marque": marque or "", "dispo": dispo or ""
            })

        cur.execute("""
            SELECT fo.id_produit, f.nom_entreprise, f.telephone_pro, f.site_web, fo.prix
            FROM fournit fo
            JOIN fournisseur f ON f.id_fournisseur = fo.id_fournisseur
            ORDER BY f.nom_entreprise
        """)
        d["fournisseurs"] = {}
        for id_p, ent, tel, web, prix in cur.fetchall():
            d["fournisseurs"].setdefault(id_p, []).append({
                "entreprise": ent, "tel": tel or "", "web": web or "",
                "prix": str(prix) if prix else ""
            })

        cur.execute("SELECT DISTINCT nom_catgorie FROM categorie ORDER BY nom_catgorie")
        d["_cats"] = ["Toutes"] + [r[0] for r in cur.fetchall() if r[0]]

        cur.execute("SELECT DISTINCT nom_allergene FROM allergien ORDER BY nom_allergene")
        d["_alls"] = ["Tous"] + [r[0] for r in cur.fetchall() if r[0]]

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erreur de connexion", str(e))
    return d


def allergenes_recette(id_r, d):
    result = set()
    for ing in d.get("ingredients", {}).get(id_r, []):
        for a in d.get("allergenes_ing", {}).get(ing["id"], []):
            result.add(a)
    return result


def fiche_fournisseurs(parent, produit, d):
    fours = d.get("fournisseurs", {}).get(produit["id"], [])

    win = tk.Toplevel(parent)
    win.title(f"Fournisseurs · {produit['nom']}")
    win.geometry("680x500")
    win.configure(bg=BG)
    win.grab_set()
    win.resizable(True, True)

    win_header(win, "🏭", f"Fournisseurs de « {produit['nom']} »",
               f"Marque : {produit.get('marque','—')}   ·   Disponibilité : {produit.get('dispo','—')}")

    wrap = tk.Frame(win, bg=BG)
    wrap.pack(fill="both", expand=True)
    _, body = scrollable(wrap)
    tk.Frame(body, bg=BG, height=10).pack()

    if not fours:
        tk.Label(body, text="\n  Aucun fournisseur enregistré pour ce produit.",
                 font=("Helvetica", 11, "italic"), bg=BG, fg=DIM).pack(pady=50)
    else:
        for f in fours:
            card = tk.Frame(body, bg=CARD, pady=14)
            card.pack(fill="x", padx=22, pady=6)
            tk.Frame(card, bg=TEAL, width=5).pack(side="left", fill="y")
            ic = tk.Frame(card, bg=TEAL_D, width=52, height=52)
            ic.pack(side="left", padx=14, pady=8)
            ic.pack_propagate(False)
            tk.Label(ic, text="🏭", font=("Helvetica", 18), bg=TEAL_D).place(relx=.5, rely=.5, anchor="center")
            info = tk.Frame(card, bg=CARD, pady=8)
            info.pack(side="left", fill="both", expand=True)
            tk.Label(info, text=f.get("entreprise", "—"),
                     font=("Georgia", 14, "bold"), bg=CARD, fg=TEXT).pack(anchor="w")
            if f.get("prix"):
                tk.Label(info, text=f"💶  Prix unitaire : {f['prix']} €",
                         font=("Helvetica", 10, "bold"), bg=CARD, fg=GOLD).pack(anchor="w", pady=(4, 0))
            row2 = tk.Frame(info, bg=CARD)
            row2.pack(fill="x", pady=(4, 0))
            if f.get("tel"):
                tk.Label(row2, text=f"📞  {f['tel']}",
                         font=("Helvetica", 9), bg=CARD, fg=MED).pack(side="left", padx=(0, 20))
            if f.get("web"):
                tk.Label(row2, text=f"🌐  {f['web']}",
                         font=("Helvetica", 9), bg=CARD, fg=TEAL).pack(side="left")

    tk.Frame(body, bg=BG, height=16).pack()
    pied = tk.Frame(win, bg=SURF, pady=10)
    pied.pack(fill="x")
    mk_btn(pied, "✕  Fermer", win.destroy, bg=PANEL, fg=MED).pack(side="right", padx=20)


def fiche_recette(parent, recette, d):
    id_r   = recette["id"]
    etapes = d.get("etapes", {}).get(id_r, [])
    ustens = d.get("ustensiles", {}).get(id_r, [])
    ings   = d.get("ingredients", {}).get(id_r, [])

    produits_recette = []
    vus = set()
    for ing in ings:
        for p in d.get("produits_ing", {}).get(ing["id"], []):
            if p["id"] not in vus:
                vus.add(p["id"])
                produits_recette.append(p)
    produits_recette.sort(key=lambda x: x["nom"])

    win = tk.Toplevel(parent)
    win.title(f"Recette · {recette['nom']}")
    win.geometry("980x750")
    win.configure(bg=BG)
    win.grab_set()
    win.resizable(True, True)

    win_header(win, "🍳", recette["nom"],
               f"Catégorie : {recette['categorie']}   ·   "
               f"Préparation : {recette['prep']} min   ·   "
               f"Cuisson : {recette['cuisson']} min")

    band = tk.Frame(win, bg=PANEL)
    band.pack(fill="x")
    for icon, lbl, val in [
        ("📂", "Catégorie",   recette["categorie"]),
        ("⏱",  "Préparation", f"{recette['prep']} min"),
        ("🔥", "Cuisson",     f"{recette['cuisson']} min"),
        ("🧂", "Ingrédients", str(len(ings))),
        ("📋", "Étapes",      str(len(etapes))),
        ("🔪", "Ustensiles",  str(len(ustens))),
    ]:
        blk = tk.Frame(band, bg=PANEL, padx=18, pady=10)
        blk.pack(side="left")
        tk.Label(blk, text=f"{icon}  {lbl}", font=("Helvetica", 8), bg=PANEL, fg=DIM).pack(anchor="w")
        tk.Label(blk, text=str(val), font=("Helvetica", 12, "bold"), bg=PANEL, fg=TEXT).pack(anchor="w")
        tk.Frame(band, bg=BORDER, width=1).pack(side="left", fill="y", pady=6)
    tk.Frame(win, bg=GOLD, height=2).pack(fill="x")

    wrap = tk.Frame(win, bg=BG)
    wrap.pack(fill="both", expand=True)
    _, body = scrollable(wrap)

    section_sep(body, "📋", "Étapes de préparation")
    if etapes:
        for et in etapes:
            row = tk.Frame(body, bg=CARD, pady=11, padx=14)
            row.pack(fill="x", padx=20, pady=3)
            bn = tk.Frame(row, bg=GOLD, width=38, height=38)
            bn.pack(side="left", padx=(0, 14))
            bn.pack_propagate(False)
            tk.Label(bn, text=str(et["ordre"]), font=("Georgia", 13, "bold"),
                     bg=GOLD, fg=BG).place(relx=.5, rely=.5, anchor="center")
            tk.Label(row, text=et["desc"], font=("Helvetica", 10),
                     bg=CARD, fg=TEXT, wraplength=760, justify="left", anchor="w"
                     ).pack(side="left", fill="x", expand=True)
    else:
        tk.Label(body, text="  Aucune étape enregistrée.",
                 font=("Helvetica", 10, "italic"), bg=BG, fg=DIM).pack(anchor="w", padx=24, pady=6)

    section_sep(body, "🔪", "Ustensiles nécessaires", TEAL)
    if ustens:
        uf = tk.Frame(body, bg=BG)
        uf.pack(fill="x", padx=20, pady=4)
        for u in ustens:
            row = tk.Frame(uf, bg=CARD, padx=14, pady=8)
            row.pack(fill="x", pady=2)
            tk.Label(row, text="◈", font=("Georgia", 12), bg=CARD, fg=TEAL).pack(side="left", padx=(0, 10))
            tk.Label(row, text=u["nom"], font=("Helvetica", 10, "bold"), bg=CARD, fg=TEXT).pack(side="left")
            if u["type"]:
                tk.Label(row, text=f"  ·  {u['type']}", font=("Helvetica", 9),
                         bg=CARD, fg=DIM).pack(side="left")
    else:
        tk.Label(body, text="  Aucun ustensile enregistré.",
                 font=("Helvetica", 10), bg=BG, fg=DIM).pack(anchor="w", padx=24, pady=4)

    section_sep(body, "🧂", "Ingrédients")
    if ings:
        grid = tk.Frame(body, bg=BG)
        grid.pack(fill="x", padx=20, pady=4)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        for idx, ing in enumerate(ings):
            cell = tk.Frame(grid, bg=CARD, pady=10, padx=14)
            cell.grid(row=idx // 2, column=idx % 2, padx=4, pady=3, sticky="ew")
            top = tk.Frame(cell, bg=CARD)
            top.pack(fill="x")
            tk.Label(top, text="·", font=("Georgia", 18), bg=CARD, fg=GOLD).pack(side="left", padx=(0, 8))
            tk.Label(top, text=ing["nom"], font=("Helvetica", 10, "bold"),
                     bg=CARD, fg=TEXT).pack(side="left")
            if ing.get("unite"):
                tk.Label(top, text=f"  ({ing['unite']})", font=("Helvetica", 9),
                         bg=CARD, fg=MED).pack(side="left")
            alls_i = d.get("allergenes_ing", {}).get(ing["id"], [])
            if alls_i:
                al_row = tk.Frame(cell, bg=CARD)
                al_row.pack(fill="x", pady=(5, 0))
                for a in sorted(alls_i):
                    tk.Label(al_row, text=f"⚠ {a}", font=("Helvetica", 7, "bold"),
                             bg=RED, fg=WHITE, padx=5, pady=2).pack(side="left", padx=2)
    else:
        tk.Label(body, text="  Aucun ingrédient renseigné.",
                 font=("Helvetica", 10), bg=BG, fg=DIM).pack(anchor="w", padx=24, pady=4)

    section_sep(body, "📦", "Produits associés  —  cliquez pour voir le fournisseur", GOLD_L)
    if produits_recette:
        pg = tk.Frame(body, bg=BG)
        pg.pack(fill="x", padx=20, pady=4)
        pg.columnconfigure(0, weight=1)
        pg.columnconfigure(1, weight=1)
        for idx, p in enumerate(produits_recette):
            pcard = tk.Frame(pg, bg=CARD, pady=10, padx=14, cursor="hand2")
            pcard.grid(row=idx // 2, column=idx % 2, padx=4, pady=3, sticky="ew")
            left = tk.Frame(pcard, bg=CARD)
            left.pack(side="left", fill="both", expand=True)
            tk.Label(left, text=f"📦  {p['nom']}", font=("Helvetica", 10, "bold"),
                     bg=CARD, fg=TEXT).pack(anchor="w")
            det = tk.Frame(left, bg=CARD)
            det.pack(fill="x", pady=(3, 0))
            if p["marque"]:
                tk.Label(det, text=p["marque"], font=("Helvetica", 8),
                         bg=CARD, fg=MED).pack(side="left", padx=(0, 8))
            if p["dispo"]:
                dc = GREEN if any(k in p["dispo"].lower() for k in ["oui", "dispo", "yes"]) else RED
                tk.Label(det, text=p["dispo"], font=("Helvetica", 8),
                         bg=dc, fg=WHITE, padx=5, pady=1).pack(side="left")
            tk.Label(pcard, text="→ fournisseur", font=("Helvetica", 8, "italic"),
                     bg=CARD, fg=GOLD).pack(side="right", padx=4)

            def _enter(e, c=pcard): set_bg(c, CARD_H)
            def _leave(e, c=pcard): set_bg(c, CARD)
            def _click(e, prod=p): fiche_fournisseurs(win, prod, d)

            pcard.bind("<Enter>", _enter)
            pcard.bind("<Leave>", _leave)
            pcard.bind("<Button-1>", _click)
            for w in all_children(pcard):
                try:
                    w.bind("<Button-1>", _click)
                except:
                    pass
    else:
        tk.Label(body, text="  Aucun produit associé à cette recette.",
                 font=("Helvetica", 10), bg=BG, fg=DIM).pack(anchor="w", padx=24, pady=4)

    tk.Frame(body, bg=BG, height=20).pack()
    pied = tk.Frame(win, bg=SURF, pady=10)
    pied.pack(fill="x")
    mk_btn(pied, "✕  Fermer", win.destroy, bg=PANEL, fg=MED).pack(side="right", padx=20)


def liste_recettes_menu(parent, menu, d):
    id_m = menu["id"]
    recs = d.get("menu_recettes", {}).get(id_m, [])

    win = tk.Toplevel(parent)
    win.title(f"Menu — {menu['nom']}")
    win.geometry("1020x680")
    win.configure(bg=BG)
    win.grab_set()
    win.resizable(True, True)

    win_header(win, "📋", menu["nom"],
               f"{len(recs)} recette{'s' if len(recs) != 1 else ''} dans ce menu")

    fb = tk.Frame(win, bg=SURF, pady=11)
    fb.pack(fill="x")

    def lbl(t):
        tk.Label(fb, text=t, font=("Helvetica", 9), bg=SURF, fg=DIM).pack(side="left", padx=(14, 4))

    lbl("🔍  Nom / ingrédient")
    rech_var = tk.StringVar()
    mk_entry(fb, rech_var, 22).pack(side="left", padx=(0, 10))

    lbl("Catégorie")
    cat_var = tk.StringVar(value="Toutes")
    mk_combo(fb, cat_var, d.get("_cats", ["Toutes"]), 15).pack(side="left", padx=(0, 8))

    lbl("Allergène")
    all_var = tk.StringVar(value="Tous")
    mk_combo(fb, all_var, d.get("_alls", ["Tous"]), 15).pack(side="left", padx=(0, 12))

    mk_btn(fb, "✕ Reset",
           lambda: [rech_var.set(""), cat_var.set("Toutes"), all_var.set("Tous")],
           bg=RED, fg=WHITE, small=True).pack(side="left")

    tk.Frame(fb, bg=GOLD, height=2).pack(fill="x", side="bottom")

    zone = tk.Frame(win, bg=BG)
    zone.pack(fill="both", expand=True)
    _, inner = scrollable(zone)

    def rafraichir(*_):
        for w in inner.winfo_children():
            w.destroy()

        q   = rech_var.get().strip().lower()
        cat = cat_var.get()
        al  = all_var.get()
        filtered = []

        for r in recs:
            id_r = r["id"]
            if q:
                nom_ok = q in r["nom"].lower()
                ing_ok = any(q in ing["nom"].lower()
                             for ing in d.get("ingredients", {}).get(id_r, []))
                if not (nom_ok or ing_ok):
                    continue
            if cat != "Toutes":
                if (r.get("categorie") or "").strip().lower() != cat.strip().lower():
                    continue
            if al != "Tous":
                if al not in allergenes_recette(id_r, d):
                    continue
            filtered.append(r)

        if not filtered:
            tk.Label(inner, text="\n\n  Aucune recette ne correspond à votre recherche.",
                     font=("Helvetica", 12, "italic"), bg=BG, fg=DIM).pack(pady=60)
            return

        for rec in filtered:
            id_r   = rec["id"]
            alls_r = allergenes_recette(id_r, d)
            nb_et  = len(d.get("etapes", {}).get(id_r, []))
            nb_in  = len(d.get("ingredients", {}).get(id_r, []))

            card = tk.Frame(inner, bg=CARD)
            card.pack(fill="x", padx=22, pady=6)
            tk.Frame(card, bg=GOLD, width=6).pack(side="left", fill="y")

            body = tk.Frame(card, bg=CARD, padx=18, pady=14)
            body.pack(side="left", fill="both", expand=True)

            top = tk.Frame(body, bg=CARD)
            top.pack(fill="x")
            tk.Label(top, text=rec["nom"], font=("Georgia", 14, "bold"),
                     bg=CARD, fg=TEXT).pack(side="left")
            tk.Label(top, text=f"  {rec['categorie']}", font=("Helvetica", 9),
                     bg=CARD, fg=TEAL).pack(side="left", padx=8)

            meta = tk.Frame(body, bg=CARD)
            meta.pack(fill="x", pady=(5, 0))
            for info in [f"⏱ {rec['prep']} min prép.",
                         f"🔥 {rec['cuisson']} min cuisson",
                         f"🧂 {nb_in} ingrédient{'s' if nb_in != 1 else ''}",
                         f"📋 {nb_et} étape{'s' if nb_et != 1 else ''}"]:
                tk.Label(meta, text=info, font=("Helvetica", 9),
                         bg=CARD, fg=MED).pack(side="left", padx=(0, 16))

            if alls_r:
                al_row = tk.Frame(body, bg=CARD)
                al_row.pack(fill="x", pady=(6, 0))
                tk.Label(al_row, text="Allergènes :", font=("Helvetica", 8),
                         bg=CARD, fg=DIM).pack(side="left", padx=(0, 6))
                for a in sorted(alls_r)[:5]:
                    badge(al_row, a, bg_c=RED, size=8)
                if len(alls_r) > 5:
                    badge(al_row, f"+{len(alls_r)-5}", bg_c="#7f1c1c", size=8)
            else:
                tk.Label(body, text="✔  Sans allergènes", font=("Helvetica", 8, "bold"),
                         bg=GREEN, fg=WHITE, padx=8, pady=2).pack(anchor="w", pady=(5, 0))

            bz = tk.Frame(card, bg=CARD, padx=18)
            bz.pack(side="right", fill="y")
            mk_btn(bz, "Voir  →", lambda r=rec: fiche_recette(win, r, d),
                   bg=TEAL, fg=BG).pack(expand=True)

    rech_var.trace_add("write", rafraichir)
    cat_var.trace_add("write", rafraichir)
    all_var.trace_add("write", rafraichir)
    rafraichir()

    pied = tk.Frame(win, bg=SURF, pady=9)
    pied.pack(fill="x")
    tk.Label(pied, text="Cliquez sur « Voir » pour accéder à la fiche complète d'une recette.",
             font=("Helvetica", 9, "italic"), bg=SURF, fg=DIM).pack(side="left", padx=18)
    mk_btn(pied, "✕  Fermer", win.destroy, bg=PANEL, fg=MED).pack(side="right", padx=16)


def onglet_menus(notebook, d):
    frame = tk.Frame(notebook, bg=BG)
    notebook.add(frame, text="  🍽  Menus  ")

    sub = tk.Frame(frame, bg=SURF, pady=10)
    sub.pack(fill="x")
    tk.Label(sub, text="  Sélectionnez un menu pour explorer ses recettes",
             font=("Helvetica", 10, "italic"), bg=SURF, fg=MED).pack(side="left", padx=14)
    tk.Frame(frame, bg=GOLD, height=2).pack(fill="x")

    wrap = tk.Frame(frame, bg=BG)
    wrap.pack(fill="both", expand=True)
    _, inner = scrollable(wrap)

    menus = d.get("menus", [])
    if not menus:
        tk.Label(inner, text="\n\n  Aucun menu disponible.",
                 font=("Helvetica", 12, "italic"), bg=BG, fg=DIM).pack(pady=60)
        return

    tk.Frame(inner, bg=BG, height=12).pack()

    for i, menu in enumerate(menus):
        id_m   = menu["id"]
        nb_rec = len(d.get("menu_recettes", {}).get(id_m, []))

        card = tk.Frame(inner, bg=CARD)
        card.pack(fill="x", padx=28, pady=8)
        tk.Frame(card, bg=GOLD, width=7).pack(side="left", fill="y")

        ic = tk.Frame(card, bg=GOLD_D, width=68, height=68)
        ic.pack(side="left", padx=18, pady=16)
        ic.pack_propagate(False)
        tk.Label(ic, text="🍽", font=("Helvetica", 26),
                 bg=GOLD_D).place(relx=.5, rely=.5, anchor="center")

        txt = tk.Frame(card, bg=CARD, pady=16)
        txt.pack(side="left", fill="both", expand=True)
        tk.Label(txt, text=menu["nom"], font=("Georgia", 17, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Label(txt,
                 text=f"{nb_rec} recette{'s' if nb_rec != 1 else ''} disponible{'s' if nb_rec != 1 else ''}",
                 font=("Helvetica", 10), bg=CARD, fg=MED).pack(anchor="w", pady=(4, 0))

        bz = tk.Frame(card, bg=CARD, padx=22)
        bz.pack(side="right", fill="y")
        mk_btn(bz, "Voir les recettes  ›",
               lambda m=menu: liste_recettes_menu(notebook.winfo_toplevel(), m, d),
               bg=GOLD, fg=BG).pack(expand=True)

        if i < len(menus) - 1:
            tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=28, pady=2)

    tk.Frame(inner, bg=BG, height=24).pack()


root = tk.Tk()
root.title("Cuisine & Menus — Gestion Culinaire")
root.geometry("1300x760")
root.configure(bg=BG)
root.minsize(900, 560)

apply_style()

hdr = tk.Frame(root, bg=SURF)
hdr.pack(fill="x")
hdr_in = tk.Frame(hdr, bg=SURF)
hdr_in.pack(fill="x", padx=28, pady=18)

logo = tk.Frame(hdr_in, bg=SURF)
logo.pack(side="left")
tk.Label(logo, text="✦  CUISINE & MENUS", font=("Georgia", 21, "bold"),
         bg=SURF, fg=GOLD).pack(anchor="w")
tk.Label(logo, text="Plateforme de gestion culinaire professionnelle",
         font=("Helvetica", 9), bg=SURF, fg=DIM).pack(anchor="w")

tk.Frame(root, bg=GOLD, height=3).pack(fill="x")

nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True)

d = charger()

stat_frame = tk.Frame(hdr_in, bg=SURF)
stat_frame.pack(side="right")
b = tk.Frame(stat_frame, bg=CARD, padx=20, pady=10)
b.pack(side="left", padx=5)
tk.Label(b, text=str(len(d.get("menus", []))), font=("Georgia", 20, "bold"),
         bg=CARD, fg=GOLD).pack()
tk.Label(b, text="Menus", font=("Helvetica", 9), bg=CARD, fg=DIM).pack()

onglet_menus(nb, d)

root.mainloop()