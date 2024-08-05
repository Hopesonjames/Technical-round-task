# Copyright (c) 2024, hopeson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


# class RentalReturnVoucher(Document):
# 	pass

# class RentalReturnVoucher(Document):
#     def on_submit(self):
#         # Fetch the original rental voucher details
#         # rental_voucher = frappe.get_doc('Rental Voucher', self.rental_voucher)
        
#         # Validate the return quantity
#         if self.return_quantity > self.actual_quantity:
#             frappe.throw("Returned quantity cannot exceed the rented quantity.")

#         # Create Stock Entry for returned items
#         stock_entry = frappe.get_doc({
#             "doctype": "Stock Entry",
#             "stock_entry_type": "Material Receipt",
#             "items": [{
#                 "item_code": self.item,
#                 "qty": self.return_quantity,  # Use return_quantity for stock update
#                 "t_warehouse": "Stores - D",  # Replace with the appropriate warehouse
#                 "rate": self.rate
#             }]
#         })
#         stock_entry.insert()
#         stock_entry.submit()
#         frappe.msgprint("Successfull...")


import frappe
from frappe.model.document import Document

class RentalReturnVoucher(Document):
    def on_submit(self):
        # Fetch the original rental voucher details
        rental_voucher = frappe.get_doc('Rental Voucher', self.rental_voucher)

        # Validate the return quantity
        if self.return_quantity > rental_voucher.quantity:
            frappe.throw("Returned quantity cannot exceed the rented quantity.")

        # Create Stock Entry for returned items
        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "items": [{
                "item_code": rental_voucher.item,
                "qty": self.return_quantity,  # Use return_quantity for stock update
                "t_warehouse": "Stores - D",  # Replace with the appropriate warehouse
                "rate": self.rental_rate
            }]
        })

        stock_entry.insert()
        stock_entry.submit()
        frappe.msgprint("Stock entry for returned items created successfully.")
