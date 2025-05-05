frappe.pages['reset'].on_page_load = function (wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Reset Data',
        single_column: true
    });

    $(page.body).html(`
        <div class="reset-form shadow-sm p-4 bg-white rounded" style="max-width: 500px; margin: 40px auto;">
            <h4 class="mb-4">Reset Data</h4>
            <div class="form-group mb-3">
                <label class="form-label">Tables <small class="text-muted">(séparés par des virgules)</small></label>
                <input type="text" class="form-control" id="reset-table-names" placeholder="ex: Sales Invoice, Customer" />
            </div>
            <button class="btn btn-outline-primary w-100" id="reset-delete-btn">
                Delete
            </button>
        </div>
    `);

    // Action du bouton
    $('#reset-delete-btn').on('click', function () {
        let tables = $('#reset-table-names').val().split(',').map(t => t.trim()).filter(Boolean);

        if (tables.length === 0) {
            frappe.msgprint(__('Veuillez spécifier au moins une table.'));
            return;
        }

        frappe.confirm(
            `Êtes-vous sûr de vouloir supprimer toutes les données de : <b>${tables.join(', ')}</b> ?`,
            function () {
                tables.forEach((table) => {
                    frappe.call({
                        method: 'frappe.desk.doctype.bulk_update.bulk_update.delete_documents',
                        args: { doctype: table },
                        callback: function () {
                            frappe.show_alert({ message: `Données supprimées pour ${table}`, indicator: 'blue' });
                        }
                    });
                });
            }
        );
    });
};
