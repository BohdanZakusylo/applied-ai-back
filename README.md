# applied-ai-back

windows:
python -m venv ./.venv

./.venv\Scripts\activate

macos
python -m venv ./.venv

source .venv/bin/

after that for both platforms:

pip install -r requirements.txt

uvicorn main:app --reload