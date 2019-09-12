import enum
from typing import List


class IncludeDirectives(str, enum.Enum):
    """Categories of information that can optionally be requested
    These categories may be included in the include[] request parameter to
    request additional information in the response content.
    API docs: https://octopart.com/api/docs/v3/rest-api#include-directives
    """
    short_description = 'short_description'
    datasheets = 'datasheets'
    compliance_documents = 'compliance_documents'
    descriptions = 'descriptions'
    imagesets = 'imagesets'
    specs = 'specs'
    category_uids = 'category_uids'
    external_links = 'external_links'
    reference_designs = 'reference_designs'
    cad_models = 'cad_models'


def include_directives_from_kwargs(**kwargs) -> List[str]:
    """Turn "include_"-prefixed kwargs into list of strings for the request
    Arguments:
        All keyword arguments whose name consists of "include_*" and an
        entry of the INCLUDE enum are used to construct the output. All
        others are ignored.
    Known directives are included in the output if their value is truthy:
    >>> include_directives_from_kwargs(
    ...    include_datasheets=True, include_specs=True,
    ...    include_imagesets=False)
    ['datasheets', 'specs']
    Keyword args whose name starts with "include_" but don't match known
    directives trigger an exception:
    >>> include_directives_from_kwargs(include_abcdefg=True)
    Traceback (most recent call last):
        ...
    ValueError: abcdefg is not a known include directive
    However, keyword arguments not starting with "include_" are ignored
    silently:
    >>> include_directives_from_kwargs(abcdefg=True, include_specs=True)
    ['specs']
    """
    includes = []

    for kw_key, kw_val in kwargs.items():
        # filter for kwargs named include_* and value True
        if kw_key.startswith('include_') and kw_val:
            _, incl_key = kw_key.split('include_')
            # only accept documented values for the include directive
            if hasattr(IncludeDirectives, incl_key):
                includes.append(incl_key)
            else:
                raise ValueError(
                    f"{incl_key} is not a known include directive")

    return includes