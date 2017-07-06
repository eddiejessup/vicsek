Vicsek
======

An implementation of a couple of variants of the Vicsek model, using Cython to be fast, and cell lists to scale well with the number of agents.

Intended for Python 3, but I've had a skim through the code and I can't see anything particularly three-ey.

Installation
============

First, clone this repository:

```bash
git clone https://github.com/eddiejessup/vicsek.git
```

Now go into the top level (also known as the 'root') of the repository (inside the `vicsek` directory where you ran `git clone`).

As in most situations when messing around with a Python package, I recommend working inside a Python virtual environment (often shortened to 'virtualenv'). [Here](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) is an explanation of how and why to use them.

If you don't use a virtual environment then you can prepend the `pip` commands with `sudo` if they don't work (try without first). But this is discouraged because it could mess up the Python environment used by your operating system.

While inside the virtual environment you wish to use, install the dependencies needed to build, run and test the code:

```bash
pip install -r requirements.txt
```

If this fails with errors saying things like 'permission denied', probably you aren't inside a virtualenv, so you need to activate one, or, if you're feeling lazy, add `sudo` to the beginning of the command.

Now, again in the root of the repository, compile the Cython extension for the core numerics:

```bash
python setup.py build_ext --inplace
```

You should now have a file ending in `.so` inside the `vicsek` directory. Now check you can run the tests, by going into the root and running `pytest`. If the test pass, then that's better than if they had failed.

Usage
=====

See `examples.py` for some illustrations.

Authors
=======

Elliot Marsden
