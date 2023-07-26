from __future__ import unicode_literals
import frappe, erpnext
from frappe import _

def execute(filters=None):
    company_currency = erpnext.get_company_currency(filters.get("company"))
    columns = get_columns()
    data = get_data(filters, company_currency)

    return columns, data

def get_columns():
    columns = [
        {
            'label': _('Emp #'),
            'fieldname': 'employee',
            'fieldtype': 'Link',
            'options': 'Employee',
            'width': 150
        },
        {
            'label': _('Name'),
            'fieldname': 'employee_name',
            'fieldtype': 'Data',
            'width': 140
        },
        {
            'label': _('Basic Salary'),
            'fieldname': 'base',
            'fieldtype': 'Currency',
            'width': 120
        },
        {
            'label': _('H/A'),
            'fieldname': 'housing_allowance',
            'fieldtype': 'Currency',
            'width': 120
        },
        {
            'label': _('Gross Pay'),
            'fieldname': 'gross_pay',
            'fieldtype': 'Currency',
            'width': 120
        },
        {
            'label': _('NSSF'),
            'fieldname': 'nssf',
            'fieldtype': 'Currency',
            'width': 120
        },
        {
            'label': _('NHIF'),
            'fieldname': 'nhif',
            'fieldtype': 'Currency',
            'width': 120
        },
        {
            'label': _('PAYE'),
            'fieldname': 'paye',
            'fieldtype': 'Currency',
            'width': 120
        },
        {
            'label': _('Deductions'),
            'fieldname': 'total_deductions',
            'fieldtype': 'Currency',
            'width': 120
        },
        {
            'label': _('Net Pay'),
            'fieldname': 'net_pay',
            'fieldtype': 'Currency',
            'width': 120
        }
    ]

    return columns

def get_data(filters, company_currency, conditions=""):
    conditions = get_conditions(filters, company_currency)

    if filters.from_date > filters.to_date:
        frappe.throw(_("To Date cannot be before From Date. {}").format(filters.to_date))

    data = frappe.db.sql("""
        SELECT ss.employee, ss.employee_name, ss.base, ss.housing_allowance,
        ss.gross_pay, ss.nssf, ss.nhif, ss.paye, ss.total_deduction, ss.net_pay
        FROM `tabEmployee` e
        INNER JOIN `tabSalary Slip` ss ON e.name = ss.employee
        INNER JOIN `tabSalary Detail` sd ON sd.parent = ss.name
        WHERE %s
    """ % conditions, filters, as_dict=1)

    return data

def get_conditions(filters, company_currency):
    conditions = ""
    doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

    if filters.get("docstatus"):
        conditions += "ss.docstatus = {0}".format(doc_status[filters.get("docstatus")])

    if filters.get("from_date"):
        conditions += " and ss.start_date = %(from_date)s"

    if filters.get("to_date"):
        conditions += " and ss.end_date = %(to_date)s"

    if filters.get("company"):
        conditions += " and ss.company = %(company)s"

    if filters.get("currency") and filters.get("currency") != company_currency:
        conditions += " and ss.currency = %(currency)s"

    return conditions
