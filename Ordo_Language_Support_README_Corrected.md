
# Ordo Language Support

**Version:** 1.0.0  
**Date:** 2024-11-12  

Ordo Language Support is a VS Code extension designed to facilitate writing and managing Ordo language programs. Ordo enables the creation of complex, acyclic task pipelines with both sequential and parallel execution phases, making it ideal for building data-driven workflows and orchestrating tasks with clear dependencies.

> **Note:** Ordo is a language-agnostic framework, structured as a JSON-like blueprint for designing cross-functional pipelines. It provides a readable, adaptable way to define task interactions, allowing pipelines to be implemented across various programming environments.

## Key Features

- **Acyclic Graph Structure**: Supports acyclic graphs for task pipelines, enabling recursive tasks and efficient scheduling.
- **Sequential and Parallel Execution**: Each phase executes sequentially, while tasks within a phase can run in parallel, creating a structured yet flexible execution model.
- **Dynamic Variable Scoping**: Variables are scoped dynamically across phases, ensuring a smooth flow of data between them.
- **Entry Point Specification**: Programs include an `entryPoint` to define the starting point for execution, supporting flexibility in launching and managing workflows.

## Installation

Install the Ordo Language Support extension through the VS Code marketplace. The extension provides:

- Syntax highlighting
- IntelliSense support
- Error-checking capabilities for Ordo programs

## Language Overview

An Ordo program consists of two main sections:

1. **Header**: Defines objects, methods, and expected input/output types, supporting the complex interactions required within a pipeline.
2. **Pipeline Library**: Contains pipelines structured as acyclic graphs, enabling complex task orchestration through sequential and recursive phases.

### Syntax and Definitions

In Ordo, a task is defined as follows:

```plaintext
result_name: object.method(input_1, input_2, ...)
```

Where:
- `result_name` specifies the output.
- `object` is the instance or type.
- `method` is the operation to execute, with `input_1`, `input_2`, etc., as its parameters.

### Variable Scoping

Variables are scoped by phase and accessible across subsequent phases unless redefined, ensuring efficient data transfer within a pipeline. The `generateSequentialTask` function is highly flexible, allowing any iterable object to generate a sequence of tasks. This means `generateSequentialTask` can accept various iterable objects, like lists of dates, tickers, or custom-defined sets, making it adaptable to many pipeline requirements.

### Example Header Definition

```plaintext
header: {
  DataLoader: {
    getUniverseFromTickers: [String] -> Universe,
    getStatistics: Universe, [String] -> Universe,
    getSnapshot: Universe, [String, DateTime] -> DataSnapshot,
    getHistory: Universe, [String, DateTime] -> HistoricalData
  },
  ComputeEngine: {
    getEqualWeight: Universe -> Allocation,
    calculatePerformance: BacktestAllocation -> PerformanceMetrics
  },
  Pipeline: {
    generateSequentialTask: [Iterable], Pipeline -> BacktestAllocation
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

## Example Pipeline

The following example demonstrates a backtesting pipeline with sequential rebalancing and final performance calculations, using the chosen syntax with pipes.

```plaintext
{
  entryPoint: pipelineLibrary.COMPUTE,
  rebalancingDate: orchestrator.getCurrentDate(),

  pipelineLibrary: {
    MONTHLY_EQUAL_WEIGHT: {
      universe: data_loader.getUniverseFromTickers(['AAPL', 'GOOGLE']),
      enrichedUniverse: data_loader.getSnapshot(universe, ['Price'], observationDate),
      targetAllocation: compute_engine.getEqualWeight(enrichedUniverse)
    },

    BACKTEST: {
      observationTime: rebalancingDate,
      observationDates: orchestrator.getSchedule(2020-01-01, observationTime, monthly),
      rebalancingResults: observationDates.map(observationDate | MONTHLY_EQUAL_WEIGHT)
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
2. **MONTHLY_EQUAL_WEIGHT Pipeline**: Retrieves data for `AAPL` and `GOOGLE`, enriches it with the required statistics, and calculates an equal-weight target allocation for each observation date.
3. **BACKTEST Pipeline**: Uses `mapSequentially` to apply `MONTHLY_EQUAL_WEIGHT` at each `observationDate`, clearly passing each date to `MONTHLY_EQUAL_WEIGHT` through the pipe (`|`).
4. **COMPUTE Pipeline**: Aggregates the backtest results, calculates performance metrics, and finalizes a report, providing a complete evaluation of the backtesting results.

## Conclusion

Ordo’s clear, JSON-like syntax for defining acyclic task pipelines supports the design of complex workflows with both sequential and parallel execution. This extension for VS Code enhances productivity by providing syntax support, error-checking, and IntelliSense, simplifying the development and debugging of Ordo programs.

---

## Appendix: JSON Format for Ordo Programs

For an in-depth explanation of the JSON format used for Ordo programs, see the appendix. The appendix describes each component's logic, distinguishing between literal strings and Ordo dependencies, and demonstrates the `map` function's enhanced syntax for clarity.
