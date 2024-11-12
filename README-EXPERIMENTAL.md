
# OrdoLang: An Experimental JSON-Based Workflow Language

**Date**: 2024-11-12

## Overview

**OrdoLang** is an experimental programming language designed to specify complex task pipelines with sequential and parallel execution across multiple phases, all within an elegant JSON-like syntax. OrdoLang excels in scenarios like financial back-testing, automated trading systems, and data analysis workflows where tasks are well-defined and need to be executed efficiently.

**Note**: OrdoLang is a flexible, human-readable blueprint for designing task pipelines, adaptable to multiple programming languages. It serves as a clear framework for defining objects, methods, and task sequencing, making it ideal for creating cross-functional pipeline blueprints that can be implemented across various systems.

## Key Features

- **Sequential and Parallel Execution**: Structured task execution across sequential phases, with parallelism for tasks within each phase.
- **Pipeline Definitions (Computational Graphs)**: Define reusable pipelines (graphs) that can be invoked within other tasks, similar to computational graphs in frameworks like TensorFlow.
- **Conditional Execution**: Tasks can be conditionally executed based on indicators or the results of other tasks, using the primitive `conditional` function within the JSON-like syntax.
- **Indicators**: Compute indicators that influence execution flow, facilitating decision-making in workflows.
- **Scheduling**: Tasks can be scheduled to run at specific times or intervals, enabling time-based workflows.
- **Header for Object and Method Definitions**: Clearly define objects, methods, and their expected input/output types.
- **Dynamic Scoping and Data Flow**: Variables defined in one phase are accessible in subsequent phases, allowing for efficient data flow.

## Language Overview

An OrdoLang program is structured as a JSON-like array, where each element is a **phase** represented as an object with the phase name as the key.

- **Phases**: Execute sequentially from the first to the last in the array.
- **Tasks**: Execute in parallel within each phase unless dependencies specify otherwise.
- **Pipeline Definitions**: Reusable pipelines (graphs) can be defined and invoked within other tasks.
- **Conditional Execution**: Implemented using the primitive `conditional(indicator, task_if_true, task_if_false)`.
- **Scheduling**: Defined within tasks using a `schedule` property.
- **Indicators**: Tasks can compute indicators that influence subsequent task execution.

### New Concepts

#### Pipeline Definitions (Computational Graphs)

- **`pipelines` Section**: Define reusable pipelines that can be invoked within the main pipeline.
- **Pipeline Invocation**: Use pipelines within tasks by invoking them as needed.

#### Conditional Execution

- **`conditional(indicator, task_if_true, task_if_false)`**: A primitive function that executes `task_if_true` if the `indicator` evaluates to true, otherwise executes `task_if_false`.

#### Indicators

- Tasks can compute indicators (boolean values or other metrics) that are used in decision-making for conditional execution.

#### Scheduling

- **`schedule` Property**: Specifies when or how often a task should execute. Can be a specific time, interval, or event.

