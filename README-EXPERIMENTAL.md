
# OrdoLang: A Time Series-Centric Workflow Language

**Date**: 2024-11-12

## Overview

**OrdoLang** is an experimental programming language designed to specify complex task pipelines with sequential and parallel execution across multiple phases, all within a JSON-like syntax. OrdoLang’s JSON-based structure provides an intuitive way to organize workflows, where lists (`[]`) indicate **sequential execution** and objects (`{}`) allow **parallel execution** of tasks, automatically resolving dependencies within each phase. This design is ideal for time series-based applications where tasks require bo...

**Note**: OrdoLang serves as a flexible, human-readable blueprint for designing task pipelines, adaptable to multiple programming languages. It provides a clear framework for defining objects, methods, and task sequencing, making it ideal for creating cross-functional pipeline blueprints.

## Key Features

- **Time Series-Centric**: All objects can be transformed into time series (`Series<Object>`), allowing for consistent and powerful time-based operations.
- **Vectorizable Objects**: Certain objects support vectorized operations, enabling efficient computations over entire time series without explicit iteration.
- **Sequential and Parallel Execution**: Structured task execution with sequential execution in lists (`[]`) and parallelism within objects (`{}`) in each phase.
- **Pipeline Definitions (Computational Graphs)**: Define reusable pipelines (graphs) that can be invoked within other tasks, similar to computational graphs in data processing frameworks.
- **Conditional Execution**: Tasks can be conditionally executed based on indicators or the results of other tasks, using the primitive `conditional` function within the JSON-like syntax.
- **Indicators**: Compute indicators that influence execution flow, facilitating decision-making in workflows.
- **Scheduling**: Tasks can be scheduled to run at specific times or intervals, enabling time-based workflows.
- **Header for Object and Method Definitions**: Clearly define objects, methods, and their expected input/output types, including time series transformations.
- **Dynamic Scoping and Data Flow**: Variables defined in one phase are accessible in subsequent phases, allowing for efficient data flow.

## Language Overview

An OrdoLang program is structured as a JSON-like array, where each element is a **phase** represented as an object with the phase name as the key.

- **Phases**: Execute sequentially from the first to the last in the array (`[]`).
- **Tasks**: Execute in parallel within each phase (`{}`) unless dependencies specify otherwise.
- **Pipeline Definitions**: Reusable pipelines (graphs) can be defined and invoked within other tasks.
- **Time Series Operations**: Objects can be transformed into `Series<Object>`, supporting vectorized operations over time.
- **Conditional Execution**: Implemented using the primitive `conditional(indicator, task_if_true, task_if_false)`.
- **Scheduling**: Defined within tasks using a `schedule` property.
- **Indicators**: Tasks can compute indicators that influence subsequent task execution.

### New Concepts

#### Time Series and Vectorizable Objects

- **Series Objects**: Any object can be transformed into a `Series<Object>`, a time-indexed sequence of a specific object type. Each `Series<Object>` expression can only include one `Series` per line, ensuring clarity.
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

## Example Program with Strict `Series<Object>` Syntax

Below is a self-consistent example that includes all class definitions, uses instances from previous phases, and demonstrates the new features while adhering to the one `Series<Object>` per line rule.

### Header: Object and Method Definitions

Each time-indexed sequence is represented as `Series<Object>`, with only one `Series` per line for clarity and consistency.

```plaintext
header: {
  ComputeEngine: {
    getUniverse: String -> Universe,
    getAllocation: String -> Allocation,
    allocate: Universe, Allocation -> Allocation,
    optimise: Allocation, Float -> Allocation,
    value: Allocation -> Valuation,
    risk: Universe -> RiskAnalysis,
    backtest: Series<(Allocation, MarketData)> -> Series<BacktestResult>,
    generateAllocationSeries: Pipeline, DateRange, Frequency -> Series<Allocation>
  },
  RiskAnalysis: {
    getVar: _ -> Float,
    computeRiskMetrics: Allocation -> RiskMetrics
  },
  DataLoader: {
    getUniverse: String -> Universe,
    getAllocation: String -> Allocation,
    loadMarketData: String, DateRange -> Series<MarketData>,
    getMarketIndicator: String -> Series<Indicator>
  },
  Orchestrator: {
    rebalance: Allocation -> Allocation
  },
  Plotter: {
    plotPerformance: Series<BacktestResult> -> Plot,
    plotRiskMetrics: Series<RiskMetrics> -> Plot
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

This pipeline shows the `REBALANCING` process, using clear, type-specific sequences while conforming to the one `Series<Object>` per line rule.

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

In this main pipeline, the `Series<(Allocation, MarketData)>` structure is used to ensure that `backtest` respects the single `Series<Object>` rule.

```plaintext
pipeline: [
  [
    // BACK_TESTING Task - Sequential Phases
    {
      phase1: {
        marketData: data_loader.loadMarketData("SP500", "2020-01-01 to 2023-01-01"),
        allocationSeries: compute_engine.generateAllocationSeries(
          REBALANCING("SP500"),
          "2020-01-01 to 2023-01-01",
          "Monthly"
        ),
        combinedSeries: allocationSeries.zip(marketData),  // Combine Allocation and MarketData into a single series
        backtestResults: compute_engine.backtest(combinedSeries)
      }
    }
  ],
  [
    // Time Series Operations and Analysis
    {
      phase2: {
        returnsSeries: backtestResults.pctChange(),
        cumulativeReturns: returnsSeries.cumsum(),
        averageReturn: returnsSeries.mean(),
        riskMetricsSeries: allocationSeries.apply(RiskAnalysis.computeRiskMetrics),
        performancePlot: plotter.plotPerformance(cumulativeReturns),
        riskPlot: plotter.plotRiskMetrics(riskMetricsSeries)
      }
    }
  ]
]
```

### Explanation of Updates

1. **Sequential and Parallel Execution**: The JSON format uses lists (`[]`) for sequential phases and objects (`{}`) for parallel tasks within a phase.

2. **Single `Series<Object>` per Line**: Each function now adheres to the rule of only having one `Series<Object>` per line.

3. **Combined Series for Backtesting**: To handle multiple inputs, we created a `Series<(Allocation, MarketData)>` by combining `Allocation` and `MarketData` into a tuple series with `zip`. This allows `backtest` to process both inputs within a single `Series` object.

4. **Consistent `Series<Object>` Application**: All time-based sequences are expressed as `Series<Object>`, keeping the syntax streamlined and compliant with the framework’s structure.

This design approach maintains clarity and ensures that all operations are syntactically correct while preserving OrdoLang's core principles.
