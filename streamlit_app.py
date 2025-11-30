import streamlit as st
import random
import pandas as pd

#30 nov 16h05

# --- 1. Définition des données des verbes irréguliers ---

VERBES = [
    # Verbes de la seconde image (lignes 1 à 35)
    {"id": 1, "base": "awake", "past": "awoke", "participle": "awoken", "fr": "réveiller"},
    {"id": 2, "base": "be", "past": "was, were", "participle": "been", "fr": "être"},
    {"id": 3, "base": "bear", "past": "bore", "participle": "born/borne", "fr": "supporter"},
    {"id": 4, "base": "beat", "past": "beat", "participle": "beaten", "fr": "battre"},
    {"id": 5, "base": "become", "past": "became", "participle": "become", "fr": "devenir"},
    {"id": 6, "base": "begin", "past": "began", "participle": "begun", "fr": "commencer"},
    {"id": 7, "base": "bend", "past": "bent", "participle": "bent", "fr": "plier"},
    {"id": 8, "base": "bet", "past": "bet", "participle": "bet", "fr": "gager, parier"},
    {"id": 9, "base": "bid", "past": "bid", "participle": "bid", "fr": "miser"},
    {"id": 10, "base": "bind", "past": "bound", "participle": "bound", "fr": "lier"},
    {"id": 11, "base": "bite", "past": "bit", "participle": "bitten", "fr": "mordre"},
    {"id": 12, "base": "bleed", "past": "bled", "participle": "bled", "fr": "saigner"},
    {"id": 13, "base": "blow", "past": "blew", "participle": "blown", "fr": "souffler"},
    {"id": 14, "base": "break", "past": "broke", "participle": "broken", "fr": "casser"},
    {"id": 15, "base": "bring", "past": "brought", "participle": "brought", "fr": "apporter"},
    {"id": 16, "base": "broadcast", "past": "broadcast", "participle": "broadcast", "fr": "diffuser"},
    {"id": 17, "base": "build", "past": "built", "participle": "built", "fr": "bâtir"},
    {"id": 18, "base": "buy", "past": "bought", "participle": "bought", "fr": "acheter"},
    {"id": 19, "base": "catch", "past": "caught", "participle": "caught", "fr": "attraper"},
    {"id": 20, "base": "choose", "past": "chose", "participle": "chosen", "fr": "choisir"},
    {"id": 21, "base": "come", "past": "came", "participle": "come", "fr": "venir"},
    {"id": 22, "base": "cost", "past": "cost", "participle": "cost", "fr": "coûter"},
    {"id": 23, "base": "cut", "past": "cut", "participle": "cut", "fr": "couper"},
    {"id": 24, "base": "deal", "past": "dealt", "participle": "dealt", "fr": "négocier"},
    {"id": 25, "base": "dig", "past": "dug", "participle": "dug", "fr": "creuser"},
    {"id": 26, "base": "do", "past": "did", "participle": "done", "fr": "faire"},
    {"id": 27, "base": "draw", "past": "drew", "participle": "drawn", "fr": "dessiner"},
    {"id": 28, "base": "drive", "past": "drove", "participle": "driven", "fr": "conduire"},
    {"id": 29, "base": "drink", "past": "drank", "participle": "drunk", "fr": "boire"},
    {"id": 30, "base": "eat", "past": "ate", "participle": "eaten", "fr": "manger"},
    {"id": 31, "base": "fall", "past": "fell", "participle": "fallen", "fr": "tomber"},
    {"id": 32, "base": "feed", "past": "fed", "participle": "fed", "fr": "nourrir"},
    {"id": 33, "base": "feel", "past": "felt", "participle": "felt", "fr": "sentir, ressentir"},
    {"id": 34, "base": "fight", "past": "fought", "participle": "fought", "fr": "combattre"},
    {"id": 35, "base": "find", "past": "found", "participle": "found", "fr": "trouver"},

    # Verbes de votre liste initiale (lignes 36 à 70)
    {"id": 36, "base": "fly", "past": "flew", "participle": "flown", "fr": "voler"},
    {"id": 37, "base": "forbid", "past": "forbade", "participle": "forbidden", "fr": "interdire"},
    {"id": 38, "base": "forget", "past": "forgot", "participle": "forgotten", "fr": "oublier"},
    {"id": 39, "base": "forgive", "past": "forgave", "participle": "forgiven", "fr": "pardonner"},
    {"id": 40, "base": "freeze", "past": "froze", "participle": "frozen", "fr": "geler"},
    {"id": 41, "base": "get", "past": "got", "participle": "gotten", "fr": "recevoir, obtenir"},
    {"id": 42, "base": "give", "past": "gave", "participle": "given", "fr": "donner"},
    {"id": 43, "base": "go", "past": "went", "participle": "gone", "fr": "aller"},
    {"id": 44, "base": "grow", "past": "grew", "participle": "grown", "fr": "grandir"},
    {"id": 45, "base": "hang", "past": "hung", "participle": "hung", "fr": "suspendre"},
    {"id": 46, "base": "have", "past": "had", "participle": "had", "fr": "avoir"},
    {"id": 47, "base": "hear", "past": "heard", "participle": "heard", "fr": "entendre"},
    {"id": 48, "base": "hide", "past": "hid", "participle": "hidden", "fr": "cacher"},
    {"id": 49, "base": "hit", "past": "hit", "participle": "hit", "fr": "frapper"},
    {"id": 50, "base": "hold", "past": "held", "participle": "held", "fr": "tenir"},
    {"id": 51, "base": "hurt", "past": "hurt", "participle": "hurt", "fr": "blesser"},
    {"id": 52, "base": "keep", "past": "kept", "participle": "kept", "fr": "garder"},
    {"id": 53, "base": "know", "past": "knew", "participle": "known", "fr": "connaître"},
    {"id": 54, "base": "lay", "past": "laid", "participle": "laid", "fr": "poser, coucher"},
    {"id": 55, "base": "lead", "past": "led", "participle": "led", "fr": "mener, diriger"},
    {"id": 56, "base": "leave", "past": "left", "participle": "left", "fr": "partir"},
    {"id": 57, "base": "lend", "past": "lent", "participle": "lent", "fr": "prêter"},
    {"id": 58, "base": "let", "past": "let", "participle": "let", "fr": "laisser"},
    {"id": 59, "base": "lie", "past": "lay", "participle": "lain", "fr": "s'allonger, s'étendre"},
    {"id": 60, "base": "light", "past": "lit", "participle": "lit", "fr": "allumer"},
    {"id": 61, "base": "lose", "past": "lost", "participle": "lost", "fr": "perdre"},
    {"id": 62, "base": "make", "past": "made", "participle": "made", "fr": "fabriquer"},
    {"id": 63, "base": "mean", "past": "meant", "participle": "meant", "fr": "signifier"},
    {"id": 64, "base": "meet", "past": "met", "participle": "met", "fr": "rencontrer"},
    {"id": 65, "base": "pay", "past": "paid", "participle": "paid", "fr": "payer"},
    {"id": 66, "base": "put", "past": "put", "participle": "put", "fr": "mettre"},
    {"id": 67, "base": "quit", "past": "quit", "participle": "quit", "fr": "abandonner"},
    {"id": 68, "base": "read", "past": "read", "participle": "read", "fr": "lire"},
    {"id": 69, "base": "ride", "past": "rode", "participle": "ridden", "fr": "aller à, se promener à"},
    {"id": 70, "base": "ring", "past": "rang", "participle": "rung", "fr": "sonner"},

    # Verbes de la première image (lignes 71 à 100)
    {"id": 71, "base": "rise", "past": "rose", "participle": "risen", "fr": "lever"},
    {"id": 72, "base": "run", "past": "ran", "participle": "run", "fr": "courir"},
    {"id": 73, "base": "say", "past": "said", "participle": "said", "fr": "dire"},
    {"id": 74, "base": "see", "past": "saw", "participle": "seen", "fr": "voir"},
    {"id": 75, "base": "sell", "past": "sold", "participle": "sold", "fr": "vendre"},
    {"id": 76, "base": "send", "past": "sent", "participle": "sent", "fr": "envoyer"},
    {"id": 77, "base": "set", "past": "set", "participle": "set", "fr": "mettre"},
    {"id": 78, "base": "shake", "past": "shook", "participle": "shaken", "fr": "secouer"},
    {"id": 79, "base": "show", "past": "showed", "participle": "shown", "fr": "montrer"},
    {"id": 80, "base": "shoot", "past": "shot", "participle": "shot", "fr": "tirer"},
    {"id": 81, "base": "shut", "past": "shut", "participle": "shut", "fr": "fermer"},
    {"id": 82, "base": "sing", "past": "sang", "participle": "sung", "fr": "chanter"},
    {"id": 83, "base": "sit", "past": "sat", "participle": "sat", "fr": "asseoir"},
    {"id": 84, "base": "sleep", "past": "slept", "participle": "slept", "fr": "dormir"},
    {"id": 85, "base": "speak", "past": "spoke", "participle": "spoken", "fr": "parler"},
    {"id": 86, "base": "spend", "past": "spent", "participle": "spent", "fr": "dépenser"},
    {"id": 87, "base": "stand", "past": "stood", "participle": "stood", "fr": "se tenir debout"},
    {"id": 88, "base": "swim", "past": "swam", "participle": "swum", "fr": "nager"},
    {"id": 89, "base": "take", "past": "took", "participle": "taken", "fr": "prendre"},
    {"id": 90, "base": "teach", "past": "taught", "participle": "taught", "fr": "enseigner"},
    {"id": 91, "base": "tear", "past": "tore", "participle": "torn", "fr": "déchirer"},
    {"id": 92, "base": "tell", "past": "told", "participle": "told", "fr": "raconter"},
    {"id": 93, "base": "think", "past": "thought", "participle": "thought", "fr": "penser"},
    {"id": 94, "base": "throw", "past": "threw", "participle": "thrown", "fr": "lancer"},
    {"id": 95, "base": "understand", "past": "understood", "participle": "understood", "fr": "comprendre"},
    {"id": 96, "base": "wake", "past": "woke", "participle": "woken", "fr": "réveiller"},
    {"id": 97, "base": "wear", "past": "wore", "participle": "worn", "fr": "porter"},
    {"id": 98, "base": "win", "past": "won", "participle": "won", "fr": "gagner"},
    {"id": 99, "base": "wring", "past": "wrung", "participle": "wrung", "fr": "tordre, essorer"},
    {"id": 100, "base": "write", "past": "wrote", "participle": "written", "fr": "écrire"}
]

