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
            'label': _('Pin #'),
            'fieldname': 'tax_id',
            'options': 'Pin',
            'width': 180
        },
        {
            'label': _('Name'),
            'fieldname': 'other_name',
            'width':300
        },
        {
            'label': _('Residential Status'),
            'fieldname': 'resident',
            
            'width':150,

        },
        {
            'label': _('Employee Type'),
            'fieldname': 'employment_type',
            
            'width':150,

        },
        {
            'label': _('Basic Salary'),
            'fieldname': 'basic_salary',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Housing Allowance'),
            'fieldname': 'house_allowance',
            'fieldtype': 'Currency',
            'width':150,

        },
          {
            'label': _(' Transport Allowance'),
            'fieldname': 'transport_allowance',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Leave Pay'),
            'fieldname': 'leave_encashment',
            'fieldtype': 'Currency',
            'width':150,

        },
        {
            'label': _('Overtime Allowance'),
            'fieldname': 'overtime',
            'fieldtype': 'Currency',
            'width':150,

        },
       
        {
            'label': _('Directors Fee'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Lump Sum Payment'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
           {
            'label': _('Other Allowance'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
           {
            'label': _('Total Cash Pay(A)'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
           {
            'label': _('Value Of Car Benefit'),
            'fieldname': 'car_benefit',
            'fieldtype': 'Currency',
            'width':150,

        },
           {
            'label': _('Other Non Cash Benefits'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
           {
            'label': _('Total Non Cash Pay'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
          {
            'label': _('Global Income'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
          {
            'label': _('Type Of Housing'),
            'fieldname': 'amount',
           
            'width':150,

        },
         {
            'label': _('Rent Of House/Market Value'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Computed Rent Of House'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Net Value Of Housing'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Total Gross Pay'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('30% Of Cash Pay'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Actual Contribution'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('30% Of Cash Pay'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Permissable Limit'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Mortgage Interest'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Deposit Of House Ownership Plan'),
            'fieldname': 'amount',
            'fieldtype': 'Currency',
            'width':150,

        },
         {
            'label': _('Monthly Personal Relief'),
            'fieldname': 'personal_relief',
            'fieldtype': 'Currency',
            'width':150,

        },
           {
            'label': _(' PAYE Tax (KSH)'),
            'fieldname': 'paye',
            'fieldtype': 'Currency',
            'width':150,

        },
          {
            'label': _('Self Assesed PAYE Tax (KSH)'),
            'fieldname': 'paye',
            'fieldtype': 'Currency',
            'width':150,

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
        MAX(CASE WHEN sd.abbr = 'BS' THEN sd.amount  ELSE 0 END) AS basic_salary,
        MAX(CASE WHEN sd.abbr = 'HseAlw' THEN sd.amount  ELSE 0 END) AS house_allowance,
        MAX(CASE WHEN sd.abbr = 'TransAlw' THEN sd.amount  ELSE 0 END) AS transport_allowance,
        MAX(CASE WHEN sd.abbr = 'LE' THEN sd.amount  ELSE 0 END) AS leave_encashment,
        MAX(CASE WHEN sd.abbr = 'CB' THEN sd.amount  ELSE 0 END) AS car_benefit,
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
        AND (sd.abbr IN ('BS', 'HseAlw', 'TransAlw', 'LE', 'EMPNSSF', 'PR', 'IT_2', 'OT15', 'OT20','CB'))
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

