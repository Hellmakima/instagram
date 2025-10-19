# app/tests/unit/utils/test_loggers.py

import logging
from pathlib import Path
import pytest
from app.utils.loggers import init_loggers

@pytest.fixture(scope="function")
def setup_logs(tmp_path_factory, monkeypatch):
    tmp_dir = tmp_path_factory.mktemp("logs_test")
    # Ensure init_loggers writes to tmp_dir by setting AUTH_SERVER_LOG_DIR
    log_dir = tmp_dir / "logs"
    monkeypatch.setenv("AUTH_SERVER_LOG_DIR", str(log_dir))
    # Make sure any previously-configured handlers (from app import) are removed/closed
    try:
        logging.shutdown()
    except Exception:
        pass
    # Clear handlers on root and all existing loggers so init_loggers creates fresh handlers
    logging.root.handlers.clear()
    for name, obj in list(logging.root.manager.loggerDict.items()):
        if isinstance(obj, logging.Logger):
            obj.handlers.clear()
            obj.filters.clear()

    init_loggers()
    try:
        yield tmp_dir
    finally:
        # Explicit cleanup: remove any logs directory created under the tmp dir
        import shutil
        logs_dir = tmp_dir / "logs"
        shutil.rmtree(logs_dir, ignore_errors=True)

def test_flow_logger_writes_file(setup_logs):
    logger = logging.getLogger("app_flow")
    logger.debug("flow debug test")
    flow_log = Path(setup_logs) / "logs" / "flow.log"
    assert flow_log.exists()
    content = flow_log.read_text()
    assert "flow debug test" in content

def test_security_logger_respects_json_or_verbose(setup_logs):
    logger = logging.getLogger("security_logger")
    logger.info("security info test")
    sec_log = Path(setup_logs) / "logs" / "security.log"
    assert sec_log.exists()
    content = sec_log.read_text()
    # Check either JSON or verbose contains the message
    assert "security info test" in content

def test_db_logger_level(setup_logs):
    logger = logging.getLogger("app_db")
    logger.debug("db debug test")
    db_log = Path(setup_logs) / "logs" / "db.log"
    assert db_log.exists()
    content = db_log.read_text()
    assert "db debug test" in content
