Vicsek
======

An implementation of a couple of variants of the Vicsek model, using Cython to be fast, and cell lists to scale well with the number of agents.

Installation
============

First, install the dependencies to build and run the code,

```bash
pip install -r requirements.txt
```

Now you should be able to compile the Cython extension for the core numerics,

```bash
python setup.py build_ext --inplace
```

Now check you can run the tests, by going into the root directory and running `pytest`. If you can, all is working!

See `examples.py` for examples of usage.
