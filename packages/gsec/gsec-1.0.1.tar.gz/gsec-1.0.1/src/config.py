import os, json

if os.name == "nt":
	config_path = os.path.join(os.getenv("APPDATA"), "git-secret")
if os.name == "posix":
	config_path = os.path.join(os.getenv("HOME"), ".config/git-secret")

try:
	with open(config_path + "/config.json", "r") as f:
		config = json.load(f)
except FileNotFoundError:
	os.makedirs(config_path, exist_ok=True)
	config = {"repo_dir": os.getcwd()}
	with open(config_path + "/config.json", "w") as f:
		f.write(json.dumps(config))

def repo_dir():
	return config["repo_dir"]