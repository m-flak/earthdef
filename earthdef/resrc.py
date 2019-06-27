import os
from earthdef import MODULE_NAME

#pkg_resources doesnt work on windows, this is equivalent
MODULE_ROOT = os.path.join(os.getcwd(), MODULE_NAME)

# Arguments 1 -> x are subdirectories
# # name = filename
def find_resource(*args, **kwargs) -> str:
    global MODULE_ROOT
    # concat dirs
    res_dir = os.path.join(MODULE_ROOT, 'data')
    res_dir = os.path.join(res_dir, *args)

    invalid = "Invalid"
    name = kwargs.get('name', invalid)
    if name is invalid:
        raise KeyError("Missing filename!")

    return os.path.join(res_dir, name)
