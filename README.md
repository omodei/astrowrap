# astrowrap
Wrapper of the astroserver using the data catalog

Author: Nicola Omodei (nicola.omodei@gmail.com)

usage: getLATFitsFiles.py [-h] [--wdir WDIR] --outfile OUTFILE --minTimestamp
                          MINTIMESTAMP --maxTimestamp MAXTIMESTAMP --type
                          {FT2,FT2SECONDS,FT1,EXTENDEDFT1} [--verbose {0,1}]
                          [--overwrite {0,1}]

Emulating the astroserver by wrapping the datacatalog

optional arguments:
  -h, --help            show this help message and exit
  --wdir WDIR           Name of the working dir where all the interidiate
                        files are saved
  --outfile OUTFILE     Name of the output file
  --minTimestamp MINTIMESTAMP
                        Minimum MET
  --maxTimestamp MAXTIMESTAMP
                        Maximum MET
  --type {FT2,FT2SECONDS,FT1,EXTENDEDFT1}
                        Type of the files
  --verbose {0,1}       Verbose or silent output
  --overwrite {0,1}     Overwrite if existsing?
