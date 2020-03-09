import inspect


def call_callable_dynamic_args(func, *args, **kwargs):
    spec = inspect.getfullargspec(func)
    call_args = []

    for i in range(len(spec.args)):
        if i < len(args):
            call_args.append(args[i])
        elif spec.args[i] in kwargs:
            call_args.append(kwargs[spec.args[i]])
            del kwargs[spec.args[i]]

    # inject eventually still missing var args
    if spec.varargs and len(args) > len(spec.args) and len(args) > len(call_args):
        call_args += args[len(call_args):]

    # inject kwargs if we have some left overs
    if spec.varkw:
        return func(*call_args, **kwargs)
    else:
        return func(*call_args)


def suitable_kwargs(func, **kwargs):
    suitable_args = inspect.getfullargspec(func).args
    return {arg: kwargs[arg] for arg in kwargs.keys() if arg in suitable_args}
