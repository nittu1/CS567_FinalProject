import unittest
from datetime import date
from apartment_manager.apartment_manager import ApartmentManager, Apartment, Tenant, Lease


class TestApartmentManager(unittest.TestCase):

    def setUp(self):
        """Set up initial data for tests."""
        self.manager = ApartmentManager()

        # Add sample apartments
        self.manager.add_apartment("101", 2, 1, 1500)
        self.manager.add_apartment("102", 3, 2, 2000)

        # Add sample tenants
        self.manager.add_tenant("Alice", "1234567890", "alice@example.com")
        self.manager.add_tenant("Bob", "9876543210", "bob@example.com")

        # Create a lease
        self.manager.lease_apartment("Alice", "101", "2023-01-01", "2023-12-31")

    def test_add_apartment(self):
        self.manager.add_apartment("103", 1, 1, 1200)
        apartment = next((a for a in self.manager.apartments if a.unit_number == "103"), None)
        self.assertIsNotNone(apartment)
        self.assertEqual(apartment.rent, 1200)

    def test_add_tenant(self):
        tenant = self.manager.add_tenant("Charlie", "5555555555", "charlie@example.com")
        self.assertIn(tenant, self.manager.tenants)
        self.assertEqual(tenant.name, "Charlie")

    def test_lease_apartment(self):
        lease = self.manager.lease_apartment("Bob", "102", "2023-01-01", "2023-12-31")
        self.assertEqual(lease.tenant.name, "Bob")
        self.assertFalse(lease.apartment.is_available)

    # def test_search_apartments(self):
    #     results = self.manager.search_apartments(max_rent=1800)
    #     self.assertEqual(len(results), 1)
    #     print(results, "sample")
    #     self.assertIn("101", results[0])

    def test_list_apartments(self):
        apartments = self.manager.list_apartments()
        self.assertEqual(len(apartments), 2)
        self.assertIn("101", apartments[0])

    def test_list_tenants(self):
        tenants = self.manager.list_tenants()
        self.assertEqual(len(tenants), 2)
        self.assertIn("Alice", tenants[0])

    def test_list_leases(self):
        leases = self.manager.list_leases()
        self.assertEqual(len(leases), 1)
        self.assertIn("Alice", leases[0])

    def test_overdue_payments(self):
        self.manager.leases[0].end_date = date(2022, 12, 31)  # Set lease to be overdue
        overdue = self.manager.overdue_payments()
        self.assertEqual(len(overdue), 1)
        self.assertIn("Alice owes", overdue[0])

    def test_generate_lease_summary(self):
        summary = self.manager.generate_lease_summary("101")
        self.assertIn("Alice", summary)
        self.assertIn("1500", summary)

    def test_view_maintenance_requests(self):
        apartment = self.manager.apartments[0]
        apartment.add_maintenance_request("Fix the heater")
        requests = self.manager.view_maintenance_requests("101")
        self.assertIn("Fix the heater", requests)

    def test_generate_monthly_report(self):
        self.manager.leases[0].add_payment(1500, "2023-01-01")
        report = self.manager.generate_monthly_report(2023, 1)
        self.assertIn("Total Rent Collected: $1500", report)

    def test_filter_tenants_by_balance(self):
        self.manager.tenants[0].balance_due = 500
        results = self.manager.filter_tenants_by_balance(100)
        self.assertEqual(len(results), 1)
        self.assertIn("Alice", results[0])

    def test_apartment_occupancy_report(self):
        report = self.manager.apartment_occupancy_report()
        self.assertIn("Total Apartments: 2", report)
        self.assertIn("Occupied Apartments: 1", report)

    def test_assign_maintenance_staff(self):
        apartment = self.manager.apartments[0]
        apartment.add_maintenance_request({"request": "Fix plumbing", "status": "Pending"})
        response = self.manager.assign_maintenance_staff("101", "John")
        self.assertIn("John", response)

    def test_apply_late_fees(self):
        self.manager.tenants[0].balance_due = 1000
        response = self.manager.apply_late_fees(100)
        self.assertIn("Late fee of $100 applied", response)
        self.assertEqual(self.manager.tenants[0].balance_due, 1100)

    def test_extend_lease(self):
        response = self.manager.extend_lease("101", "2024-12-31")
        self.assertIn("extended from 2023-12-31 to 2024-12-31", response)

    def test_track_maintenance_status(self):
        apartment = self.manager.apartments[0]
        apartment.add_maintenance_request({"request": "Fix AC", "status": "In Progress"})
        status = self.manager.track_maintenance_status()
        self.assertIn("Fix AC", status)

    def test_delete_apartment(self):
        response = self.manager.delete_apartment("101")
        self.assertIn("Apartment Unit 101 deleted", response)
        self.assertEqual(len(self.manager.apartments), 1)

    def test_delete_tenant(self):
        response = self.manager.delete_tenant("Alice")
        self.assertIn("Tenant Alice deleted", response)
        self.assertEqual(len(self.manager.tenants), 1)

    def test_view_tenant_profile(self):
        # Test case 1: View tenant profile with active leases
        profile = self.manager.view_tenant_profile("Alice")
        self.assertIn("Profile for Alice", profile)
        self.assertIn("Contact: 1234567890, alice@example.com", profile)
        self.assertIn("Balance Due: $1500", profile)  # Monthly rent of 1500

        # Test case 2: View tenant profile for a tenant without leases
        self.manager.add_tenant("Charlie", "5555555555", "charlie@example.com")
        profile = self.manager.view_tenant_profile("Charlie")
        self.assertIn("Profile for Charlie", profile)
        self.assertIn("Balance Due: $0", profile)
        self.assertIn("Leases:\n", profile)  # No leases, so empty lease info

        # Test case 3: View tenant profile for a non-existent tenant
        profile = self.manager.view_tenant_profile("NonExistent")
        self.assertEqual(profile, "Tenant not found.")

    def test_search_apartments(self):

        # Test case 2: Search by minimum rent
        results = self.manager.search_apartments(min_rent=1800)
        self.assertEqual(len(results), 1)  # Only 102 matches
        self.assertIn("Apartment 102", results[0])


        # Test case 4: Search by exact bathrooms
        results = self.manager.search_apartments(bathrooms=2)
        self.assertEqual(len(results), 1)  # Only 102 matches
        self.assertIn("Apartment 102", results[0])

        # Test case 5: Search by range of bedrooms
        results = self.manager.search_apartments(min_bedrooms=2, max_bedrooms=3)
        self.assertEqual(len(results), 1)  # Both 101 and 102 match

        # Test case 6: Search by range of bathrooms
        results = self.manager.search_apartments(min_bathrooms=1, max_bathrooms=2)
        self.assertEqual(len(results), 1)  # Both 101 and 102 match

        # Test case 7: Include occupied apartments in search
        results = self.manager.search_apartments(include_occupied=True)
        self.assertEqual(len(results), 2)  # Both apartments are listed

        # Test case 8: Exclude occupied apartments in search
        results = self.manager.search_apartments(include_occupied=False)
        self.assertEqual(len(results), 1)  # Only 102 is available

        # Test case 9: Search with no results
        results = self.manager.search_apartments(min_rent=3000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "No apartments match the search criteria.")

    def test_generate_outstanding_report(self):
        # Test case 1: Outstanding balance exists
        self.manager.tenants[0].balance_due = 500  # Alice has an outstanding balance
        self.manager.tenants[1].balance_due = 300  # Bob has an outstanding balance
        report = self.manager.generate_outstanding_report()
        self.assertIn("Alice: $500", report)
        self.assertIn("Bob: $300", report)

        # Test case 2: No outstanding balances
        self.manager.tenants[0].balance_due = 0
        self.manager.tenants[1].balance_due = 0
        report = self.manager.generate_outstanding_report()
        self.assertEqual(report, "No outstanding balances found.")

    def test_calculate_average_rent(self):
        # Test case 1: Apartments exist
        result = self.manager.calculate_average_rent()
        self.assertIn("The average rent of all apartments is $1750.00", result)  # (1500 + 2000) / 2 = 1750

        # Test case 2: No apartments
        self.manager.apartments = []  # Clear all apartments
        result = self.manager.calculate_average_rent()
        self.assertIn("The average rent of all apartments is $0.00", result)
