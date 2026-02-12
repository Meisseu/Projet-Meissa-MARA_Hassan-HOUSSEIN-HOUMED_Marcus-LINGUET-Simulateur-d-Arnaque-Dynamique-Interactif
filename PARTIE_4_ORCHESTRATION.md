# 🎬 Partie 4 : Orchestration Complète

## Vue d'ensemble

La **Partie 4** intègre l'ensemble des composants développés par les trois membres de l'équipe en une application interactive complète. Le fichier `main.py` constitue le cœur de cette orchestration.

---

## 🏗️ Architecture d'Intégration

```
┌─────────────────────────────────────────────────────────┐
│                    SCAMMEUR (USER)                       │
│                    Input Terminal                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              DIRECTOR AGENT (Partie 2)                   │
│  • Analyse l'historique de conversation                 │
│  • Identifie l'étape du scénario                        │
│  • Calcule le niveau de risque                          │
│  • Fournit l'objectif tactique pour Jeanne              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│        AUDIENCE EVENT MANAGER (Partie 3)                 │
│  • Déclenché tous les N tours                           │
│  • Collecte suggestions d'événements                     │
│  • ModeratorAgent filtre et sélectionne 3 options       │
│  • AudienceInterface gère le vote                       │
│  • Retourne contrainte textuelle                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              VICTIM AGENT (Partie 1)                     │
│  • Reçoit : scammer_input + objective + constraint      │
│  • Génère réponse avec personnalité Jeanne              │
│  • Maintient historique conversationnel                 │
│  • Peut déclencher effets audio (audio_tools)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  AFFICHAGE RÉPONSE                       │
│              (Rich Console Output)                       │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Composants Intégrés

### 1. VictimAgent (Hassan - Partie 1)
**Fichier :** `simulateur_arnaque/agents/victim_agent.py`

**Rôle :** Jouer le personnage de Mme Jeanne Dubois, 78 ans
- Maintient un historique de conversation (`chat_history`)
- Répond selon un objectif tactique fourni par le Director
- Intègre les contraintes d'audience (événements perturbateurs)
- Génère des réponses cohérentes et naturelles en français

**Interface principale :**
```python
VictimAgent.respond(
    scammer_input: str,      # Message du scammeur
    objective: str,          # Objectif tactique (ex: "Rester sceptique")
    audience_constraint: str # Contrainte audience (ex: "Le chien aboie")
) -> str
```

### 2. DirectorAgent (Marcus - Partie 2)
**Fichier :** `simulateur_arnaque/agents/director.py`

**Rôle :** Analyser la conversation et orchestrer la progression du scénario
- Détecte l'étape actuelle via regex sur l'historique
- Calcule le niveau de risque (0-3) selon mots-clés sensibles
- Fournit contexte dynamique et objectif pour Jeanne
- Basé sur des règles (pas de LLM) pour garantir cohérence

**Structure de sortie :**
```python
DirectorUpdate(
    script_id="microsoft_support",
    stage_id="alert_initiale",
    completed_stages=[...],
    next_objective_for_victim="Rester sceptique et demander des preuves",
    dynamic_context_from_director="...",
    risk_level=2
)
```

### 3. AudienceEventManager (Meissa - Partie 3)
**Fichiers :** 
- `simulateur_arnaque/audience_events.py`
- `simulateur_arnaque/audience_interface.py`
- `simulateur_arnaque/agents/moderator.py`

**Rôle :** Créer des événements perturbateurs cohérents avec l'aide du public
- **AudienceInterface** : Collecte suggestions (console/simulé/web)
- **ModeratorAgent** : Filtre suggestions inappropriées via LLM
- **AudienceEventManager** : Coordonne le tout

**Flux d'exécution :**
1. Vérifie si c'est le tour d'audience (`turn_count % frequency == 0`)
2. Collecte suggestions du public
3. ModeratorAgent sélectionne 3 meilleures options
4. Vote du public sur les 3 options
5. Retourne contrainte textuelle pour Jeanne

### 4. Script Loader (Marcus - Partie 2)
**Fichier :** `simulateur_arnaque/scripts/script_loader.py`

**Rôle :** Charger les scripts d'arnaque prédéfinis
- Format JSON avec étapes progressives
- Signaux de succès pour détecter progression
- Objectifs tactiques pour chaque étape

**Scripts disponibles :**
- `microsoft_support.json` : Faux support technique
- `bank_fraud.json` : Arnaque bancaire

---

## 🔧 Classe ScamSimulator

### Initialisation

```python
simulator = ScamSimulator(
    script_id="microsoft_support",  # ou "bank_fraud"
    use_audience=True               # Active/désactive audience
)
```

**Actions lors de l'initialisation :**
1. Charge le script JSON
2. Instancie `VictimAgent`
3. Si `use_audience=True` :
   - Crée `ModeratorAgent(api_key=OPENAI_API_KEY)`
   - Crée `AudienceInterface(mode="console")`
   - Crée `AudienceEventManager(moderator, interface, vote_frequency=5)`

### Boucle Principale : run_turn()

```python
def run_turn(scammer_input: str) -> str:
    # 1. Analyser avec DirectorAgent
    update = director.analyze_conversation(history, script)
    
    # 2. Gérer événement d'audience (si applicable)
    if should_trigger_audience():
        audience_constraint = audience_manager.process_audience_round(...)
    
    # 3. Générer réponse de Jeanne
    response = victim.respond(
        scammer_input=scammer_input,
        objective=update.next_objective_for_victim,
        audience_constraint=audience_constraint
    )
    
    return response
