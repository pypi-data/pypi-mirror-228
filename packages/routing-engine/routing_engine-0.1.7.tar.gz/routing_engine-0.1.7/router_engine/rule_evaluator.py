OPERATIONS = {
    'string': {
        'equals': lambda x, y: x == y,
        'contains': lambda x, y: y in x,
        'is_in': lambda x, y: x in y if isinstance(y, (list, tuple)) else False
    },
    'number': {
        'equals': lambda x, y: x == y,
        'greater_than': lambda x, y: x > y,
        'is_in': lambda x, y: x in y if isinstance(y, (list, tuple)) else False
    }
    # Add other types as needed
}



def resolve_reference(reference, context):
    parts = reference.split('.')
    obj = context.get(parts[0])

    if obj is None:
        return None

    for part in parts[1:]:
        obj = getattr(obj, part, None)
        if obj is None:
            return None

    return obj

def evaluate_condition(condition, context):
    if 'and' in condition:
        return all(evaluate_condition(c, context) for c in condition['and'])
    elif 'or' in condition:
        return any(evaluate_condition(c, context) for c in condition['or'])
    else:
        arg1 = resolve_arg(condition['arg1'], context)
        arg2 = resolve_arg(condition['arg2'], context)
        operation = condition['operation']
        arg_type = condition.get('type', 'generic')
        
        return evaluate_operation(operation, arg1, arg2, arg_type)

def resolve_arg(argument, context):
    if argument['type'] == 'reference':
        return resolve_reference(argument['value'], context)
    elif argument['type'] == 'static':
        return argument['value']
    else:
        raise ValueError(f"Unsupported argument type: {argument['type']}")

def evaluate_operation(operation, arg1, arg2, arg_type):

    operations_for_type = OPERATIONS.get(arg_type)
    if not operations_for_type:
        raise ValueError(f"Unsupported argument type: {arg_type}")

    operation_function = operations_for_type.get(operation)
    if not operation_function:
        raise ValueError(f"Unsupported operation for type {arg_type}: {operation}")

    return operation_function(arg1, arg2)
