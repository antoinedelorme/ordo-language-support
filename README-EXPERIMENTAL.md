
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
      observationDates: orchestrator.getSchedule('2020-01-01', observationTime, monthly),
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


# Appendix: Understanding the Pure JSON Format for Ordo

This appendix explains the JSON format used to represent Ordo programs in a structured, machine-readable way. 
This format clarifies dependencies, literal values, and mapping functions, ensuring that each element in the pipeline 
is fully transparent and easy to interpret.

## JSON Format Components

In the Ordo JSON format, every component follows specific conventions:

1. **Result Declaration (`"result"`)**: 
   - Every task or computation in the pipeline declares a `"result"` key. This specifies the name of the variable to store 
     the result of this computation, allowing other tasks to reference it.

2. **Method Invocation (`"method"`)**:
   - To invoke a method on an object, use the `"method"` key followed by the method’s name as a string (e.g., `"orchestrator.getCurrentDate"`).
   - The parameters for each method go into a `"params"` array.

3. **Literal Values (`"String"`)**:
   - To clearly differentiate between literal strings and Ordo dependencies, wrap any literal string in an object with a 
     `"String"` key (e.g., `{ "String": "AAPL" }`). Unmarked values in the `"params"` array are interpreted as references 
     to Ordo variables or dependencies.

4. **Dependencies**:
   - When a task depends on an existing variable, list that variable name in the `"dependencies"` array. This clarifies 
     which tasks rely on outputs from prior computations, ensuring that the data flow is explicit.

5. **Path Access (`"path"`)**:
   - To access nested results from other tasks or pipelines, use the `"path"` key with an array that represents the nested 
     structure. This approach makes it clear how to locate results within a hierarchical structure.

6. **Mapping Function (`"map"`)**:
   - The `"map"` function is structured to apply a specified task to each element in an iterable list.
   - Use `"iterable"` to specify the list, `"iterator"` to define the loop variable, and `"apply"` to designate the task 
     to apply to each element.

## Example: JSON Representation of an Ordo Program

Below is an example JSON structure illustrating these components. This example describes a simple program that maps 
a `MONTHLY_EQUAL_WEIGHT` calculation across multiple observation dates.

```json
{
  "entryPoint": {
    "result": "pipelineLibrary.COMPUTE"
  },
  "rebalancingDate": {
    "result": "rebalancingDate",
    "method": "orchestrator.getCurrentDate",
    "params": []
  },
  "pipelineLibrary": {
    "MONTHLY_EQUAL_WEIGHT": {
      "universe": {
        "result": "universe",
        "method": "data_loader.getUniverseFromTickers",
        "params": [
          {"String": "AAPL"},
          {"String": "GOOGLE"}
        ]
      },
      "enrichedUniverse": {
        "result": "enrichedUniverse",
        "method": "data_loader.getSnapshot",
        "params": [
          "universe",
          [{"String": "Price"}],
          "observationDate"
        ]
      },
      "targetAllocation": {
        "result": "targetAllocation",
        "method": "compute_engine.getEqualWeight",
        "params": ["enrichedUniverse"]
      }
    },
    "BACKTEST": {
      "observationTime": {
        "result": "observationTime",
        "dependencies": ["rebalancingDate"]
      },
      "observationDates": {
        "result": "observationDates",
        "method": "orchestrator.getSchedule",
        "params": [
          {"String": "2020-01-01"},
          "observationTime",
          {"String": "monthly"}
        ]
      },
      "rebalancingResults": {
        "result": "rebalancingResults",
        "method": "map",
        "params": {
          "iterable": "observationDates",
          "iterator": "observationDate",
          "apply": "MONTHLY_EQUAL_WEIGHT"
        }
      }
    },
    "COMPUTE": {
      "backtestResults": {
        "result": "backtestResults",
        "path": ["pipelineLibrary", "BACKTEST", "rebalancingResults"]
      },
      "performanceMetrics": {
        "result": "performanceMetrics",
        "method": "compute_engine.calculatePerformance",
        "params": ["backtestResults"]
      },
      "report": {
        "result": "report",
        "method": "orchestrator.finalizeReport",
        "params": ["performanceMetrics"]
      }
    }
  }
}
```

## Explanation of the Example

This example program defines a pipeline with three main components: `MONTHLY_EQUAL_WEIGHT`, `BACKTEST`, and `COMPUTE`.

- **`MONTHLY_EQUAL_WEIGHT`**: This task calculates an equal-weight allocation for `AAPL` and `GOOGLE`. Literal stock tickers (`"AAPL"`, `"GOOGLE"`) 
  are marked with `{ "String": ... }`, while `"universe"` and `"observationDate"` are unmarked, indicating that they are dependencies or previously computed variables.

- **`BACKTEST`**: 
  - `"observationTime"` depends on `rebalancingDate`, as specified in `"dependencies"`.
  - `"observationDates"` is generated by `orchestrator.getSchedule` with literal values (`"2020-01-01"`, `"monthly"`) and the dependency `observationTime`.
  - `"rebalancingResults"` uses `"map"` to iterate over `observationDates`, applying `MONTHLY_EQUAL_WEIGHT` to each `observationDate`.

- **`COMPUTE`**: 
  - `"backtestResults"` accesses `BACKTEST.rebalancingResults` using the `"path"` key.
  - `"performanceMetrics"` calculates performance from `backtestResults`.
  - `"report"` generates a final report from `performanceMetrics`.

This JSON format provides clarity on data flow, method invocation, and variable dependencies, ensuring a structured and fully JSON-compatible way to represent Ordo pipelines.
