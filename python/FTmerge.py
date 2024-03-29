#!/usr/bin/env python
"""
@brief Use the fmerge FTOOL to merge FT1 files, combining both the
EVENTS and GTI extensions.  It is implicitly assumed that the time
intervals covered by the files do not overlap and that any other
selections, such as acceptance cone, energy range, or event class
cuts, are the same for all of the files.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header: /nfs/slac/g/glast/ground/cvs/GRBAnalysis-scons/GtGRB/python/GTGRB/FTmerge.py,v 1.6 2019/02/26 16:56:05 omodei Exp $
#

import os,sys
import astropy.io.fits as pyfits
from GtApp import GtApp
from met2date import met2date

fcopy = GtApp('fcopy')
fmerge = GtApp('fmerge')
fchecksum = GtApp('fchecksum')

def _fileList(infiles, extnum=1):
    filelist = 'ft1merge_file_list'
    if len(infiles) > 1000:
        raise RuntimeError('Number of input files exceeds 1000, '
                             + 'the fmerge maximum.')
    infile_list = open(filelist, 'w')
    for item in infiles:
        infile_list.write(item + ('[%s]\n' % extnum))
    infile_list.close()
    return filelist

def _getTimeKeywords(infiles, extnum=1):
    header = pyfits.open(infiles[0])[extnum].header
    tstart = header['TSTART']
    tstop  = header['TSTOP']
    for item in infiles[1:]:
        header = pyfits.open(item)[extnum].header
        if header['TSTART'] < tstart:
            tstart = header['TSTART']
        if header['TSTOP'] > tstop:
            tstop = header['TSTOP']
    return tstart, tstop

def updateTimeKeywords(fitsfile, tstart, tstop):
    foo = pyfits.open(fitsfile)
    foo[0].header['FILENAME'] = os.path.basename(fitsfile)
    for i in range(len(foo)):
        try:
            foo[i].header['TSTART']   = tstart
            foo[i].header['TSTOP']    = tstop
            foo[i].header['DATE-OBS'] = met2date(tstart)
            foo[i].header['DATE-END'] = met2date(tstop)
        except KeyError:
            pass
    foo.writeto(fitsfile, overwrite=True)

def updateTLKeywords(fitsfile):
    foo = pyfits.open(fitsfile)
    foo[0].header['SOFTWARE'] = 'astrowrap'
    foo['SC_DATA'].header['TLMAX1']   = 10000000000.0
    foo['SC_DATA'].header['TLMAX10'] =      100.0
    foo['SC_DATA'].header['TLMAX11'] =       90.0
    foo['SC_DATA'].header['TLMAX12'] =       90.0
    foo['SC_DATA'].header['TLMAX14'] =      360.0
    foo['SC_DATA'].header['TLMAX15'] =       90.0
    foo['SC_DATA'].header['TLMAX16'] =      360.0
    foo['SC_DATA'].header['TLMAX17'] =       90.0
    foo['SC_DATA'].header['TLMAX18'] =      360.0
    foo['SC_DATA'].header['TLMAX19'] =       90.0
    foo['SC_DATA'].header['TLMAX2']  = 10000000000.0
    foo['SC_DATA'].header['TLMAX20'] =      180.0
    foo['SC_DATA'].header['TLMAX29'] =      360.0
    foo['SC_DATA'].header['TLMAX30'] =       90.0
    foo['SC_DATA'].header['TLMAX4']  =       90.0
    foo['SC_DATA'].header['TLMAX5']  =      360.0
    foo['SC_DATA'].header['TLMAX6']  =    10000.0
    foo['SC_DATA'].header['TLMAX7']  =      360.0
    foo['SC_DATA'].header['TLMAX8']  =       90.0
    foo['SC_DATA'].header['TLMAX9']  =      100.0
    foo['SC_DATA'].header['TLMIN1']  =        0.0
    foo['SC_DATA'].header['TLMIN10'] =        0.0
    foo['SC_DATA'].header['TLMIN11'] =        0.0
    foo['SC_DATA'].header['TLMIN12'] =      -90.0
    foo['SC_DATA'].header['TLMIN14'] =        0.0
    foo['SC_DATA'].header['TLMIN15'] =      -90.0
    foo['SC_DATA'].header['TLMIN16'] =        0.0
    foo['SC_DATA'].header['TLMIN17'] =      -90.0
    foo['SC_DATA'].header['TLMIN18'] =        0.0
    foo['SC_DATA'].header['TLMIN19'] =      -90.0
    foo['SC_DATA'].header['TLMIN2']  =        0.0
    foo['SC_DATA'].header['TLMIN20'] =     -180.0
    foo['SC_DATA'].header['TLMIN29'] =        0.0
    foo['SC_DATA'].header['TLMIN30'] =      -90.0
    foo['SC_DATA'].header['TLMIN4']  =      -90.0
    foo['SC_DATA'].header['TLMIN5']  =        0.0
    foo['SC_DATA'].header['TLMIN6']  =        0.0
    foo['SC_DATA'].header['TLMIN7']  =        0.0
    foo['SC_DATA'].header['TLMIN8']  =      -90.0
    foo['SC_DATA'].header['TLMIN9']  =        0.0
    foo.writeto(fitsfile, overwrite=True)

def ft1merge(infiles, outfile):
    tstart, tstop = _getTimeKeywords(infiles)
    fmerge['infiles'] = '@' + _fileList(infiles)
    fmerge['outfile'] = outfile
    fmerge['clobber'] = 'yes'
    fmerge['columns'] = ' '
    fmerge['mextname'] = ' '
    fmerge['lastkey'] = ' '
    fmerge.run()

    fmerge['infiles'] = '@' + _fileList(infiles, 'GTI')
    fmerge['outfile'] = 'ft1merge_gti.fits'
    fmerge.run()

    foo = pyfits.open(outfile)
    gti = pyfits.open(fmerge['outfile'].strip('"'))
    foo.append(gti['GTI'])

    try:
        foo[0].header['FILENAME'] = outfile
        foo[0].header['TSTART'] = tstart
        foo[0].header['TSTOP'] = tstop
    except KeyError:
        pass
    foo[1].header['TSTART'] = tstart
    foo[1].header['TSTOP'] = tstop
    foo[2].header['TSTART'] = tstart
    foo[2].header['TSTOP'] = tstop
    foo.writeto(outfile, overwrite=True)
    
    fchecksum['infile'] = outfile
    fchecksum['update'] = 'yes'
    fchecksum['datasum'] = 'yes'
    fchecksum.run()
    
    try:
        os.remove(fmerge['outfile'].strip('"'))
    except OSError:
        pass
    try:
        filename = fmerge['infiles'].strip('"').strip('@')
        os.remove(filename)
    except OSError:
        pass

class UnpaddedFT2Files(list):
    def __init__(self, infiles, prefix='ft2_filtered'):
        list.__init__(self)
        for infile in infiles:
            outfile = infile.replace(".fits","_filtered.fits")
            try:
                os.remove(outfile)
            except OSError:
                pass
            fcopy.run(infile='%s[SC_DATA][LIVETIME>0]'%infile, 
                      outfile=outfile)
            self.append(outfile)
    def cleanup(self):
        for item in self:
            os.remove(item)

def ft2merge(infiles_arg, outfile, filter_zeros=True):
    tstart, tstop = _getTimeKeywords(infiles_arg)
    if not infiles_arg:
        raise RuntimeError("FT2 file list is empty")
    infiles = infiles_arg
    if filter_zeros:
        infiles = UnpaddedFT2Files(infiles_arg)
    tmpfile = "ft2_file_list"
    ft2list = open(tmpfile, 'w')
    for item in infiles:
        ft2list.write("%s\n" % item)
    ft2list.close()
    print ('ft2merge: tmpfile=',tmpfile)
    fmerge['infiles'] = '@%s' % tmpfile
    fmerge['outfile'] = outfile
    fmerge['clobber'] = 'yes'
    fmerge['columns'] = ' '
    fmerge['mextname'] = ' '
    fmerge['lastkey'] = ' '
    fmerge.run()
    updateTimeKeywords(outfile, tstart, tstop)
    updateTLKeywords(outfile)
    try:
        os.remove(tmpfile)
    except OSError:
        pass
    try:
        infiles.cleanup()
    except AttributeError:
        pass
    pass

if __name__ == '__main__':
    from glob import glob
    if sys.argv[1:]:
        infiles = sorted(glob(sys.argv[1]))
        try:
            ft1merge(infiles, 'merged_files_ft1.fits')
        except:
            try:
                ft2merge(infiles, 'merged_files_ft2.fits')
            except:
                pass
            pass
        pass
    # os.system('fverify merged_files.fits')
    # os.system('fchecksum merged_files.fits update=yes')
    else:
        print ('usage: ./merge_files.py \'*events*\'')
        
