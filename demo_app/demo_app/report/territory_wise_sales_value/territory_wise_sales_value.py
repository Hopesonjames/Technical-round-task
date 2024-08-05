# Copyright (c) 2024, hopeson and contributors
# For license information, please see license.txt

# import frappe



import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": _("Territory"), "fieldname": "territory", "fieldtype": "Link", "options": "Territory", "width": 400},
        {"label": _("Sales Value"), "fieldname": "sales_value", "fieldtype": "Currency", "width": 200},
    ]

    data = get_sales_data(filters)
    
    # Calculate total sales value
    total_sales_value = sum(row['sales_value'] for row in data if row['sales_value'] is not None)

    # Add total sales row
    total_row = {
        'territory': 'Total',
        'sales_value': total_sales_value,
    }

    # Set the total sales value only for the last row and None for others
    data.append(total_row)

    return columns, data

def get_sales_data(filters):
    conditions = []
    
    # Date filters
    if filters.get("from_date"):
        conditions.append(f"si.posting_date >= '{filters['from_date']}'")
    if filters.get("to_date"):
        conditions.append(f"si.posting_date <= '{filters['to_date']}'")

    # Territory filter
    if filters.get("territory"):
        territory = filters["territory"]
        territory_doc = frappe.get_doc("Territory", territory)
        if territory_doc.is_group:
            child_territories = get_child_territories(territory)
            conditions.append(f"c.territory IN ({', '.join(['%s'] * len(child_territories))})")
        else:
            conditions.append(f"c.territory = %s")

    condition_str = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            c.territory AS territory,
            SUM(si.net_total) AS sales_value
        FROM
            `tabSales Invoice` AS si
        JOIN
            `tabCustomer` AS c ON si.customer = c.name
        WHERE
            {condition_str}
        GROUP BY
            c.territory
    """
    
    if filters.get("territory"):
        if territory_doc.is_group:
            return frappe.db.sql(query, tuple(child_territories), as_dict=True)
        else:
            return frappe.db.sql(query, (territory,), as_dict=True)
    else:
        return frappe.db.sql(query, as_dict=True)

def get_child_territories(parent):
    child_territories = []
    def get_children(name):
        children = frappe.get_all("Territory", filters={"parent_territory": name})
        for child in children:
            child_territories.append(child.name)
            get_children(child.name)
    get_children(parent)
    return child_territories
