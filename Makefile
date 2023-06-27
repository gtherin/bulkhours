.ONESHELL:

# Need to specify bash in order for conda activate to work.
SHELL=/bin/bash
# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH
CONDA=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda

# Get versions
include config.mk
PYTHON_VERSION = $(shell echo ${ENV_NAME} | tail -c 5)
PACKAGE_NAME = $(shell basename ${PWD})
ONLINE_CONNECT = $(shell cat ~/.ssh/onl)
LOCAL_DEPENDENCIES = $(shell grep LOCAL_DEPENDENCIES config.mk | cut -c 20-)


nstopv:
	$(CONDA) activate ${ENV_NAME}; cd ../nstopv && pip install develop -e .;

dapir:
	$(CONDA) activate ${ENV_NAME}; cd ../dapir && pip install develop -e .;

create:
	$(CONDA) create -n ${ENV_NAME} python=$(PYTHON_VERSION) -y;

requirements:
	($(CONDA) activate ${ENV_NAME}; pip install -r requirements.txt; pip install -r requirements-dev.txt;)

kernel:
	$(CONDA) activate ${ENV_NAME}; ipython3 kernel install --user --name=${ENV_NAME};

install: $(LOCAL_DEPENDENCIES)
	($(CONDA) activate ${ENV_NAME} ; python setup.py develop)

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
	/home/guydegnol/projects/web/deploy2online.sh
