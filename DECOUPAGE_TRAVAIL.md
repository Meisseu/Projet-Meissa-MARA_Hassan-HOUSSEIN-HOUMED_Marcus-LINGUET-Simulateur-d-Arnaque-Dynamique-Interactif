# Découpage du Projet en 4 Parties - Groupe de 2 Personnes

## **PARTIE 1 : Infrastructure & Agent Victime** 
**Personne A - Estimation : 25% du projet**

### Objectifs:
- Mettre en place le repository GitHub avec `.gitignore` et structure de base
- Créer le système de gestion des variables d'environnement (`.env`)
- Implémenter l'**Agent "Victime" (Mme Jeanne Dubois)**
- Développer le système de bruitages (Tools/MCP)

### Livrables détaillés:
1. **Setup du projet:**
   - Repository public avec README.md (noms des membres)
   - Fichier `.env.example` avec placeholders
   - Structure de dossiers (`/agents`, `/tools`, `/scripts`, `/audio`)
   - `requirements.txt` avec dépendances (langchain, openai, python-dotenv)

2. **Persona de la Victime:**
   - Fichier `victim_prompt.py` contenant le System Prompt modulaire
   - Implémentation de la personnalité (lente, confuse, 78 ans)
   - Gestion de la mémoire conversationnelle (ConversationBufferMemory)

3. **Système de Bruits (Tools):**
   ```python
   @tool decorators pour:
   - play_dog_bark()
   - play_doorbell()
   - play_cough()
   - play_tv_background()
   ```
   - Soit fichiers audio réels, soit marqueurs textuels `[SOUND_EFFECT: XXX]`
   - Logique pour que le LLM appelle ces outils de manière contextuelle

---

## **PARTIE 2 : Agent Directeur & Système de Scripts**
**Personne B - Estimation : 25% du projet**

### Objectifs:
- Créer l'**Agent "Directeur de Scénario"** (superviseur)
- Développer au moins 2 scripts d'arnaque types
- Implémenter le système de progression dans le scénario

### Livrables détaillés:
1. **Agent Directeur:**
   - LLM qui analyse les échanges sans parler directement
   - Fonction `analyze_conversation(history, script)` retournant le nouvel objectif
   - Détection des étapes du script franchies

2. **Scripts d'Arnaque:**
   - **Script 1 - Support Technique Microsoft:**
     - Étape 1: Contact initial (prétexte virus)
     - Étape 2: Demande d'accès TeamViewer
     - Étape 3: Tentative de paiement
     
   - **Script 2 - Arnaque Bancaire:**
     - Étape 1: Alerte fraude
     - Étape 2: Demande d'informations bancaires
     - Étape 3: Code de vérification

3. **Système de Contexte Dynamique:**
   - Fonction qui injecte le contexte courant dans le prompt de la Victime
   - Mise à jour de `{dynamic_context_from_director}`
   - Gestion des transitions d'objectifs

---

## **PARTIE 3 : Système d'Audience Interactif**
**Personne A - Estimation : 25% du projet**

### Objectifs:
- Créer l'**Agent "Modérateur Audience"**
- Développer l'interface de suggestion/vote
- Intégrer les événements audience dans la simulation

### Livrables détaillés:
1. **Modérateur LLM:**
   - Reçoit des propositions textuelles (ex: "Le facteur sonne à la porte")
   - Filtre les inappropriées (violence, hors-sujet)
   - Génère 3 options cohérentes avec le contexte actuel
   - Prompt system: "Vous évaluez la pertinence d'événements perturbateurs..."

2. **Interface Audience:**
   - Simple: Input console avec liste de suggestions
   - Avancé (bonus): Interface web Flask/Streamlit
   - Système de vote (peut être simulé pour la démo)

3. **Intégration dans la Boucle:**
   - Déclenchement tous les X tours (configurable)
   - Modification temporaire de `{current_audience_constraint}`
   - Exemples d'événements:
     - "Poupoune (le chien) demande à sortir"
     - "La casserole déborde dans la cuisine"
     - "Un coup de fil d'un vrai petit-fils arrive"

---

## **PARTIE 4 : Orchestration & Boucle Principale**
**Personne B - Estimation : 25% du projet**

### Objectifs:
- Créer la **boucle d'exécution principale**
- Intégrer tous les agents ensemble
- Tester et documenter avec screenshots
- Rédiger le README.md final

