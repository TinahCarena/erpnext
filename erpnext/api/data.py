import frappe
from frappe import _

@frappe.whitelist()
def get_all_data():
    projects = frappe.get_all("Project", fields=["*"], limit=0)
    companies = frappe.get_all("Company", fields=["*"], limit=0)
    customers = frappe.get_all("Customer", fields=["*"], limit=0)
    suppliers = frappe.get_all("Supplier", fields=["*"], limit=0)
    
    items = frappe.get_all("Item", fields=["*"], limit=0)
    materialrequests = frappe.get_all("Material Request", fields=["*"], limit=0)
    brands = frappe.get_all("Brand", fields=["*"], limit=0)

    leads = frappe.get_all("Lead", fields=["*"], limit=0)

    purchaseorders = frappe.get_all("Purchase Order", fields=["*"], limit=0)
    purchaseordersitems = frappe.get_all("Purchase Order Item", fields=["*"], limit=0)
    
    dashboard = frappe.get_all("Dashboard", fields=["*"], limit=0)
    dashboardchart = frappe.get_all("Dashboard Chart", fields=["*"], limit=0)
    
    purchase_invoices = frappe.get_all("Purchase Invoice", fields=["*"], limit=0)
    sales_partners = frappe.get_all("Sales Partner", fields=["*"], limit=0)
    sales_persons = frappe.get_all("Sales Person", fields=["*"], limit=0)
    blanket_orders = frappe.get_all("Blanket Order", fields=["*"], limit=0)
    sales_invoices = frappe.get_all("Sales Invoice", fields=["*"], limit=0)
    sales_orders = frappe.get_all("Sales Order", fields=["*"], limit=0)
    quotations = frappe.get_all("Quotation", fields=["*"], limit=0)
    reports = frappe.get_all("Report", fields=["*"], limit=0)
    pages = frappe.get_all("Page", fields=["*"], limit=0)
    warehouses = frappe.get_all("Warehouse", fields=["*"], limit=0)
    
    stock_entries = frappe.get_all("Stock Entry", fields=["*"], limit=0)
    purchase_receipts = frappe.get_all("Purchase Receipt", fields=["*"], limit=0)
    delivery_trips = frappe.get_all("Delivery Trip", fields=["*"], limit=0)
    
    job_cards = frappe.get_all("Job Card", fields=["*"], limit=0)
    production_plans = frappe.get_all("Production Plan", fields=["*"], limit=0)
    tasks = frappe.get_all("Task", fields=["*"], limit=0)
    
    opportunities = frappe.get_all("Opportunity", fields=["*"], limit=0)
    appointments = frappe.get_all("Appointment", fields=["*"], limit=0)
    campaigns = frappe.get_all("Campaign", fields=["*"], limit=0)
    maisons = frappe.get_all("Maison", fields=["name","adresse"], limit=0)

    return {
        "maisons": maisons,
        "suppliers": suppliers
        # "projects": projects,
        # "companies": companies,
        # "customers": customers,
        # "items": items,
        # "materialrequests": materialrequests,
        # "brands": brands,
        # "leads": leads,
        # "purchaseorders": purchaseorders,
        # "dashboard": dashboard,
        # "dashboardchart": dashboardchart,
        # "purchaseordersitems": purchaseordersitems,
        
        # "purchase_invoices": purchase_invoices,
        # "sales_partners": sales_partners,
        # "sales_persons": sales_persons,
        # "blanket_orders": blanket_orders,
        # "sales_invoices": sales_invoices,
        # "sales_orders": sales_orders,
        # "quotations": quotations,
        # "reports": reports,
        # "pages": pages,
        # "warehouses": warehouses,
        # "stock_entries": stock_entries,
        # "purchase_receipts": purchase_receipts,
        # "delivery_trips": delivery_trips,
        # "job_cards": job_cards,
        # "production_plans": production_plans,
        # "tasks": tasks,
        # "opportunities": opportunities,
        # "appointments": appointments,
        # "campaigns": campaigns
    }

@frappe.whitelist()
def get_purchase_invoices():
    # Récupérer toutes les factures d'achat
    purchase_invoices = frappe.get_all("Purchase Invoice", fields=["*"])
    return purchase_invoices

@frappe.whitelist()
def get_purchase_orders(supplier):
    # Récupérer toutes les commandes d'achat pour le fournisseur spécifié
    purchase_orders = frappe.get_all("Purchase Order", filters={"supplier": supplier}, fields=["*"])
    return purchase_orders

@frappe.whitelist()
def get_supplier_quotations(supplier):
    # Récupérer tous les devis pour le fournisseur spécifié
    quotations = frappe.get_all("Supplier Quotation", filters={"supplier": supplier}, fields=["*"])
    return quotations

@frappe.whitelist()
def get_supplier_data(supplier):
    # Récupérer toutes les commandes d'achat pour le fournisseur spécifié
    purchase_orders = frappe.get_all("Purchase Order", filters={"supplier": supplier}, fields=["*"])

    # Récupérer tous les devis pour le fournisseur spécifié
    quotations = frappe.get_all("Supplier Quotation", filters={"supplier": supplier}, fields=["*"])

    # Retourner les deux ensembles de données dans un dictionnaire
    return {
        "purchase_orders": purchase_orders,
        "supplier_quotations": quotations
    }

@frappe.whitelist(allow_guest=True)
def get_all_buying():
    purchase_orders = frappe.get_all("Purchase Order", fields=["*"], limit=0)
    purchase_invoices = frappe.get_all("Purchase Invoice", fields=["*"], limit=0)
    suppliers = frappe.get_all("Supplier", fields=["*"], limit=0)
    purchase_order_items = frappe.get_all("Purchase Order Item", fields=["*"], limit=0)
    purchase_receipts = frappe.get_all("Purchase Receipt", fields=["*"], limit=0)
    material_requests = frappe.get_all("Material Request", fields=["*"], limit=0)

    return {
        "purchase_orders": purchase_orders,
        "purchase_invoices": purchase_invoices,
        "suppliers": suppliers,
        "purchase_order_items": purchase_order_items,
        "purchase_receipts": purchase_receipts,
        "material_requests": material_requests,
    }
