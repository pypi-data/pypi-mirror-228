from .._req_builder import _list_dataitem
from ..._common.const import CompanyRelAttributeType as _CompanyRelAttributeType
from ..._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent
from ..._utils import _get_params, _validate_args
from ..._utils.exceptions import PrismValueError


__all__ = [
    "competitor",
    "description",
    "product",
    "relationship",
]


_data_category = __name__.split(".")[-1]


class _PrismCompanyComponent(_PrismDataComponent, _PrismComponent):
    _component_category_repr = _data_category


class competitor(_PrismCompanyComponent):
    @_validate_args
    def __init__(
        self,
        target: bool,
        attribute: _CompanyRelAttributeType,
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class description(_PrismCompanyComponent):
    @_validate_args
    def __init__(
        self,
        long: bool,
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class product(_PrismCompanyComponent):
    @_validate_args
    def __init__(
        self,
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))


class relationship(_PrismCompanyComponent):
    @_validate_args
    def __init__(
        self,
        target: bool,
        attribute: _CompanyRelAttributeType,
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))
