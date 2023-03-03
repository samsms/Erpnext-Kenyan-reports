// Copyright (c) 2023, samson  and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["P10 monthly itax"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1).replace(day=1),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"to_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"default": (frappe.datetime.get_today().replace(day=1) ),
			"reqd": 1,
			"width": "100px"
		}
	]
};

