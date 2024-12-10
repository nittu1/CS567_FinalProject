import datetime

class Apartment:
    def __init__(self, unit_number, bedrooms, bathrooms, rent):
        self.unit_number = unit_number
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.rent = rent
        self.is_available = True
        self.maintenance_requests = []

    def add_maintenance_request(self, request):
        self.maintenance_requests.append(request)
    def update_request_status(self, index, status):
        if 0 <= index < len(self.maintenance_requests):
            self.maintenance_requests[index]["status"] = status
    def calculate_annual_rent(self):
        return self.rent * 12
    def __str__(self):
        status = "Available" if self.is_available else "Occupied"
        return (f"Unit {self.unit_number}: {self.bedrooms}BR/{self.bathrooms}BA, "
                f"${self.rent}/month, Status: {status}")

class Tenant:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.balance_due = 0
        self.payment_history = []

    def make_payment(self, amount):
        self.balance_due -= amount
        self.payment_history.append({"amount": amount, "date": datetime.date.today()})
        return f"Payment of ${amount} made. Remaining balance: ${self.balance_due}"

    def get_payment_history(self):
        """Returns the payment history for the tenant."""
        return "\n".join([f"${p['amount']} on {p['date']}" for p in self.payment_history]) or "No payments made."

    def __str__(self):
        return f"{self.name} ({self.phone}, {self.email}, Balance Due: ${self.balance_due})"


class Lease:
    def __init__(self, tenant, apartment, start_date, end_date):
        self.tenant = tenant
        self.apartment = apartment
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        self.payments = []
        self.apartment.is_available = False

    def add_payment(self, amount, date):
        self.payments.append({"amount": amount, "date": date})
        self.tenant.balance_due -= amount

    def calculate_remaining_days(self):
        today = datetime.date.today()
        return (self.end_date - today).days if today <= self.end_date else 0

    def terminate_lease(self):
        self.apartment.is_available = True
        return f"Lease for {self.apartment.unit_number} terminated."

    def is_overdue(self):
        today = datetime.date.today()
        return today > self.end_date

    def __str__(self):
        payments_info = "\n".join(
            [f"${p['amount']} on {p['date']}" for p in self.payments]
        )
        return (f"Lease for {self.tenant.name} in {self.apartment.unit_number}: "
                f"{self.start_date} to {self.end_date}\nPayments:\n{payments_info}")