NB_QUESTIONS_QCM = 15 # Nombre de verbes pour le mode QCM
NB_VERBES_SAISIE = 10 # Nombre de verbes pour le mode Saisie
MAX_POINTS_PAR_CELLULE = 5 # Points de base pour le mode Saisie

# --- Fonctions Générales (Réinitialisation, Points) ---

def reinitialiser_session():
    """Supprime toutes les variables d'état pour recommencer."""
    # Réinitialise les états liés aux quizzes sans perdre la sélection de verbes
    preserve = ['mode_selectionne', 'selected_mode', 'verbs_selected_labels', 'selected_verbes']
    for key in list(st.session_state.keys()):
        if key in preserve:
            continue
        del st.session_state[key]
    # Valeurs par défaut
    st.session_state.quiz_fini = False
    st.session_state.score_total = 0
    st.session_state.started = False
    # Le rerun n'est pas nécessaire : les boutons déclenchent un rerun automatiquement

def calculer_points(tentatives, max_points):
    """Calcule le score basé sur le nombre de tentatives."""
    return max(0, max_points - tentatives)

# --- LOGIQUE QCM (Version 1) ---

def initialiser_session_qcm():
    """Initialise les variables d'état nécessaires au jeu QCM."""
    if 'score_qcm' not in st.session_state: st.session_state.score_qcm = 0
    if 'question_actuelle' not in st.session_state: st.session_state.question_actuelle = 0
    if 'quiz_fini' not in st.session_state: st.session_state.quiz_fini = False
    # Déterminer le pool et le nombre effectif de questions (éviter répétitions non souhaitées)
    if 'sequence_questions' not in st.session_state:
        pool = st.session_state.get('selected_verbes') or VERBES
        effective = min(NB_QUESTIONS_QCM, len(pool))
        st.session_state.effective_nb_qcm = effective
        if len(pool) < NB_QUESTIONS_QCM:
            # On préfère réduire le nombre de questions plutôt que répéter
            st.session_state.sequence_questions = random.sample(pool, effective)
        else:
            st.session_state.sequence_questions = random.sample(pool, NB_QUESTIONS_QCM)
    if 'current_verb_data' not in st.session_state: st.session_state.current_verb_data = None
    if 'phase' not in st.session_state: st.session_state.phase = 'base_form'
    if 'tentatives_base' not in st.session_state: st.session_state.tentatives_base = 0
    if 'tentatives_past' not in st.session_state: st.session_state.tentatives_past = 0
    if 'choices_base' not in st.session_state: st.session_state.choices_base = []
    if 'choices_past' not in st.session_state: st.session_state.choices_past = []
    if 'base_correcte' not in st.session_state: st.session_state.base_correcte = False
    if 'past_correcte' not in st.session_state: st.session_state.past_correcte = False

