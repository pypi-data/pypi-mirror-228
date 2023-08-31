import os
import shutil
from pathlib import Path
from typing import Dict

import nox
from laminci.nox import login_testuser1, login_testuser2, run_pre_commit

nox.options.default_venv_backend = "none"

COVERAGE_ARGS = "--cov=lnhub_rest --cov-append --cov-report=term-missing"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


def get_local_env() -> Dict[str, str]:
    env = {
        "LAMIN_ENV": "local",
        "POSTGRES_DSN": os.environ["DB_URL"].replace('"', ""),
        "SUPABASE_API_URL": os.environ["API_URL"].replace('"', ""),
        "SUPABASE_ANON_KEY": os.environ["ANON_KEY"].replace('"', ""),
        "SUPABASE_SERVICE_ROLE_KEY": os.environ["SERVICE_ROLE_KEY"].replace('"', ""),
    }
    return env


@nox.session
def test_lnhub_ui(session: nox.Session):
    session.run(*"pip install -e .[dev,test,server]".split())
    env = get_local_env()
    session.run(*"lnhub alembic upgrade head".split(), env=env)
    # the -n 1 is to ensure that supabase thread exits properly
    session.run(*f"pytest -n 1 {COVERAGE_ARGS}".split(), env=env)


@nox.session
@nox.parametrize("lamin_env", ["local", "staging", "prod"])
def test_lamindb_setup(session: nox.Session, lamin_env: str):
    session.run(*"pip install .[dev,test,server]".split())
    session.run(*"pip install ./lamindb-setup[dev,test,aws]".split())
    if lamin_env != "local":
        env = {"LAMIN_ENV": lamin_env}
        login_testuser1(session, env=env)
        login_testuser2(session, env=env)
        with session.chdir("./lamindb-setup"):
            session.run(
                *"pytest --ignore tests/test_bionty.py --ignore tests/hub"
                " ./tests".split(),
                env=env,
            )
    else:
        env = get_local_env()
        session.run(*"lnhub alembic upgrade head".split(), env=env)
        shutil.copy("./tests/conftest.py", "./lamindb-setup/tests/")
        try:
            with session.chdir("./lamindb-setup"):
                # the -n 1 is to ensure that supabase thread exits properly
                session.run(*"pytest -n 1 ./tests/hub".split(), env=env)
        finally:
            Path("./lamindb-setup/tests/conftest.py").unlink()
