import frappe
@frappe.whitelist()
def update_purchase_order(*args,**kwargs):
    """update items table in a purchase order"""
    frappe.log_error("args",args)
    frappe.log_error("kwargs", kwargs)
    try:
        if kwargs.get("purchase_order_number"):
            #check if purchase order is existing
            current_user = frappe.session.user
            frappe.session.user = "Administrator"
            po_number = kwargs.get("purchase_order_number")
            if frappe.db.exists("Purchase Order", po_number):
                po_doc = frappe.get_doc("Purchase Order", po_number)
                if po_doc.items:
                    #delete existing items
                    existing_items = frappe.get_all("Purchase Order Item",{"parent":po_number})
                    if existing_items:
                        for doc in existing_items:
                            frappe.db.delete("Purchase Order Item", doc.get("name"))
                    
                if po_doc.taxes:
                    existing_taxes = frappe.get_all("Purchase Taxes and Charges",{"parent":po_number})
                    if existing_taxes:
                        for doc in existing_taxes:
                            frappe.db.delete("Purchase Taxes and Charges",doc.get("name"))
                        
                po_items = []
                tax_doc_items = []
                if kwargs.get("items"):
                    for p_item in kwargs.get("items"):
                        p_item["item_name"] = frappe.db.get_value("Item", {"item_code":p_item["item_code"]},"item_name")
                        p_item["doctype"] = "Purchase Order Item" 
                        p_item["parent"] = po_number
                        p_item["base_rate"] = p_item["rate"]
                        doc = frappe.get_doc(p_item)
                        doc.flags.ignore_mandatory = True
                        doc.flags.ignore_permissions = True
                        doc.save()
                        po_items.append(doc)
                
                if kwargs.get("taxes"):
                    for tax in kwargs.get("taxes"):
                        tax["doctype"] = "Purchase Taxes and Charges"
                        tax["parent"] = po_number
                        tax_doc = frappe.get_doc(tax)
                        tax_doc.flags.ignore_mandatory = True
                        tax_doc.flags.ignore_permissions = True
                        tax_doc.save()
                        tax_doc_items.append(tax)
                
                # po_doc.reload()
                po_doc.items = po_items
                po_doc.taxes = tax_doc_items
                
                frappe.db.set_value("Purchase Order",po_number, "net_total", kwargs.get("net_total"))
                frappe.db.set_value("Purchase Order",po_number, "total", kwargs.get("total"))
                frappe.db.set_value("Purchase Order",po_number, "grand_total", kwargs.get("total"))
                frappe.db.set_value("Purchase Order",po_number, "taxes_and_charges_added", kwargs.get("tax_amount"))
                frappe.db.set_value("Purchase Order",po_number, "total_taxes_and_charges", kwargs.get("tax_amount"))
                
                
                po_doc.flags.ignore_validate_update_after_submit=True
                po_doc.flags.ignore_mandatory = True
                po_doc.flags.ignore_permissions = True
                frappe.db.commit()
                frappe.local.response["http_status_code"] = 200
                frappe.local.response['data'] = {"server":"Webhook Received and Processed"}
                frappe.local.response['_server_messages'] = "Webhook Received and Processed"
            else:
                frappe.local.response["http_status_code"] = 404
                frappe.local.response['data'] = {"server":"purchase order_does not exist"}
                frappe.local.response["message"] = "Webhook Received"
    except Exception as e:
        frappe.local.response["status_code"] = 500
        frappe.local.response["message"] = "Error Updating PO, Please check error logs"
        frappe.log_error("update_po", frappe.get_traceback())        


def update_linked_purchase_invoice(po_number):
    
    if frappe.db.exists("Purchase Invoice",{}):
        pass