def generer_choix_qcm(bonne_reponse_key, nombre=5):
    """Génère les choix de réponse pour le QCM."""
    reponse_key = bonne_reponse_key
    bonne_reponse = st.session_state.current_verb_data[reponse_key]
    autres_verbes = [v for v in VERBES if v != st.session_state.current_verb_data]
    toutes_les_formes_sauf_correcte = [v[reponse_key] for v in autres_verbes if v[reponse_key] != bonne_reponse]
    nombre_distracteurs = min(nombre - 1, len(toutes_les_formes_sauf_correcte))
    distracteurs = random.sample(toutes_les_formes_sauf_correcte, nombre_distracteurs)
    choix_list = distracteurs
    if bonne_reponse not in choix_list: choix_list.append(bonne_reponse)
    random.shuffle(choix_list)
    return choix_list

def generer_choix_past_intelligent_qcm(verbe_base, verbe_past, nombre=5):
    """Génère des choix de réponse crédibles pour le Simple Past QCM."""
    # Choisir des distracteurs parmi les formes au prétérit des autres verbes
    autres_pasts = [v['past'] for v in VERBES if v['past'] != verbe_past]
    # Nettoyage: si une forme contient plusieurs alternatives séparées par ',', on considère l'ensemble
    autres_pasts = list(dict.fromkeys(autres_pasts))  # unique
    random.shuffle(autres_pasts)
    nombre_distracteurs = min(nombre - 1, len(autres_pasts))
    distracteurs = autres_pasts[:nombre_distracteurs]
    choix_list = distracteurs.copy()
    if verbe_past not in choix_list:
        choix_list.append(verbe_past)
    random.shuffle(choix_list)
    return choix_list

