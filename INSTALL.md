# Installation

* Init the submodules

```bash
git submodule update --init --recursive
```

* Install python dependencies

```bash
pip install -r requirements.txt 
```

## Gurobi Installation

* install gurobi by downloading the linux version from here: https://www.gurobi.com/downloads/gurobi-software/

```bash
tar xvfz gurobi9.5.2_linux64.tar.gz
```

* install gurobi python

```bash
python -m pip install gurobipy
```

* add the following to the bashrc

```bashrc
export GUROBI_HOME="~/gurobi1001/linux64" 
export PATH="${PATH}:${GUROBI_HOME}/bin" 
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"
```

* generate a license here
https://portal.gurobi.com/iam/home
https://portal.gurobi.com/iam/licenses/list/
