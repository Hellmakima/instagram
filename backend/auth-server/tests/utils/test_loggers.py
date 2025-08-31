# test_loggers.py
import logging
import os
from pathlib import Path
import pytest
from app.utils.loggers import init_loggers

@pytest.fixture(scope="module")
def setup_logs(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("logs_test")
    os.chdir(tmp_dir)  # isolate log files
    init_loggers()
    return tmp_dir

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