def passer_a_la_question_suivante_qcm():
    st.session_state.question_actuelle += 1
    st.session_state.phase = 'base_form'
    st.session_state.tentatives_base = 0
    st.session_state.tentatives_past = 0
    st.session_state.current_verb_data = None
    st.session_state.base_correcte = False
    st.session_state.past_correcte = False
    # Réinitialiser les choix pour la nouvelle question afin qu'ils soient régénérés
    st.session_state.choices_base = []
    st.session_state.choices_past = []
    if st.session_state.question_actuelle >= NB_QUESTIONS_QCM:
        st.session_state.quiz_fini = True

def transition_vers_simple_past_qcm():
    st.session_state.phase = 'simple_past'
    st.session_state.base_correcte = False
    # Forcer la régénération des choix du Simple Past pour le verbe courant
    st.session_state.choices_past = []

def verifier_reponse_qcm(reponse_utilisateur, bonne_reponse, type_question):
    
    if reponse_utilisateur == bonne_reponse:
        st.success("🎉 **Bonne réponse !**")

        points = calculer_points(st.session_state.tentatives_base if type_question == 'base_form' else st.session_state.tentatives_past, 3)
        st.session_state.score_qcm += points

        # Marquer l'étape comme réussie ; ceci déclenchera l'affichage du bouton de suite lors du rerun
        if type_question == 'base_form':
            st.session_state.base_correcte = True
        else:
            st.session_state.past_correcte = True

        st.info(f"Vous avez gagné **{points} points** pour cette étape. Score total : **{st.session_state.score_qcm}**")
        # Lorsque cette fonction est utilisée comme callback (`on_click`),
        # Streamlit provoque déjà un rerun après exécution du callback.
        # On évite d'appeler `st.rerun()` ici pour prévenir des comportements
        # de re-rendering inattendus.
        pass
        
    else:
        st.warning("❌ **Mauvaise réponse.** Essayez encore !")
        if type_question == 'base_form':
            st.session_state.tentatives_base += 1
            # Retirer la mauvaise réponse des choix disponibles
            if reponse_utilisateur in st.session_state.choices_base:
                 st.session_state.choices_base.remove(reponse_utilisateur)
        else:
            st.session_state.tentatives_past += 1
            # Retirer la mauvaise réponse des choix disponibles
            if reponse_utilisateur in st.session_state.choices_past:
                 st.session_state.choices_past.remove(reponse_utilisateur)
        # Pas de rerun forcé ici non plus.

