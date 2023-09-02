from schema_validation import credit_line_validator


class GenerateDataStructure:
    def __init__(self,
                 credit_line: dict = None,
                 credit_request: dict = None,
                 contact: dict = None,
                 disbursements: list = None,
                 product: dict = None,
                 ) -> dict:

        self.credit_line = {
            "uid": "1",
            "created_at": 2,
            "balance": 0,
            "todayToPay": {
                "value": 497819.23,
                "total": 582662.65,
                "date": "2023-08-30",
                "last_quota": 448773.98
            }
        }
        self.credit_request = credit_request
        self.disbursements = disbursements
        self.product = product
        self.contact = contact
        self.error_messages = {}

        self.process()

    def process(self):
        errors = credit_line_validator(self.credit_line)

    def build_disbursement_information(self):
        line_data = {}
        total_disbursements = []
        total_disbursement = 0
        mora_amount_accumulated = 0
        total_accumulated = 0
        value_accumulated = 0
        total_amount_of_arrears = 0
        days_late_line = 0
        today_pay = self.credit_line.get("todayToPay", {})

        for app in self.disbursements:
            mora_amount = app.get("resume", {}).get("last_quota", {})
            total = app.get("resume", {}).get("total", {})
            value = app.get("resume", {}).get("value", {})
            days_late = app.get("days_late", 0)
            days_late_line = days_late if days_late > days_late_line else days_late_line
            inf_periods = {
                "periodicy": self.product.get("type", "")
            }
            expiration_date = "N/A"
            quotas_in_arrears = 0
            all_quotas = app.get("quotas", [])
            if all_quotas:
                expiration_date = all_quotas[-1].get("payment_date", "N/A")
                quotas_in_arrears = len([
                    quota for quota in all_quotas if quota.get('is_late') == 1])

            app["quotas_in_arrears"] = quotas_in_arrears
            app["quotas"] = all_quotas
            app["status"] = app.get("flow_state", "")
            app["expiration_date"] = expiration_date
            app["payment_date"] = today_pay.get("date", "N/A")
            app["moratorium_amount"] = mora_amount
            app["periods"] = inf_periods
            app["todayToPay"] = today_pay

            total_disbursements.append(app)
            total_amount_of_arrears += quotas_in_arrears
            mora_amount_accumulated += mora_amount
            total_accumulated += total
            value_accumulated += value
            total_disbursement += float(app.get("principal", 0))

        line_data['total'] = total_accumulated
        line_data['value'] = value_accumulated
        line_data['moratorium_amount'] = mora_amount_accumulated
        line_data['quotas_in_arrears'] = total_amount_of_arrears
        line_data['days_late'] = days_late_line
        line_data['product_uuid'] = self.product.get("uuid", "")
        line_data['product_name'] = self.product.get("name", "")
        line_data['disbursements'] = total_disbursements
        line_data['periods'] = inf_periods
        line_data['payment_date'] = today_pay.get("date", "N/A")
        line_data['created_at'] = str(self.credit_line.get("created_at", ""))
        line_data['amount_disbursed'] = self.credit_line.get("balance", 0)
        line_data['total_disbursement'] = total_disbursement
        data_credit_request = {
            "code": self.credit_request.get("code", ""),
            "approve_amount": self.credit_request.get("approve_amount", {}),
            "contact": self.contact,
        }
        line_data['credit_request'] = data_credit_request
        return line_data


data = GenerateDataStructure()
