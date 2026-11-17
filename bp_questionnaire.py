#!/usr/bin/env python3
"""
Questionnaire de suivi de tension artérielle
Détermine le seuil cible et le nombre de prises recommandées par jour
selon le profil de risque du patient.
"""


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (oui/non) : ").strip().lower()
        if answer in ("oui", "o", "yes", "y"):
            return True
        if answer in ("non", "n", "no"):
            return False
        print("  → Répondez par 'oui' ou 'non'.")


def ask_choice(prompt: str, options: dict) -> str:
    print(f"\n{prompt}")
    for key, label in options.items():
        print(f"  {key}. {label}")
    while True:
        choice = input("Votre choix : ").strip()
        if choice in options:
            return choice
        print(f"  → Choisissez parmi : {', '.join(options.keys())}")


def ask_int(prompt: str, min_val: int = 0, max_val: int = 150) -> int:
    while True:
        try:
            value = int(input(f"{prompt} : ").strip())
            if min_val <= value <= max_val:
                return value
            print(f"  → Entrez un nombre entre {min_val} et {max_val}.")
        except ValueError:
            print("  → Entrez un nombre entier.")


def ask_float(prompt: str, min_val: float = 0.0, max_val: float = 300.0) -> float:
    while True:
        try:
            value = float(input(f"{prompt} : ").strip().replace(",", "."))
            if min_val <= value <= max_val:
                return value
            print(f"  → Entrez un nombre entre {min_val} et {max_val}.")
        except ValueError:
            print("  → Entrez un nombre (ex: 70.5).")


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def bmi_category(bmi: float) -> tuple[str, float]:
    if bmi < 18.5:
        return "Insuffisance pondérale", 1.0
    if bmi < 25:
        return "Poids santé", 0.0
    if bmi < 30:
        return "Surpoids", 1.4
    if bmi < 35:
        return "Obésité classe 1", 2.0
    if bmi < 40:
        return "Obésité classe 2", 2.3
    return "Obésité classe 3", 2.6


