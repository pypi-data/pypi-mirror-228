# Flake8 Import Linter

Flake8 plugin that checks for forbidden imports in your code

It works for both python2 and python3 since it only uses ast and configparser libraries :)

# Usage

1. flake8 config
   
    add "flake8_import_linter" section

    add "forbidden_modules" config

    example:
   
    `[flake8_import_linter]`
   
    `forbidden_modules = pytest, unittest`

3. run flake8 as always
   
    `flake8 .`

4. if a forbidden module is detected, flake8 will show:
   
     `IMP100 forbidden import`

ENJOY!