class ApartmentManager:
    def __init__(self):
        self.apartments = []
        self.tenants = []
        self.leases = []

    def add_apartment(self, unit_number, bedrooms, bathrooms, rent):
        self.apartments.append(Apartment(unit_number, bedrooms, bathrooms, rent))

    def add_tenant(self, name, phone, email):
        tenant = Tenant(name, phone, email)
        self.tenants.append(tenant)
        return tenant

    def lease_apartment(self, tenant_name, unit_number, start_date, end_date):
        tenant = next((t for t in self.tenants if t.name == tenant_name), None)
        apartment = next(
            (a for a in self.apartments if a.unit_number == unit_number), None
        )
        if tenant and apartment and apartment.is_available:
            lease = Lease(tenant, apartment, start_date, end_date)
            tenant.balance_due += apartment.rent
            self.leases.append(lease)
            return lease
        raise ValueError("Tenant or apartment not found, or apartment not available.")

    def search_apartments(self, min_rent=None, max_rent=None, bedrooms=None, bathrooms=None, min_bedrooms=None, max_bedrooms=None, min_bathrooms=None, max_bathrooms=None, include_occupied=False):
        results = []

        for apartment in self.apartments:
            if not include_occupied and not apartment.is_available:
                continue

            if min_rent is not None and apartment.rent < min_rent:
                continue
            if max_rent is not None and apartment.rent > max_rent:
                continue

            if bedrooms is not None and apartment.bedrooms != bedrooms:
                continue
            if bathrooms is not None and apartment.bathrooms != bathrooms:
                continue

            if min_bedrooms is not None and apartment.bedrooms < min_bedrooms:
                continue
            if max_bedrooms is not None and apartment.bedrooms > max_bedrooms:
                continue
            if min_bathrooms is not None and apartment.bathrooms < min_bathrooms:
                continue
            if max_bathrooms is not None and apartment.bathrooms > max_bathrooms:
                continue

            results.append(apartment)

        if not results:
            return ["No apartments match the search criteria."]
        
        return [
            f"Apartment {apartment.unit_number}: {apartment.bedrooms}BR/{apartment.bathrooms}BA, "
            f"${apartment.rent}/month, Status: {'Available' if apartment.is_available else 'Occupied'}"
            for apartment in results
        ]


    def list_apartments(self):
        return [str(a) for a in self.apartments]

    def list_tenants(self):
        return [str(t) for t in self.tenants]

    def list_leases(self):
        return [str(l) for l in self.leases]

    def overdue_payments(self):
        today = datetime.date.today()
        overdue = []
        for lease in self.leases:
            if lease.is_overdue() and lease.tenant.balance_due > 0:
                overdue.append(f"{lease.tenant.name} owes ${lease.tenant.balance_due}")
        return overdue

    def calculate_total_annual_rent(self):
        return sum(apartment.calculate_annual_rent() for apartment in self.apartments)
    def generate_lease_summary(self, unit_number):
        lease = next(
            (l for l in self.leases if l.apartment.unit_number == unit_number), None
        )
        if lease:
            payments_info = "\n".join(
                [f"${p['amount']} on {p['date']}" for p in lease.payments]
            )
            summary = (
                f"Lease Summary for Unit {unit_number}:\n"
                f"Tenant: {lease.tenant.name}\n"
                f"Contact: {lease.tenant.phone}, {lease.tenant.email}\n"
                f"Apartment: {lease.apartment.bedrooms}BR/{lease.apartment.bathrooms}BA, ${lease.apartment.rent}/month\n"
                f"Lease Period: {lease.start_date} to {lease.end_date}\n"
                f"Payments:\n{payments_info}\n"
                f"Outstanding Balance: ${lease.tenant.balance_due}\n"
            )
            return summary
        return "No active lease found for the specified unit number."

    def view_maintenance_requests(self, unit_number):
        apartment = next(
            (a for a in self.apartments if a.unit_number == unit_number), None
        )
        if apartment:
            if apartment.maintenance_requests:
                requests = "\n".join(apartment.maintenance_requests)
                return f"Maintenance Requests for Unit {unit_number}:\n{requests}"
            return f"No maintenance requests for Unit {unit_number}."
        return "Apartment not found."
    def generate_monthly_report(self, year, month):
        total_rent_collected = 0
        total_balance_due = 0

        for lease in self.leases:
            for payment in lease.payments:
                payment_date = datetime.datetime.strptime(payment["date"], "%Y-%m-%d").date()
                if payment_date.year == year and payment_date.month == month:
                    total_rent_collected += payment["amount"]
            total_balance_due += lease.tenant.balance_due

        return (f"Monthly Report for {month}/{year}\n"
                f"Total Rent Collected: ${total_rent_collected}\n"
                f"Total Outstanding Balances: ${total_balance_due}")

    def filter_tenants_by_balance(self, threshold):
        filtered_tenants = [tenant for tenant in self.tenants if tenant.balance_due > threshold]
        if filtered_tenants:
            return [str(tenant) for tenant in filtered_tenants]
        return "No tenants with balance above the specified threshold."

    def apartment_occupancy_report(self):
        total_units = len(self.apartments)
        occupied_units = len([apt for apt in self.apartments if not apt.is_available])
        occupancy_rate = (occupied_units / total_units) * 100 if total_units else 0
        return (f"Total Apartments: {total_units}\n"
                f"Occupied Apartments: {occupied_units}\n"
                f"Occupancy Rate: {occupancy_rate:.2f}%")

    def view_tenant_profile(self, tenant_name):
        tenant = next((t for t in self.tenants if t.name == tenant_name), None)
        if tenant:
            leases = [l for l in self.leases if l.tenant == tenant]
            lease_info = "\n".join([str(l) for l in leases])
            return (f"Profile for {tenant_name}:\n"
                    f"Contact: {tenant.phone}, {tenant.email}\n"
                    f"Balance Due: ${tenant.balance_due}\n"
                    f"Leases:\n{lease_info}")
        return "Tenant not found."

    def assign_maintenance_staff(self, unit_number, staff_name):
        apartment = next((a for a in self.apartments if a.unit_number == unit_number), None)
        if apartment:
            if apartment.maintenance_requests:
                for request in apartment.maintenance_requests:
                    if request["status"] == "Pending":
                        request["staff"] = staff_name
                return f"Staff {staff_name} assigned to pending requests for Unit {unit_number}."
            return f"No pending maintenance requests for Unit {unit_number}."
        return "Apartment not found."


    def apply_late_fees(self, late_fee):
        for tenant in self.tenants:
            if tenant.balance_due > 0:
                tenant.balance_due += late_fee
        return f"Late fee of ${late_fee} applied to all tenants with outstanding balances."

    def extend_lease(self, unit_number, new_end_date):
        lease = next((l for l in self.leases if l.apartment.unit_number == unit_number), None)
        if lease:
            old_end_date = lease.end_date
            lease.end_date = datetime.datetime.strptime(new_end_date, "%Y-%m-%d").date()
            return (f"Lease for Unit {unit_number} extended from {old_end_date} to {lease.end_date}.")
        return "No active lease found for the specified unit."

    def track_maintenance_status(self):
        status_report = []
        for apartment in self.apartments:
            if apartment.maintenance_requests:
                for req in apartment.maintenance_requests:
                    status_report.append(
                        f"Unit {apartment.unit_number}: {req['request']} (Status: {req['status']}, Assigned: {req.get('staff', 'None')})"
                    )
        return "\n".join(status_report) if status_report else "No maintenance requests found."

    def track_overdue_leases(self):
        overdue = []
        for lease in self.leases:
            if lease.is_overdue():
                overdue.append(f"Lease for Unit {lease.apartment.unit_number} (Tenant: {lease.tenant.name}) is overdue.")
        return "\n".join(overdue) if overdue else "No overdue leases found."


    def generate_outstanding_report(self):
        report = []
        for tenant in self.tenants:
            if tenant.balance_due > 0:
                report.append(f"{tenant.name}: ${tenant.balance_due}")
        return "\n".join(report) if report else "No outstanding balances found."

    def calculate_average_rent(self):
        total_rent = sum(apartment.rent for apartment in self.apartments)
        average_rent = total_rent / len(self.apartments) if self.apartments else 0
        return f"The average rent of all apartments is ${average_rent:.2f}."

    def delete_apartment(self, unit_number):
        apartment = next((a for a in self.apartments if a.unit_number == unit_number), None)
        if apartment:
            self.apartments.remove(apartment)
            return f"Apartment Unit {unit_number} deleted."
        return "Apartment not found."

    def get_maintenance_summary(self):
        """Provides a summary of all maintenance requests."""
        summary = []
        for apartment in self.apartments:
            if apartment.maintenance_requests:
                for req in apartment.maintenance_requests:
                    summary.append(
                        f"Unit {apartment.unit_number}: {req['request']} (Status: {req['status']}, Staff: {req.get('staff', 'Unassigned')})"
                    )
        return "\n".join(summary) if summary else "No maintenance requests found."


    def delete_tenant(self, tenant_name):
        tenant = next((t for t in self.tenants if t.name == tenant_name), None)
        if tenant:
            self.tenants.remove(tenant)
            return f"Tenant {tenant_name} deleted."
        return "Tenant not found."