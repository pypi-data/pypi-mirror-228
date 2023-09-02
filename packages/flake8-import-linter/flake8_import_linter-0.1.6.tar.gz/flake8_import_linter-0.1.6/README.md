# Flake8 Import Linter

Flake8 plugin that checks for forbidden imports in your code

# Usage

1. flake8 config
    add "flake8_import_linter" section 
    add "forbidden_modules" config 

    example:
    `
        [flake8_import_linter]
        forbidden_modules = "pytest", "unittest"
    `

2. run flake8 as always
    `flake8 .`

3. if a forbidden module is detected, flake8 will show:
     `IMP100 forbiden import`

4. ENJOY!