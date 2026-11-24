
class PerformanceRecord:
    def __init__(self, branch_name, report_date, performance_type, target, actual, notes=""):
        self.branch_name = branch_name
        self.report_date = report_date
        self.performance_type = performance_type
        self.target = target
        self.actual = actual
        self.notes = notes

    def is_valid(self):
        if not self.branch_name.strip():
            return False

        if not self.report_date.strip():
            return False

        if not self.performance_type.strip():
            return False

        if self.target <= 0:
            return False

        if self.actual < 0:
            return False

        return True

    def variance(self):
        return self.actual - self.target

    def achievement_rate(self):
        return (self.actual / self.target) * 100

    def status(self):
        if self.achievement_rate() >= 100:
            return "On Target"
        return "Below Target"
