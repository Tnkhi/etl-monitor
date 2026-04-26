import pandas as pd
from app.core.detector import detect_sector
from app.core.kpi_engine import compute_kpis

def load_file(path: str) -> pd.DataFrame:
    if path.endswith(".csv"):
        return pd.read_csv(path, encoding="utf-8-sig")
    elif path.endswith((".xls", ".xlsx")):
        return pd.read_excel(path)
    elif path.endswith(".json"):
        return pd.read_json(path)
    raise ValueError(f"Format non supporté : {path}")

def generate_charts(df: pd.DataFrame, sector: str, kpis: dict) -> dict:
    charts = {}

    id_keywords = ["id", "code", "numero", "numéro", "index", "ref"]
    numeric_cols = [c for c in df.select_dtypes(include=["number"]).columns if not any(kw in c.lower() for kw in id_keywords)]
    text_cols = [c for c in df.select_dtypes(include=["object"]).columns if not any(kw in c.lower() for kw in id_keywords)]

    # Colonnes prioritaires par secteur
    sector_config = {
        "logistique": {
            "bar_col": ["stock", "quantite", "quantité", "quantity"],
            "group_col": ["produit", "product", "article", "item", "nom"],
            "pie_col": ["statut", "status", "categorie", "catégorie"],
            "bar2_col": ["prix_unitaire", "prix", "price", "valeur"],
        },
        "ventes": {
            "bar_col": ["montant", "amount", "revenue", "total", "prix"],
            "group_col": ["produit", "product", "client", "customer"],
            "pie_col": ["categorie", "statut", "region", "canal"],
            "bar2_col": ["quantite", "quantité", "quantity"],
        },
        "rh": {
            "bar_col": ["salaire", "salary", "remuneration"],
            "group_col": ["departement", "département", "department", "poste"],
            "pie_col": ["poste", "contrat", "statut", "departement"],
            "bar2_col": ["anciennete", "age"],
        },
        "finance": {
            "bar_col": ["montant", "depense", "dépense", "budget", "amount"],
            "group_col": ["categorie", "catégorie", "category", "type"],
            "pie_col": ["type", "statut", "categorie"],
            "bar2_col": ["budget", "montant"],
        },
        "marketing": {
            "bar_col": ["impression", "clic", "click", "conversion"],
            "group_col": ["campagne", "campaign", "canal", "channel"],
            "pie_col": ["canal", "channel", "source", "statut"],
            "bar2_col": ["conversion", "lead"],
        },
    }

    config = sector_config.get(sector, {
        "bar_col": [], "group_col": [], "pie_col": [], "bar2_col": []
    })

    def find_col(candidates, fallback_list):
        for kw in candidates:
            for c in df.columns:
                if kw in c.lower():
                    return c
        return fallback_list[0] if fallback_list else None

    bar_col = find_col(config["bar_col"], numeric_cols)
    group_col = find_col(config["group_col"], text_cols)
    pie_col = find_col(config["pie_col"], text_cols)
    bar2_col = find_col(config["bar2_col"], [c for c in numeric_cols if c != bar_col])

    # Graphique 1 : Bar — valeur principale par produit/groupe
    if bar_col and group_col:
        grouped = df.groupby(group_col)[bar_col].sum().sort_values(ascending=False).head(10)
        charts["bar_principal"] = {
            "type": "bar",
            "title": f"{bar_col.replace('_',' ').title()} par {group_col.replace('_',' ').title()}",
            "labels": grouped.index.tolist(),
            "values": [round(float(v), 2) for v in grouped.values.tolist()],
        }

    # Graphique 2 : Donut — répartition catégorielle
    if pie_col and pie_col != group_col:
        if bar_col:
            grouped_pie = df.groupby(pie_col)[bar_col].sum().sort_values(ascending=False).head(8)
            charts["pie_repartition"] = {
                "type": "pie",
                "title": f"{bar_col.replace('_',' ').title()} par {pie_col.replace('_',' ').title()}",
                "labels": grouped_pie.index.tolist(),
                "values": [round(float(v), 2) for v in grouped_pie.values.tolist()],
            }
        else:
            counts = df[pie_col].value_counts().head(8)
            charts["pie_repartition"] = {
                "type": "pie",
                "title": f"Répartition — {pie_col.replace('_',' ').title()}",
                "labels": counts.index.tolist(),
                "values": [float(v) for v in counts.values.tolist()],
            }

    # Graphique 3 : Bar horizontal — deuxième métrique
    if bar2_col and group_col:
        grouped2 = df.groupby(group_col)[bar2_col].mean().sort_values(ascending=False).head(8)
        charts["bar_secondaire"] = {
            "type": "bar",
            "title": f"{bar2_col.replace('_',' ').title()} moyen par {group_col.replace('_',' ').title()}",
            "labels": grouped2.index.tolist(),
            "values": [round(float(v), 2) for v in grouped2.values.tolist()],
        }

    # Graphique 4 : Ligne — évolution temporelle
    date_col = None
    for col in df.columns:
        if any(kw in col.lower() for kw in ["date", "time", "mois", "annee", "année"]):
            try:
                parsed = pd.to_datetime(df[col], errors="coerce")
                if parsed.notna().sum() > 0:
                    df[col] = parsed
                    date_col = col
                    break
            except Exception:
                pass

    if date_col and bar_col:
        df_sorted = df[[date_col, bar_col]].dropna().sort_values(date_col)
        charts["line_evolution"] = {
            "type": "line",
            "title": f"Évolution — {bar_col.replace('_',' ').title()}",
            "labels": df_sorted[date_col].dt.strftime("%d/%m/%Y").tolist(),
            "values": [round(float(v), 2) for v in df_sorted[bar_col].tolist()],
        }

    return charts

def run_pipeline(path: str) -> dict:
    df = load_file(path)

    # Normaliser les colonnes
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[\s\-]+", "_", regex=True)
        .str.replace(r"[^\w]", "", regex=True)
    )

    sector = detect_sector(df)
    kpis = compute_kpis(df, sector)
    charts = generate_charts(df, sector, kpis)

    return {
        "sector": sector,
        "rows_count": len(df),
        "columns_count": len(df.columns),
        "kpis": kpis,
        "charts": charts,
    }