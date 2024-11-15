import re

class Task:
    def __init__(self, name, task_type="single", formula=None, parent=None):
        self.name = name
        self.task_type = task_type  # 'single' or 'multitask'
        self.formula = formula
        self.parent = parent
        self.children = []
        self.siblings = []
        self.parents = []
        self.dependencies = []
        self.object_dependencies = []

    def set_relationships(self):
        if self.parent:
            self.siblings = [child for child in self.parent.children if child != self]
            self.parents = self.parent.parents + [self.parent]

    def add_child(self, child_task):
        self.children.append(child_task)

    def add_dependency(self, dependency_task):
        if dependency_task not in self.dependencies:
            self.dependencies.append(dependency_task)

    def add_object_dependency(self, object_dependency):
        if object_dependency not in self.object_dependencies:
            self.object_dependencies.append(object_dependency)

    def __repr__(self):
        # Print relationships as task names (labels) for readability
        return (f"Task(name='{self.name}', type='{self.task_type}', formula='{self.formula}', "
                f"parents={[p.name for p in self.parents]}, siblings={[s.name for s in self.siblings]}, "
                f"children={[c.name for c in self.children]}, dependencies={[dep.name for dep in self.dependencies]}, "
                f"object_dependencies={[obj.name for obj in self.object_dependencies]})")


class TaskGraph:
    def __init__(self):
        self.tasks = {}  # Dictionary to store tasks with their scoped names
        self.main_entry_point = None

    def parse(self, data, parent=None, scope=""):
        for key, value in data.items():
            # Determine if this is a multitask based on the type of value
            task_type = "multitask" if isinstance(value, dict) else "single"
            scoped_name = f"{scope}.{key}" if scope else key

            if task_type == "multitask":
                # Create a multitask and parse its children
                task = Task(name=scoped_name, task_type="multitask", parent=parent)
                self.tasks[scoped_name] = task
                child_tasks = self.parse(value, parent=task, scope=scoped_name)

                # Set siblings for all multitask children
                for child in child_tasks:
                    child.siblings = [sibling for sibling in child_tasks if sibling != child]
            else:
                # Single task with a formula
                task = Task(name=scoped_name, formula=value, task_type="single", parent=parent)
                self.tasks[scoped_name] = task
                if key == "main":
                    self.main_entry_point = task

            if parent:
                parent.add_child(task)

        if parent is None:
            # Set relationships for all tasks after parsing is complete
            self.set_all_relationships()
            # Resolve dependencies across the entire graph
            self.set_all_dependencies()

        return list(self.tasks.values())  # Return list of tasks

    def set_all_relationships(self):
        for task in self.tasks.values():
            task.set_relationships()

        # Identify top-level tasks and set them as siblings
        top_level_tasks = [task for task in self.tasks.values() if task.parent is None]
        for task in top_level_tasks:
            task.siblings = [sibling for sibling in top_level_tasks if sibling != task]

    def set_all_dependencies(self):
        for task in self.tasks.values():
            if task.formula:
                dependencies, object_dependencies = self._find_dependencies(task)
                for dep_name in dependencies:
                    resolved_dependency = self._resolve_dependency(task, dep_name)
                    if resolved_dependency:
                        task.add_dependency(resolved_dependency)
                    else:
                        print(f"Warning: Dependency '{dep_name}' for task '{task.name}' not found in the task structure.")
                for obj_dep_name in object_dependencies:
                    resolved_object_dependency = self._resolve_dependency(task, obj_dep_name)
                    if resolved_object_dependency:
                        task.add_object_dependency(resolved_object_dependency)
                    else:
                        print(f"Warning: Object Dependency '{obj_dep_name}' for task '{task.name}' not found in the task structure.")

    def _resolve_dependency(self, task, dep_name):
        # Step 1: Check among siblings in the same scope
        for sibling in task.siblings:
            if sibling.name.endswith(dep_name):  # Check by name ending to account for full-scoped names
                return sibling

        # Step 2: Traverse up the parent hierarchy
        parent = task.parent
        while parent:
            # Check if the parent itself matches
            if parent.name.endswith(dep_name):
                return parent
            # Check the parent's siblings
            for sibling in parent.siblings:
                if sibling.name.endswith(dep_name):
                    return sibling
            # Move to the next ancestor
            parent = parent.parent

        # Return None if no matching task was found in the hierarchy
        return None

    def _find_dependencies(self, task):
        dependencies = set()
        object_dependencies = set()

        # Remove all quoted strings from the formula to ignore them as dependencies
        formula_without_strings = re.sub(r'["\'](.*?)["\']', '', task.formula)

        # Identify potential names in the formula that could be dependencies
        names_in_formula = re.findall(r'\b\w+\b', formula_without_strings)

        for name in names_in_formula:
            # Ignore method calls by checking for names followed by parentheses
            if re.search(rf'\b{name}\s*\(', formula_without_strings):
                continue  # Skip any names followed by '(' as they are method calls

            # If the name appears to be part of a method call chain, add it to object dependencies
            if re.search(rf'\b{name}\.\w+\(', formula_without_strings):
                object_dependencies.add(name)
            else:
                dependencies.add(name)

        return dependencies, object_dependencies

    def get_entry_point(self):
        return self.main_entry_point

    def __repr__(self):
        return "\n".join(str(task) for task in self.tasks.values())

# Main function to parse a JSON object or file
def create_task_graph_from_json(json_data):
    task_graph = TaskGraph()
    task_graph.parse(json_data)
    return task_graph

# Sample Usage
if __name__ == "__main__":
    # Generate the task graph
    task_graph = create_task_graph_from_json(json_data)

    # Display main entry point and full graph
    print("Main Entry Point:", task_graph.get_entry_point())
    print("Full Task Graph:")
    print(task_graph)
