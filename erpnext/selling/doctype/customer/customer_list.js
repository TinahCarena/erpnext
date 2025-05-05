frappe.listview_settings["Customer"] = {
	add_fields: ["customer_name", "territory", "customer_group", "customer_type", "image"],

	// Bouton en haut
	onload: function (listview) {
		listview.page.add_inner_button(__('Exporter tout'), function () {
			frappe.call({
				method: "frappe.desk.reportview.export_query",
				args: {
					doctype: "Customer",
					file_format_type: "Excel",
					with_data: true
				},
				callback: function () {
					frappe.msgprint("Export Excel lancé !");
				}
			});
		});
	},
};
