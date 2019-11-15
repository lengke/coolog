import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from coolog import create_app

# 正式上线应将development改为production
# 并且正式上线环境记得建立coolog_pro数据库
app = create_app('development')
