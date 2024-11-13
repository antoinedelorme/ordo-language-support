
# OrdoLang: A Time Series-Centric Workflow Language

**Date**: 2024-11-12

## Overview

**OrdoLang** is an experimental programming language designed to specify complex task pipelines with sequential and parallel execution across multiple phases, all within an elegant JSON-like syntax. At its core, OrdoLang treats everything as a **time series**, enabling powerful and efficient manipulation of data over time. This time series perspective allows any object to be transformed into a `Series` object—a time-indexed sequence of objects—providing a unified framework for temporal data processing and analysis.

**Note**: OrdoLang serves as a flexible, human-readable blueprint for designing task pipelines, adaptable to multiple programming languages. It offers a clear framework for defining objects, methods, and task sequencing, making it ideal for creating cross-functional pipeline blueprints that can be implemented across various systems.

## Key Features

- **Time Series-Centric**: All objects can be transformed into time series (`Series` objects), allowing for consistent and powerful time-based operations.
- **Vectorizable Objects**: Certain objects support vectorized operations, enabling efficient computations over entire time series without explicit iteration.
- **Sequential and Parallel Execution**: Structured task execution across sequential phases, with parallelism for tasks within each phase.
- **Pipeline Definitions (Computational Graphs)**: Define reusable pipelines (graphs) that can be invoked within other tasks, similar to computational graphs in data processing frameworks.
- **Conditional Execution**: Tasks can be conditionally executed based on indicators or the results of other tasks, using the primitive `conditional` function within the JSON-like syntax.
- **Indicators**: Compute indicators that influence execution flow, facilitating decision-making in workflows.
- **Scheduling**: Tasks can be scheduled to run at specific times or intervals, enabling time-based workflows.
- **Header for Object and Method Definitions**: Clearly define objects, methods, and their expected input/output types, including time series transformations.
- **Dynamic Scoping and Data Flow**: Variables defined in one phase are accessible in subsequent phases, allowing for efficient data flow.

## Language Overview

An OrdoLang program is structured as a JSON-like array, where each element is a **phase** represented as an object with the phase name as the key.

- **Phases**: Execute sequentially from the first to the last in the array.
- **Tasks**: Execute in parallel within each phase unless dependencies specify otherwise.
- **Pipeline Definitions**: Reusable pipelines (graphs) can be defined and invoked within other tasks.
- **Time Series Operations**: Objects can be transformed into `Series` objects, supporting vectorized operations over time.
- **Conditional Execution**: Implemented using the primitive `conditional(indicator, task_if_true, task_if_false)`.
- **Scheduling**: Defined within tasks using a `schedule` property.
- **Indicators**: Tasks can compute indicators that influence subsequent task execution.

### New Concepts

#### Time Series and Vectorizable Objects

- **Series Objects**: Any object can be transformed into a `Series`, a time-indexed sequence of objects.
- **Vectorized Operations**: Certain objects support operations that apply over entire time series, enabling efficient computations without explicit loops.

#### Pipeline Definitions (Computational Graphs)

- **`pipelines` Section**: Define reusable pipelines that can be invoked within the main pipeline.
- **Pipeline Invocation**: Use pipelines within tasks by invoking them as needed.

#### Conditional Execution

- **`conditional(indicator, task_if_true, task_if_false)`**: A primitive function that executes `task_if_true` if the `indicator` evaluates to true, otherwise executes `task_if_false`.

#### Indicators

- Tasks can compute indicators (boolean values or other metrics) that are used in decision-making for conditional execution.

#### Scheduling

- **`schedule` Property**: Specifies when or how often a task should execute. Can be a specific time, interval, or event.

## Example Program Incorporating Time Series and Vectorizable Objects

Below is a self-consistent example that includes all class definitions, uses instances from previous phases, and demonstrates the new features while maintaining the elegance of the JSON-like syntax.

### Header: Object and Method Definitions

