from simpleai.search import CspProblem, backtrack

def constraint_nho_hon_1(variables, values):
    return values[0] + 1 <= values[1]

def constraint_nho_hon_2(variables, values):
    return values[0] + 2 <= values[1]

def constraint_nho_hon_10(variables, values):
    return values[0] + 10 <= values[1]

def constraint_inspect(variables, values):
    return values[0] + 3 <= values[1]

def disjunctive_constraint(variables, values):
    if values[0] < values[1]:
        return values[0] + 10 <= values[1]
    else:
        return values[1] + 10 <= values[0]

if __name__=='__main__':
    names = ('AxleF', 'AxleB', 
             'WheelRF', 'WheelLF', 'WheelRB', 'WheelLB',
             'NutRF', 'NutLF', 'NutRB', 'NutLB',
             'CapRF', 'CapLF', 'CapRB', 'CapLB',
             'Inspect')
    domains = {
        'AxleF': list(range(0,31)),
        'AxleB': list(range(0,31)),
        'WheelRF': list(range(0,31)),
        'WheelLF': list(range(0,31)),
        'WheelRB': list(range(0,31)),
        'WheelLB': list(range(0,31)),
        'NutRF': list(range(0,31)),
        'NutLF': list(range(0,31)),
        'NutRB': list(range(0,31)),
        'NutLB': list(range(0,31)),
        'CapRF': list(range(0,31)),
        'CapLF': list(range(0,31)),
        'CapRB': list(range(0,31)),
        'CapLB': list(range(0,31)),
        'Inspect': list(range(0,31))
    }

    constraints = [
        (('AxleF', 'WheelRF'), constraint_nho_hon_10),
        (('AxleF', 'WheelLF'), constraint_nho_hon_10),
        (('AxleB', 'WheelRB'), constraint_nho_hon_10),
        (('AxleB', 'WheelLB'), constraint_nho_hon_10),

        (('WheelRF', 'NutRF'), constraint_nho_hon_1),
        (('WheelLF', 'NutLF'), constraint_nho_hon_1),
        (('WheelRB', 'NutRB'), constraint_nho_hon_1),
        (('WheelLB', 'NutLB'), constraint_nho_hon_1),

        (('NutRF', 'CapRF'), constraint_nho_hon_2),
        (('NutLF', 'CapLF'), constraint_nho_hon_2),
        (('NutRB', 'CapRB'), constraint_nho_hon_2),
        (('NutLB', 'CapLB'), constraint_nho_hon_2),

        (('CapRF', 'Inspect'), constraint_nho_hon_1),
        (('CapLF', 'Inspect'), constraint_nho_hon_1),
        (('CapRB', 'Inspect'), constraint_nho_hon_1),
        (('CapLB', 'Inspect'), constraint_nho_hon_1),

        (('AxleF', 'AxleB'), disjunctive_constraint)

    ]
    problem = CspProblem(names, domains, constraints)
    print('\nSolutions:\n:', backtrack(problem))