def executer_quiz_qcm():
    initialiser_session_qcm()
    
    st.title("🧠 Le Maître des Verbes Irréguliers")
    
    col_score, col_progress = st.columns([1, 2])
    
    with col_score:
        st.metric(label="Score total", value=st.session_state.score_qcm)
    
    with col_progress:
        total_q = st.session_state.get('effective_nb_qcm', NB_QUESTIONS_QCM)
        progress_val = (st.session_state.question_actuelle) / total_q
        st.progress(progress_val, text=f"Progression : Question {st.session_state.question_actuelle + 1} / {total_q}")
    
    st.markdown("---")
    
    if st.session_state.quiz_fini:
        st.balloons()
        st.header(f"🎉 Quiz Terminé ! Votre score final est de **{st.session_state.score_qcm}** points.")
        st.markdown("---")
        st.markdown("### Contrôles de l'Exercice")
        cols = st.columns([1, 2])
        with cols[0]:
            if st.button("Reconfigurer"):
                st.session_state.started = False
                # le rerun est implicite après le clic sur le bouton
            
        with cols[1]:
            if st.button("Réinitialiser le Quiz Actuel"):
                reinitialiser_session()
                # le rerun est implicite après le clic sur le bouton
        
        if st.button("Recommencer le Quiz QCM"):
            reinitialiser_session()
        return

    if st.session_state.current_verb_data is None:
        try:
            st.session_state.current_verb_data = st.session_state.sequence_questions[st.session_state.question_actuelle]
        except IndexError:
            st.session_state.quiz_fini = True
            return

    verbe = st.session_state.current_verb_data
    
    st.subheader(f"Question {st.session_state.question_actuelle + 1}")
    st.header(f"**{verbe['fr']}**") 
    st.markdown("---")

    # --- Étape 1 : Deviner la BASE FORM ---
    if st.session_state.phase == 'base_form':
        st.subheader("**Base Form** ?")
        
        if not st.session_state.choices_base:
            st.session_state.choices_base = generer_choix_qcm('base')
        
        choices = st.session_state.choices_base
        
        cols = st.columns(len(choices))
        
        # Trouver l'indice de la bonne réponse
        index_bonne = -1
        try:
            index_bonne = choices.index(verbe['base'])
        except ValueError:
            pass 

        for i, choice in enumerate(choices):
            key = f"base_choice_{i}_{verbe['fr']}" 
            with cols[i]:
                if not st.session_state.base_correcte:
                    # Boutons cliquables utilisant un callback pour éviter des reruns forcés
                    st.button(f"{choice}", key=key, use_container_width=True, on_click=verifier_reponse_qcm, args=(choice, verbe['base'], 'base_form'))
                else:
                    # Afficher le texte statique si la réponse est correcte
                    # Mettre en gras la bonne réponse pour la visibilité
                    st.write(f"**{choice}**" if i == index_bonne else choice)
                    
                    # AFFICHAGE DU BOUTON SOUS LA BONNE RÉPONSE
                    if i == index_bonne:
                        # Ce bouton apparaît automatiquement après la mise à jour de l'état
                        st.button("👉 Continuer vers le Simple Past", on_click=transition_vers_simple_past_qcm, use_container_width=True)


    # --- Étape 2 : Deviner le SIMPLE PAST ---
    elif st.session_state.phase == 'simple_past':
        
        st.subheader(f"Base Form : **{verbe['base']}**")
        st.subheader("2. **Simple Past** ?")
        
        if not st.session_state.choices_past:
            st.session_state.choices_past = generer_choix_past_intelligent_qcm(verbe['base'], verbe['past']) 
            
        choices = st.session_state.choices_past
        
        cols = st.columns(len(choices))
        
        index_bonne_past = -1
        try:
            index_bonne_past = choices.index(verbe['past'])
        except ValueError:
            pass

        for i, choice in enumerate(choices):
            key = f"past_choice_{i}_{verbe['fr']}"
            with cols[i]:
                if not st.session_state.past_correcte:
                    st.button(f"{choice}", key=key, use_container_width=True, on_click=verifier_reponse_qcm, args=(choice, verbe['past'], 'simple_past'))
                else:
                    # Afficher le texte statique si la réponse est correcte
                    st.write(f"**{choice}**" if i == index_bonne_past else choice)

                    # AFFICHAGE DU BOUTON SOUS LA BONNE RÉPONSE
                    if st.session_state.past_correcte and i == index_bonne_past:
                        st.button("✅ Question suivante", on_click=passer_a_la_question_suivante_qcm, use_container_width=True)

