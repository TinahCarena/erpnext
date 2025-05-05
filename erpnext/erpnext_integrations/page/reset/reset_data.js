frappe.pages['reset_data'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Reset Data',
        single_column: true
    });

    $(page.body).html(`
		<div class="data-managment-container">
			<div style="margin-bottom: 15px;">
				<button class="btn btn-danger" id="effacer-btn">Effacer les données</button>
			</div>
			<form id="upload-form">
				<div class="form-group">
					<label>Fichier CSV 1</label>
					<input type="file" name="csv1" class="form-control" accept=".csv" required />
				</div>
				<div class="form-group">
					<label>Fichier CSV 2</label>
					<input type="file" name="csv2" class="form-control" accept=".csv" required />
				</div>
				<br>
				<button class="btn btn-primary" type="submit">Envoyer</button>
			</form>
		</div>
	`);

	// Effacer les données avec confirmation
	$('#effacer-btn').on('click', () => {
		frappe.confirm(
			'Cette action supprimera toutes les données du module sélectionné. Êtes-vous sûr ?',
			() => {
				// Si l'utilisateur confirme
				frappe.call({
					method: 'erpnext.testmodule.data_managment.effacer_donnees',
					callback: function(r) {
						const res = r.message;

						frappe.msgprint({
							title: __('Résultat de l\'effacement'),
							message: res.message + '<br><br>' + res.details.join('<br>'),
							indicator: 'green'
						});
					}
				});
			},
			() => {
				// Si l'utilisateur annule
				frappe.msgprint(__('Action annulée. Rien n’a été supprimé 👌'));
			}
		);
	});


	// Upload fichiers
	$('#upload-form').on('submit', function(e) {
		e.preventDefault();
		const formData = new FormData(this);
	
		$.ajax({
			url: '/api/method/erpnext.testmodule.data_managment.upload_csv',
			type: 'POST',
			data: formData,
			processData: false,
			contentType: false,
			headers: {
				'X-Frappe-CSRF-Token': frappe.csrf_token
			},
			success: function(response) {
				const res = response.message;

				if (res.erreurs) {
					frappe.msgprint({
						title: __('Erreur validation'),
						message: res.message + '<br><br>' + res.erreurs.join('<br>'),
						indicator: 'red'
					});
				} else {
					frappe.msgprint({
						title: "Succès",
						indicator: 'green',
						message: res.message + "<br>Personnes insérées: " + 
								res.personnes_inserées + "<br>Maisons insérées: " + 
								res.maisons_inserées
					} || "Upload réussi !");
				}
			},
			error: function(xhr) {
				frappe.msgprint("Erreur lors de l'envoi des fichiers: " + xhr.responseText);
				console.error(xhr.responseText);
			}
		});
	});
}