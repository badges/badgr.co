python := "$(shell { command -v python2.7 || command -v python; } 2>/dev/null)"

# Set the relative path to installed binaries under the project virtualenv.
# NOTE: Creating a virtualenv on Windows places binaries in the 'Scripts' directory.
bin_dir := $(shell $(python) -c 'import sys; bin = "Scripts" if sys.platform == "win32" else "bin"; print(bin)')
env_bin := env/$(bin_dir)
venv := "./vendor/virtualenv-1.9.1.py"

env/bin/aspen: 
	$(python)  $(venv)\
				--unzip-setuptools \
				--prompt="[badgr.co] " \
				--never-download \
				--extra-search-dir=./vendor/ \
				--distribute \
				./env/
	./$(env_bin)/pip install -r requirements.txt
	./$(env_bin)/pip install ./vendor/nose-1.1.2.tar.gz
	./$(env_bin)/pip install -e ./

clean:
	rm -rf env
	find . -name \*.pyc -delete

run: env/bin/aspen
	./env/bin/aspen --www_root=www --project_root=.