```

---

## 🎮 Scénarios Implémentés

### 1. Microsoft Support (microsoft_support.json)

**Étapes :**
1. **alert_initiale** : Alerte virus/sécurité
2. **verification_technique** : Demande vérification système
3. **demande_acces_distant** : Installation TeamViewer/AnyDesk
4. **demande_paiement** : Proposition service payant
5. **pression_urgence** : Augmentation pression temporelle

### 2. Arnaque Bancaire (bank_fraud.json)

**Étapes :**
1. **appel_banque** : Présentation conseiller bancaire
2. **verification_identite** : Demande infos personnelles
3. **code_securite** : Demande code SMS/OTP
4. **demande_iban_carte** : Tentative obtention RIB/carte
5. **virement_urgent** : Proposition "sécurisation" via virement

---

## 🖥️ Interface Utilisateur

### Affichages Rich Console

1. **Panneau Scénario** : Titre et description à l'initialisation
2. **Panneau Director** : Analyse après chaque tour
   - Étape courante
   - Étapes complétées
   - Objectif pour Jeanne
   - Niveau de risque (couleur : vert/jaune/orange/rouge)
3. **Panneau Événement Public** : Contrainte d'audience en magenta
4. **Panneau Réponse Jeanne** : Réponse de la victime en vert

### Commandes Utilisateur

- **Message libre** : Joue le rôle du scammeur
- `status` : Affiche état de la simulation
- `reset` : Réinitialise la conversation
- `quit` / `exit` : Quitte le simulateur

---

## 🔑 Configuration Requise

### Variables d'environnement (.env)

```env
# OpenAI API
OPENAI_API_KEY=sk-...

# Configuration LLM
OPENAI_MODEL=gpt-4-turbo-preview

# Températures
VICTIM_TEMPERATURE=0.8
DIRECTOR_TEMPERATURE=0.3

# Audience
AUDIENCE_VOTE_FREQUENCY=5

# Google Cloud (optionnel)
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
```

### Dépendances Principales

```txt
langchain>=1.0.0
langchain-openai>=0.0.5
langchain-community>=0.0.19
langchain-core>=0.1.0
openai>=1.12.0
python-dotenv>=1.0.0
rich>=13.7.0
colorama>=0.4.6
```

---

## 🧪 Tests d'Intégration

### Test Director
```bash
python test_director.py
```
Vérifie que le Director analyse correctement l'historique.

### Test Intégration P1-P3
```bash
python test_integration_p1_p3.py
```
Vérifie la communication VictimAgent ↔ AudienceEventManager.

### Test Complet
```bash
python main.py
```
Lance le simulateur interactif complet.

---

## 🐛 Résolution de Problèmes

### Erreur : ModuleNotFoundError

**Solution :** Imports corrigés pour utiliser imports relatifs
```python
from simulateur_arnaque.agents.victim_agent import VictimAgent
from simulateur_arnaque.agents.moderator import ModeratorAgent
```

### Erreur : No module named 'langchain.memory'

**Solution :** Migration vers implémentation manuelle de l'historique
```python
# Ancien (deprecated)
from langchain.memory import ConversationBufferMemory

# Nouveau
self.chat_history = []  # Simple liste de dictionnaires
```

### Erreur : TypeError: AudienceEventManager() got unexpected keyword

**Solution :** Utiliser la bonne signature
```python
# Incorrect
AudienceEventManager(frequency=5, mode="console")

# Correct
moderator = ModeratorAgent(api_key=OPENAI_API_KEY)
interface = AudienceInterface(mode="console")
manager = AudienceEventManager(moderator, interface, vote_frequency=5)
```

---

## 📊 Statistiques d'Intégration

- **Fichiers modifiés :** 8
- **Lignes de code main.py :** ~290
- **Tests créés :** 3
- **Scripts JSON créés :** 2
- **Agents intégrés :** 3 (Victim, Director, Moderator)
- **Systèmes coordonnés :** 4 (Victim, Director, Audience, Scripts)

---

## 🎯 Points Clés de l'Orchestration

1. **Séparation des responsabilités** : Chaque agent a un rôle précis
2. **Communication unidirectionnelle** : Director → Audience → Victim
3. **Aucune dépendance circulaire** : Architecture claire en cascade
4. **Gestion d'état centralisée** : `ScamSimulator` maintient historique
5. **Interface utilisateur riche** : Rich console pour expérience immersive

---

## 🚀 Évolutions Futures

### Court Terme
- [ ] Mode arnaqueur bot (LLM joue le scammeur)
- [ ] Sauvegarde automatique des conversations
- [ ] Export statistiques en JSON

### Moyen Terme
- [ ] Interface web Streamlit
- [ ] Support multi-langues
- [ ] Plus de scénarios d'arnaque

### Long Terme
- [ ] API REST pour intégration externe
- [ ] Support audio réel (TTS/STT)
- [ ] Base de données pour analytics

---

## 👥 Crédits Partie 4

**Implémentation :** Collaboration Hassan, Marcus, Meissa  
**Fichier principal :** `main.py`  
**Date de finalisation :** Février 2026  
**Statut :** ✅ **COMPLÈTE ET FONCTIONNELLE**
