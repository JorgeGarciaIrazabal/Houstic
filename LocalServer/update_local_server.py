import os
import sys
from jenkinsapi.jenkins import Jenkins

sys.path += [os.path.join(os.path.dirname(__file__), os.pardir, "PythonUtils")]

from libs.config import Config

Config.get().read_config_file()

J = Jenkins('http://{}:8080'.format(Config.get().house_ip))
J.build_job('GithubHandler')
