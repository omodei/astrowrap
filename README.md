# astrowrap
Wrapper of the astroserver using the data catalog

### Author: Nicola Omodei (nicola.omodei@gmail.com)
```
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
```
Make sute the python directory is addded to your $PATH

The environment variable **DATACATALOG_EXE** needs to point to the datacatalog application. If you don't define it, it points to the datacatalog app at SLAC in S3DF : `/sdf/home/g/glast/a/datacat/prod/datacat`. 
If you want to change it, add this to your setup:
```
export DATACATALOG_EXE=_new_datacatalog_app_path_
```
##Examples:
The following examples downloads an FT2 file:

```
getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft2.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type FT2 --verbose 1 --overwrite 1
```
An FT2 file with 1 second cadence:
```
getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft2_1sec.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type FT2SECONDS --verbose 1 --overwrite 1
```
A FT1 file and an extended FT1 file:
```getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft1.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type FT1 --verbose 1 --overwrite 1
```
An extended FT1 file:
```
./getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft1_ext.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type EXTENDEDFT1 --verbose 1 --overwrite 1
 ```
Note that no extra selection are made, so the FT1 files will always contain the full sky, and the full energy range. Subsequent selection cut needs to be independently done with gtselect, gtmktime, etc...

To decide which FT1 you need to retrieve, please ahve a look here:
https://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_Data/LAT_DP.html
