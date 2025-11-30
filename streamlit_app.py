import streamlit as st
import random
import pandas as pd

# --- 1. Définition des données des verbes irréguliers ---

VERBES = [
    {"base": "fly", "past": "flew", "fr": "voler"},
    {"base": "forbid", "past": "forbade", "fr": "interdire"},
    {"base": "forget", "past": "forgot", "fr": "oublier"},
    {"base": "forgive", "past": "forgave", "fr": "pardonner"},
    {"base": "freeze", "past": "froze", "fr": "geler"},
    {"base": "get", "past": "got", "fr": "recevoir, obtenir"},
    {"base": "give", "past": "gave", "fr": "donner"},
    {"base": "go", "past": "went", "fr": "aller"},
    {"base": "grow", "past": "grew", "fr": "grandir"},
    {"base": "hang", "past": "hung", "fr": "suspendre"},
    {"base": "have", "past": "had", "fr": "avoir"},
    {"base": "hear", "past": "heard", "fr": "entendre"},
    {"base": "hide", "past": "hid", "fr": "cacher"},
    {"base": "hit", "past": "hit", "fr": "frapper"},
    {"base": "hold", "past": "held", "fr": "tenir"},
    {"base": "hurt", "past": "hurt", "fr": "blesser"},
    {"base": "keep", "past": "kept", "fr": "garder"},
    {"base": "know", "past": "knew", "fr": "connaître"},
    {"base": "lay", "past": "laid", "fr": "poser, coucher"},
    {"base": "lead", "past": "led", "fr": "mener, diriger"},
    {"base": "leave", "past": "left", "fr": "partir"},
    {"base": "lend", "past": "lent", "fr": "prêter"},
    {"base": "let", "past": "let", "fr": "laisser"},
    {"base": "lie", "past": "lay", "fr": "s'allonger, s'étendre"},
    {"base": "light", "past": "lit", "fr": "allumer"},
    {"base": "lose", "past": "lost", "fr": "perdre"},
    {"base": "make", "past": "made", "fr": "fabriquer"},
    {"base": "mean", "past": "meant", "fr": "signifier"},
    {"base": "meet", "past": "met", "fr": "rencontrer"},
    {"base": "pay", "past": "paid", "fr": "payer"},
    {"base": "put", "past": "put", "fr": "mettre"},
    {"base": "quit", "past": "quit", "fr": "abandonner"},
    {"base": "read", "past": "read", "fr": "lire"},
    {"base": "ride", "past": "rode", "fr": "aller à, se promener à"},
    {"base": "ring", "past": "rang", "fr": "sonner"},
]

NB_QUESTIONS_QCM = 15 # Nombre de verbes pour le mode QCM
NB_VERBES_SAISIE = 10 # Nombre de verbes pour le mode Saisie
MAX_POINTS_PAR_CELLULE = 5 # Points de base pour le mode Saisie

# --- Fonctions Générales (Réinitialisation, Points) ---

def reinitialiser_session():
    """Supprime toutes les variables d'état pour recommencer."""
    for key in list(st.session_state.keys()):
        # Conserver la sélection du mode si elle existe
        if key not in ['mode_selectionne']:
            del st.session_state[key]
    st.session_state.quiz_fini = False
    st.session_state.score_total = 0
    st.rerun()

def calculer_points(tentatives, max_points):
    """Calcule le score basé sur le nombre de tentatives."""
    return max(0, max_points - tentatives)

# --- LOGIQUE QCM (Version 1) ---

