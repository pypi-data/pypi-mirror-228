"""**Evaluation** chains for grading LLM and Chain outputs.

This module contains off-the-shelf evaluation chains for grading the output of
LangChain primitives such as language models and chains.

**Loading an evaluator**

To load an evaluator, you can use the :func:`load_evaluators <langchain_xfyun.evaluation.loading.load_evaluators>` or
:func:`load_evaluator <langchain_xfyun.evaluation.loading.load_evaluator>` functions with the
names of the evaluators to load.

.. code-block:: python

    from langchain_xfyun.evaluation import load_evaluator

    evaluator = load_evaluator("qa")
    evaluator.evaluate_strings(
        prediction="We sold more than 40,000 units last week",
        input="How many units did we sell last week?",
        reference="We sold 32,378 units",
    )

The evaluator must be one of :class:`EvaluatorType <langchain_xfyun.evaluation.schema.EvaluatorType>`.

**Datasets**

To load one of the LangChain HuggingFace datasets, you can use the :func:`load_dataset <langchain_xfyun.evaluation.loading.load_dataset>` function with the
name of the dataset to load.

.. code-block:: python

        from langchain_xfyun.evaluation import load_dataset
        ds = load_dataset("llm-math")

**Some common use cases for evaluation include:**

- Grading the accuracy of a response against ground truth answers: :class:`QAEvalChain <langchain_xfyun.evaluation.qa.eval_chain.QAEvalChain>`
- Comparing the output of two models: :class:`PairwiseStringEvalChain <langchain_xfyun.evaluation.comparison.eval_chain.PairwiseStringEvalChain>` or :class:`LabeledPairwiseStringEvalChain <langchain_xfyun.evaluation.comparison.eval_chain.LabeledPairwiseStringEvalChain>` when there is additionally a reference label.
- Judging the efficacy of an agent's tool usage: :class:`TrajectoryEvalChain <langchain_xfyun.evaluation.agents.trajectory_eval_chain.TrajectoryEvalChain>`
- Checking whether an output complies with a set of criteria: :class:`CriteriaEvalChain <langchain_xfyun.evaluation.criteria.eval_chain.CriteriaEvalChain>` or :class:`LabeledCriteriaEvalChain <langchain_xfyun.evaluation.criteria.eval_chain.LabeledCriteriaEvalChain>` when there is additionally a reference label.
- Computing semantic difference between a prediction and reference: :class:`EmbeddingDistanceEvalChain <langchain_xfyun.evaluation.embedding_distance.base.EmbeddingDistanceEvalChain>` or between two predictions: :class:`PairwiseEmbeddingDistanceEvalChain <langchain_xfyun.evaluation.embedding_distance.base.PairwiseEmbeddingDistanceEvalChain>` 
- Measuring the string distance between a prediction and reference :class:`StringDistanceEvalChain <langchain_xfyun.evaluation.string_distance.base.StringDistanceEvalChain>` or between two predictions :class:`PairwiseStringDistanceEvalChain <langchain_xfyun.evaluation.string_distance.base.PairwiseStringDistanceEvalChain>`

**Low-level API**

These evaluators implement one of the following interfaces:

- :class:`StringEvaluator <langchain_xfyun.evaluation.schema.StringEvaluator>`: Evaluate a prediction string against a reference label and/or input context.
- :class:`PairwiseStringEvaluator <langchain_xfyun.evaluation.schema.PairwiseStringEvaluator>`: Evaluate two prediction strings against each other. Useful for scoring preferences, measuring similarity between two chain or llm agents, or comparing outputs on similar inputs.
- :class:`AgentTrajectoryEvaluator <langchain_xfyun.evaluation.schema.AgentTrajectoryEvaluator>` Evaluate the full sequence of actions taken by an agent.

These interfaces enable easier composability and usage within a higher level evaluation framework.

"""  # noqa: E501
from langchain_xfyun.evaluation.agents import TrajectoryEvalChain
from langchain_xfyun.evaluation.comparison import (
    LabeledPairwiseStringEvalChain,
    PairwiseStringEvalChain,
)
from langchain_xfyun.evaluation.criteria import (
    Criteria,
    CriteriaEvalChain,
    LabeledCriteriaEvalChain,
)
from langchain_xfyun.evaluation.embedding_distance import (
    EmbeddingDistance,
    EmbeddingDistanceEvalChain,
    PairwiseEmbeddingDistanceEvalChain,
)
from langchain_xfyun.evaluation.loading import load_dataset, load_evaluator, load_evaluators
from langchain_xfyun.evaluation.qa import ContextQAEvalChain, CotQAEvalChain, QAEvalChain
from langchain_xfyun.evaluation.schema import (
    AgentTrajectoryEvaluator,
    EvaluatorType,
    PairwiseStringEvaluator,
    StringEvaluator,
)
from langchain_xfyun.evaluation.string_distance import (
    PairwiseStringDistanceEvalChain,
    StringDistance,
    StringDistanceEvalChain,
)

__all__ = [
    "EvaluatorType",
    "PairwiseStringEvalChain",
    "LabeledPairwiseStringEvalChain",
    "QAEvalChain",
    "CotQAEvalChain",
    "ContextQAEvalChain",
    "StringEvaluator",
    "PairwiseStringEvaluator",
    "TrajectoryEvalChain",
    "CriteriaEvalChain",
    "Criteria",
    "EmbeddingDistance",
    "EmbeddingDistanceEvalChain",
    "PairwiseEmbeddingDistanceEvalChain",
    "StringDistance",
    "StringDistanceEvalChain",
    "PairwiseStringDistanceEvalChain",
    "LabeledCriteriaEvalChain",
    "load_evaluators",
    "load_evaluator",
    "load_dataset",
    "AgentTrajectoryEvaluator",
]
