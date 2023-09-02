from .._req_builder import _list_dataitem
from ..._common.const import CompanyRelAttributeType as _CompanyRelAttributeType
from ..._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent
from ..._utils import _get_params, _validate_args
from ..._utils.exceptions import PrismValueError


__all__ = [
    "ma",
    "buyback",
    "dataitems",
]


_data_category = __name__.split(".")[-1]


class _PrismTransactionComponent(_PrismDataComponent, _PrismComponent):
    _component_category_repr = _data_category

    @classmethod
    def _dataitems(cls, search : str = None, package : str = None):
        return _list_dataitem(
            datacategoryid=cls.categoryid,
            datacomponentid=cls.componentid,
            search=search,
            package=package,
        )


class ma(_PrismTransactionComponent):
    @_validate_args
    def __init__(
        self,
        dataitemid: int,
        target: bool,
        attribute: _CompanyRelAttributeType,
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search : str = None, package : str = None):
        return cls._dataitems(search=search, package=package)


class buyback(_PrismTransactionComponent):
    @_validate_args
    def __init__(
        self,
        currency: str = "report",
        package : str = None,
    ):
        super().__init__(**_get_params(vars()))

    @classmethod
    @_validate_args
    def dataitems(cls, search : str = None, package : str = None):
        return cls._dataitems(search=search, package=package)


@_validate_args
def dataitems(search: str = None, package: str = None):
    return _list_dataitem(
            datacategoryid=_PrismTransactionComponent.categoryid,
            datacomponentid=None,
            search=search,
            package=package,
        )