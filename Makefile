.ONESHELL:

# Need to specify bash in order for conda activate to work.
SHELL=/bin/bash
# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH
CONDA=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda

# Get versions
PACKAGE_NAME=$(shell python3 -c "from configparser import ConfigParser; p = ConfigParser(); p.read('setup.cfg'); print(p['metadata']['name'])")
PYTHON_VERSION=$(shell python3 -c "from configparser import ConfigParser; p = ConfigParser(); p.read('setup.cfg'); print(p['options']['recommended_python'])")
ENV_NAME=${PACKAGE_NAME}_py${PYTHON_VERSION}

create:
	$(CONDA) create -n ${ENV_NAME} python=$(PYTHON_VERSION) -y;

requirements:
	($(CONDA) activate ${ENV_NAME}; pip install -r requirements.txt; pip install -r requirements-dev.txt;)
	[[ -f requirements-dev.txt ]] && echo "This file exists!"

kernel:
	$(CONDA) activate ${ENV_NAME}; ipython3 kernel install --user --name=${ENV_NAME};

install:
	$(CONDA) activate ${ENV_NAME} ; python setup.py develop

clean: clean-pyc
	@echo clean ${ENV_NAME};
	$(CONDA) activate base;
	$(CONDA) remove env -n ${ENV_NAME};
	rm -rf ~/.local/share/jupyter/kernels/${ENV_NAME};

env: create requirements kernel install

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +;
	find . -name '*.pyo' -exec rm --force {} +;

test: clean-pyc
	pytest --verbose --color=yes tests;

web:
	~/projects/web/deploy2online.sh