# --- LOGIQUE SAISIE (Version 2) ---

def initialiser_session_saisie():
    """Initialise ou réinitialise le quiz de Saisie."""
    if 'quiz_data_saisie' not in st.session_state: st.session_state.quiz_data_saisie = None
    if 'df_quiz_saisie' not in st.session_state: st.session_state.df_quiz_saisie = None
    if 'score_total' not in st.session_state: st.session_state.score_total = 0
    if 'nb_erreurs' not in st.session_state: st.session_state.nb_erreurs = 0
    if 'tentatives_par_cellule' not in st.session_state: st.session_state.tentatives_par_cellule = {}
    if 'quiz_termine' not in st.session_state: st.session_state.quiz_termine = False
    if 'df_correction_display' not in st.session_state: st.session_state.df_correction_display = None

    if st.session_state.quiz_data_saisie is None:
        pool = st.session_state.get('selected_verbes') or VERBES
        if len(pool) >= NB_VERBES_SAISIE:
            st.session_state.quiz_data_saisie = random.sample(pool, NB_VERBES_SAISIE)
        else:
            st.session_state.quiz_data_saisie = random.choices(pool, k=NB_VERBES_SAISIE)
        data = {
            'Verbe Français': [v['fr'] for v in st.session_state.quiz_data_saisie],
            'Base Form': [''] * NB_VERBES_SAISIE,
            'Simple Past': [''] * NB_VERBES_SAISIE,
            'Base Form (Correct)': [v['base'] for v in st.session_state.quiz_data_saisie],
            'Simple Past (Correct)': [v['past'] for v in st.session_state.quiz_data_saisie],
        }
        st.session_state.df_quiz_saisie = pd.DataFrame(data)
        st.session_state.tentatives_par_cellule = {}
        for i in range(NB_VERBES_SAISIE):
            st.session_state.tentatives_par_cellule[f'base_{i}'] = 0
            st.session_state.tentatives_par_cellule[f'past_{i}'] = 0
        st.session_state.df_correction_display = None


