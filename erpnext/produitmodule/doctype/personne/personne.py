# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Personne(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		adresse: DF.Link | None
		date_naissance: DF.Date | None
		nom: DF.Data | None
		prenom: DF.Data | None
	# end: auto-generated types

	pass
