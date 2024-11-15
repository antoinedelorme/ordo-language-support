import ast
import inspect

class DynamicMock:
    """Base class for dynamically handling undefined methods or attributes.
    
    This class is designed to simulate calls to any method or attribute 
    that is not explicitly defined, allowing flexible and dynamic 
    interactions for graph creation.
    """
    
    def __getattr__(self, name):
        """Dynamically handle calls to undefined methods or attributes, simulating node addition in the graph."""
        def method(*args, **kwargs):
            # Construct a string that represents the function call instead of executing it
            args_str = ', '.join(map(str, args))
            kwargs_str = ', '.join(f"{k}={v}" for k, v in kwargs.items())
            all_args = f"{args_str}, {kwargs_str}".strip(', ')
            return f"{self.__class__.__name__.lower()}.{name}({all_args})"
        return method  # Return the dynamically created method

    def __repr__(self):
        """Return the class name in lowercase for symbolic representation."""
        return self.__class__.__name__.lower()

class Date(DynamicMock):
    """Represents a date object with offset functionality."""
    
    def offset(self, period):
        """Return the expression as a string for the offset operation."""
        return f"{self}.offset({period})"
    
    def __repr__(self):
        """Return a symbolic name for Date instances."""
        return "rebalancingDate"

class PipelineLibrary(DynamicMock):
    """Simulates a pipeline library that provides compute operations."""
    
    def compute(self, date):
        """Return the expression as a string."""
        return f"pipelineLibrary.compute({date})"

class Orchestrator(DynamicMock):
    """Simulates an orchestrator for scheduling tasks and events."""
    
    def getSchedule(self, startDate, endDate, frequency):
        """Return the expression as a string."""
        # Ensure the literals are correctly represented as strings
        startDate = f'"{startDate}"' if isinstance(startDate, str) else startDate
        frequency = f'"{frequency}"' if isinstance(frequency, str) else frequency
        return f"orchestrator.getSchedule({startDate}, {endDate}, {frequency})"

class Universe(DynamicMock):
    """Represents a universe of assets or instruments."""
    
    def getData(self, universe, argumentList, startDate, endDate):
        startDate = f'"{startDate}"' if isinstance(startDate, str) else startDate
        endDate = f'"{endDate}"' if isinstance(endDate, str) else endDate
        """Return the expression as a string."""
        return f"data_loader.getData({universe}, {argumentList}, {startDate}, {endDate})"

class DataLoader(DynamicMock):
    """Simulates data loading operations for various universe configurations."""
    
    def getUniverseFromTickers(self, tickerList):
        """Return the expression as a string."""
        return f"data_loader.getUniverseFromTickers({tickerList})"

class ComputeEngine(DynamicMock):
    """Simulates a computation engine for performing portfolio calculations."""
    
    def calculatePerformance(self, backtest):
        """Return the expression as a string."""
        return f"compute_engine.calculatePerformance({backtest})"

    def getEqualWeightAllocation(self, universe, refDate):
        """Return the expression as a string."""
        return f"compute_engine.getEqualWeight({universe})"

class Task(DynamicMock):
    """Represents a task in the pipeline that can take zero or more arguments."""
    
    def __call__(self, *args):
        """Return the expression as a string when Task is called."""
        args_str = ', '.join(map(str, args))
        return f"Task({args_str})"

class Dates:
    """Class to simulate a list of dates with a functional programming style map method."""
    
    _dates = [Date(), Date(), Date()]  # Default list of Date objects
    
    @classmethod
    def map(cls, func):
        """
        Apply a function or Task to each date in the class-level list.
        
        The map method simply returns expressions as strings without actual execution.
        """
        return [f"{func}({date})" for date in cls._dates]

class BackTestResult(DynamicMock):
    """Specific class to represent backtest results."""
    
    def __call__(self, *args):
        """Return the expression as a string when BackTestResult is called."""
        args_str = ', '.join(map(str, args))
        return f"backtestResults({args_str})"
    
    def __repr__(self):
        """Provide a symbolic name for BackTestResult instances."""
        return "backtestResults"


# Instantiate objects for use in JSON-like configuration
data_loader = DataLoader()
universe = Universe()
enrichedUniverse = Universe()
compute_engine = ComputeEngine()
backtestResults = BackTestResult()  # Properly instantiated as a specific BackTestResult object
pipelineLibrary = PipelineLibrary()
orchestrator = Orchestrator()
rebalancingDate = Date()
observationDate = Date()
rebalancing = Task()
backtest = Task()
performanceMetrics = Task()
observationDates = Dates

def getCurrentDate():
    """Return the expression as a string for current date."""
    return "getCurrentDate()"

def getParams():
    """Return the expression as a string for params."""
    return "getParams()"

PRIMITIVE = 'PRIMITIVE'

def Stringify(targetId):
    # Get the source code of the current file
    source = inspect.getsource(inspect.currentframe().f_back)
    # Parse the source code
    tree = ast.parse(source)

    # Find the assignment to json_data_useful
    class AssignVisitor(ast.NodeVisitor):
        def __init__(self):
            self.json_data_useful_node = None

        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == targetId:
                    self.json_data_useful_node = node.value

    visitor = AssignVisitor()
    visitor.visit(tree)
    if visitor.json_data_useful_node is None:
        raise ValueError("json_data_useful not found in the source code.")

    # Function to process AST nodes
    def process_node(node):
        if isinstance(node, ast.Dict):
            new_dict = {}
            for key, value in zip(node.keys, node.values):
                key_value = process_node(key)
                value_processed = process_node(value)
                new_dict[key_value] = value_processed
            return new_dict
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Str):  # For Python versions before 3.8
            return node.s
        elif isinstance(node, ast.Name):
            if node.id == 'PRIMITIVE':
                return '"PRIMITIVE"'
            else:
                return node.id
        elif isinstance(node, ast.Call):
            return ast.unparse(node)
        elif isinstance(node, ast.Attribute):
            return ast.unparse(node)
        elif isinstance(node, ast.List):
            return [process_node(elt) for elt in node.elts]
        elif isinstance(node, ast.Subscript):
            return ast.unparse(node)
        else:
            return ast.unparse(node)

    json_data = process_node(visitor.json_data_useful_node)
    return json_data
