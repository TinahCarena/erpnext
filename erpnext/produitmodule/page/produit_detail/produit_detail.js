frappe.pages['produit_detail'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'produits',
		single_column: true
	});
}