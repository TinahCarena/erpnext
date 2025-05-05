import frappe

@frappe.whitelist()
def reset_data():
    # Original method (unchanged)
    return "Data reset successfully"

@frappe.whitelist()
def reset_doctypes_data(doctypes, filters=None):
    """
    Delete all records from the specified DocTypes.
    
    Args:
        doctypes (str): JSON-encoded list of DocType names (e.g., '["ToDo", "Note"]').
        filters (str, optional): JSON-encoded filters for specific records (e.g., '[["ToDo", "status", "=", "Open"]]').
    
    Returns:
        str: Success message indicating the number of records deleted.
    """
    try:
        # Parse doctypes from JSON string (since frappe.call sends JSON strings)
        doctypes = frappe.parse_json(doctypes) if isinstance(doctypes, str) else doctypes
        filters = frappe.parse_json(filters) if filters and isinstance(filters, str) else filters

        if not doctypes or not isinstance(doctypes, list):
            frappe.throw("Please provide a valid list of DocTypes.")

        deleted_count = 0
        for doctype in doctypes:
            # Verify that the DocType exists
            if not frappe.db.exists("DocType", doctype):
                frappe.throw(f"DocType {doctype} does not exist.")

            # Check user permissions for deletion
            if not frappe.has_permission(doctype, "delete"):
                frappe.throw(f"You do not have permission to delete {doctype} records.")

            # Build query to fetch records
            query = frappe.get_all(doctype, fields=["name"], filters=filters)

            # Delete each record
            for record in query:
                frappe.delete_doc(doctype, record.name, ignore_missing=True)
                deleted_count += 1

            # Commit changes to the database
            frappe.db.commit()

        return f"Successfully deleted {deleted_count} record(s) from {len(doctypes)} DocType(s)."

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error resetting DocTypes data: {str(e)}")
        frappe.throw(f"Failed to reset data: {str(e)}")