def initialiser_session_qcm():
    """Initialise les variables d'état nécessaires au jeu QCM."""
    if 'score_qcm' not in st.session_state: st.session_state.score_qcm = 0
    if 'question_actuelle' not in st.session_state: st.session_state.question_actuelle = 0
    if 'quiz_fini' not in st.session_state: st.session_state.quiz_fini = False
    if 'sequence_questions' not in st.session_state:
        st.session_state.sequence_questions = random.sample(VERBES, NB_QUESTIONS_QCM)
    if 'current_verb_data' not in st.session_state: st.session_state.current_verb_data = None
    if 'phase' not in st.session_state: st.session_state.phase = 'base_form'
    if 'tentatives_base' not in st.session_state: st.session_state.tentatives_base = 0
    if 'tentatives_past' not in st.session_state: st.session_state.tentatives_past = 0
    if 'choices_base' not in st.session_state: st.session_state.choices_base = []
    if 'choices_past' not in st.session_state: st.session_state.choices_past = []
    if 'base_correcte' not in st.session_state: st.session_state.base_correcte = False

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
    distracteurs = set()
    distracteurs.add(verbe_base) 
    autres_pasts = [v['past'] for v in VERBES if v['past'] != verbe_past]
    random.shuffle(autres_pasts)
    nombre_de_distracteurs_a_ajouter = nombre - 1
    for past_form in autres_pasts:
        if past_form not in distracteurs and len(distracteurs) < nombre_de_distracteurs_a_ajouter:
            distracteurs.add(past_form)
        if len(distracteurs) == nombre_de_distracteurs_a_ajouter: break
    choix_list = list(distracteurs)
    if verbe_past not in choix_list: choix_list.append(verbe_past)
    random.shuffle(choix_list)
    return choix_list

def passer_a_la_question_suivante_qcm():
    st.session_state.question_actuelle += 1
    st.session_state.phase = 'base_form'
    st.session_state.tentatives_base = 0
    st.session_state.tentatives_past = 0
    st.session_state.current_verb_data = None
    st.session_state.base_correcte = False 
    if st.session_state.question_actuelle >= NB_QUESTIONS_QCM:
        st.session_state.quiz_fini = True
    st.rerun()

def transition_vers_simple_past_qcm():
    st.session_state.phase = 'simple_past'

def verifier_reponse_qcm(reponse_utilisateur, bonne_reponse, type_question):
    if reponse_utilisateur == bonne_reponse:
        st.success("🎉 **Bonne réponse !**")
        
        points = calculer_points(st.session_state.tentatives_base if type_question == 'base_form' else st.session_state.tentatives_past, 3)
        st.session_state.score_qcm += points
        
        if type_question == 'base_form':
            st.session_state.base_correcte = True
        else:
            st.button("✅ Question suivante", on_click=passer_a_la_question_suivante_qcm)

        st.info(f"Vous avez gagné **{points} points** pour cette étape. Score total : **{st.session_state.score_qcm}**")
        st.session_state.choices_base = [] 
        st.session_state.choices_past = [] 
        
    else:
        st.warning("❌ **Mauvaise réponse.** Essayez encore !")
        if type_question == 'base_form':
            st.session_state.tentatives_base += 1
            st.session_state.choices_base.remove(reponse_utilisateur)
        else:
            st.session_state.tentatives_past += 1
            st.session_state.choices_past.remove(reponse_utilisateur)
        st.rerun() 

