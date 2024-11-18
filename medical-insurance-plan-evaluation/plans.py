# 2025 Medical Plan Options and limit
HSA_FAMILY_CONTRIBUTION_LIMIT = 8550
HSA_INDIVIDUAL_CONTRIBUTION_LIMIT = 4300
MEDICAL_PLANS = {
    # each plan has 4 compositions: EE only, EE + Spouse, EE + Children, EE + Family
    # each composition has default attributes: premium, deductible, oopm, hsa_company_match, hsa_employee_contribution
    "premera": [
        [0, 1750, 2750, 1000, HSA_INDIVIDUAL_CONTRIBUTION_LIMIT - 1000],
        [0, 3500, 5500, 2000, HSA_FAMILY_CONTRIBUTION_LIMIT - 2000],
        [0, 3500, 5500, 2000, HSA_FAMILY_CONTRIBUTION_LIMIT - 2000],
        [0, 4375, 6875, 2500, HSA_FAMILY_CONTRIBUTION_LIMIT - 2500]
    ],

    "surest": [
        [0, 0, 2750, 0, 0],
        [0, 0, 5500, 0, 0],
        [0, 0, 5500, 0, 0],
        [0, 0, 6875, 0, 0]
    ],

    "cigna": [
        [240, 1650, 3300, 1000, HSA_INDIVIDUAL_CONTRIBUTION_LIMIT - 1000],
        [960, 3300, 6600, 2000, HSA_FAMILY_CONTRIBUTION_LIMIT - 2000],
        [840, 3300, 6600, 2000, HSA_FAMILY_CONTRIBUTION_LIMIT - 2000],
        [1200, 3300, 6600, 2000, HSA_FAMILY_CONTRIBUTION_LIMIT - 2000]
    ],

    "sph": [
        [240, 0, 2000, 0, 0],
        [960, 0, 4000, 0, 0],
        [840, 0, 4000, 0, 0],
        [1200, 0, 4000, 0, 0]
    ]
}


class MedicalPlan:
    def __init__(self, name, premium, deductible, oopm, cm, hec, spouse, children):
        # built in plan attributes
        self.name = name
        self.premium = premium
        self.deductible = deductible
        self.oopm = oopm
        # variable arguments
        self.spouse = spouse
        self.children = children
        # calculated attributes
        self.company_match = cm
        self.hsa_employee_contribution = hec

    @classmethod
    def make_plan(cls, name, spouse, children):
        if name == "premera":
            return Premera(spouse, children)
        elif name == "surest":
            return Surest(spouse, children)
        elif name == "cigna":
            return Cigna(spouse, children)
        elif name == "sph":
            return SPH(spouse, children)
        else:
            raise ValueError(f"Unknown plan name: {name}")

    def get_name(self):
        return self.name

    def get_tax_saving(self, tax_rate):
        return self.hsa_employee_contribution * tax_rate

    def get_cost(self, expenses, tax_rate):
        tax_saving = self.get_tax_saving(tax_rate)
        if expenses > self.oopm:
            return self.premium + self.oopm - self.company_match - tax_saving
        return self.premium + expenses - self.company_match - tax_saving

    def __repr__(self):
        return (f"{self.name}:(premium={self.premium}, deductible={self.deductible}, "
                f"oopm={self.oopm}, company_match={self.company_match}, hsa_employee_contribution={self.hsa_employee_contribution}, "
                f"spouse={self.spouse}, children={self.children})")


class Premera(MedicalPlan):
    def __init__(self, spouse, children):
        if spouse and children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["premera"][3]
        elif spouse or children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["premera"][1]
        else:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["premera"][0]
        super().__init__("premera", premium, deductible, oopm, company_match, hsa_employee_contribution, spouse,
                         children)


class Surest(MedicalPlan):
    def __init__(self, spouse, children):
        if spouse and children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["surest"][3]
        elif spouse or children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["surest"][1]
        else:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["surest"][0]
        super().__init__("surest", premium, deductible, oopm, company_match, hsa_employee_contribution, spouse,
                         children)


class Cigna(MedicalPlan):
    def __init__(self, spouse, children):
        if spouse and children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["cigna"][3]
        elif spouse:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["cigna"][1]
        elif children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["cigna"][2]
        else:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["cigna"][0]
        super().__init__("cigna", premium, deductible, oopm, company_match, hsa_employee_contribution, spouse, children)


class SPH(MedicalPlan):
    def __init__(self, spouse, children):
        if spouse and children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["sph"][3]
        elif spouse:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["sph"][1]
        elif children:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["sph"][2]
        else:
            premium, deductible, oopm, company_match, hsa_employee_contribution \
                = MEDICAL_PLANS["sph"][0]
        super().__init__("sph", premium, deductible, oopm, company_match, hsa_employee_contribution, spouse, children)


class FamilyMedicalInsuranceOption:
    def __init__(self, name, dad_plan, mom_plan, baby_plan):
        self.name = name
        self.mom_plan = mom_plan
        self.dad_plan = dad_plan
        self.baby_plan = baby_plan
        self.total_cost = 0

    def __str__(self):
        return (f"Option: {self.get_name()}\n"
                f"Mom: {self.mom_plan}\n"
                f"Dad: {self.dad_plan}\n"
                f"Baby: {self.baby_plan}\n"
                f"Total_cost: {self.total_cost}\n")

    def get_name(self):
        baby_plan = "both" if self.baby_plan == "both" else self.baby_plan.name
        mom_plan = "None" if self.mom_plan is None else self.mom_plan.name
        dad_plan = "None" if self.dad_plan is None else self.dad_plan.name
        return f"{mom_plan}|{dad_plan}|{baby_plan}"

    def get_total_cost(self, m, d, b, tax_rate):
        if self.mom_plan is None:  # everyone is under dads plan
            self.total_cost = self.dad_plan.get_cost(m + d + b, tax_rate) + 75*24 # penalty
        elif self.dad_plan is None:  # everyone is under moms plan
            self.total_cost = self.mom_plan.get_cost(m + d + b, tax_rate)
        else:
            if self.baby_plan == "both":  # baby's primary insurance is moms plan since mom's birthdate is earlier in the year compared to dad's
                self.total_cost = self.dad_plan.get_cost(d, tax_rate) + self.mom_plan.get_cost(m + b, tax_rate)
            elif self.baby_plan == self.dad_plan:  # baby is under dad's plan
                self.total_cost = self.dad_plan.get_cost(d + b, tax_rate) + self.mom_plan.get_cost(m, tax_rate)
            elif self.baby_plan == self.mom_plan:  # baby is under mom's plan
                self.total_cost = self.dad_plan.get_cost(d, tax_rate) + self.mom_plan.get_cost(m + b, tax_rate)
            else:
                raise ValueError(f"Unknown baby plan: {self.baby_plan}")
        return self.total_cost
