from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Generic, List, Optional, Sequence, TypeVar, Union

import pydantic
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from great_expectations.datasource.fluent.interfaces import Batch


class MetricRepositoryBaseModel(BaseModel):
    """Base class for all MetricRepository related models."""

    class Config:
        extra = pydantic.Extra.forbid


class MetricException(MetricRepositoryBaseModel):
    exception_type: Optional[str] = Field(
        description="Exception type if an exception is thrown", default=None
    )
    exception_message: Optional[str] = Field(
        description="Exception message if an exception is thrown", default=None
    )


_ValueType = TypeVar("_ValueType")


class Metric(MetricRepositoryBaseModel, Generic[_ValueType]):
    """Abstract computed metric. Domain, value and parameters are metric dependent.

    Note: This implementation does not currently take into account
    other domain modifiers, e.g. row_condition, condition_parser, ignore_row_if
    """

    def __new__(cls, *args, **kwargs):
        if cls is Metric:
            raise NotImplementedError("Metric is an abstract class.")
        instance = super().__new__(cls)
        return instance

    id: uuid.UUID = Field(description="Metric id")
    batch: Batch = Field(description="Batch")
    metric_name: str = Field(description="Metric name")
    value: _ValueType = Field(description="Metric value")
    exception: MetricException = Field(description="Exception info if thrown")

    @classmethod
    def update_forward_refs(cls):
        from great_expectations.datasource.fluent.interfaces import Batch

        super().update_forward_refs(
            Batch=Batch,
        )


# Metric domain types


class TableMetric(Metric, Generic[_ValueType]):
    pass


class ColumnMetric(Metric, Generic[_ValueType]):
    column: str = Field(description="Column name")


# TODO: Add ColumnPairMetric, MultiColumnMetric


# Metrics with parameters (aka metric_value_kwargs)
# This is where the concrete metric types are defined that
# bring together a domain type, value type and any parameters (aka metric_value_kwargs)

# TODO: Add metrics here for all Column Descriptive Metrics
#  QuantileValuesColumnMetric is an example of a metric that has parameters


class QuantileValuesColumnMetric(ColumnMetric[List[float]]):
    quantiles: List[float] = Field(description="Quantiles to compute")
    allow_relative_error: Union[str, float] = Field(
        description="Relative error interpolation type (pandas) or limit (e.g. spark) depending on data source"
    )


class MetricRun(MetricRepositoryBaseModel):
    """Collection of Metric objects produced during the same execution run."""

    id: uuid.UUID = Field(description="Run id")
    # created_at, created_by filled in by the backend.
    metrics: Sequence[Metric]
