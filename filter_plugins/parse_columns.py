import re
import yaml

from ansible.module_utils.network.common.utils import Template

DEFAULT_TEMPLATE = '{{ value.strip() }}'


def filter_parse_columns(val, column_def_file):
    with open(column_def_file, 'r') as fd:
        column_def = yaml.safe_load(fd)

    match_start_block = (
        re.compile(column_def['start_block']) if 'start_block' in column_def
        else None
    )

    match_start_table = (
        re.compile(column_def['start_table']) if 'start_table' in column_def
        else None
    )

    match_end_table = (
        re.compile(column_def['end_table']) if 'end_table' in column_def
        else None
    )

    in_block = match_start_block is None
    in_table = match_start_table is None
    lines = val.splitlines()
    rows = []
    template = Template()

    for line in lines:
        if not in_block:
            if match_start_block and match_start_block.match(line):
                in_block = True
            continue

        if not in_table:
            if match_start_table and match_start_table.match(line):
                in_table = True
            continue

        if match_end_table and match_end_table.match(line):
            break

        row = {}
        for coldef in column_def['columns']:
            if 'start' in coldef and 'end' in coldef:
                val1 = line[coldef['start']:coldef['end']]
            else:
                val1 = None

            val2 = template(coldef.get('value', DEFAULT_TEMPLATE),
                            {'value': val1, 'obj': row})
            # template() returns None if the result of template
            # expansion is empty, which will break the subsequent
            # re.match.
            if val2 is None:
                val2 = ''

            if 'check' in coldef:
                if not re.match(coldef['check'], val2):
                    raise ValueError(val2)

            row[coldef['name']] = val2
        rows.append(row)

    return rows


class FilterModule(object):
    filter_map = {
        'parse_columns': filter_parse_columns,
    }

    def filters(self):
        return self.filter_map
