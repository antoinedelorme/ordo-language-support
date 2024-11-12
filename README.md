
# Ordo Language Support

**Date**: 2024-11-12

## Overview

Ordo Language Support is a VS Code extension for the Ordo programming language, designed to specify complex task pipelines with sequential and parallel execution across multiple phases. Each phase executes sequentially, while tasks within a phase execute in parallel unless dependencies specify otherwise. The Ordo language uses a JSON-like syntax for readability and ease of use.

**Note**: Ordo is not intended as a finalized language. It’s a versatile, human-readable blueprint for designing task pipelines, adaptable to multiple programming languages. Ordo’s purpose is to provide a clear, structured framework for defining objects and their interactions in any system that supports such constructs. The language can be implemented differently across systems as long as it can represent objects, methods, and task sequencing. This flexibility makes Ordo ideal for creating cross-functional pipeline blueprints.

## Key Features

- **Sequential and Parallel Execution**: Ordo enables structured task execution across sequential phases, with parallelism for tasks within each phase.
- **Header for Object and Method Definitions**: Ordo programs include a header section where objects and methods are defined, ensuring clear and flexible task execution. The objects support definitions beyond basic types (e.g., float, int, string) and allow for complex interactions.
- **Dynamic Scoping Across Phases**: Variables defined in one phase are accessible in subsequent phases, allowing for efficient data flow across phases.

## Language Overview

An Ordo program is structured as a JSON-like array, where each element is a **Phase** represented as an object with the phase name as the key.

- **Phases**: Execute sequentially from the first to the last in the array.
- **Tasks**: Execute in parallel within each phase unless dependencies on other tasks are specified.

### Example Program

```plaintext
[
  {
    phase1: {
      SP500: data_loader.getUniverse('SP500'),
      SP500Index: data_loader.getAllocation('SP500'),
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
```

In this example:
- **Phase 1**: Tasks `SP500`, `SP500Index`, `initialAllocation`, and `riskAnalysis` execute in parallel.
- **Phase 2**: Tasks `valuation` and `rebalanceTask` can execute in parallel after `optimizedAllocation` completes.

## Syntax Definition

### Program Structure

An Ordo program has two main parts:
1. **Header**: Defines objects, methods, and their expected input/output types.
2. **Pipeline**: An array of sequential phases, each containing tasks.

### Task Definition Syntax

Each task within a phase follows this format:

```
result_name: object.method(input_1, input_2, ...)
```

where:
- `result_name` is the output variable.
- `object` is the instance or type.
- `method` is the operation, with `input_1`, `input_2`, etc., as parameters.

### Variable Referencing and Scoping Rules

- Variables are scoped by phase, with access allowed from previous phases unless redefined.

### Header: Object and Method Definitions

The header in an Ordo program specifies objects, methods, and their expected input/output types in a structured format, allowing for complex interactions and functionality.

An example header format is as follows:

```plaintext
ComputeEngine: {
  getUniverse: String -> Universe,
  getTrackingError: Allocation, Index -> Float,
  allocate: Universe, Index -> Allocation,
  optimize: Allocation, Float -> Allocation
},
Allocation: {
  rank: _ -> Allocation,
  topPercentile: Float -> Allocation,
  merge: Allocation, Allocation -> Allocation
},
RiskManager: {
  calculateVaR: Allocation -> Float,
  analyzeRisk: Allocation, MarketData -> RiskReport
},
DataLoader: {
  getUniverse: String -> Universe,
  getAllocation: String -> Allocation,
  loadMarketData: String -> MarketData
},
Orchestrator: {
  rebalance: Allocation -> Allocation,
  finalizeReport: Allocation -> Report
}
```

In this example:
- **`ComputeEngine`** provides methods for creating and optimizing allocations, and calculating tracking errors.
- **`Allocation`** includes methods for ranking, selecting top assets, and merging allocations.
- **`RiskManager`** includes risk-related methods, such as `calculateVaR` and `analyzeRisk`.
- **`DataLoader`** fetches universes, allocations, and market data.
- **`Orchestrator`** manages rebalancing and report generation.

## Example of Sequential and Parallel Execution with Financial Logic

Below is a self-consistent, realistic example that includes the `DataLoader` and `Orchestrator` classes, with financial logic. This pipeline performs tasks like loading market data, calculating allocations, and generating a risk report.

```plaintext
header: {
  ComputeEngine: {
    getUniverse: String -> Universe,
    getTrackingError: Allocation, Index -> Float,
    allocate: Universe, Index -> Allocation,
    value: Allocation -> Valuation,
    optimize: Allocation, Float -> Allocation
  },
  Allocation: {
    rank: _ -> Allocation,
    topPercentile: Float -> Allocation,
    merge: Allocation, Allocation -> Allocation
  },
  RiskManager: {
    calculateVaR: Allocation -> Float,
    analyzeRisk: Allocation, MarketData -> RiskReport
  },
  DataLoader: {
    getUniverse: String -> Universe,
    getAllocation: String -> Allocation,
    loadMarketData: String -> MarketData
  },
  Orchestrator: {
    rebalance: Allocation -> Allocation,
    finalizeReport: Allocation -> Report
  }
}

instances: {
  data_loader: DataLoader,
  compute_engine: ComputeEngine,
  risk_manager: RiskManager,
  orchestrator: Orchestrator
}

pipeline: [
  {
    phase1: {
      SP500: data_loader.getUniverse("SP500"),
      SP500Index: data_loader.getAllocation("SP500"),
      initialAllocation: compute_engine.allocate(SP500, SP500Index),
      riskAnalysis: risk_manager.calculateVaR(initialAllocation)
    }
  },
  {
    phase2: {
      marketData: data_loader.loadMarketData("SP500"),
      analyzedRisk: risk_manager.analyzeRisk(initialAllocation, marketData),
      riskVar: riskAnalysis.getVar(),
      optimizedAllocation: compute_engine.optimize(initialAllocation, riskVar),
      valuation: compute_engine.value(optimizedAllocation)
    }
  },
  {
    phase3: {
      rankedAllocation: initialAllocation.rank(),
      topAllocation: rankedAllocation.topPercentile(0.10),
      mergedAllocation: compute_engine.allocate(SP500, SP500Index).merge(topAllocation, initialAllocation),
      finalRebalance: orchestrator.rebalance(optimizedAllocation),
      report: orchestrator.finalizeReport(finalRebalance)
    }
  }
]
```

In this example:
- **Phase 1**: Initializes SP500 universe and performs a basic allocation and risk analysis.
- **Phase 2**: Loads market data and performs risk analysis based on market conditions.
- **Phase 3**: Finalizes allocation by ranking and selecting top assets, merging allocations, rebalancing, and generating a final report.

## Conclusion

Ordo is a structured language for defining task pipelines, supporting both sequential and parallel execution. Its syntax allows for compact, readable definitions, making it ideal for workflows that benefit from efficient task management across phases.

Ordo is intended to serve as a flexible blueprint for various programming environments. Its design allows for customization and adaptation across different languages and systems, making it versatile for both human readability and computational efficiency.

This extension provides syntax highlighting, IntelliSense, and error checking, making it easy to work with Ordo programs in VS Code.
