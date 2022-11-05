#!/bin/zsh

alias python="python3.11"

if [[ ! -d venv ]]
then
    echo "creating build venv"
    python -m venv venv/
fi

if [[ -d dist ]]
then
    rm -rf dist/
fi

./venv/bin/python -m pip install --upgrade build
./venv/bin/python -m pip install --upgrade wheel
./venv/bin/python -m pip install --upgrade twine

./venv/bin/python setup.py sdist
./venv/bin/python setup.py bdist_wheel

cd dist/

python -m venv venv/
venv/bin/python -m pip install $(find . | grep whl)
echo "starting interactive shell to test package..."
venv/bin/python