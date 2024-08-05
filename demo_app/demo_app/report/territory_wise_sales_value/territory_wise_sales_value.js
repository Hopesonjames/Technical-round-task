// Copyright (c) 2024, hopeson and contributors
// For license information, please see license.txt

// frappe.query_reports["Territory-wise sales value"] = {
// 	"filters": [

// 	]
// };





frappe.query_reports["Territory-wise sales value"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "territory",
            "label": __("Territory"),
            "fieldtype": "Link",
            "options": "Territory",
            "default": "",
            "reqd": 0
        }
    ],
    onload: function(report) {
        report.page.set_title(__('Territory-wise sales value'));
    },
    formatter: function(value, row, column, data, default_formatter) {
        // if (data.territory === 'Total') {
        //     value = `<b>${value}</b>`;
        // }
        return default_formatter(value, row, column, data);
    }
};
