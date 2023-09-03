# SnippetConverter
## Usage
This converts a KDevelop (or Kate) snippet to a VSCode snippet.
Example of usage:

```bash
snippetconverter.py -i  $HOME/.local/share/ktexteditor_snippets/data/CMake\ snippets.xml -o $HOME/.config/Code/User/snippets/cmake.json
```

## Development

How to install development dependencies
```bash
python3 -m pip install -r requirements
```

How to run tests
```python
coverage run -m pytest
``````

How to see code coverage
```python
coverage html && xdg-open htmlcov/index.html
``````
