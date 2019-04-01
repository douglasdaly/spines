##########
Parameters
##########

Spines models hold stores of :class:`spines.Parameter` objects.  These object
specify parameters that the model requires as well as any restrictions or
constraints on them.  There are different types of :class:`spines.Parameter`
classes aside from the basic one, but they share these common attributes:

name
    The name of the parameter.

value_type
    The type(s) of data that are allowed for the value of the parameter.

required
    Whether or not this parameter is required for the model.

default
    An optional default value for the parameter if it's not otherwise
    specified.
