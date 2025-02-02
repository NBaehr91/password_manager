import sys
sys.path.insert(0, 's:/Programming/Projects/password_manager')
import src
from src.database import passwordStorage as ps


ps.register_master_password("test2", "test")
ps.check_master_password("test", "test")