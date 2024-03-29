import requests
import frappe
from datetime import datetime

# @frappe.whitelist(allow_guest=True)
def update_employee_checkins():
    url = "http://197.254.14.222/biometricAPI/attendanceTimesheet.php"
    headers = {
        'Secret-Key': '/c054XQX5xsSrGh+yN/WWoEDzJqImC5NMLP4J521EJY='
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            attendance_data = response.json()

            # Process the attendance data in batches of 100 records
            batch_size = 100
            for i in range(0, len(attendance_data), batch_size):
                batch = attendance_data[i:i + batch_size]
                process_batch(batch)

        else:
            print("Failed to fetch attendance data. Status code:", response.status_code)

    except Exception as e:
        print("Error during API request:", e)

def process_batch(batch):
    for attendance in batch:
        emp_id = attendance["empid"]
        log_type = attendance["type"]
        log_time_str = attendance["date"]
        log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S")

        try:
            employee = frappe.get_doc("Employee", emp_id)
            if employee:
                frappe.enqueue(make_checkin, employee=employee, log_type=log_type, time=log_time)
        except frappe.DoesNotExistError:
            frappe.log_error(f"Employee {emp_id} not found.")
            continue
        except Exception as e:
            frappe.log_error(e)

        # Add logid to the list after successful update
        log_id = attendance["Logid"]
        frappe.enqueue(post_data_to_api, log_id=log_id, queue="long")


def make_checkin(employee, log_type, time):
    try:
        log = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": employee.name,
            "time": time,
            "device_id": "device1",  # Set the appropriate device ID
            "log_type": log_type
        })
        log.insert(ignore_permissions=True)
        frappe.db.commit()
        return log
    except Exception as e:
        frappe.log_error(e)
        return None

def post_data_to_api(log_id):
    url = "http://197.254.14.222/biometricAPI/attendance_sync.php"
    headers = {
        'Secret-Key': '/c054XQX5xsSrGh+yN/WWoEDzJqImC5NMLP4J521EJY='
    }
    data =[log_id]
    

    try:
        response = requests.post(url, headers=headers, json=data)
        print(response.text)
        if response.status_code == 200:
            print("Data posted successfully for logid:", log_id)
        else:
            print("Failed to post data for logid:", log_id)

    except Exception as e:
        print("Error during data posting for logid:", log_id, e)
