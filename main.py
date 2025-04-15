# main.py

import sys
import importlib.util
import os

import src.addcolumns
import src.addtables
import src.renametask
import src.renametables

seq = 0

def next_seq():
    global seq
    seq += 1
    return seq

def main():
    # We need at least 3 arguments: script name, input file, and at least one function
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_file> <func1> [args...] [-- <func2> [args...]] ...")
        sys.exit(1)

    # The first argument is always the input file
    input_file = sys.argv[1]

    # The rest of the arguments specify functions and their parameters
    raw_args = sys.argv[2:]

    # Split into segments on '--'
    segments = []
    current = []
    for token in raw_args:
        if token == '--':
            if current:
                segments.append(current)
                current = []
        else:
            current.append(token)
    if current:
        segments.append(current)

    # Start chaining with the input file as the initial "previous output"
    previous_output = input_file

    for segment in segments:
        # First element is the function/module name
        func_name = segment[0]
        # The rest are that function’s arguments
        func_args = segment[1:]

        # Always prepend the previous output (initially the input file)
        func_args = [previous_output] + func_args

        # Dynamically import the module from src/
        try:
            func_file = f"src{os.sep}{func_name}.py"
            spec = importlib.util.spec_from_file_location(func_name, func_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
        except ImportError:
            print(f"Module 'src{os.sep}{func_name}.py' not found.")
            sys.exit(1)

        # Look for a function matching the module name, or fallback to main()
        if hasattr(module, func_name):
            func = getattr(module, func_name)
        elif hasattr(module, "main"):
            func = getattr(module, "main")
        else:
            print(f"Module '{func_name}' has no function '{func_name}' or 'main'.")
            sys.exit(1)

        # Execute the function and capture its return value
        try:
            result = func(*func_args)
        except Exception as e:
            print(f"Error executing function '{func_name}': {e}")
            sys.exit(1)

        # If the function returned a non-empty string, treat it as the next output file
        if isinstance(result, str) and result:
            previous_output = result
        else:
            # Otherwise, error
            raise "Fail in creating output"

    # Finally, print the resulting output file (if any)
    if previous_output:
        print(f"{previous_output}")
        return previous_output
    
    print(f"No Final file")
    return

if __name__ == "__main__":
    main()
