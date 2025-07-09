REM --------------0. project root------------
cd /d  D:\Davin.ai\assign\Dravin_new_assign\chatbot-suite\backend

REM--------------1. create/activate env -----
IF NOT EXIST ".venv" (py -3 -m venv .venv)

CALL .venv\Scripts\activate.bat

pip install -r requirements.txt

@REM REM ------------2. load env vars from .env-------
@REM for /f "usebackq tokens=* delims=" %%A in (`
@REM     type "backend\.env" ^| findstr /R /V "^\s*#"
@REM `) do (
@REM     set "%%A"
@REM )

REM -------- 3. run migrations if alembic present --------
IF EXIST backend\alembic (
    alembic -c backend\alembic.ini upgrade head
)

set PYTHONUTF8=1

REM -------- 4. start API --------
uvicorn app.main:app --reload