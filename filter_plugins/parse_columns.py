import re
import yaml


def filter_parse_columns(val, column_def_file):
    with open(column_def_file, 'r') as fd:
        column_def = yaml.safe_load(fd)

    match_start = (
        re.compile(column_def['start_block']) if 'start_block' in column_def
        else None
    )

    match_end = (
        re.compile(column_def['end_block']) if 'end_block' in column_def
        else None
    )

    started = match_start is None
    lines = val.splitlines()
    rows = []

    for line in lines:
        if not started:
            if match_start and match_start.match(line):
                started = True
            continue

        if match_end and match_end.match(line):
            break

        row = {}
        for col, coldef in column_def['columns'].items():
            val = line[coldef['start']:coldef['end']]

            if not coldef.get('no_strip', False):
                val = val.strip()

            if 'check' in coldef:
                if not re.match(coldef['check'], val):
                    raise ValueError(val)

            row[col] = val
        rows.append(row)

    return rows


class FilterModule(object):
    filter_map = {
        'parse_columns': filter_parse_columns,
    }

    def filters(self):
        return self.filter_map