## Example Program with Pipeline Definitions and Conditional Execution

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
    backtest: AllocationSeries, MarketData -> BacktestResult,
    generateAllocationSeries: Pipeline, DateRange, Frequency -> AllocationSeries
  },
  RiskAnalysis: {
    getVar: _ -> Float,
    computeRiskMetrics: AllocationSeries -> RiskMetrics
  },
  DataLoader: {
    getUniverse: String -> Universe,
    getAllocation: String -> Allocation,
    loadMarketData: String, DateRange -> MarketData,
    getMarketIndicator: String -> Indicator
  },
  Orchestrator: {
    rebalance: Allocation -> Allocation
  },
  Plotter: {
    plotPerformance: BacktestResult -> Plot,
    plotRiskMetrics: RiskMetrics -> Plot
  },
  Scheduler: {
    scheduleTask: Task, Schedule -> ScheduledTask
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
  REBALANCING: [
    {
      phase1: {
        SP500: data_loader.getUniverse("SP500"),
        SP500Index: data_loader.getAllocation("SP500"),
        initialAllocation: compute_engine.allocate(SP500, SP500Index),
        riskAnalysis: compute_engine.risk(SP500)
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
      marketData: data_loader.loadMarketData("SP500", "2020-01-01 to 2023-01-01"),
      allocationSeries: compute_engine.generateAllocationSeries(
        REBALANCING,
        "2020-01-01 to 2023-01-01",
        "Monthly"
      ),
      backtestResult: compute_engine.backtest(allocationSeries, marketData)
    }
  },
  {
    // PLOT and RISK Computation Task
    phase2: {
      performancePlot: plotter.plotPerformance(backtestResult),
      riskMetrics: RiskAnalysis.computeRiskMetrics(allocationSeries),
      riskPlot: plotter.plotRiskMetrics(riskMetrics)
    }
  }
]
```

## Explanation of the Example

### Defining the REBALANCING Pipeline

- In the pipelines section, we define REBALANCING as a reusable computational graph.
- It consists of two phases, phase1 and phase2, which include tasks for allocating and optimizing the portfolio.
- This pipeline is not executed immediately but can be invoked elsewhere.

### Using REBALANCING in BACK_TESTING

- In the main pipeline, we use the REBALANCING pipeline as a parameter to generate an allocationSeries.
- The method compute_engine.generateAllocationSeries takes the REBALANCING pipeline, a date range, and a frequency to simulate rebalancing over time.

### How It Works

- **generateAllocationSeries**: This method uses the REBALANCING pipeline to generate allocations at each point in time over the specified date range.
- **Plotting and Risk Analysis**: The backtestResult is used to plot performance, and the allocationSeries is used to compute and plot risk metrics.

## Additional Details

### Parameterization of Pipelines

If needed, the REBALANCING pipeline can be parameterized to allow different inputs when invoked.

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

### Invoking with Parameters

```plaintext
allocationSeries: compute_engine.generateAllocationSeries(
  REBALANCING("SP500"),
  "2020-01-01 to 2023-01-01",
  "Monthly"
)
```

## Key Points

- **Pipeline Definitions**: Allows defining reusable computational graphs.
- **Pipeline Invocation**: Pipelines can be invoked within tasks using their names and parameters.
- **Self-Contained**: All classes and methods used are defined in the header.
- **Sequential Execution**: Phases execute in order, and tasks within phases can execute in parallel unless dependencies dictate otherwise.
- **Data Flow**: Results from previous phases are used in subsequent phases, demonstrating dynamic scoping and efficient data flow.
- **Elegant Syntax**: Maintains the elegance of the JSON-like syntax without additional complexity.

## Linking Sequential Execution and Scheduler

OrdoLang combines sequential execution of phases and precise timing control within each phase through its Scheduler.

### Example

```plaintext
{
  phase3: {
    market_data: data_loader.loadMarketData("SP500", "2020-01-01 to 2023-01-01"),
    scheduled_backtest: scheduler.scheduleTask(
      compute_engine.backtest(optimizedAllocation, market_data),
      "2024-12-01T09:30:00Z"
    ),
    backtest_result: scheduled_backtest
  }
}
```

## Conclusion

OrdoLang is a powerful yet simple language for defining complex task pipelines, supporting sequential and parallel execution, pipeline definitions, conditional logic, and scheduling—all within an elegant JSON-like syntax. It provides a clear and concise way to design, maintain, and execute complex pipelines.

complexity.

### Linking Sequential Execution and Scheduler

In OrdoLang, the sequential execution of phases is represented by the JSON-like array notation [...], where each element in the array is a phase that executes in order from the first to the last. The Scheduler is integrated within this structure to control the timing and execution of tasks within these phases.

**Sequential Phases ([...])**:

- **Phases**: Represented as objects within the array [...], phases execute sequentially—the next phase starts only after the previous one has completed.
- **Tasks within Phases**: Inside each phase, tasks can execute in parallel unless specified otherwise through dependencies or conditions.

**Scheduler Integration**

- **Scheduling Tasks**: Within a phase, individual tasks can use the scheduler.scheduleTask method to specify when or how often they should execute.
- **Flexible Timing**: This allows tasks to be executed at specific times, intervals, or events, providing flexibility within the sequential structure of phases.

**Linking Sequential Execution and Scheduler**

- **Sequential Structure**: The array [...] ensures that phases execute in a specific order, maintaining the logical flow of the pipeline.
- **Scheduled Tasks within Phases**: Even though phases execute sequentially, tasks within those phases can be scheduled to run at particular times using the Scheduler.
- **Controlled Execution**: This combination allows for precise control over both the order of operations (through phases) and the timing of individual tasks (through the Scheduler).

### Example

In Phase 3 of the previous example (assuming a scheduled backtest):

```plaintext
{
  phase3: {
    // Load market data for back-testing
    market_data: data_loader.loadMarketData("SP500", "2020-01-01 to 2023-01-01"),
    // Schedule the backtest to run at a specific time
    scheduled_backtest: scheduler.scheduleTask(
      compute_engine.backtest(optimizedAllocation, market_data),
      "2024-12-01T09:30:00Z"
    ),
    // Backtest result will be available after the scheduled time
    backtest_result: scheduled_backtest
  }
}
```

**Explanation**

- **Phase 3**: Executes after Phase 2 has completed, following the sequential order.
- **scheduled_backtest Task**: Uses the Scheduler to schedule the compute_engine.backtest task to run at "2024-12-01T09:30:00Z".
- **Dependency Management**: Other tasks in the phase, like market_data, can execute immediately. The backtest_result depends on scheduled_backtest, which will only be available after the scheduled time.

## Conclusion

OrdoLang is a powerful yet simple language for defining complex task pipelines, supporting sequential and parallel execution, pipeline definitions (computational graphs), conditional logic using indicators, and scheduling—all within an elegant JSON-like syntax. This makes it ideal for workflows requiring dynamic and efficient task management, such as financial back-testing and automated trading systems.

By introducing the conditional primitive function and integrating pipeline definitions and scheduling within the tasks, we enable sophisticated control flow without compromising syntax elegance. This experimental language provides a clear and concise way to define workflows, making it easier to design, maintain, and execute complex pipelines.

- **Elegant Syntax**: The entire program maintains the elegance of the JSON-like syntax, without introducing any additional complexity.

### Linking Sequential Execution and Scheduler

In OrdoLang, the sequential execution of phases is represented by the JSON-like array notation [...], where each element in the array is a phase that executes in order. The Scheduler is integrated within this structure to control the timing and execution of tasks within these phases.

**Sequential Phases ([...])**:
- **Phases**: Represented as objects within the array [...], executing sequentially, with each phase starting only after the previous one completes.
- **Tasks within Phases**: Inside each phase, tasks can run in parallel unless dependencies dictate otherwise.
- **Scheduler Integration**: Within a phase, individual tasks can specify scheduling using `scheduleTask` for precise timing and interval control.

### Example

In Phase 3 of the previous example:

```plaintext
{
  phase3: {
    market_data: data_loader.loadMarketData("SP500", "2020-01-01 to 2023-01-01"),
    scheduled_backtest: scheduler.scheduleTask(
      compute_engine.backtest(optimizedAllocation, market_data),
      "2024-12-01T09:30:00Z"
    ),
    backtest_result: scheduled_backtest
  }
}
```

This setup ensures:
- **Sequential Structure**: Phases proceed in a set order, maintaining logical workflow structure.
- **Controlled Timing**: The Scheduler allows precise execution timing for individual tasks within a sequential phase array.

## Conclusion

OrdoLang provides a powerful and structured approach for complex task pipelines, supporting sequential and parallel execution, reusable pipeline definitions, conditional execution, and precise scheduling, all within a JSON-like syntax. It is ideal for dynamic, efficient workflows like financial back-testing and automated trading systems, enabling clear design, maintenance, and execution of complex pipelines.

