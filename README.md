# uCAPTURE

Imaging and selfcal pipeline taken from CAPTURE-CASA6, written by Ruta Kale. Utilizes wsclean for ridiculous speedup. Requires cleaned and calibrated msfiles. 

To run this pipeline, you need to build and install wsclean. The command is passed as a subprocess call, and the specific imaging paramters can be passed as a "wsclean-command" in the config.ini file.

## How to use

1. To install, make a python environment and do:

```bash
pip install .
```

2. To run you need to make a config.ini file. It can be made using:

```bash 
make_config -c <config.ini name> <msfile>
```

3. Edit the parameters in the config file to your use case.

4. To run the selfcal loop, do:

```bash
ucapture <config.ini>
```

