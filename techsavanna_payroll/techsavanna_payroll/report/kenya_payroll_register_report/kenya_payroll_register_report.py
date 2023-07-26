from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
    if not filters: filters = {}
    currency = None
    if filters.get('currency'):
        currency = filters.get('currency')
    company_currency = frappe.get_cached_value('Company', filters.get("company"), 'default_currency')
    salary_slips = get_salary_slips(filters, company_currency)
    if not salary_slips:
        return [], []

    columns, earning_types, ded_types = get_columns()

    ss_earning_map = get_ss_earning_map(salary_slips, currency, company_currency)
    ss_ded_map = get_ss_ded_map(salary_slips, currency, company_currency)

    data = []
    for ss in salary_slips:
        row = [
            ss.employee, ss.employee_name, ss.base, ss.housing_allowance,
            ss.gross_pay, ss.nssf, ss.nhif, ss.paye,
            get_total_deductions(ss, ss_ded_map), ss.net_pay
        ]
        data.append(row)

    return columns, data

def get_columns():
    return [
        _("Emp #") + ":Link/Employee:120",
        _("Name") + "::140",
        _("Basic Salary") + ":Currency:120",
        _("H/A") + ":Currency:120",
        _("Gross Pay") + ":Currency:120",
        _("NSSF") + ":Currency:120",
        _("NHIF") + ":Currency:120",
        _("PAYE") + ":Currency:120",
        _("Deductions") + ":Currency:120",
        _("Net Pay") + ":Currency:120",
    ], [], []

def get_salary_slips(filters, company_currency):
    filters.update({"from_date": filters.get("from_date"), "to_date": filters.get("to_date")})
    conditions, filters = get_conditions(filters, company_currency)
    salary_slips = frappe.db.sql("""
        select * from `tabSalary Slip` where %s order by employee
        """ % conditions, filters, as_dict=1)

    return salary_slips or []

def get_conditions(filters, company_currency):
    conditions = ""
    doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

    if filters.get("docstatus"):
        conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

    if filters.get("from_date"):
        conditions += " and start_date = %(from_date)s"
    if filters.get("to_date"):
        conditions += " and end_date = %(to_date)s"
    if filters.get("company"):
        conditions += " and company = %(company)s"
    if filters.get("employee"):
        conditions += " and employee = %(employee)s"
    if filters.get("currency") and filters.get("currency") != company_currency:
        conditions += " and currency = %(currency)s"

    return conditions, filters

def get_total_deductions(salary_slip, ss_ded_map):
    total_deductions = 0
    ded_map = ss_ded_map.get(salary_slip.name, {})
    for ded in ded_map.values():
        total_deductions += ded
    return total_deductions

def get_ss_earning_map(salary_slips, currency, company_currency):
    ss_earnings = frappe.db.sql("""
        select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
        from `tabSalary Detail` sd, `tabSalary Slip` ss
        where sd.parent=ss.name and sd.parent in (%s)
        """ % (', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

    ss_earning_map = {}
    for d in ss_earnings:
        ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
        if currency == company_currency:
            ss_earning_map[d.parent][d.salary_component] = flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
        else:
            ss_earning_map[d.parent][d.salary_component] = flt(d.amount)

    return ss_earning_map

def get_ss_ded_map(salary_slips, currency, company_currency):
    ss_deductions = frappe.db.sql("""
        select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
        from `tabSalary Detail` sd, `tabSalary Slip` ss
        where sd.parent=ss.name and sd.parent in (%s)
        """ % (', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

    ss_ded_map = {}
    for d in ss_deductions:
        ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
        if currency == company_currency:
            ss_ded_map[d.parent][d.salary_component] = flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
        else:
            ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

    return ss_ded_map
