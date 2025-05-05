import frappe
import pymysql
import csv
import io
from frappe.utils.data import getdate
from frappe import _

@frappe.whitelist()
def effacer_donnees():
    modules_cibles = ["produitmodule"]
    nb_total_supprimes = 0
    summary = []

    for module in modules_cibles:
        doctypes = frappe.get_all("DocType",
            filters={"module": module}, pluck="name")

        for doctype in doctypes:
            meta = frappe.get_meta(doctype)
            if meta.issingle:
                continue

            # Crée un nouveau curseur PyMySQL
            conn = frappe.db.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Exécute le DELETE
            cursor.execute(f"DELETE FROM `tab{doctype}`")
            deleted_count = cursor.rowcount

            # Commit & close
            conn.commit()
            cursor.close()

            nb_total_supprimes += deleted_count
            summary.append(f"{doctype}: {deleted_count} supprimé(s)")

    return {
        "message": f"{nb_total_supprimes} enregistrements supprimés au total.",
        "details": summary
    }


@frappe.whitelist()
def upload_csv():
    files = frappe.request.files
    csv_file = files.get('csv1')

    if not csv_file:
        frappe.throw(_("Fichier CSV manquant."))

    file_content = csv_file.stream.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file_content))

    personnes = []
    personnes_uniques = set()
    maisons_set = set()
    erreurs = []

    ligne_index = 1

    for row in reader:
        ligne_index += 1
        nom = row.get('nom', '').strip()
        prenom = row.get('prenom', '').strip()
        date_naissance_str = row.get('date_naissance', '').strip()
        maison_adresse = row.get('maison_adresse', '').strip()

        # Vérifie si tous les champs sont remplis
        if not all([nom, prenom, date_naissance_str, maison_adresse]):
            erreurs.append(f"Ligne {ligne_index}: Champ manquant.")
            continue

        # Vérifie que la date est valide
        try:
            date_naissance = getdate(date_naissance_str)
        except Exception:
            erreurs.append(f"Ligne {ligne_index}: Date invalide: {date_naissance_str}")
            continue

        # Détection de doublon dans le tableau
        cle_personne = (nom, prenom, str(date_naissance))
        if cle_personne in personnes_uniques:
            erreurs.append(f"Ligne {ligne_index}: Doublon détecté: {nom} {prenom} ({date_naissance})")
            continue

        personnes_uniques.add(cle_personne)
        personnes.append({
            'nom': nom,
            'prenom': prenom,
            'date_naissance': date_naissance,
            'maison_adresse': maison_adresse
        })

        maisons_set.add(maison_adresse)

    if erreurs:
        return {
            "message": "Import échoué ❌",
            "erreurs": erreurs
        }

    # Création des Maisons
    maison_map = {}
    for adresse in maisons_set:
        maison_doc = frappe.get_doc({
            "doctype": "Maison",
            "adresse": adresse
        })
        maison_doc.insert(ignore_permissions=True)
        maison_map[adresse] = maison_doc.name

    # Création des Personnes
    for p in personnes:
        personne_doc = frappe.get_doc({
            "doctype": "Personne",
            "nom": p['nom'],
            "prenom": p['prenom'],
            "date_naissance": p['date_naissance'],
            "adresse": maison_map[p['maison_adresse']]
        })
        personne_doc.insert(ignore_permissions=True)

    return {
        "message": _("Import réussi ✅"),
        "personnes_inserées": len(personnes),
        "maisons_inserées": len(maisons_set)
    }