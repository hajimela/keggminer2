#!/usr/bin/python
#First version: by Yi Huang on 2013.02.22
#Final edit for adding commets: 2014.11.29

import datetime
import sys
import re

class KeggHierFormatter(object):

	def __init__(self,infile):
		
		self.infile = infile

	def gen_relationship(self):

		now = datetime.datetime.now()
		str_time = now.strftime("%Y%m%d")
		infile = open (self.infile,"r")
		outfile = open ('%s_kegghier_formatted_ver%s.txt' % (self.infile, str_time), "w")
		
		# Variable for the first lvl of KO
		a = ''
		# Variable for the second lvl of KO
		b = ''
		# Variable for the pathway name
		c = ''
		# merge a, b and c
		merge = ''
		# KEGG pathway ID
		kegg_id = ''
		# Hash: kegg_id -> merged info
		relationship = {}
		
		for line in infile:
			line =  re.sub(r'\n','',line)
			if re.search(r'^#',line) or re.search(r'^!',line):
				next
			elif re.search(r'^A',line):
				# Example: A<b>Global Map</b>
				line = re.sub('A<b>','',line)
				line = re.sub('</b>','',line)
				a = line
			elif re.search(r'^B',line):
				# Example: B  Metabolism
				line = re.sub(r'^B\s+','',line)
				b = line
			elif re.search(r'^C',line):
				# Example: C    01100  Metabolic pathways
				line = re.sub(r'^C\s+','',line)
				line = re.sub(r'\s\s+','\t',line)
				(kegg_id, c) = line.split('\t')
				c2 = re.sub('\'','_',c)
				c2 = re.sub(',','_',c2)
				c2 = re.sub('-','_',c2)
				c2 = re.sub(r'\s-\s','_',c2)
				c2 = re.sub(r'\s/\s','_',c2)
				c2 = re.sub(' ','_',c2)
				c2 = re.sub(r'_\(\S+\)_','_',c2)
				c2 = re.sub(r'_\(\S+\)','',c2)
				c2 = re.sub(r'\(\S+\)_','_',c2)
				c2 = re.sub('__','_',c2)
				c2 = re.sub('___','_',c2)
				merge = '%s\t%s\t%s\t%s\n' % (str(a),str(b),str(c),str(c2))
				outfile.write(merge)
		infile.close()
		outfile.close()

kf = KeggHierFormatter('br08901.keg')
kf.gen_relationship()
