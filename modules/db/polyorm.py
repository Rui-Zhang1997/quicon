import re

class Query:
    def __init__(self, table):
        self.table = table
    
    def gq(self):
        raise NotImplementedError

class Insert(Query):
    def __init__(self, table):
        Query.__init__(self, table)
        self.fields = []
        self.values = []
        self.update_fields = {}

    def set_fields(self, fields):
        self.fields += fields
    
    def add_values(self, values):
        self.values.append(values)

    def set_update_fields(self, updates):
        self.update_fields = updates
    
    def gq(self):
        fields_str = ', '.join(self.fields)
        values_str = ', '.join(['(' + ', '.join(['"%s"' % v if isinstance(v, str) else str(v) for v in vs]) + ')' for vs in self.values])
        update_keys = ', '.join(['%s=%s' % (x, y) for x, y in self.update_fields.items()])
        return 'insert into %s (%s) values %s %s;' % (self.table, fields_str, values_str,
               ('on duplicate key update %s' % update_keys) if len(self.update_fields) > 0 else '')