def main():
    print("=" * 60)
    print("  QUESTIONNAIRE – SEUIL ET FRÉQUENCE DE MESURE DE TENSION")
    print("=" * 60)
    print("Répondez aux questions. À la fin vous obtiendrez votre seuil")
    print("cible et le nombre de prises recommandées par jour.\n")

    # ------------------------------------------------------------------
    # 1. Sexe et âge
    # ------------------------------------------------------------------
    sexe = ask_choice("Quelle est votre sexe ?", {
        "1": "Homme",
        "2": "Femme"
    })
    is_woman = sexe == "2"

    age = ask_int("Quel est votre âge (en années)", 18, 120)

    # Score d'âge (facteur de risque)
    if age < 30:
        age_score = 0.0
    elif age <= 49:
        age_score = 0.5
    elif age <= 64:
        age_score = 1.0
    elif age <= 74:
        age_score = 1.3
    else:
        age_score = 1.5

    if is_woman:
        if age <= 34:
            age_score_f = 0.3
        elif age <= 49:
            age_score_f = 0.3
        elif age <= 64:
            age_score_f = 1.3
        elif age <= 74:
            age_score_f = 1.5
        else:
            age_score_f = 1.8
        age_score = age_score_f

    # ------------------------------------------------------------------
    # 2. Grossesse / post-partum (femmes uniquement)
    # ------------------------------------------------------------------
    is_pregnant = False
    if is_woman:
        is_pregnant = ask_yes_no("Êtes-vous enceinte ou en post-partum ?")

    # ------------------------------------------------------------------
    # 3. Antécédents médicaux
    # ------------------------------------------------------------------
    print("\n--- Antécédents médicaux ---")
    has_cvd = ask_yes_no("Avez-vous une maladie cardiovasculaire (infarctus, AVC, insuffisance cardiaque, etc.) ?")
    has_diabetes = ask_yes_no("Avez-vous un diabète ?")
    has_ckd = ask_yes_no("Avez-vous une maladie rénale chronique (MRC) ?")
    has_high_cv_risk = ask_yes_no("Avez-vous un risque élevé de maladie cardiovasculaire (selon votre médecin) ?")

    # Compteur de facteurs de risque majeurs
    # (grossesse, maladie CV, diabète, MRC, risque élevé) + 1 si âge ≥ 65
    major_factors = 0
    if is_pregnant:
        major_factors += 1
    if has_cvd:
        major_factors += 1
    if has_diabetes:
        major_factors += 1
    if has_ckd:
        major_factors += 1
    if has_high_cv_risk:
        major_factors += 1
    if age >= 65:
        major_factors += 1

    # ------------------------------------------------------------------
    # 4. Habitudes de vie (facteurs secondaires – influence limitée)
    # ------------------------------------------------------------------
    print("\n--- Habitudes de vie ---")

    salt = ask_choice("Consommez-vous des aliments riches en sel ?", {
        "1": "Souvent",
        "2": "Parfois",
        "3": "Jamais"
    })
    salt_score = {"1": 1.5, "2": 1.3, "3": 1.0}[salt]

    activity = ask_choice("Faites-vous de l'activité physique ?", {
        "1": "Jamais",
        "2": "Parfois",
        "3": "2 fois par semaine",
        "4": "3+ fois par semaine"
    })
    activity_score = {"1": 1.3, "2": 1.1, "3": 0.7, "4": 0.5}[activity]

    veggies = ask_choice("Combien de portions de légumes consommez-vous ?", {
        "1": "4+ par jour",
        "2": "2-3 par jour",
        "3": "1 ou moins par jour"
    })
    veggies_score = {"1": 1.0, "2": 1.05, "3": 1.15}[veggies]

    fatty_meat = ask_choice("Mangez-vous de la viande grasse ?", {
        "1": "Moins d'1 fois par semaine",
        "2": "1-2 fois par semaine",
        "3": "3+ fois par semaine"
    })
    fatty_meat_score = {"1": 1.0, "2": 1.05, "3": 1.15}[fatty_meat]

    smoking = ask_choice("Fumez-vous ou vapotez-vous ?", {
        "1": "Oui",
        "2": "Parfois / Ex-fumeur",
        "3": "Non"
    })
    smoking_score = {"1": 1.5, "2": 1.0, "3": 0.0}[smoking]

    stress = ask_choice("Comment décrivez-vous votre niveau de stress ?", {
        "1": "Faible",
        "2": "Modéré",
        "3": "Élevé"
    })
    stress_score = {"1": 0.5, "2": 1.0, "3": 1.5}[stress]

    sleep = ask_choice("Combien d'heures dormez-vous en moyenne par nuit ?", {
        "1": "Moins de 5 h",
        "2": "5 à 6 heures",
        "3": "7 à 9 heures",
        "4": "Plus de 9 heures"
    })
    sleep_score = {"1": 2.0, "2": 1.5, "3": 0.0, "4": 0.5}[sleep]

    sedentary = ask_choice("Combien d'heures restez-vous assis pendant une journée ?", {
        "1": "Moins de 4 h",
        "2": "4 à 8 h",
        "3": "Plus de 8 h"
    })
    sedentary_score = {"1": 0.0, "2": 0.5, "3": 1.5}[sedentary]

    # ------------------------------------------------------------------
    # 5. IMC
    # ------------------------------------------------------------------
    print("\n--- Calcul de l'IMC ---")
    height = ask_float("Quelle est votre taille (en cm)", 100, 250)
    weight = ask_float("Quel est votre poids (en kg)", 30, 300)
    bmi = calculate_bmi(weight, height)
    bmi_label, bmi_score = bmi_category(bmi)
    print(f"  → Votre IMC est de {bmi:.1f} ({bmi_label})")

    # ------------------------------------------------------------------
    # 6. Antécédents familiaux d'hypertension
    # ------------------------------------------------------------------
    print("\n--- Antécédents familiaux ---")
    family = ask_choice(
        "Parmi vos parents proches (mère, père, frères, sœurs), y a-t-il des personnes qui ont ou ont eu de l'hypertension ?",
        {
            "1": "Aucun",
            "2": "Un parent proche",
            "3": "2 parents proches ou plus",
            "4": "Je ne sais pas"
        }
    )
    family_score = {"1": 0.0, "2": 1.5, "3": 2.0, "4": 1.0}[family]

    # ------------------------------------------------------------------
    # 7. Consommation d'alcool
    # ------------------------------------------------------------------
    alcohol = ask_choice("Combien d'alcool consommez-vous ?", {
        "1": "Aucun",
        "2": "1-2 verres par semaine",
        "3": "3-6 verres par semaine",
        "4": "7-14 verres par semaine",
        "5": "14+ verres par semaine"
    })
    alcohol_score = {"1": 0.0, "2": 1.0, "3": 1.1, "4": 1.3, "5": 1.5}[alcohol]

    # ------------------------------------------------------------------
    # Détermination du seuil et de la fréquence
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  RÉSULTAT")
    print("=" * 60)

    seuil = ""
    prises = ""
    profil = 0

    # ----- Règles prioritaires (selon les tableaux fournis) -----

    # 1-3 : Enceinte ≥ 35 ans
    if is_pregnant and age >= 35:
        if major_factors <= 1:  # grossesse seule
            seuil = "Discrétion du médecin"
            prises = "1 prise par 2 jours"
            profil = 1
        elif major_factors == 2:  # grossesse + 1 autre facteur
            seuil = "Discrétion du médecin"
            prises = "2 par jour"
            profil = 2
        else:  # grossesse + 2 facteurs ou plus
            seuil = "Discrétion du médecin"
            prises = "3 par jour"
            profil = 3

    # 4-5 : Maladie CV + diabète
    elif has_cvd and has_diabetes:
        if major_factors <= 2:  # seulement CV + diabète
            seuil = "Discrétion du médecin"
            prises = "2 par jour"
            profil = 4
        else:
            seuil = "Discrétion du médecin"
            prises = "3 par jour"
            profil = 5

    # 6-7 : Diabétique ≥ 75 ans (sans maladie CV)
    elif has_diabetes and age >= 75 and not has_cvd:
        if major_factors <= 2:  # diabète + âge
            seuil = "Discrétion du médecin"
            prises = "2 par jour"
            profil = 6
        else:
            seuil = "Discrétion du médecin"
            prises = "3 par jour"
            profil = 7

    # 8-9 : Maladie CV ≥ 75 ans (sans diabète)
    elif has_cvd and age >= 75 and not has_diabetes:
        if major_factors <= 2:
            seuil = "Discrétion du médecin"
            prises = "2 par jour"
            profil = 8
        else:
            seuil = "Discrétion du médecin"
            prises = "3 par jour"
            profil = 9

    # 10-12 : Enceinte ≤ 34 ans
    elif is_pregnant and age <= 34:
        if major_factors <= 1:
            seuil = "diastolique < 85 mmHg"
            prises = "1 prise par 2 jours"
            profil = 10
        elif major_factors == 2:
            seuil = "diastolique < 85 mmHg"
            prises = "2 par jour"
            profil = 11
        else:
            seuil = "diastolique < 85 mmHg"
            prises = "3 par jour"
            profil = 12

    # 13-15 : Diabète seul, < 75 ans, sans maladie CV
    elif has_diabetes and age < 75 and not has_cvd:
        extra = 0
        if has_ckd:
            extra += 1
        if has_high_cv_risk:
            extra += 1
        if 65 <= age <= 74:
            extra += 1

        if extra == 0:
            seuil = "< 130/80 mmHg"
            prises = "1 prise par 2 jours"
            profil = 13
        elif extra == 1:
            seuil = "< 130/80 mmHg"
            prises = "2 par jour"
            profil = 14
        else:
            seuil = "< 130/80 mmHg"
            prises = "3 par jour"
            profil = 15

    # 16-18 : Maladie CV seule, < 75 ans, sans diabète
    elif has_cvd and age < 75 and not has_diabetes:
        extra = 0
        if has_ckd:
            extra += 1
        if has_high_cv_risk:
            extra += 1
        if 65 <= age <= 74:
            extra += 1

        if extra == 0:
            seuil = "< 140/90 mmHg"
            prises = "1 prise par 2 jours"
            profil = 16
        elif extra == 1:
            seuil = "< 140/90 mmHg"
            prises = "2 par jour"
            profil = 17
        else:
            seuil = "< 140/90 mmHg"
            prises = "3 par jour"
            profil = 18

    # 19-21 : MRC seule, 51-74 ans, sans CV ni diabète ni grossesse
    # (CORRECTION : "age < 75" ajouté pour que les 75 ans et plus avec MRC
    #  passent aux règles 24-26 au lieu de tomber ici)
    elif has_ckd and 50 < age < 75 and not has_cvd and not has_diabetes and not is_pregnant:
        extra = 0
        if has_high_cv_risk:
            extra += 1
        if 65 <= age <= 74:
            extra += 1

        if extra == 0 and age <= 64:
            seuil = "< 140/90 mmHg"
            prises = "1 prise par 2 jours"
            profil = 19
        elif extra == 1:
            seuil = "< 140/90 mmHg"
            prises = "2 par jour"
            profil = 20
        else:
            seuil = "< 140/90 mmHg"
            prises = "3 par jour"
            profil = 21

    # 22-26 : 61 ans et plus, sans CV, diabète ni grossesse
    elif age >= 61 and not has_cvd and not has_diabetes and not is_pregnant:
        if age <= 64 or (65 <= age <= 74 and not has_high_cv_risk):
            seuil = "< 140/90 mmHg"
            prises = "1 prise par 2 jours"
            profil = 22
        elif 65 <= age <= 74 and has_high_cv_risk:
            seuil = "< 140/90 mmHg"
            prises = "2 par jour"
            profil = 23
        else:
            # 75+ sans CV ni diabète
            if has_ckd and has_high_cv_risk:
                seuil = "systolique < 120 mmHg"
                prises = "3 par jour"
                profil = 26
            elif has_ckd or has_high_cv_risk:
                seuil = "systolique < 120 mmHg"
                prises = "2 par jour"
                profil = 25
            else:
                seuil = "systolique < 120 mmHg"
                prises = "1 prise par 2 jours"
                profil = 24

    # 27-28 : Cas par défaut (≤ 60 ans ou aucune règle)
    else:
        extra = 0
        if has_high_cv_risk:
            extra += 1
        if has_ckd and age <= 50:
            extra += 1

        if extra <= 1:
            seuil = "140/90 mmHg (à confirmer par le médecin)"
            prises = "1 prise par 2 jours"
            profil = 27
        else:
            seuil = "140/90 mmHg (à confirmer par le médecin)"
            prises = "2 par jour"
            profil = 28

    # ------------------------------------------------------------------
    # Affichage final
    # ------------------------------------------------------------------
    print(f"\nProfil n° {profil}")
    print(f"Nombre de facteurs de risque majeurs : {major_factors}")
    print(f"IMC : {bmi:.1f} ({bmi_label})")
    print()
    print(f"▶ SEUIL CIBLE : {seuil}")
    print(f"▶ PRISES RECOMMANDÉES : {prises}")
    print()
    print("Note : Ce questionnaire est un outil d'aide à la décision.")
    print("Le seuil final et la fréquence doivent être confirmés par votre médecin.")
    print("=" * 60)


if __name__ == "__main__":
    main()
