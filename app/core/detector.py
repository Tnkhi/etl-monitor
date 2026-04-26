import pandas as pd

SECTOR_KEYWORDS = {
    "ventes": [
        "montant", "vente", "client", "commande", "produit", "prix",
        "quantite", "quantité", "revenue", "chiffre", "facture",
        "order", "sale", "customer", "amount", "product", "price"
    ],
    "rh": [
        "employe", "employé", "salaire", "departement", "département",
        "poste", "conge", "congé", "recrutement", "contrat", "anciennete",
        "employee", "salary", "department", "position", "contract"
    ],
    "finance": [
        "budget", "depense", "dépense", "comptabilite", "comptabilité",
        "tresorerie", "trésorerie", "bilan", "charge", "revenu",
        "expense", "accounting", "balance", "income", "cost", "profit"
    ],
    "logistique": [
        "livraison", "stock", "entrepot", "entrepôt", "transport",
        "expedition", "expédition", "fournisseur", "inventaire",
        "delivery", "warehouse", "supplier", "inventory", "shipment", "pneu"
    ],
    "marketing": [
        "campagne", "lead", "conversion", "impression", "clic",
        "audience", "canal", "trafic", "engagement", "publicite",
        "campaign", "click", "traffic", "channel", "advertisement"
    ],
}

def detect_sector(df: pd.DataFrame) -> str:
    """Détecte le secteur d'activité en analysant les noms de colonnes."""
    columns_lower = " ".join(df.columns.str.lower().tolist())

    scores = {}
    for sector, keywords in SECTOR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in columns_lower)
        scores[sector] = score

    best_sector = max(scores, key=scores.get)

    if scores[best_sector] == 0:
        return "generique"

    return best_sector