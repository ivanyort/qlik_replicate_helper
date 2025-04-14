# main.py

import sys
import importlib

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <function_name> [parameters...]")
        sys.exit(1)

    # The argument provided should correspond to the module name in the src directory (without file extension)
    func_name = sys.argv[1]
    # Additional parameters provided in the command line (if any)
    additional_args = sys.argv[2:]

    try:
        # Dynamically import the module located in the src directory
        # For example, if func_name is "test", this will import "src.test"
        module = importlib.import_module(f"src.{func_name}")
    except ImportError:
        print(f"Module src/{func_name}.py not found.")
        sys.exit(1)

    # Try to find a function within the module with the same name as the module.
    # If not found, try to use a function named 'main' defined inside the module.
    if hasattr(module, func_name):
        func = getattr(module, func_name)
    elif hasattr(module, "main"):
        func = getattr(module, "main")
    else:
        print(f"The module '{func_name}' does not have a function named '{func_name}' or 'main'.")
        sys.exit(1)

    # Execute the found function, passing any additional arguments
    try:
        func(*additional_args)
    except Exception as e:
        print(f"An error occurred while executing the function: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
