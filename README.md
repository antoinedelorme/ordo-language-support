
# Ordo Language Support

**Date**: 2024-11-12

## Overview

Ordo Language Support is a VS Code extension for the Ordo programming language, designed to specify complex task pipelines with sequential and parallel execution across multiple phases. Each phase executes sequentially, while tasks within a phase execute in parallel unless dependencies specify otherwise. The Ordo language uses a JSON-like syntax for readability and ease of use.

## Key Features

- **Sequential and Parallel Execution**: Ordo enables structured task execution across sequential phases, with parallelism for tasks within each phase.
- **Header for Object and Method Definitions**: Ordo programs include a header section where objects and methods are defined, ensuring clear and flexible task execution. The objects support definitions beyond basic types (e.g., float, int, string) and allow for complex interactions.
- **Dynamic Scoping Across Phases**: Variables defined in one phase are accessible in subsequent phases, allowing for efficient data flow across phases.

## Language Overview

An Ordo program is structured as a JSON-like array, where each element is a **Phase** represented as an object with the phase name as the key.

- **Phases**: Execute sequentially from the first to the last in the array.
- **Tasks**: Execute in parallel within each phase unless dependencies on other tasks are specified.

### Example Program

```json
[
  {
    phase1: {
      SP500: data_loader.getUniverse(SP500),
      SP500Index: data_loader.getAllocation(SP500),
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

The header in an Ordo program specifies objects, methods, and their expected input/output types. It follows this format:

```
object_name: ClassName
ClassName.method_name: InputType(s) -> OutputType
```

For example:

```json
{
  "header": {
    "objects": [
      { "object_name": "compute_engine", "class": "ComputeEngine" },
      { "object_name": "data_loader", "class": "DataLoader" }
    ],
    "methods": [
      { "class": "ComputeEngine", "method_name": "value", "input_types": ["Allocation"], "output_type": "Valuation" },
      { "class": "ComputeEngine", "method_name": "risk", "input_types": ["Universe"], "output_type": "float" }
    ]
  }
}
```

In this example:
- The `ComputeEngine` object has methods `value` and `risk`, each with specified input and output types.

## Example of Sequential and Parallel Execution

The following example shows two sequential phases with parallel tasks within each phase:

```json
[
  {
    phase1: {
      SP500: data_loader.getUniverse(SP500),
      SP500Index: data_loader.getAllocation(SP500),
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

## Conclusion

Ordo is a structured language for defining task pipelines, supporting both sequential and parallel execution. Its syntax allows for compact, readable definitions, making it ideal for workflows that benefit from efficient task management across phases.

This extension provides syntax highlighting, IntelliSense, and error checking, making it easy to work with Ordo programs in VS Code.