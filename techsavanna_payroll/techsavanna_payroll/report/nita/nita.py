# Copyright (c) 2023, samson  and contributors
# For license information, please see license.txt

# import frappe


# Copyright (c) 2023, samson and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
import frappe, erpnext
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [
       {
            'label': _('NITA Member Number'),
            'fieldname': 'nita_member_number',
            'width':300
        },
        {
            'label': _('NITA Member  Name'),
            'fieldname': 'other_name',
            'width':300
        },
         {
            'label': _('KRA PIN'),
            'fieldname': 'tax_id',
            'options': 'Pin',
            'width': 180
        },
         {
            'label': _('Stardard NITA Deduction'),
            'fieldname': 'nita',
            'options': 'Pin',
            'width': 180
        },
        

    ]
    return columns


def get_data(filters,conditions=""):
    conditions = get_conditions(filters)

   
    if filters.from_date > filters.to_date:
        frappe.throw(_("To Date cannot be before From Date. {}").format(filters.to_date))
    
    data = frappe.db.sql(""" SELECT 	
        ss.employee, 
        e.tax_id, 
        ss.start_date,
        'Resident' as resident,
        e.employment_type,
        ss.end_date, 
        IFNULL(e.last_name,'') AS last_name,
        CONCAT(IFNULL(e.first_name,''), ' ', IFNULL(e.middle_name,''),' ', IFNULL(e.last_name,'')) AS other_name,			
        e.national_id, 
        e.nhif_no,
        e.nita_member_number,
        MAX(CASE WHEN sd.abbr = 'BS' THEN sd.amount  ELSE 0 END) AS basic_salary,
		 MAX(CASE WHEN sd.abbr = 'NITA' THEN sd.amount  ELSE 0 END) AS nita,
        MAX(CASE WHEN sd.abbr = 'HseAlw' THEN sd.amount  ELSE 0 END) AS house_allowance,
        MAX(CASE WHEN sd.abbr = 'TransAlw' THEN sd.amount  ELSE 0 END) AS transport_allowance,
        MAX(CASE WHEN sd.abbr = 'LE' THEN sd.amount  ELSE 0 END) AS leave_encashment,
        MAX(CASE WHEN sd.abbr = 'EMPNSSF' THEN sd.amount ELSE 0 END) AS employee_nssf,
        MAX(CASE WHEN sd.abbr = 'PR' THEN sd.amount  ELSE 0 END) AS personal_relief,
        MAX(CASE WHEN sd.abbr = 'IT_2' THEN sd.amount ELSE 0 END) AS paye,
        SUM(CASE WHEN sd.abbr IN ('OT15', 'OT20') THEN sd.amount ELSE 0 END) AS overtime
    FROM `tabEmployee` e, `tabSalary Slip` ss, `tabSalary Detail` sd
    WHERE 
        %s 
        and
        e.name = ss.employee
        AND sd.parent = ss.name		
        AND (sd.abbr IN ('BS', 'HseAlw', 'TransAlw', 'LE', 'EMPNSSF', 'PR', 'IT_2', 'OT15', 'OT20','NITA'))
        AND sd.amount != 0
    GROUP BY
        ss.employee, 
        e.tax_id, 
        ss.start_date,
        e.employment_type,
        ss.end_date,
        IFNULL(e.last_name,''),
        IFNULL(e.first_name,''),
        IFNULL(e.middle_name,''),
        e.national_id, 
        e.nhif_no;

        """ % conditions, filters,  as_dict=1)
    return data

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"): conditions += "  ss.start_date = %(from_date)s"
	if filters.get("to_date"): conditions += " and ss.end_date = %(to_date)s"
	
	return conditions

