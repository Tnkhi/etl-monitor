# 🔍 ETL Monitor

> Plateforme de surveillance et de supervision des pipelines ETL (Extract, Transform, Load) en temps réel.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellow.svg)

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Reference](#-api-reference)
- [Dashboard](#-dashboard)
- [Alertes & Notifications](#-alertes--notifications)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🚀 Présentation

**ETL Monitor** est un outil de supervision centralisé conçu pour surveiller l'état, les performances et l'intégrité des pipelines ETL au sein de votre organisation. Il offre une visibilité complète sur les jobs en cours d'exécution, les erreurs rencontrées, les volumes de données traités et les temps d'exécution.

### Pourquoi ETL Monitor ?

- 📊 **Visibilité centralisée** — Suivez tous vos pipelines depuis une seule interface.
- ⚡ **Alertes en temps réel** — Soyez notifié immédiatement en cas d'échec ou d'anomalie.
- 📈 **Historique et tendances** — Analysez les performances dans le temps.
- 🔒 **Traçabilité** — Gardez un audit trail complet de chaque exécution.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🟢 Suivi en temps réel | Visualisation live du statut des jobs ETL |
| 🔴 Détection d'erreurs | Capture et classification automatique des erreurs |
| 📧 Notifications | Alertes par e-mail, Slack ou webhook |
| 📊 Métriques | Temps d'exécution, volume de lignes, taux d'erreur |
| 🗓️ Planificateur | Intégration avec cron, Airflow, dbt Cloud |
| 🔍 Logs centralisés | Agrégation des logs par pipeline et par run |
| 🧮 Tableau de bord | Dashboard interactif avec graphiques et KPIs |
| 🔐 Authentification | Gestion des utilisateurs et des rôles (RBAC) |

---

## 🏗️ Architecture

```
etl-monitor/
├── api/                    # Backend REST API
│   ├── controllers/        # Contrôleurs des routes
│   ├── models/             # Modèles de données
│   ├── services/           # Logique métier
│   └── middlewares/        # Authentification, logging, erreurs
├── worker/                 # Processus de collecte des métriques
│   ├── collectors/         # Collecteurs par type de pipeline
│   ├── parsers/            # Parsers de logs
│   └── schedulers/         # Déclencheurs périodiques
├── frontend/               # Interface utilisateur (React/Vue)
│   ├── components/         # Composants UI
│   ├── pages/              # Pages du dashboard
│   └── hooks/              # Logique partagée
├── config/                 # Fichiers de configuration
├── migrations/             # Scripts de migration de base de données
├── tests/                  # Tests unitaires et d'intégration
└── docker/                 # Fichiers Docker
```

### Flux de données

```
Pipeline ETL → Agent/Hook → ETL Monitor API → Base de données
                                    ↓
                             Worker de métriques
                                    ↓
                        Alertes / Dashboard / Rapports
```

---

## 🛠️ Prérequis

Avant d'installer ETL Monitor, assurez-vous d'avoir :

- **Node.js** >= 18.x ou **Python** >= 3.10
- **PostgreSQL** >= 14 (base de données principale)
- **Redis** >= 7 (cache et files de messages)
- **Docker** & **Docker Compose** (recommandé)
- Accès aux pipelines ETL à surveiller

---

## 📦 Installation

### Option 1 — Docker Compose (recommandé)

```bash
# Cloner le dépôt
git clone https://github.com/Tnkhi/etl-monitor.git
cd etl-monitor

# Copier et adapter le fichier de configuration
cp .env.example .env

# Démarrer les services
docker compose up -d

# Vérifier que tout fonctionne
docker compose ps
```

L'application sera disponible sur `http://localhost:3000`.

### Option 2 — Installation manuelle

```bash
# Cloner le dépôt
git clone https://github.com/votre-org/etl-monitor.git
cd etl-monitor

# Installer les dépendances
npm install        # ou pip install -r requirements.txt

# Configurer la base de données
npm run db:migrate

# Lancer en développement
npm run dev

# Lancer en production
npm run build && npm start
```

---

## ⚙️ Configuration

Copiez `.env.example` en `.env` et renseignez les variables suivantes :

```dotenv
# Application
APP_ENV=production
APP_PORT=3000
APP_SECRET=your-secret-key-here

# Base de données
DB_HOST=localhost
DB_PORT=5432
DB_NAME=etl_monitor
DB_USER=postgres
DB_PASSWORD=your-password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Notifications
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=your-smtp-password

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz

# Authentification
JWT_SECRET=your-jwt-secret
JWT_EXPIRES_IN=24h

# Rétention des logs (jours)
LOG_RETENTION_DAYS=90
```

### Configuration des pipelines

Créez un fichier `config/pipelines.yml` pour déclarer vos pipelines :

```yaml
pipelines:
  - name: "Chargement clients"
    type: airflow
    dag_id: load_customers
    alert_on_failure: true
    sla_minutes: 30

  - name: "Export financier"
    type: dbt
    project: finance
    alert_on_failure: true
    alert_on_sla_breach: true
    sla_minutes: 60

  - name: "Sync CRM"
    type: custom
    endpoint: https://crm.internal/etl/status
    poll_interval_seconds: 60
```

---

## 🖥️ Utilisation

### Démarrer un run manuellement (API)

```bash
curl -X POST http://localhost:3000/api/v1/runs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_id": "load_customers",
    "triggered_by": "manual"
  }'
```

### Soumettre un événement depuis votre script ETL

```python
import requests

def notify_etl_monitor(pipeline_id, status, rows_processed=None, error=None):
    payload = {
        "pipeline_id": pipeline_id,
        "status": status,          # "started" | "success" | "failed"
        "rows_processed": rows_processed,
        "error_message": error
    }
    requests.post(
        "http://etl-monitor/api/v1/events",
        json=payload,
        headers={"Authorization": "Bearer <token>"}
    )

# Exemple d'usage
notify_etl_monitor("load_customers", "success", rows_processed=15000)
```

---

## 📡 API Reference

### Authentification

Tous les endpoints nécessitent un token JWT passé dans le header `Authorization: Bearer <token>`.

### Endpoints principaux

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/pipelines` | Liste tous les pipelines |
| `GET` | `/api/v1/pipelines/:id` | Détails d'un pipeline |
| `GET` | `/api/v1/runs` | Historique des runs |
| `GET` | `/api/v1/runs/:id` | Détails d'un run |
| `POST` | `/api/v1/events` | Soumettre un événement ETL |
| `GET` | `/api/v1/metrics` | Métriques globales |
| `GET` | `/api/v1/alerts` | Liste des alertes actives |
| `PUT` | `/api/v1/alerts/:id/ack` | Acquitter une alerte |

### Exemple de réponse — GET /api/v1/runs/:id

```json
{
  "id": "run_abc123",
  "pipeline_id": "load_customers",
  "status": "success",
  "started_at": "2025-04-26T08:00:00Z",
  "finished_at": "2025-04-26T08:12:34Z",
  "duration_seconds": 754,
  "rows_extracted": 50000,
  "rows_loaded": 49987,
  "rows_rejected": 13,
  "error_message": null,
  "triggered_by": "scheduler"
}
```

---

## 📊 Dashboard

Le dashboard ETL Monitor offre les vues suivantes :

- **Vue d'ensemble** — Statut global de tous les pipelines, KPIs clés du jour.
- **Timeline** — Chronologie des runs avec code couleur (succès / échec / en cours).
- **Détail pipeline** — Métriques par pipeline : durée moyenne, taux de succès, volume traité.
- **Logs** — Accès aux logs bruts filtrés par run ou par pipeline.
- **Alertes** — Historique et gestion des alertes.

Accès : `http://localhost:3000`

---

## 🔔 Alertes & Notifications

ETL Monitor déclenche des alertes dans les situations suivantes :

- ❌ **Échec d'un job** — Le pipeline se termine avec une erreur.
- ⏱️ **Dépassement de SLA** — Le job dépasse la durée maximale configurée.
- 🔇 **Job silencieux** — Un pipeline n'a pas été exécuté depuis trop longtemps.
- 📉 **Anomalie de volume** — Le nombre de lignes traitées est anormalement bas.

Les notifications sont envoyées via **e-mail**, **Slack** ou **webhook HTTP** selon la configuration.

---

## 🧪 Tests

```bash
# Lancer tous les tests
npm test

# Tests unitaires uniquement
npm run test:unit

# Tests d'intégration
npm run test:integration

# Rapport de couverture
npm run test:coverage
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/ma-fonctionnalite`)
3. Committez vos changements (`git commit -m 'feat: ajout de ma fonctionnalité'`)
4. Poussez la branche (`git push origin feature/ma-fonctionnalite`)
