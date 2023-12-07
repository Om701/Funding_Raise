from datetime import datetime
class Project:
    def __init__(self, title, details, target_amount, start_date, end_date, owner):
        self.title = title
        self.details = details
        self.target_amount = target_amount
        self.start_date = datetime.strptime(start_date, '%d-%m-%Y')
        self.end_date = datetime.strptime(end_date, '%d-%m-%Y')
        self.owner = owner
        self.current_fund = 0