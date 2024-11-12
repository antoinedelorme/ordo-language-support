
  

# RFC: Sequential and Parallel Task Execution Language

  

**Date:** 2024-11-12

  

## Abstract

This document defines a lightweight programming language in JSON-like syntax designed to specify pipelines with sequential and parallel tasks across multiple phases. Phases are executed sequentially, and tasks within each phase can be executed in parallel unless dependencies are specified. The syntax is simplified to allow object and method definitions inline with implicit scoping across phases.

  

## Introduction

This language enables the definition of structured tasks in a pipeline format, allowing for both sequential and parallel execution. Tasks can refer to results from previous tasks, and phases execute sequentially. The syntax resembles JSON, with simplifications that remove the need for quotes around variable names and strings, enhancing readability.

  

## Language Overview

  

The language represents a pipeline as an ordered list of phases:

- Each phase is defined as a key-value pair, with the phase key representing its name.

- Phases run sequentially in the order defined within the array.

- Tasks within a phase execute in parallel unless dependencies dictate otherwise.

  

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

  

## Syntax Definition

  

### Program Syntax

  

A program is structured as a JSON-like array:

- Each element of the array is a **Phase**, which is represented as an object with a phase name as the key.

- Phases execute sequentially from the first to the last in the array.

- Tasks within a phase execute in parallel, unless there are dependencies specified on the outputs of other tasks.

  

### Task Definition Syntax

  

A task within a phase is defined as:

  

```

result_name: object.method(input_1, input_2, ...)

```

  

where:

-  `result_name` is the name of the variable produced by the task.

-  `object` is the name of an instance or type that provides the required method.

-  `method` is the operation to execute, with `input_1`, `input_2`, etc., as parameters.

  

#### Example Task Definitions

-  `SP500: data_loader.getUniverse(SP500)`

Defines `SP500` as the output of `getUniverse` method on the `data_loader` object, using `SP500` as input.

  

-  `optimizedAllocation: compute_engine.optimise(initialAllocation, riskVar)`

Defines `optimizedAllocation` as the output of `optimise` method on the `compute_engine` object, with inputs `initialAllocation` and `riskVar`.

  

### Variable Referencing and Scoping Rules

  

Variables follow a sequential scoping rule:

- Variables defined in a phase are accessible within the same phase.

- Variables from previous phases are accessible in subsequent phases unless redefined.

  

For example, in `phase2`, the variable `riskVar` is derived from `riskAnalysis.getVar()` defined in `phase1`, allowing for dynamic data flow across phases.

  

### Object and Method Definition Syntax

  

The language allows the definition of objects and their methods with specified input and output types. This section provides the syntax for defining objects, methods, and their expected inputs and outputs to clarify how tasks interact.

  

#### Object and Method Definition Format

  

An object definition specifies a class type, its methods, and the types of their inputs and outputs:

  

```

object_name : ClassName

ClassName.method_name : InputType(s) -> OutputType

```

  

where:

-  `object_name` is the instance used in task definitions.

-  `ClassName` specifies the class of the object.

-  `method_name` is the name of the method.

-  `InputType(s)` are the expected types for each parameter.

-  `OutputType` is the expected output type of the method.

  

### Example of Object Definitions

  

-  `compute_engine : ComputeEngine`

-  `ComputeEngine.value : Allocation -> Valuation`

-  `ComputeEngine.risk : Universe -> float`

  

## Examples

  

### Example of Sequential and Parallel Execution

  

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

  

In this example:

-  **Phase 1**: `SP500`, `SP500Index`, `initialAllocation`, and `riskAnalysis` are executed in parallel.

-  **Phase 2**: Tasks `valuation` and `rebalanceTask` can execute in parallel after the `optimizedAllocation` task completes.

  

## Conclusion

  

This language specification defines a minimal yet expressive syntax for describing complex task pipelines. It supports implicit parallelism and explicit sequential execution across phases, enabling a clear, structured approach to defining workflows in a readable and compact format.# ordo-language-support
