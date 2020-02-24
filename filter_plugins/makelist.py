def filter_makelist(val):
    if isinstance(val, list):
        return val
    else:
        return [val]


class FilterModule(object):
    filter_map = {
        'makelist': filter_makelist,
    }

    def filters(self):
        return self.filter_map