### Livrables détaillés:
1. **Main Loop (`simulator.py`):**
   ```python
   - Initialisation des 3 agents
   - Gestion de la conversation (history)
   - Appel séquentiel: Input → Directeur → Audience (si tour) → Victime → Output
   - Détection de fin de scénario (arnaqueur raccroche ou Jeanne gagne)
   ```

2. **Interface Utilisateur:**
   - Mode "Arnaqueur Humain": Input console pour jouer l'arnaqueur
   - Mode "Arnaqueur Bot" (bonus): Second LLM joue l'escroc
   - Affichage formaté des réponses et effets sonores

3. **Tests & Validation:**
   - Au moins 2 conversations complètes enregistrées
   - Test de résistance: Jeanne NE DOIT PAS donner ses infos
   - Test d'outils: Les bruits s'activent-ils naturellement ?
   - Test audience: Les événements changent-ils le comportement ?

4. **Documentation (README.md):**
   - Section "À propos" avec noms/prénoms ✓
   - Installation (requirements, .env)
   - Utilisation (commande de lancement)
   - Architecture (diagramme des agents)
   - **Screenshots** avec exemples de conversations
   - Limites et améliorations possibles

---

## **Répartition Travail pour 2 Personnes:**

| **Personne A** | **Personne B** |
|----------------|----------------|
| Partie 1: Infrastructure & Victime | Partie 2: Directeur & Scripts |
| Partie 3: Système Audience | Partie 4: Orchestration & Tests |

### **Coordination clé:**
- **Après Partie 1+2:** Merge et test des deux agents séparément
- **Après Partie 3:** Intégration de l'audience dans la boucle
- **Partie 4 finale:** Personne B orchestre, Personne A aide aux tests/README

### **Timeline suggérée:**
- **Semaines 1-2:** Parties 1 & 2 (en parallèle)
- **Semaine 3:** Partie 3 + Intégration
- **Semaine 4:** Partie 4 + Polissage + Documentation

---

## **Points de Synchronisation Importants:**

### 🔄 Checkpoint 1 (Fin Semaine 2):
- **Personne A** doit avoir: Agent Victime fonctionnel + Tools audio opérationnels
- **Personne B** doit avoir: Agent Directeur fonctionnel + 2 scripts d'arnaque définis
- **Action:** Tester les deux agents séparément, créer des interfaces temporaires

### 🔄 Checkpoint 2 (Fin Semaine 3):
- **Personne A** doit avoir: Système d'audience complet avec modérateur
- **Personne B** commence la boucle principale
- **Action:** Intégrer l'audience dans un prototype de boucle

### 🔄 Checkpoint 3 (Fin Semaine 4):
- Boucle complète fonctionnelle
- Tests complets effectués
- README.md rédigé avec screenshots
- Code nettoyé, commenté, et prêt pour le rendu

---

## **Checklist de Rendu Final:**

- [ ] Repository GitHub public avec lien partagé
- [ ] `.gitignore` contient `.env`
- [ ] AUCUNE clé API dans l'historique des commits
- [ ] README.md contient noms et prénoms des membres
- [ ] README.md contient instructions d'installation
- [ ] README.md contient screenshots de conversations
- [ ] `requirements.txt` à jour
- [ ] `.env.example` fourni avec variables nécessaires
- [ ] Code commenté et structuré
- [ ] Au moins 2 scénarios d'arnaque implémentés
- [ ] Système d'audience fonctionnel
- [ ] Test de résistance validé (Jeanne ne craque pas)

---

## **Conseils de Développement:**

### Pour éviter les blocages:
1. **Utilisez des mocks au début:** Si l'API OpenAI tarde, créez des réponses simulées pour tester la logique
2. **Travaillez par feature branches:** Chaque partie dans sa branche, merge à chaque checkpoint
3. **Documentez au fur et à mesure:** Ne laissez pas le README pour la fin
4. **Testez tôt et souvent:** Un agent buggué peut bloquer tout le système

### Outils recommandés:
- **LangChain:** Pour la gestion des agents et tools
- **Python-dotenv:** Pour les variables d'environnement
- **Playsound/Pygame:** Pour les effets sonores (si audio réel)
- **Rich/Colorama:** Pour un affichage console joli
- **Streamlit (bonus):** Pour une interface web rapide

---

**Bonne chance pour le projet! 🎭**