def executer_quiz_qcm():
    initialiser_session_qcm()
    
    st.title("🧠 Le Maître des Verbes Irréguliers")
    
    col_score, col_progress = st.columns([1, 2])
    
    with col_score:
        st.metric(label="Score total", value=st.session_state.score_qcm)
    
    with col_progress:
        progress_val = (st.session_state.question_actuelle) / NB_QUESTIONS_QCM
        st.progress(progress_val, text=f"Progression : Question {st.session_state.question_actuelle + 1} / {NB_QUESTIONS_QCM}")
    
    st.markdown("---")
    
    if st.session_state.quiz_fini:
        st.balloons()
        st.header(f"🎉 Quiz Terminé ! Votre score final est de **{st.session_state.score_qcm}** points.")
        if st.button("Recommencer le Quiz QCM"):
            reinitialiser_session()
        return

    if st.session_state.current_verb_data is None:
        try:
            st.session_state.current_verb_data = st.session_state.sequence_questions[st.session_state.question_actuelle]
        except IndexError:
            st.session_state.quiz_fini = True
            st.rerun()
            return

    verbe = st.session_state.current_verb_data
    
    st.subheader(f"Question {st.session_state.question_actuelle + 1}")
    st.header(f"Verbe en français : **{verbe['fr']}**") 
    st.markdown("---")

    # --- Étape 1 : Deviner la BASE FORM ---
    if st.session_state.phase == 'base_form':
        st.subheader("1. Quelle est la **Base Form** ?")
        
        if not st.session_state.choices_base:
            st.session_state.choices_base = generer_choix_qcm('base')
        
        choices = st.session_state.choices_base
        
        cols = st.columns(len(choices))
        
        if not st.session_state.base_correcte:
            for i, choice in enumerate(choices):
                key = f"base_choice_{i}_{verbe['fr']}" 
                with cols[i]:
                    if st.button(f"{choice}", key=key, use_container_width=True):
                        verifier_reponse_qcm(choice, verbe['base'], 'base_form')
        
        if st.session_state.base_correcte:
            st.button("👉 Continuer vers le Simple Past", on_click=transition_vers_simple_past_qcm)


    # --- Étape 2 : Deviner le SIMPLE PAST ---
    elif st.session_state.phase == 'simple_past':
        
        st.subheader(f"Base Form : **{verbe['base']}**")
        st.subheader("2. Quel est le **Simple Past** (Prétérit) ?")
        
        if not st.session_state.choices_past:
            st.session_state.choices_past = generer_choix_past_intelligent_qcm(verbe['base'], verbe['past']) 
            
        choices = st.session_state.choices_past
        
        cols = st.columns(len(choices))
        
        for i, choice in enumerate(choices):
            key = f"past_choice_{i}_{verbe['fr']}"
            with cols[i]:
                if st.button(f"{choice}", key=key, use_container_width=True):
                    verifier_reponse_qcm(choice, verbe['past'], 'simple_past')

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
        st.session_state.quiz_data_saisie = random.sample(VERBES, NB_VERBES_SAISIE)
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
    
    erreurs_courantes = 0
    nouveaux_points = 0
    tout_est_correct = True
    
    for i in range(NB_VERBES_SAISIE):
        key_base = f'base_{i}'
        key_past = f'past_{i}'
        
        reponse_base = df_reponses_utilisateur.loc[i, 'Base Form'].strip().lower()
        correct_base = df_correct.loc[i, 'Base Form (Correct)'].strip().lower()
        reponse_past = df_reponses_utilisateur.loc[i, 'Simple Past'].strip().lower()
        correct_past = df_correct.loc[i, 'Simple Past (Correct)'].strip().lower()

        # --- LOGIQUE BASE FORM ---
        if st.session_state.tentatives_par_cellule[key_base] != -1: 
            if reponse_base == correct_base:
                nouveaux_points += calculer_points(st.session_state.tentatives_par_cellule[key_base], MAX_POINTS_PAR_CELLULE)
                st.session_state.tentatives_par_cellule[key_base] = -1 
                df_correction.loc[i, 'Correction Base'] = '✅'
            elif reponse_base != '':
                erreurs_courantes += 1
                st.session_state.tentatives_par_cellule[key_base] += 1
                df_correction.loc[i, 'Correction Base'] = f"❌ {df_correct.loc[i, 'Base Form (Correct)']}"
                tout_est_correct = False
            else:
                df_correction.loc[i, 'Correction Base'] = '❔'
                tout_est_correct = False
        else: 
            df_correction.loc[i, 'Correction Base'] = '✅'
            
        # --- LOGIQUE SIMPLE PAST ---
        if st.session_state.tentatives_par_cellule[key_past] != -1: 
            if reponse_past == correct_past:
                nouveaux_points += calculer_points(st.session_state.tentatives_par_cellule[key_past], MAX_POINTS_PAR_CELLULE)
                st.session_state.tentatives_par_cellule[key_past] = -1 
                df_correction.loc[i, 'Correction Past'] = '✅'
            elif reponse_past != '':
                erreurs_courantes += 1
                st.session_state.tentatives_par_cellule[key_past] += 1
                df_correction.loc[i, 'Correction Past'] = f"❌ {df_correct.loc[i, 'Simple Past (Correct)']}"
                tout_est_correct = False
            else:
                df_correction.loc[i, 'Correction Past'] = '❔'
                tout_est_correct = False
        else: 
            df_correction.loc[i, 'Correction Past'] = '✅'
            
    st.session_state.score_total += nouveaux_points
    st.session_state.nb_erreurs = erreurs_courantes
    st.session_state.quiz_termine = tout_est_correct
    st.session_state.df_correction_display = df_correction.copy()
    
    st.session_state.df_quiz_saisie.loc[:, 'Base Form'] = df_reponses_utilisateur['Base Form']
    st.session_state.df_quiz_saisie.loc[:, 'Simple Past'] = df_reponses_utilisateur['Simple Past']

