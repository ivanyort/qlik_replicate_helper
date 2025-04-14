# qlik_replicate_helper

`qlik_replicate_helper` is a command-line utility designed to simplify the manipulation of Qlik Replicate task definitions exported as JSON. It provides a set of commands to streamline common operations such as creating REST endpoints, adding tables to tasks, renaming schemas, and more.

---

## Features

- **Rename task**: Renames the task in the exported json file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/qlik_replicate_helper.git
   cd qlik_replicate_helper
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

All commands are executed via the `main.py` entrypoint. The first argument is the operation name, followed by operation-specific parameters.

### Rename task

```bash
Usage: python main.py <input_file> renametask <new_name>
```
### Add Tables

```bash
Usage: python main.py <input_file> addtables <xlsx_new_tables>
```
### Add Columns

```bash
Usage: python main.py <input_file> addcolumns <xlsx_new_columns>
```

### Command Concatenation

```bash
python main.py template.json renametask new_name \
-- addtables list_add.xlsx \
-- addcolumns list_new_columns.xlsx
```


## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -m "Add my feature"`.
4. Push to the branch: `git push origin feature/my-feature`.
5. Open a Pull Request.

Please follow the existing code style and add tests for new functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
