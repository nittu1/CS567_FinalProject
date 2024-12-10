from apartment_manager.apartment_manager import ApartmentManager

def main():
    manager = ApartmentManager()

    while True:
        print("\nApartment Management System")
        print("1. Add Apartment")
        print("2. Add Tenant")
        print("3. Lease Apartment")
        print("4. Search Apartments")
        print("5. List Apartments")
        print("6. List Tenants")
        print("7. List Leases")
        print("8. Make Payment")
        print("9. Submit Maintenance Request")
        print("10. View Overdue Payments")
        print("11. Terminate Lease")
        print("12. Generate Lease Summary")
        print("13. View Maintenance Requests")
        print("14. Generate Monthly Report")
        print("15. Filter Tenants by Balance")
        print("16. Apartment Occupancy Report")
        print("17. View Tenant Profile")
        print("18. Assign Maintenance Staff")
        print("19. Apply Late Fees")
        print("20. Extend Lease")
        print("21. Track Maintenance Status")
        print("22. Track Overdue Leases")
        print("23. Generate Outstanding Payment Report")
        print("24. Calculate Average Rent")
        print("25. Delete Apartment")
        print("26. Delete Tenant")
        print("27. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            unit_number = input("Enter unit number: ")
            bedrooms = int(input("Enter number of bedrooms: "))
            bathrooms = int(input("Enter number of bathrooms: "))
            rent = float(input("Enter rent: "))
            manager.add_apartment(unit_number, bedrooms, bathrooms, rent)
            print("Apartment added.")
        elif choice == "2":
            name = input("Enter tenant name: ")
            phone = input("Enter tenant phone: ")
            email = input("Enter tenant email: ")
            tenant = manager.add_tenant(name, phone, email)
            print(f"Tenant added: {tenant}")
        elif choice == "3":
            tenant_name = input("Enter tenant name: ")
            unit_number = input("Enter unit number: ")
            start_date = input("Enter lease start date (YYYY-MM-DD): ")
            end_date = input("Enter lease end date (YYYY-MM-DD): ")
            try:
                lease = manager.lease_apartment(tenant_name, unit_number, start_date, end_date)
                print(f"Lease created:\n{lease}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "4":
            min_rent = input("Enter minimum rent (or press Enter to skip): ")
            max_rent = input("Enter maximum rent (or press Enter to skip): ")
            bedrooms = input("Enter bedrooms (or press Enter to skip): ")
            bathrooms = input("Enter bathrooms (or press Enter to skip): ")
            apartments = manager.search_apartments(
                min_rent=float(min_rent) if min_rent else None,
                max_rent=float(max_rent) if max_rent else None,
                bedrooms=int(bedrooms) if bedrooms else None,
                bathrooms=int(bathrooms) if bathrooms else None,
            )
            print("\nAvailable Apartments:")
            print("\n".join(apartments))
        elif choice == "5":
            print("\nApartments:")
            print("\n".join(manager.list_apartments()))
        elif choice == "6":
            print("\nTenants:")
            print("\n".join(manager.list_tenants()))
        elif choice == "7":
            print("\nLeases:")
            print("\n".join(manager.list_leases()))
        elif choice == "8":
            tenant_name = input("Enter tenant name: ")
            amount = float(input("Enter payment amount: "))
            tenant = next((t for t in manager.tenants if t.name == tenant_name), None)
            if tenant:
                print(tenant.make_payment(amount))
            else:
                print("Tenant not found.")
        elif choice == "9":
            unit_number = input("Enter apartment unit number: ")
            request = input("Enter maintenance request details: ")
            apartment = next((a for a in manager.apartments if a.unit_number == unit_number), None)
            if apartment:
                apartment.add_maintenance_request(request)
                print("Maintenance request submitted.")
            else:
                print("Apartment not found.")
        elif choice == "10":
            overdue = manager.overdue_payments()
            print("\nOverdue Payments:")
            print("\n".join(overdue) if overdue else "No overdue payments.")
        elif choice == "11":
            unit_number = input("Enter apartment unit number: ")
            lease = next((l for l in manager.leases if l.apartment.unit_number == unit_number), None)
            if lease:
                print(lease.terminate_lease())
                manager.leases.remove(lease)
            else:
                print("Lease not found.")
        elif choice == "12":
            unit_number = input("Enter apartment unit number: ")
            print(manager.generate_lease_summary(unit_number))
        elif choice == "13":
            unit_number = input("Enter apartment unit number: ")
            print(manager.view_maintenance_requests(unit_number))
        elif choice == "14":
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (MM): "))
            print(manager.generate_monthly_report(year, month))
        elif choice == "15":
            threshold = float(input("Enter balance threshold: "))
            print("\n".join(manager.filter_tenants_by_balance(threshold)))
        elif choice == "16":
            print(manager.apartment_occupancy_report())
        elif choice == "17":
            tenant_name = input("Enter tenant name: ")
            print(manager.view_tenant_profile(tenant_name))
        elif choice == "18":
            unit_number = input("Enter apartment unit number: ")
            staff_name = input("Enter staff name: ")
            print(manager.assign_maintenance_staff(unit_number, staff_name))
        elif choice == "19":
            late_fee = float(input("Enter late fee amount: "))
            print(manager.apply_late_fees(late_fee))
        elif choice == "20":
            unit_number = input("Enter apartment unit number: ")
            new_end_date = input("Enter new lease end date (YYYY-MM-DD): ")
            print(manager.extend_lease(unit_number, new_end_date))
        elif choice == "21":
            print(manager.track_maintenance_status())
        elif choice == "22":
            print(manager.track_overdue_leases())
        elif choice == "23":
            print(manager.generate_outstanding_report())
        elif choice == "24":
            print(manager.calculate_average_rent())
        elif choice == "25":
            unit_number = input("Enter unit number to delete: ")
            print(manager.delete_apartment(unit_number))
        elif choice == "26":
            tenant_name = input("Enter tenant name to delete: ")
            print(manager.delete_tenant(tenant_name))
        elif choice == "27":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()