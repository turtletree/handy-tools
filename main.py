from plans import MedicalPlan, FamilyMedicalInsuranceOption

# This file is the main file that should be run to evaluate the best family medical insurance option.
# Update the consts in plans.py to reflect the medical insurance plans and their costs.
# Assumptions:
# 1. The family consists of a mom, dad, and baby.
# 2. The mom, dad, and baby can each have their own medical insurance plan, and can be on one or both plans
# 3. All expenses are in-network expenses
# 4. When contributing to HSA, the company match is treated as a bonus income
#    the employee contribution * tax_rate is treated as a bonus income or opportunity cost/income
#    If not favor this, the tax_rate should be set to 0

def main():
    mom_expenses, dad_expenses, baby_expenses, tax_rate = 10000, 500, 1000, 0

    realistic_example_evaluation(mom_expenses, dad_expenses, baby_expenses, tax_rate)

    # exhausitive_evaluation()

def realistic_example_evaluation(mom_expenses, dad_expenses, baby_expenses, tax_rate):
    options = get_all_plan_combinations()
    sorted_options = sorted(options, key=lambda option: option.get_total_cost(mom_expenses, dad_expenses, baby_expenses, tax_rate))

    best_option = sorted_options[0]
    print(f"Mom's expenses: {mom_expenses}, Dad's expenses: {dad_expenses}, Baby's expenses: {baby_expenses}, Tax rate: {tax_rate}")
    print ("Best Option:")
    print(best_option)
    print (f"Total estimated cost: {best_option.total_cost}")
    print(f"Mom's cost: {best_option.mom_plan.get_cost(mom_expenses, tax_rate)}")
    print(f"Dad's cost: {best_option.dad_plan.get_cost(dad_expenses, tax_rate)}")
    print()


def exhausitive_evaluation():
    options = get_all_plan_combinations()

    mom_expenses_list = [0, 500, 1000, 2000, 3000, 4000, 8000, 10000, 20000, 50000]
    dad_expenses_list = [0, 500, 1000, 2000, 3000, 4000, 8000, 10000, 20000, 50000]
    baby_expenses_list = [0, 500, 1000, 2000, 3000, 4000, 8000, 10000, 20000, 50000]
    tax_rate_list = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]

    best_option = None
    counter = 0
    for mom_expenses in mom_expenses_list:
        for dad_expenses in dad_expenses_list:
            for baby_expenses in baby_expenses_list:
                for tax_rate in tax_rate_list:
                    lowest_cost = float('inf')
                    for option in options:
                        total_cost = option.get_total_cost(mom_expenses, dad_expenses, baby_expenses, tax_rate)
                        if total_cost < lowest_cost:
                            lowest_cost = total_cost
                            best_option = option
                counter += 1
                print(f"New best option found:")
                print(f"Mom's expenses: {mom_expenses}, Dad's expenses: {dad_expenses}, Baby's expenses: {baby_expenses}, Tax rate: {tax_rate}")
                print(f"Option: {best_option}")
    print(f"Total number of best options: {counter}")

def get_all_plan_combinations():
    options = []
    # plan compositions consists of tuples of booleans, where each notes [includeSpouse, includeChildren]
    plan_compositions = [[False, False], [True, False], [False, True], [True, True]]
    for d in ["premera", "surest", None]:
        for m in ["cigna", "sph", None]:
            # for all options of dads plan, (dad only, dad + mom, dad + baby, dad + mom + baby)
            for i in plan_compositions:
                # for all options of moms plan, (mom only, mom + baby, mom + dad, mom + dad + baby)
                for j in plan_compositions:
                    # edge cases
                    if d is None and m is None:
                        continue
                    elif d is None:
                        if j == [True, True]:  # everyone is under moms plan only
                            mom_plan = MedicalPlan.make_plan(m, j[0], j[1])
                            option = FamilyMedicalInsuranceOption(f"None|{m}", None, mom_plan, mom_plan)
                            options.append(option)
                            continue
                        else:
                            continue
                    elif m is None:
                        if i == [True, True]:  # everyone is under dads plan only
                            dad_plan = MedicalPlan.make_plan(d, i[0], i[1])
                            option = FamilyMedicalInsuranceOption(f"{d}|None", dad_plan, None, dad_plan)
                            options.append(option)
                            continue
                        else:
                            continue
                    # normal cases
                    dad_plan = MedicalPlan.make_plan(d, i[0], i[1])
                    mom_plan = MedicalPlan.make_plan(m, j[0], j[1])
                    if i[1] and j[1]:  # baby is under both plans
                        option = FamilyMedicalInsuranceOption(f"{dad_plan.name}|{mom_plan.name}", dad_plan, mom_plan, "both")
                    elif i[1]:  # baby is under dads plan
                        option = FamilyMedicalInsuranceOption(f"{dad_plan.name}|{mom_plan.name}", dad_plan, mom_plan,
                                                              dad_plan)
                    elif j[1]:  # baby is under moms plan
                        option = FamilyMedicalInsuranceOption(f"{dad_plan.name}|{mom_plan.name}", dad_plan, mom_plan,
                                                              mom_plan)
                    else:
                        continue
                    options.append(option)
    return options


if __name__ == "__main__":
    main()
