from abc import ABC, abstractmethod

from pydantic import BaseModel

from chemchef.engine.indexing import FuzzyIndexCollection


class AbstractQueryExpression(ABC, BaseModel):

    def __and__(self, other: "AbstractQueryExpression") -> "AbstractQueryExpression":
        return And(left=self, right=other)

    def __or__(self, other: "AbstractQueryExpression") -> "AbstractQueryExpression":
        return Or(left=self, right=other)

    def __invert__(self) -> "AbstractQueryExpression":
        return Not(original=self)

    @abstractmethod
    def to_query(self) -> "AbstractQuery":
        raise NotImplementedError


class Exact(AbstractQueryExpression):
    """Returns documents where at least one value for the field is equal to at least one of the targets"""

    field: str
    targets: set[str]

    def to_query(self) -> "AbstractQuery":
        return ExactQuery(self.field, self.targets)


class Fuzzy(AbstractQueryExpression):
    """Returns documents where at least one value for the field is a synonym or hyponym of the target."""

    field: str
    target: str
    max_candidates: int = 50

    # max_candidates = the maximum number of candidates to retrieve from the vector DB
    # (These will then be filtered by the LLM.)

    def to_query(self) -> "AbstractQuery":
        return FuzzyQuery(self.field, self.target, self.max_candidates)


class And(AbstractQueryExpression):
    left: AbstractQueryExpression
    right: AbstractQueryExpression

    def to_query(self) -> "AbstractQuery":
        return AndQuery(self.left.to_query(), self.right.to_query())


class Or(AbstractQueryExpression):
    left: AbstractQueryExpression
    right: AbstractQueryExpression

    def to_query(self) -> "AbstractQuery":
        return OrQuery(self.left.to_query(), self.right.to_query())


class Not(AbstractQueryExpression):
    original: AbstractQueryExpression

    def to_query(self) -> "AbstractQuery":
        return AndNotQuery(AllQuery(), self.original.to_query())


class All(AbstractQueryExpression):

    def to_query(self) -> "AbstractQuery":
        return AllQuery()


class AbstractQuery:

    @abstractmethod
    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        """
        Runs query.
        :return: Set of document ids returned by query
        """
        raise NotImplementedError


class ExactQuery(AbstractQuery):

    def __init__(self, field: str, targets: set[str]) -> None:
        self._field = field
        self._targets = targets

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        return indexes.exact_query(self._field, self._targets)


class FuzzyQuery(AbstractQuery):

    def __init__(self, field: str, target: str, max_candidates: int) -> None:
        self._field = field
        self._target = target
        self._max_candidates = max_candidates

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        return indexes.fuzzy_query(self._field, self._target, self._max_candidates)


class AndQuery(AbstractQuery):

    def __init__(self, left_query: AbstractQuery, right_query: AbstractQuery) -> None:
        self._left_query = left_query
        self._right_query = right_query

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        left_results = self._left_query.run(indexes)
        right_results = self._right_query.run(indexes)
        return left_results.intersection(right_results)


class OrQuery(AbstractQuery):

    def __init__(self, left_query: AbstractQuery, right_query: AbstractQuery) -> None:
        self._left_query = left_query
        self._right_query = right_query

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        left_results = self._left_query.run(indexes)
        right_results = self._right_query.run(indexes)
        return left_results.union(right_results)


class AndNotQuery(AbstractQuery):
    """Returns documents that meet the condition of the left query and do not meet the condition of the right query"""

    def __init__(self, left_query: AbstractQuery, right_query: AbstractQuery) -> None:
        self._left_query = left_query
        self._right_query = right_query

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        left_results = self._left_query.run(indexes)
        right_results = self._right_query.run(indexes)
        return left_results.difference(right_results)


class AllQuery(AbstractQuery):

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        return indexes.all_doc_ids