def executer_quiz_saisie():
    initialiser_session_saisie()
    
    st.title("✍️ Exercice de Saisie : Verbes Irréguliers")
    st.header(f"Score actuel : **{st.session_state.score_total}** points")
    st.markdown("---")

    if st.session_state.quiz_termine:
        st.balloons()
        st.success(f"🎉 **Félicitations !** Vous avez complété tous les verbes. Score final : **{st.session_state.score_total}** points.")
        if st.button("Commencer un nouveau quiz de Saisie"):
            reinitialiser_session()
        return

    st.markdown("Veuillez saisir la **Base Form** et le **Simple Past** (Prétérit) des verbes ci-dessous.")
    st.markdown(f"*(**Max. {MAX_POINTS_PAR_CELLULE} points** par cellule pour la première tentative.)*")
    
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

        submitted = st.form_submit_button("Vérifier les réponses et mettre à jour le score")

    if submitted:
        verifier_et_generer_correction_saisie(edited_df_form)
        
        if st.session_state.quiz_termine:
            st.rerun()
        else:
            if st.session_state.nb_erreurs > 0:
                st.warning(f"⚠️ Il reste **{st.session_state.nb_erreurs} erreurs** ou réponses manquantes (❔). Corrigez dans le tableau ci-dessus et vérifiez à nouveau.")
            else:
                 st.info("👍 Aucune nouvelle erreur n'a été trouvée. Continuez de corriger les champs manquants.")
            st.rerun()

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
    
    st.sidebar.title("Configuration de l'Exercice")
    
    # 1. Sélection du Mode
    mode = st.sidebar.selectbox(
        "Choisissez le mode d'exercice :",
        ["Sélectionner un mode", "1. QCM (Choix de Réponse - 15 verbes)", "2. Saisie de Texte (Tableau - 10 verbes)"],
        key='mode_selectionne',
        index=0 if 'mode_selectionne' not in st.session_state or st.session_state.mode_selectionne == "Sélectionner un mode" else 
              (1 if st.session_state.mode_selectionne == "1. QCM (Choix de Réponse - 15 verbes)" else 2)
    )

    if st.sidebar.button("Redémarrer l'exercice"):
        reinitialiser_session()
        st.session_state.mode_selectionne = "Sélectionner un mode" # Réinitialise le selectbox
        st.rerun()

    st.sidebar.markdown("---")


    # 2. Exécution du Mode Sélectionné
    if mode == "1. QCM (Choix de Réponse - 15 verbes)":
        executer_quiz_qcm()
    elif mode == "2. Saisie de Texte (Tableau - 10 verbes)":
        executer_quiz_saisie()
    else:
        st.title("Bienvenue au Maître des verbes irréguliers !")
        st.markdown("Veuillez choisir un mode d'exercice dans le menu déroulant à gauche pour commencer :")
        st.markdown("* **Mode QCM :** Test rapide pour identifier la Base Form et le Simple Past parmi des choix multiples.")
        st.markdown("* **Mode Saisie :** Exercice de mémorisation où vous devez écrire les deux formes dans un tableau.")
        
if __name__ == '__main__':
    menu_principal()