def verifier_et_generer_correction_saisie(df_reponses_utilisateur):
    """Vérifie les réponses, calcule le score, met à jour l'état et prépare le tableau de correction."""
    df_correct = st.session_state.df_quiz_saisie
    df_correction = pd.DataFrame(index=df_correct.index)
    df_correction['Verbe Français'] = df_correct['Verbe Français']
    df_correction['Base Form Saisie'] = df_reponses_utilisateur['Base Form']
    df_correction['Correction Base'] = ''
    df_correction['Simple Past Saisi'] = df_reponses_utilisateur['Simple Past']
    df_correction['Correction Past'] = ''

    nouveaux_points = 0

    # Single-attempt mode: on donne une seule vérification. Pour chaque cellule incorrecte,
    # on affiche la bonne réponse dans la colonne de correction et on remplace la réponse
    # utilisateur par la réponse correcte pour montrer la solution.
    for i in range(NB_VERBES_SAISIE):
        # Base
        user_base = str(df_reponses_utilisateur.loc[i, 'Base Form']).strip()
        correct_base_raw = str(df_correct.loc[i, 'Base Form (Correct)'])
        correct_bases = [c.strip() for c in correct_base_raw.split(',')]
        if user_base.lower() in [c.lower() for c in correct_bases] and user_base != '':
            df_correction.loc[i, 'Correction Base'] = '✅'
            nouveaux_points += MAX_POINTS_PAR_CELLULE
        else:
            df_correction.loc[i, 'Correction Base'] = f"❌ {correct_base_raw}"
            # Remplacer la réponse par la réponse correcte pour affichage
            st.session_state.df_quiz_saisie.at[i, 'Base Form'] = correct_base_raw

        # Past
        user_past = str(df_reponses_utilisateur.loc[i, 'Simple Past']).strip()
        correct_past_raw = str(df_correct.loc[i, 'Simple Past (Correct)'])
        correct_pasts = [c.strip() for c in correct_past_raw.split(',')]
        if user_past.lower() in [c.lower() for c in correct_pasts] and user_past != '':
            df_correction.loc[i, 'Correction Past'] = '✅'
            nouveaux_points += MAX_POINTS_PAR_CELLULE
        else:
            df_correction.loc[i, 'Correction Past'] = f"❌ {correct_past_raw}"
            st.session_state.df_quiz_saisie.at[i, 'Simple Past'] = correct_past_raw

    # Mettre à jour le score et marquer le quiz comme terminé (une seule tentative)
    st.session_state.score_total += nouveaux_points
    st.session_state.df_correction_display = df_correction.copy()
    st.session_state.quiz_termine = True

def executer_quiz_saisie():
    initialiser_session_saisie()
    
    st.title("✍️ Exercice de Saisie : Verbes Irréguliers")
    st.markdown("---")

    if st.session_state.quiz_termine:
        st.balloons()
        st.success(f"🎉 **Félicitations !** Vous avez complété tous les verbes. Score final : **{st.session_state.score_total}** points.")
        st.markdown("---")
        st.markdown("### Contrôles de l'Exercice")
        cols = st.columns([1, 2])
        with cols[0]:
            if st.button("Reconfigurer"):
                st.session_state.started = False
                # le rerun est implicite après le clic sur le bouton
            
        with cols[1]:
            if st.button("Réinitialiser le Quiz Actuel"):
                reinitialiser_session()
                # le rerun est implicite après le clic sur le bouton
        
        if st.button("Commencer un nouveau quiz de Saisie"):
            reinitialiser_session()
        return

    st.markdown("Veuillez saisir la **Base Form** et le **Simple Past** des verbes ci-dessous.")
    
    df_display = st.session_state.df_quiz_saisie[['Verbe Français', 'Base Form', 'Simple Past']].copy()

    with st.form("quiz_form_saisie"):
        
        edited_df_form = st.data_editor(
            df_display,
            key="data_editor_form_saisie",
            hide_index=True,
            column_config={
                "Verbe Français": st.column_config.Column(disabled=True)
            },
            height=37 + 35 * NB_VERBES_SAISIE 
        )

        submitted = st.form_submit_button("Vérifier les réponses")

    if submitted:
        verifier_et_generer_correction_saisie(edited_df_form)
        
        if st.session_state.quiz_termine:
            # Le rerun est implicite après la soumission du formulaire
            pass
        else:
            if st.session_state.nb_erreurs > 0:
                st.warning(f"⚠️ Il reste **{st.session_state.nb_erreurs} erreurs** ou réponses manquantes (❔). Corrigez dans le tableau ci-dessus et vérifiez à nouveau.")
            else:
                 st.info("👍 Aucune nouvelle erreur n'a été trouvée. Continuez de corriger les champs manquants.")
            # Le rerun est implicite après la soumission du formulaire

    if st.session_state.df_correction_display is not None:
        st.markdown("---")
        st.subheader("Tableau de Correction")
        
        def color_correction(s):
            if s == '✅':
                return ['background-color: #d4edda; color: #155724'] * len(s)
            elif '❌' in s:
                return ['background-color: #f8d7da; color: #721c24'] * len(s)
            elif '❔' in s:
                return ['background-color: #fff3cd; color: #856404'] * len(s)
            return [''] * len(s)

        styled_df_correction = st.session_state.df_correction_display.style.applymap(
            lambda x: color_correction(x)[0], subset=pd.IndexSlice[:, ['Correction Base', 'Correction Past']]
        )
        
        st.dataframe(
            styled_df_correction, 
            hide_index=True, 
            use_container_width=True
        )

