## FASTAPI DEV SETUP

- Tailwind:
    1. To install tailwind CLI tool, run:
        * ``` npx install -g tailwindcss ```
    2. Then, start the CLI tool to automatically generate out.css file:
        * ``` npx tailwindcss -i ./static/input.css -o ./static/output.css --watch ```
    3. done. :)))

- Fastapi:
    1. create virtual environment:
        * ``` python -m venv .venv ```
    2. Activate virtual environment:
        * Mac/Linux: ``` source .venv/bin/activate ```
        * WindowS: ``` .venv\Scripts\Activate.ps1 ```
    3. Install dependencies from requirements.txt:
        * pip install -r requirements.txt
    4. Start fastapi dev environmnet:
        * fastapi dev main.py
    5. Profit :DDDD