```plaintext
header: {
  ComputeEngine: {
    getUniverse: String -> Universe,
    getAllocation: String -> Allocation,
    allocate: Universe, Allocation -> Allocation,
    optimise: Allocation, Float -> Allocation,
    value: Allocation -> Valuation,
    risk: Universe -> RiskAnalysis,
    backtest: AllocationSeries, MarketDataSeries -> BacktestResultSeries,
    generateAllocationSeries: Pipeline, DateRange, Frequency -> AllocationSeries
  },
  RiskAnalysis: {
    getVar: _ -> Float,
    computeRiskMetrics: AllocationSeries -> RiskMetricsSeries
  },
  DataLoader: {
    getUniverse: String -> Universe,
    getAllocation: String -> Allocation,
    loadMarketData: String, DateRange -> MarketDataSeries,
    getMarketIndicator: String -> IndicatorSeries
  },
  Orchestrator: {
    rebalance: Allocation -> Allocation
  },
  Plotter: {
    plotPerformance: BacktestResultSeries -> Plot,
    plotRiskMetrics: RiskMetricsSeries -> Plot
  },
  Scheduler: {
    scheduleTask: Task, Schedule -> ScheduledTask
  },
  Series: {
    sum: _ -> Series,
    mean: _ -> Series,
    diff: _ -> Series,
    pctChange: _ -> Series,
    resample: Frequency -> Series,
    rolling: WindowSize -> Series,
    apply: Function -> Series
  }
}
```

### Instances

```plaintext
instances: {
  data_loader: DataLoader,
  compute_engine: ComputeEngine,
  orchestrator: Orchestrator,
  plotter: Plotter,
  scheduler: Scheduler
}
```

### Pipeline Definitions (Computational Graphs)

```plaintext
pipelines: {
  REBALANCING(universeName): [
    {
      phase1: {
        universe: data_loader.getUniverse(universeName),
        index: data_loader.getAllocation(universeName),
        initialAllocation: compute_engine.allocate(universe, index),
        riskAnalysis: compute_engine.risk(universe)
      }
    },
    {
      phase2: {
        riskVar: riskAnalysis.getVar(),
        optimizedAllocation: compute_engine.optimise(initialAllocation, riskVar),
        valuation: compute_engine.value(optimizedAllocation),
        rebalanceTask: orchestrator.rebalance(optimizedAllocation)
      }
    }
  ]
}
```

### Main Pipeline

```plaintext
pipeline: [
  {
    // BACK_TESTING Task
    phase1: {
      marketDataSeries: data_loader.loadMarketData("SP500", "2020-01-01 to 2023-01-01"),
      allocationSeries: compute_engine.generateAllocationSeries(
        REBALANCING("SP500"),
        "2020-01-01 to 2023-01-01",
        "Monthly"
      ),
      backtestResultSeries: compute_engine.backtest(allocationSeries, marketDataSeries)
    }
  },
  {
    // Time Series Operations and Analysis
    phase2: {
      returnsSeries: backtestResultSeries.pctChange(),
      cumulativeReturnsSeries: returnsSeries.cumsum(),
      averageReturn: returnsSeries.mean(),
      riskMetricsSeries: RiskAnalysis.computeRiskMetrics(allocationSeries),
      performancePlot: plotter.plotPerformance(cumulativeReturnsSeries),
      riskPlot: plotter.plotRiskMetrics(riskMetricsSeries)
    }
  }
]
```

### Series Object and Methods

OrdoLang introduces the `Series` object with methods for temporal data analysis:

- **Aggregation Methods**: `sum()`, `mean()`, `cumsum()` for cumulative sums and means.
- **Transformation Methods**: `diff()`, `pctChange()`, `resample(frequency)`, `rolling(windowSize)`.
- **Custom Functions**: `apply(function)` allows applying a custom function to each element or window in the series.

### Key Points

- **Time Series-Centric Framework**: Focus on temporal data processing, enhancing consistency across workflows.
- **Vectorizable Objects**: Efficient computations over entire time series.
- **Pipeline Definitions**: Define reusable computational graphs that can be parameterized.
- **Elegant Syntax**: JSON-like, concise, and maintainable.
- **Dynamic Data Flow**: Context-aware, sequential and parallel processing.

## Conclusion

OrdoLang provides a powerful yet simple language for defining complex task pipelines, emphasizing a time-series perspective. It allows any object to be transformed into a `Series` object, supporting flexible and efficient workflows ideal for finance, trading systems, or any domain where temporal data is critical.

---

**Note**: This framework is adaptable to various programming environments and does not depend on specific libraries. Vectorization refers to the capability of certain objects to support efficient operations over sequences.
