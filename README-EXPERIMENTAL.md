# OrdoLang: An Experimental JSON-Based Workflow Language

**Date**: 2024-11-12

## Overview

**OrdoLang** is an experimental programming language designed to specify complex task pipelines with sequential and parallel execution across multiple phases, all within an elegant JSON-like syntax. OrdoLang excels in scenarios like financial back-testing, automated trading systems, and data analysis workflows where tasks are well-defined and need to be executed efficiently.

**Note**: OrdoLang is a flexible, human-readable blueprint for designing task pipelines, adaptable to multiple programming languages. It serves as a clear framework for defining objects, methods, and task sequencing, making it ideal for creating cross-functional pipeline blueprints that can be implemented across various systems.

## Key Features

- **Sequential and Parallel Execution**: Structured task execution across sequential phases, with parallelism for tasks within each phase.
- **Conditional Execution**: Tasks can be conditionally executed based on indicators or the results of other tasks, using the primitive `conditional` function within the JSON-like syntax.
- **Indicators**: Compute indicators that influence execution flow, facilitating decision-making in workflows.
- **Scheduling**: Tasks can be scheduled to run at specific times or intervals, enabling time-based workflows.
- **Header for Object and Method Definitions**: Clearly define objects, methods, and their expected input/output types.
- **Dynamic Scoping and Data Flow**: Variables defined in one phase are accessible in subsequent phases, allowing for efficient data flow.

## Language Overview

An OrdoLang program is structured as a JSON-like array, where each element is a **phase** represented as an object with the phase name as the key.

- **Phases**: Execute sequentially from the first to the last in the array.
- **Tasks**: Execute in parallel within each phase unless dependencies specify otherwise.
- **Conditional Execution**: Implemented using the primitive `conditional(indicator, task_if_true, task_if_false)`.
- **Scheduling**: Defined within tasks using a `schedule` property.
- **Indicators**: Tasks can compute indicators that influence subsequent task execution.

### New Concepts

#### Conditional Execution

- **`conditional(indicator, task_if_true, task_if_false)`**: A primitive function that executes `task_if_true` if the `indicator` evaluates to true, otherwise executes `task_if_false`. This keeps the JSON-like syntax intact and elegant.

#### Indicators

- Tasks can compute indicators (boolean values or other metrics) that are used in decision-making for conditional execution.

#### Scheduling

- **`schedule` Property**: Specifies when or how often a task should execute. Can be a specific time, interval, or event.

## Example Program with Conditional Execution Using Indicators

Below is a self-consistent example that includes all class definitions, uses instances from previous phases, and demonstrates the new features while maintaining the elegance of the JSON-like syntax.

```plaintext
header: {
  ComputeEngine: {
    getUniverse: String -> Universe,
    allocate: Universe, Index -> Allocation,
    optimize: Allocation, Parameters -> Allocation,
    backtest: Allocation, MarketData -> BacktestResult,
    analyzeResults: BacktestResult -> AnalysisReport
  },
  DataLoader: {
    getUniverse: String -> Universe,
    getIndex: String -> Index,
    loadMarketData: String, DateRange -> MarketData,
    getMarketIndicator: String -> Indicator
  },
  Parameters: {
    create: Dictionary -> Parameters
  },
  ReportGenerator: {
    generateReport: AnalysisReport -> Report
  },
  Scheduler: {
    scheduleTask: Task, Schedule -> ScheduledTask
  }
}

instances: {
  data_loader: DataLoader,
  compute_engine: ComputeEngine,
  report_generator: ReportGenerator,
  scheduler: Scheduler
}

pipeline: [
  {
    phase1: {
      // Load the universe and index data
      universe: data_loader.getUniverse("SP500"),
      index: data_loader.getIndex("SP500"),
      // Initial allocation
      initial_allocation: compute_engine.allocate(universe, index)
    }
  },
  {
    phase2: {
      // Get a market indicator
      market_indicator: data_loader.getMarketIndicator("SP500"),
      // Define optimization parameters
      optimization_params: Parameters.create({
        risk_tolerance: 0.05,
        max_assets: 50
      }),
      // Conditional optimization
      optimized_allocation: conditional(
        market_indicator.isBullish(),
        compute_engine.optimize(initial_allocation, optimization_params),
        initial_allocation
      )
    }
  },
  {
    phase3: {
      // Load market data for back-testing
      market_data: data_loader.loadMarketData("SP500", "2020-01-01 to 2023-01-01"),
      // Schedule the backtest to run at a specific time
      scheduled_backtest: scheduler.scheduleTask(
        compute_engine.backtest(optimized_allocation, market_data),
        "2024-12-01T09:30:00Z"
      ),
      // Backtest result will be available after the scheduled time
      backtest_result: scheduled_backtest
    }
  },
  {
    phase4: {
      // Analyze the backtest results
      analysis_report: compute_engine.analyzeResults(backtest_result),
      // Conditional report generation
      final_report: conditional(
        analysis_report.performance > 0,
        report_generator.generateReport(analysis_report),
        "Performance not sufficient; report not generated."
      )
    }
  }
]