# --- 4. Fonction Principale (Menu de Sélection) ---

def menu_principal():
    st.set_page_config(
        page_title="Le Maître des Verbes Irréguliers (Fusion)",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Controls moved from sidebar into the main page for simpler management
    options = [f"{v['id']}: {v['base']} — {v['fr']}" for v in VERBES]

    # Ensure we have a 'started' flag in session state
    if 'started' not in st.session_state:
        st.session_state.started = False
    
    # NOTE: le mode sera déterminé APRÈS l'affichage des contrôles ci-dessous,
    # afin que les clics sur les boutons "Démarrer QCM/Saisie" soient pris en compte
    # (les boutons écrivent dans `st.session_state.selected_mode` durant la même passe).

    # If not started, show full configuration UI; once started, hide it
    if not st.session_state.started:
        st.title("🧠 Le Maître des Verbes Irréguliers")
        st.markdown("## Configuration de l'Exercice")
        st.markdown("---")

        controls_col, info_col = st.columns([1, 2])

        with controls_col:
            st.markdown("### Choisir les verbes (optionnel)")
            selected_labels = st.multiselect(
                "Cochez les verbes à inclure (laisser vide = aléatoire)",
                options,
                key='verbs_selected_labels'
            )

            # Boutons pratiques pour tout sélectionner / effacer
            def _set_labels_by_range(start, end):
                st.session_state['verbs_selected_labels'] = [opt for opt in options if int(opt.split(":")[0]) in range(start, end + 1)]

            def _select_all():
                st.session_state['verbs_selected_labels'] = options

            def _clear_selection():
                st.session_state['verbs_selected_labels'] = []
                st.session_state['selected_verbes'] = None

            cols_range = st.columns([1,1,1])
            with cols_range[0]:
                st.button("Sélection 1-35", on_click=_set_labels_by_range, args=(1, 35))
            with cols_range[1]:
                st.button("Sélection 36-70", on_click=_set_labels_by_range, args=(36, 70))
            with cols_range[2]:
                st.button("Sélection 71-100", on_click=_set_labels_by_range, args=(71, 100))

            cols_select = st.columns([1,1])
            with cols_select[0]:
                st.button("Tout sélectionner", on_click=_select_all)
            with cols_select[1]:
                st.button("Effacer la sélection", on_click=_clear_selection)

            # Mettre à jour `selected_verbes` (liste de dicts) utilisable par les initialisateurs
            if 'verbs_selected_labels' in st.session_state and st.session_state.verbs_selected_labels:
                try:
                    selected_ids = [int(s.split(":")[0]) for s in st.session_state.verbs_selected_labels]
                    st.session_state.selected_verbes = [v for v in VERBES if v['id'] in selected_ids]
                except Exception:
                    st.session_state.selected_verbes = None
            elif 'selected_verbes' not in st.session_state:
                st.session_state.selected_verbes = None

            st.markdown("---")
            st.markdown("### Choisissez le mode d'exercice")
            cols_mode = st.columns([1, 1, 1])
            with cols_mode[0]:
                if st.button("QCM"):
                    st.session_state.selected_mode = "1. QCM (Choix de Réponse - 15 verbes)"
                    st.session_state.started = True
            with cols_mode[1]:
                if st.button("Saisie"):
                    st.session_state.selected_mode = "2. Saisie de Texte (Tableau - 10 verbes)"
                    st.session_state.started = True



    # Déterminer le mode EFFECTIF après le rendu des contrôles ci-dessus
    mode = st.session_state.get('selected_mode', st.session_state.get('mode_selectionne', "Sélectionner un mode"))

    # --- Lancement du Quiz ---
    if st.session_state.started:
        if mode == "1. QCM (Choix de Réponse - 15 verbes)":
            executer_quiz_qcm()
        elif mode == "2. Saisie de Texte (Tableau - 10 verbes)":
            executer_quiz_saisie()
        elif mode == "Sélectionner un mode":
            st.warning("Veuillez choisir un mode d'exercice pour commencer.")

if __name__ == '__main__':
    menu_principal()