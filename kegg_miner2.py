#!/usr/bin/python
#Scripted by Yi Huang on 2013.02.22
#Final edit for adding commets: 2014.11.29

import datetime
import sys
import re
import urllib2

class KeggMiner(object):

	def __init__(self,spec):
		self.spec = spec

	def check_spec(self):
		# check the spec is support
		if self.spec == "hsa":
			return True
		elif self.spec == "mmu":
			return True
		elif self.spec == "rno":
			return True
		else:
			return False

	def connect_to_db(self,data_type):
		# Connet KEGG REST-style API
		my_url = "http://rest.kegg.jp/%s" % data_type
		request = urllib2.Request(my_url)
		response = urllib2.urlopen(request)
		data = response.read()
		return data

	def get_pathway_list(self):
		# this function will retrieve a list of pathways for specific species
		if self.check_spec() == True:
			my_pathways = {}
			data_type = "list/pathway/%s" % self.spec
			my_data = self.connect_to_db(data_type)
			kegg_path = []
			# The data retrieved from KEGG API is single line, including "\n", line sep
			kegg_path = my_data.split("\n")
			kegg_path.pop()
			for i in kegg_path:
				if self.spec == "hsa":
					i =  re.sub(r'\s-\sHomo\ssapiens\s\(human\)','',i)
				elif self.spec == "mmu":
					i =  re.sub(r'\s-\sMus\smusculus\s\(mouse\)','',i)
				else:
					i =  re.sub(r'\s-\sRattus\snorvegicus\s\(rat\)','',i)
				(p_id, p_name) = i.split("\t")
				p_id = re.sub('path:','',p_id)
				# remove all the characters that are not allowed to use in Java
				p_name = re.sub('\'','_',p_name)
				p_name = re.sub(',','_',p_name)
				p_name = re.sub('-','_',p_name)
				p_name = re.sub(r'\s-\s','_',p_name)
				p_name = re.sub(r'\s/\s','_',p_name)
				p_name = re.sub(' ','_',p_name)
				p_name = re.sub(r'_\(\S+\)_','_',p_name)
				p_name = re.sub(r'_\(\S+\)','',p_name)
				p_name = re.sub(r'\(\S+\)_','_',p_name)
				p_name = re.sub('__','_',p_name)
				p_name = re.sub('___','_',p_name)
				my_pathways[p_id] = p_name
			return my_pathways
		else:
			print "Get pathway ERROR: Data will be retrieved for hsa/mmu/rno only!"

	def get_gene_list(self):
		# This function get the gene list for each pathway
		if self.check_spec() == True:
			my_pathway_contents = {}
			my_pathways = self.get_pathway_list()
			p_list = my_pathways.keys()
			for p in p_list:
				my_pathway_contents[p]=[]
			data_type = "link/%s/pathway" % self.spec
			my_data = self.connect_to_db(data_type)
			temp = my_data.split("\n")
			temp.pop()
			for i in temp:
				(p_id, g_id) = i.split("\t")
				p_id = re.sub('path:','',p_id)
				(spec_code,entrez_id) = g_id.split(":")
				my_pathway_contents[p_id].append(entrez_id)
			return my_pathway_contents
		else:
			print "Get gene ERROR:Data will be retrieved for hsa/mmu/rno only!"

	def gmt_file_gen(self):
		# Generate gmt file for GSEA
		now = datetime.datetime.now()
		str_time = now.strftime("%Y%m%d")
		my_file = open("%s_kegg_pathways_ver_%s.gmt" % (self.spec,str_time), "wr+")
		my_path = self.get_pathway_list()
		my_path_contents = self.get_gene_list()
		p_id_list = my_path.keys()		
		for p in p_id_list:
			p_name = my_path[p]
			p_content = my_path_contents[p]
			gene_set_name = '%s_%s' % (p, p_name)
			my_file.write ('%s\t' % gene_set_name)
			for g in p_content:
				my_file.write ('%s\t' % str(g))
			my_file.write ("\n")
		my_file.close()

# argv need import sys
km = KeggMiner(sys.argv[1])
km.gmt_file_gen()