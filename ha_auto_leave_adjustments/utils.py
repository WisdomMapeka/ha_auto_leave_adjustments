import frappe


# this only updates ameployees in a payroll entry
def add_leave_allocation(doc, method):
    """
    After Payroll Entry is created:
    - Fetch latest Ha Leave Adjustments Settings
    - For each employee in Payroll Entry
    - For each leave adjustment configured
    - Update existing Leave Allocation (increase allocated leaves)
    """

    # Get the latest Ha Leave Adjustments Settings
    latest = frappe.get_all(
        "Ha Leave Adjustments Settings",
        fields=["name"],
        order_by="creation desc",
        limit=1
    )
    if not latest:
        frappe.msgprint("No Ha Leave Adjustments Settings record found")
        return

    settings = frappe.get_doc("Ha Leave Adjustments Settings", latest[0].name)

    if not settings.leave_adjustments:
        frappe.msgprint("No leave adjustments configured")
        return

    for row in settings.leave_adjustments:
        # Fetch allocations with fields
        allocations = frappe.get_all(
            "Leave Allocation",
            filters={
                "leave_type": row.leave_type,
                "docstatus": ["!=", 2]   # exclude Cancelled allocations
            },
            fields=["name", "employee", "total_leaves_allocated", "new_leaves_allocated"]
        )

        print("ALL ALLOCATIONS ---------------------")
        print(allocations)

        for alloc in allocations:
            # Load full document
            allocation_doc = frappe.get_doc("Leave Allocation", alloc.name)

            # Increase leaves
            allocation_doc.new_leaves_allocated = (
                allocation_doc.new_leaves_allocated + float(row.leave_number)
            )
            allocation_doc.save(ignore_permissions=True)
            frappe.db.commit()

        frappe.msgprint("Leave Allocations updated successfully for all employees in this payroll entry")




# # this only updates ameployees in a payroll entry
# def add_leave_allocation2(doc, method):
#     """
#     After Payroll Entry is created:
#     - Fetch latest Ha Leave Adjustments Settings
#     - For each employee in Payroll Entry
#     - For each leave adjustment configured
#     - Update existing Leave Allocation (increase allocated leaves)
#     """

#     # Get the latest Ha Leave Adjustments Settings
#     latest = frappe.get_all(
#         "Ha Leave Adjustments Settings",
#         fields=["name"],
#         order_by="creation desc",
#         limit=1
#     )
#     if not latest:
#         frappe.msgprint("No Ha Leave Adjustments Settings record found")
#         return

#     settings = frappe.get_doc("Ha Leave Adjustments Settings", latest[0].name)

#     if not settings.leave_adjustments:
#         frappe.msgprint("No leave adjustments configured")
#         return

#     # Loop employees in Payroll Entry
#     if hasattr(doc, "employees"):
#         for emp in doc.employees:
#             for row in settings.leave_adjustments:
#                 # Find existing allocation for employee + leave type
#                 existing = frappe.get_all(
#                     "Leave Allocation",
#                     filters={
#                         "employee": emp.employee,
#                         "leave_type": row.leave_type
#                     },
#                     fields=["name", "total_leaves_allocated"]
#                 )

#                 if existing:
      
#                     allocation = frappe.get_doc("Leave Allocation", existing[0].name)
#                     allocation.total_leaves_allocated = (
#                         allocation.total_leaves_allocated + int(row.leave_number)
#                     )
#                     allocation.save(ignore_permissions=True)
#                     frappe.db.commit()
#                 else:
#                     # No allocation exists → create one
#                     allocation = frappe.new_doc("Leave Allocation")
#                     allocation.employee = emp.employee
#                     allocation.leave_type = row.leave_type
#                     allocation.from_date = doc.start_date
#                     allocation.to_date = doc.end_date
#                     allocation.new_leaves_allocated = int(row.leave_number)
#                     allocation.insert(ignore_permissions=True)
#                     allocation.submit()

#         frappe.msgprint("Leave Allocations updated successfully for all employees in this payroll entry")
#     else:
#         frappe.msgprint("No employees found in Payroll Entry to allocate leave")

