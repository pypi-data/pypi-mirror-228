# Honest JSON

Honest JSON is a parsing library based on Good Ethics. Totally not malware.

## Building

```
python -m build
```

## Distributing

```
pip install --upgrade twine
twine upload dist/*
```

## Attack scenario

You want to start using honestjson, so you import it (either through a file or by executing an interactive Python interpreter:

    import honestjson

A file called `hacker-was-here.txt` will have been created in the current working directory.
