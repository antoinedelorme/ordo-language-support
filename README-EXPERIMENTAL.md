
# Ordo Language Support

**Date**: 2024-11-12

## Overview

Ordo Language Support is a VS Code extension for the Ordo programming language, designed to specify complex task pipelines using an acyclic graph structure with sequential and parallel execution across multiple phases. Each phase executes sequentially, while tasks within each phase can execute in parallel unless dependencies specify otherwise. Ordo's JSON-like syntax promotes readability and simplifies task orchestration.

> **Note**: Ordo is a versatile, human-readable blueprint for designing task pipelines. It is intended to be adaptable across different programming languages, serving as a structured framework to define objects and their interactions. This design flexibility makes Ordo ideal for cross-functional pipeline blueprints in various systems.

## Key Features

- **Acyclic Graph Structure**: Ordo now supports acyclic graph pipelines, with the ability to define recursive tasks for sequential or parallel execution over scheduled dates.
- **Sequential and Parallel Execution**: Tasks can execute in parallel within each phase, while phases themselves execute sequentially. `generateSequentialTask` supports date-specific, time-sensitive pipelines that depend on prior executions.
- **Dynamic Scoping Across Phases**: Variables defined in one phase are accessible in subsequent phases, allowing efficient data flow across phases.
- **Entry Point Specification**: Ordo programs now include an `entryPoint`, indicating the main pipeline for execution, providing flexibility in launching complex workflows.

## Language Overview

An Ordo program consists of a **Header** and a **Pipeline Library**:

- **Header**: Defines objects, methods, and expected input/output types, supporting complex interactions.
- **Pipeline Library**: Contains pipelines as acyclic graph structures, with each phase allowing for recursive tasks based on defined observation schedules.

### Syntax and Definitions

An Ordo program is structured with phases and tasks. Tasks within a phase are defined as follows:

```
result_name: object.method(input_1, input_2, ...)
```

where:
- `result_name` is the output variable.
- `object` is the instance or type.
- `method` is the operation, with `input_1`, `input_2`, etc., as parameters.

### Variable Referencing and Scoping

Variables are scoped by phase, and accessible to subsequent phases unless redefined. Recursive pipelines can use `generateSequentialTask` for tasks that depend on prior executions.

### Example Header Definition

```plaintext
header: {
  DataLoader: {
    getUniverseFromTickers: [String] -> Universe,
    getStatistics: Universe, [String] -> Universe,
    getSnapshot: Universe, [String] -> DataSnapshot,
    getHistory: Universe, [String] -> HistoricalData
  },
  ComputeEngine: {
    getEqualWeight: Universe -> Allocation,
    calculatePerformance: BacktestAllocation -> PerformanceMetrics
  },
  Pipeline: {
    generateSequentialTask: [DateTime], Pipeline -> BacktestAllocation
  },
  Orchestrator: {
    getCurrentDate: _ -> DateTime,
    getSchedule: DateTime, DateTime, String -> [DateTime],
    finalizeReport: PerformanceMetrics -> Report
  },
  BacktestAllocation: {
    allocations: [Allocation],
    dates: [DateTime]
  },
  PerformanceMetrics: {
    returns: Float,
    volatility: Float,
    drawdown: Float
  },
  Report: {
    summary: String,
    details: String
  }
}
```

### Example Pipeline with Sequential and Parallel Execution

This example shows a backtesting pipeline with sequential rebalancing and final performance calculation.

```plaintext
{
  entryPoint: pipelineLibrary.COMPUTE,
  rebalancingDate: orchestrator.getCurrentDate(),

  pipelineLibrary: {
    MONTHLY_EQUAL_WEIGHT: {
      universe: data_loader.getUniverseFromTickers([AAPL, GOOGLE]),
      enrichedUniverse: data_loader.getStatistics(universe, [Price]),
      targetAllocation: compute_engine.getEqualWeight(enrichedUniverse)
    },

    BACKTEST: {
      observationTime: rebalancingDate,
      observationDates: orchestrator.getSchedule(2020-01-01, observationTime, monthly),
      rebalancingResults: pipeline.generateSequentialTask(observationDates, MONTHLY_EQUAL_WEIGHT)
    },

    COMPUTE: {
      backtestResults: pipelineLibrary.BACKTEST.rebalancingResults,
      performanceMetrics: compute_engine.calculatePerformance(backtestResults),
      report: orchestrator.finalizeReport(performanceMetrics)
    }
  }
}
```

### Explanation of the Example

1. **Entry Point**: `entryPoint` specifies `pipelineLibrary.COMPUTE` as the main execution path.
2. **MONTHLY_EQUAL_WEIGHT Pipeline**: Retrieves data for `AAPL` and `GOOGLE`, enriches it with the necessary statistics, and computes an equal-weight target allocation.
3. **BACKTEST Pipeline**: Uses `generateSequentialTask` to apply `MONTHLY_EQUAL_WEIGHT` at each scheduled observation date. The sequential structure ensures that each step builds on the results of the previous date.
4. **COMPUTE Pipeline**: Aggregates the backtest results, calculates performance metrics, and finalizes a report, providing a complete evaluation of the backtesting results.

## Conclusion

Ordo is a structured language for defining acyclic task pipelines, supporting sequential and parallel execution with recursive capabilities. Its flexible, readable syntax makes it ideal for complex workflows that require efficient task management across phases.

The Ordo Language Support extension in VS Code provides syntax highlighting, IntelliSense, and error-checking, streamlining the development and debugging of Ordo programs.
