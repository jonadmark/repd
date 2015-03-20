# REsource Provision Diagnosis

## Quick Start

Firstly you need to make sure all the dependencies are satisfied. The Linux dependencies are found on the `linux-requirements.txt` file in the repository's root.

With the dependencies solved, you can execute the REPD daemon process with the following command (It is recommended to run the programs with python version 3.4):
```
python3 repdd.py
```

With the daemon process running, the client process can be executed to show the diagnostics for the last minute with the following command:
```
python3 repd.py 1
```

If you want to diagnose a especific period, you can pass the start and end timestamps of the period:
```
python3 repd.py 123 456
```
In this example the period starts at timestamp 123 and ends at 456.

## Further reading

Find more about on (PT-BR): http://pergamumweb.udesc.br/dados-bu/000001/000001e9.pdf


LICENSE: The MIT License
