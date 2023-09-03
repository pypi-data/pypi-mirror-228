# Extensions to Frictionless Framework

from frictionless import Plugin, checks, errors, system
from functools import reduce
import simpleeval

class DataforgePlugin(Plugin):
    
    def create_check(self, name, *, descriptor=None):
        return BaselineExtended(descriptor)

class BaselineExtended(checks.baseline):
    """Add validation of row constraints specified in schema
    
    Patterned after frictionless.checks.row_constraint()
    """
    
    Errors = checks.baseline.Errors + [errors.RowConstraintError]
    
    # resource.schema appears to not be available during initialization, so we
    # access it here; any way to avoid doing this repeatedly for every row?
    # We could use @cached_property, though that might have undesirable
    # consequences.
    @property
    def row_constraints(self):
        return reduce(lambda d, k: d.get(k) if d else [],
                      ['custom','dataforge:rowConstraints'], self.resource.schema)
    
    def validate_row(self, row):
        
        result = row.errors
        for constraint in self.row_constraints:
            try:
                evalclass = simpleeval.EvalWithCompoundTypes
                assert evalclass(names=row).eval(constraint)
            except Exception:
                result.append(errors.RowConstraintError.from_row(row,
                    note='the row constraint to conform is "%s"' % constraint)
                )
        yield from result

system.register('dataforge', DataforgePlugin())
