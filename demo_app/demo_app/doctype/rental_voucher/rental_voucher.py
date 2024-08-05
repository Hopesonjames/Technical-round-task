# Copyright (c) 2024, hopeson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


# class RentalVoucher(Document):
# 	pass


class RentalVoucher(Document):
    def on_submit(self):
        # Create a Stock Entry of type "Material Issue"
        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Issue",
            "items": [{
                "item_code": self.item,
                "qty": self.quantity,
                "s_warehouse": "Stores - D",  # Ensure the name matches exactly
                "rate": self.rate
            }]
        })
        
        # Insert and Submit the Stock Entry to deduct the quantity from stock
        stock_entry.insert()
        stock_entry.submit()
        frappe.msgprint("Done")