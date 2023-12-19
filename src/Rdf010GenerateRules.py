"""Generate rules
Rdf010GenerateRules.py
T. Masuda, 2023/12/11
"""


def main_rules_number_100():
    """Generate next_number for symbolic numbers

    Returns:
        None
    """

    """
    VAL:fact_next_number_1_2
    VAL:type VAL:fact ;
    VAL:operation VAL:next_number ;
    VAL:variable_x VAL:one ;
    VAL:variable_y VAL:two .
    """
    lines = []
    lines_out = []
    with open('../rules/rules_number_100/rules_next_number_100.template', 'r') as template_file:
        lines = template_file.readlines()
    for line in lines:
        if line.find('## insert ##') >= 0:
            for i in range(1, 99):
                lines_out.append(f'VAL:fact_next_number_{str(i)}_{str(i+1)}\n')
                lines_out.append(f'\tVAL:type VAL:fact ;\n')
                lines_out.append(f'\tVAL:operation VAL:next_number ;\n')
                lines_out.append(f'\tVAL:variable_x VAL:{str(i)} ;\n')
                lines_out.append(f'\tVAL:variable_y VAL:{str(i+1)} .\n')
                lines_out.append(f'\n')
        else:
            lines_out.append(line)
    with open('../rules/rules_number_100/rules_next_number_100.ttl', 'w') as output_file:
        output_file.writelines(lines_out)
    pass


if __name__ == '__main__':
    main_rules_number_100()
    