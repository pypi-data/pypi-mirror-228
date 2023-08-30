import io
import sys
import gzip
import tempfile
from itertools import chain as chain

from genbank.locus import Locus

class File(dict):
	def __init__(self, filename=None):
		if not hasattr(self, 'locus'):
			self.locus = Locus
		''' use tempfiles since using next inside a for loop is easier'''
		temp = tempfile.TemporaryFile()
		
		lib = gzip if filename.endswith(".gz") else io
		with lib.open(filename, mode="rb") as fp:
			for line in chain(fp, [b'>']):
				# FASTA
				if line.startswith(b'>') and temp.tell() > 1:
					locus = self.parse_locus(temp)
					self[locus] = True
				temp.write(line)
				# GENBANK
				if line.startswith(b'//'):
					locus = self.parse_locus(temp)
					self[locus] = True 
		temp.close()
	
	def __init_subclass__(cls, locus, **kwargs):
		'''this method allows for a Locus class to be modified through inheritance in other code '''
		super().__init_subclass__(**kwargs)
		cls.locus = locus

	'''
	def __iter__(self):
		# hopefully this doesnt break stuff
		return iter(self.values())
	'''

	def features(self, include=None, exclude=None):
		for locus in self:
			for feature in locus.features(include=include):
				yield feature
	
	def dna(self):
		dna = [locus.dna for locus in self.values()]
		return "".join(dna)

	def parse_locus(self, fp):
		locus = self.locus()
		current = fasta = False
		dna = []	
		fp.seek(0)
		for line in fp:
			line = line.decode("utf-8")
			if line.startswith('\n'):
				pass
			elif not line.startswith(' '):
				# ITS A NEW MAIN GROUP
				group,*value = line.split(maxsplit=1)
				if line.startswith('>'):
					locus.groups['LOCUS'] = [group[1:]]
					fasta = True
				elif fasta:
					dna.append( line.rstrip().replace(' ','').lower() )
				elif line.startswith('//'):
					break
				else:
					locus.groups.setdefault(group, []).append(''.join(map(str, value)))
					#if group in locus.groups and locus.groups[group][-1]:
					#	locus.groups[group].append(''.join(map(str,value)))
					#else:
					#	locus.groups[group] = [''.join(map(str,value))]
			elif group == 'ORIGIN':
				#locus.dna += line.split(maxsplit=1)[1].rstrip().replace(' ','').lower()
				dna.append( line.split(maxsplit=1)[1].rstrip().replace(' ','').lower() )
			elif group == 'FEATURES':
				line = line.rstrip()
				if not line.startswith(' ' * 21):
					while line.endswith(','):
						line += next(fp).decode('utf-8').strip()
					current = locus.read_feature(line)
				else:
					while line.count('"') == 1:
						line += " " + next(fp).decode('utf-8').strip()
					tag,sep,value = line[22:].partition('=')
					#current.tags[tag] = value #.replace('"', '')
					if sep:
						current.tags.setdefault(tag, []).append(value)
					else:
						current.tags.setdefault(tag, []).append(None)
			else:
				locus.groups[group][-1] += line

		locus.dna = ''.join(dna)
		fp.seek(0)
		if fp.writable():
			fp.truncate()
		return locus

	def write(self, outfile=sys.stdout):
		for locus in self:
			locus.write(outfile)

