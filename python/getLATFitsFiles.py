#!/usr/bin/env python
import os, subprocess
import socket
import sys
from astropy.io import fits as pyfits

def runShellCommand(string,echo=False):
	# This is to substitute os.system, which is not working well
	# in the ipython notebook
	if(echo): print("\n%s\n" % string)
	try:
		retcode = subprocess.call(string, shell=True)
		if retcode < 0:
			print >>sys.stderr, "Child was terminated by signal", -retcode
		else:
			pass
		pass
	except OSError, e:
		print >>sys.stderr, "Execution failed:", e
		pass
	pass

class astrowrap():
	''' Emulate the astroserver using the datacatalog at SLAC '''
	def __init__(self, verbose = True,  wdir    = 'WDIR'):

		self.wdir  = wdir
		self.verbose = verbose
		pass


	def myprint(self,msg):
		if self.verbose: print(msg)
		pass

	def checkFile(self, name, tstart, tend):
		# This simply check that the files have the desired lenght
		self.myprint("Checking file %s" % name)		
		data = pyfits.open(name)[1].data

		if 'TIME' in data.names:   
			TMIN=data.field('TIME').min()
			TMAX=data.field('TIME').max()
		elif 'STOP' in data.names: 
			TMAX=data.field('START').max()
			TMIN=data.field('STOP').min()
		else: raise NameError('Unrecognize field name in checkFile')
		DT0=tstart-TMIN
		if DT0<0:
			self.myprint("====> file probably incomplete. DT (START)= %.1f should be positive" % DT0)
			return False	
		
		DT1=TMAX-tend
		if DT1<0:
			self.myprint("====> file probably incomplete. DT (STOP)= %.1f should be positive" % DT1)
			return False
		
		self.myprint("====> file complete (%.1f - %.1f)" % (DT0,DT1))
		return True
	
	def getDataCatalogList(self,tstart, tend, group='EXTENDEDFT1',logicalPath='/Data/Flight/Level1/LPA'):
		if 'FT2' in group:                               logicalPath = '/Data/Flight/Reprocess/P202'
		if 'FT2SECONDS' in group:                        logicalPath = '/Data/Flight/Reprocess/P203'
		
		if 'P305' in logicalPath and tstart > 564943566: logicalPath = "/Data/Flight/Level1/LPA" # Level one pipeline
		if 'P302' in logicalPath and tstart > 456835199: logicalPath = "/Data/Flight/Level1/LPA" # Level one pipeline
		if 'P203' in logicalPath and tstart > 423447612: logicalPath = "/Data/Flight/Level1/LPA" # Level one pipeline
		if 'P202' in logicalPath and tstart > 405333211: logicalPath = "/Data/Flight/Level1/LPA" # Level one pipeline
		
		fileListName='%s/fileList%s' % (self.wdir,group)
		
		met_filter='nMetStop>=%s && nMetStart<%s' % (tstart,tend)    
		cmd='/afs/slac.stanford.edu/g/glast/ground/bin/datacat find --group %s --filter \'%s\' %s > %s' % (group,met_filter,logicalPath,fileListName)    
		runShellCommand(cmd,self.verbose)		
		return fileListName

	def getFiles(self,fileListName):
		
		tmpdir = '%s/tmp' %(self.wdir)
		runShellCommand('rm -rf %s' % tmpdir,self.verbose)
		runShellCommand('mkdir -p %s' % tmpdir,self.verbose)
		
		fileListFile = file(fileListName,'r')
		mylist       = fileListFile.readlines()
		mylist.sort()

		path_list=[]
		
		shortName = fileListName[fileListName.rfind('/')+1:]    
		baseName= '%s_%06i.fits' 
		
		for i,ele in enumerate(mylist):
			base= baseName % (shortName,i)
			newFileName='%s/%s' % (tmpdir,base)
			if ('root:' in ele):
				cmd = 'xrdcp %s %s' % (ele.strip(),newFileName)
			else:
				cmd = 'cp %s %s' % (ele.strip(),newFileName)
				pass
			runShellCommand(cmd,0)			
			path_list.append(newFileName)
			pass
		return path_list
	
	
	def getFilesDataCatalog(self, tstart, tend, group, logicalPath='/Data/Flight/Level1/LPA',overwrite=False):
		import FTmerge as FTM		
		merging_alg={'FT2':FTM.ft2merge,
			     'FT2SECONDS':FTM.ft2merge,
			     'FT1':FTM.ft1merge,
			     'EXTENDEDFT1':FTM.ft1merge
			     }
		
				
		runShellCommand('mkdir -p %s' % self.wdir,self.verbose)
		file_out_name='%s_%.0f_%.0f.fits' %(group,tstart,tend)
		file_out_path='%s/%s' %(self.wdir,file_out_name)
		# ################################
		path_list = self.getFiles(self.getDataCatalogList(tstart,tend,group,logicalPath))
		if len(path_list)==0:
			file_out_path = None
		elif len(path_list)==1:
			cmd='cp %s %s' %(path_list[0],file_out_path)
			runShellCommand(cmd,self.verbose)
		else:
			merging_alg[group](path_list,file_out_path)            
			pass
		return file_out_path
	
if __name__=='__main__':
    import os,sys
    import argparse
    '''
    ./getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft2.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type FT2 --verbose 1 --overwrite 1
    ./getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft2_1sec.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type FT2SECONDS --verbose 1 --overwrite 1
    ./getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft1.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type FT1 --verbose 1 --overwrite 1
    ./getLATFitsFiles.py --wdir TMP/SRC --outfile TMP/pippo_ft1_ext.fits --minTimestamp 565660805.000 --maxTimestamp 565747205.000 --type EXTENDEDFT1 --verbose 1 --overwrite 1
    '''
    _logicalPath = '/Data/Flight/Reprocess/P305' 
    parser = argparse.ArgumentParser(description='Emulating the astroserver by wrapping the datacatalog')
    parser.add_argument('--wdir', type=str, help='Name of the working dir where all the interidiate files are saved',default=os.getenv('OUTDIR','OUTDIR'),required=False)
    parser.add_argument('--outfile',type=str,help='Name of the output file',required=True)
    parser.add_argument('--minTimestamp',type=float,help='Minimum MET',required=True)
    parser.add_argument('--maxTimestamp',type=float,help='Maximum MET',required=True)
    parser.add_argument('--type',type=str,help='Type of the files',choices=['FT2', 'FT2SECONDS', 'FT1','EXTENDEDFT1'],required=True)
    parser.add_argument('--verbose',type=bool,help='Verbose or silent output',  choices=[0,1],required=False,default=0)
    parser.add_argument('--overwrite',type=bool,help='Overwrite if existsing?', choices=[0,1],required=False,default=0)
    args=parser.parse_args()
    if args.minTimestamp<args.maxTimestamp: 
	    aw=astrowrap(args.verbose,args.wdir)
	    flag=False
	    if os.path.exists(args.outfile): flag=aw.checkFile(args.outfile,args.minTimestamp,args.maxTimestamp)
	    if (flag==False or args.overwrite):
		    file_out_path=aw.getFilesDataCatalog(args.minTimestamp,args.maxTimestamp, args.type, logicalPath=_logicalPath,overwrite=args.overwrite)
		    runShellCommand('mv %s %s' %(file_out_path,args.outfile))
		    pass
	    pass
    
