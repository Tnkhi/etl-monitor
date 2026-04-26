import pandas as pd
from typing import Any

def compute_kpis(df: pd.DataFrame, sector: str) -> dict[str, Any]:
    """Calcule les KPIs selon le secteur détecté."""
    if sector == "ventes":
        return _kpis_ventes(df)
    elif sector == "rh":
        return _kpis_rh(df)
    elif sector == "finance":
        return _kpis_finance(df)
    elif sector == "logistique":
        return _kpis_logistique(df)
    elif sector == "marketing":
        return _kpis_marketing(df)
    else:
        return _kpis_generique(df)

def _find_col(df: pd.DataFrame, keywords: list[str]):
    """Trouve la première colonne correspondant à un mot-clé."""
    for col in df.columns:
        for kw in keywords:
            if kw in col.lower():
                return col
    return None

def _kpis_ventes(df: pd.DataFrame) -> dict:
    kpis = {}
    montant_col = _find_col(df, ["montant", "amount", "revenue", "prix", "price", "total"])
    client_col = _find_col(df, ["client", "customer", "nom", "name"])
    produit_col = _find_col(df, ["produit", "product", "article", "item"])

    if montant_col:
        kpis["ca_total"] = round(float(df[montant_col].sum()), 2)
        kpis["panier_moyen"] = round(float(df[montant_col].mean()), 2)
        kpis["vente_max"] = round(float(df[montant_col].max()), 2)
        kpis["vente_min"] = round(float(df[montant_col].min()), 2)

    kpis["nb_commandes"] = len(df)

    if client_col:
        kpis["nb_clients_uniques"] = int(df[client_col].nunique())
        kpis["top_clients"] = (
            df.groupby(client_col)[montant_col].sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
            .to_dict(orient="records")
        ) if montant_col else []

    if produit_col and montant_col:
        kpis["top_produits"] = (
            df.groupby(produit_col)[montant_col].sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
            .to_dict(orient="records")
        )

    return kpis

def _kpis_rh(df: pd.DataFrame) -> dict:
    kpis = {}
    salaire_col = _find_col(df, ["salaire", "salary", "remuneration", "paie"])
    dept_col = _find_col(df, ["departement", "département", "department", "service"])
    poste_col = _find_col(df, ["poste", "position", "role", "titre", "title"])

    kpis["nb_employes"] = len(df)

    if salaire_col:
        kpis["salaire_moyen"] = round(float(df[salaire_col].mean()), 2)
        kpis["salaire_max"] = round(float(df[salaire_col].max()), 2)
        kpis["salaire_min"] = round(float(df[salaire_col].min()), 2)
        kpis["masse_salariale"] = round(float(df[salaire_col].sum()), 2)

    if dept_col:
        kpis["nb_departements"] = int(df[dept_col].nunique())
        kpis["repartition_departements"] = (
            df[dept_col].value_counts()
            .head(5)
            .reset_index()
            .to_dict(orient="records")
        )

    if poste_col:
        kpis["top_postes"] = (
            df[poste_col].value_counts()
            .head(5)
            .reset_index()
            .to_dict(orient="records")
        )

    return kpis

def _kpis_finance(df: pd.DataFrame) -> dict:
    kpis = {}
    montant_col = _find_col(df, ["montant", "amount", "depense", "dépense", "budget", "cost", "expense"])
    categorie_col = _find_col(df, ["categorie", "catégorie", "category", "type", "poste"])

    kpis["nb_transactions"] = len(df)

    if montant_col:
        kpis["total_depenses"] = round(float(df[montant_col].sum()), 2)
        kpis["depense_moyenne"] = round(float(df[montant_col].mean()), 2)
        kpis["depense_max"] = round(float(df[montant_col].max()), 2)

    if categorie_col and montant_col:
        kpis["depenses_par_categorie"] = (
            df.groupby(categorie_col)[montant_col].sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
            .to_dict(orient="records")
        )

    return kpis

def _kpis_logistique(df: pd.DataFrame) -> dict:
    kpis = {}
    stock_col = _find_col(df, ["stock", "quantite", "quantité", "quantity", "inventaire"])
    fournisseur_col = _find_col(df, ["fournisseur", "supplier", "vendor"])
    statut_col = _find_col(df, ["statut", "status", "etat", "état"])

    kpis["nb_articles"] = len(df)

    if stock_col:
        kpis["stock_total"] = round(float(df[stock_col].sum()), 2)
        kpis["stock_moyen"] = round(float(df[stock_col].mean()), 2)
        kpis["stock_min"] = round(float(df[stock_col].min()), 2)

    if fournisseur_col:
        kpis["nb_fournisseurs"] = int(df[fournisseur_col].nunique())

    if statut_col:
        kpis["repartition_statuts"] = (
            df[statut_col].value_counts()
            .reset_index()
            .to_dict(orient="records")
        )

    return kpis

def _kpis_marketing(df: pd.DataFrame) -> dict:
    kpis = {}
    impression_col = _find_col(df, ["impression", "view", "vue", "affichage"])
    clic_col = _find_col(df, ["clic", "click", "clique"])
    conversion_col = _find_col(df, ["conversion", "lead", "signup"])
    canal_col = _find_col(df, ["canal", "channel", "source", "media"])

    kpis["nb_campagnes"] = len(df)

    if impression_col:
        kpis["total_impressions"] = int(df[impression_col].sum())

    if clic_col:
        kpis["total_clics"] = int(df[clic_col].sum())

    if impression_col and clic_col:
        total_imp = df[impression_col].sum()
        total_clics = df[clic_col].sum()
        kpis["taux_clic"] = round(float(total_clics / total_imp * 100), 2) if total_imp > 0 else 0

    if canal_col:
        kpis["performance_canaux"] = (
            df[canal_col].value_counts()
            .head(5)
            .reset_index()
            .to_dict(orient="records")
        )

    return kpis

def _kpis_generique(df: pd.DataFrame) -> dict:
    kpis = {}
    kpis["nb_lignes"] = len(df)
    kpis["nb_colonnes"] = len(df.columns)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    kpis["colonnes_numeriques"] = numeric_cols

    stats = {}
    for col in numeric_cols[:5]:
        stats[col] = {
            "total": round(float(df[col].sum()), 2),
            "moyenne": round(float(df[col].mean()), 2),
            "max": round(float(df[col].max()), 2),
            "min": round(float(df[col].min()), 2),
        }
    kpis["statistiques"] = stats

    return kpis