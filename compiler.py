from random import randint
import binascii
import sys
import re
from os import path, makedirs
"""
NOP
CALL x
SE Vx, x
SE Vx, Vx

"""

class Compilation_error(LookupError):

    pass

def compiler(cmd):
	instructions = ['NOP', 'CLS', 'RET', 'JP', 'CALL']
	num_match = '[0-9a-f]'

	if cmd == 'NOP':
		print(cmd, '->', ('%0*X' % (4,0) ))
		return binascii.unhexlify('0000')
	elif cmd == 'CLS':
		code = '00E0'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif cmd == 'RET':
		code = '00EE'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'JP 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = '1'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'CALL 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = '2'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SE V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '3' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SNE V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '4' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'SE V'+num_match+', V'+num_match+'', cmd):
		x = re.findall(r'V'+num_match+'', cmd)[0].replace('V','')
		y = re.findall(r'V'+num_match+'', cmd)[1].replace('V','')
		code = '5' + x + y + '0'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
		return binascii.unhexlify(code)
	elif re.match(r'LD V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '6' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'ADD V'+num_match+', 0x'+num_match+'{2}', cmd):
		x = re.search('V'+num_match+'', cmd).group(0).replace('V','')
		kk = re.search('0x'+num_match+'{2}', cmd).group(0).replace('0x','')
		code = '7' + x + kk
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'SNE V'+num_match+', V'+num_match+'', cmd):
		x = re.findall(r'V'+num_match+'', cmd)[0].replace('V','')
		y = re.findall(r'V'+num_match+'', cmd)[1].replace('V','')
		code = '9' + x + y + '0'
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'LD, 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = 'a'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'JP V0, 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = 'b'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	elif re.match(r'JP V0, 0x'+num_match+'{3}', cmd):
		addr = re.search(''+num_match+'{3}', cmd).group(0)
		code = 'c'+addr
		print(cmd, '->', ('%0*X' % (4,int('0x'+code, 0)) ))
	else:
		raise Compilation_error("No se reconoce el comando: "+ cmd)

class Compiler:
	num_match = '[0-9a-f]'
	output_folder = 'Out'

	def __init__(self):
		self.tokens = {
			"CLS" : self.CLS, "RET":self.RET, "JP"  :  self.JP, "NOP" : self.NOP,
			"CALL":self.CALL, "SE" : self.SE, "SNE" : self.SNE, "LD"  :  self.LD,
			"ADD" : self.ADD, "OR" : self.OR, "AND" : self.AND, "XOR" : self.XOR,
			"SUB" : self.SUB, "SHR":self.SHR, "SUBN":self.SUBN, "SHL" : self.SHL,
			"RND" : self.RND, "DRW":self.DRW, "SKP" : self.SKP, "SKNP":self.SKNP,
		}

	def compile(self, cmd):
		word = cmd.split(' ', 1)
		print("Token  :", word[0])
		try:
			out = self.tokens[word[0]](word[1])
			print(out)
			return out
		except KeyError:
			raise Compilation_error("No se reconoce el comando: "+ cmd)
			#return self.NOPE


	def type_addr(self, code, cmd):
		addr = re.search(self.num_match+'{3}', cmd).group(0)
		return code+addr


	def NOP(self, cmd):

		return binascii.unhexlify('0000')

	def CLS(self, cmd):

		return binascii.unhexlify('00E0')

	def RET(self, cmd):

		return binascii.unhexlify('00EE')

	def JP(self, cmd):
		"""
			JP addr     -> JP 0xNNN
			JP V0, addr -> JP VX, 0xNNN
		"""
		print(re.match(r'V[0-9a-fA-F], 0x[0-9a-fA-F]{3}', cmd))

		return binascii.unhexlify('0000')

	def CALL(self, cmd):

		return binascii.unhexlify(self.type_addr('2', cmd))

	def SE(self, cmd):

		return binascii.unhexlify('0000')

	def SNE(self, cmd):

		return binascii.unhexlify('0000')

	def LD(self, cmd):

		return binascii.unhexlify('0000')

	def ADD(self, cmd):

		return binascii.unhexlify('0000')

	def OR(self, cmd):

		return binascii.unhexlify('0000')

	def AND(self, cmd):

		return binascii.unhexlify('0000')

	def XOR(self, cmd):

		return binascii.unhexlify('0000')

	def SUB(self, cmd):

		return binascii.unhexlify('0000')

	def SHR(self, cmd):

		return binascii.unhexlify('0000')

	def SUBN(self, cmd):

		return binascii.unhexlify('0000')

	def SHL(self, cmd):

		return binascii.unhexlify('0000')

	def RND(self, cmd):

		return binascii.unhexlify('0000')

	def DRW(self, cmd):

		return binascii.unhexlify('0000')

	def SKP(self, cmd):

		return binascii.unhexlify('0000')

	def SKNP(self, cmd):

		return binascii.unhexlify('0000')




compiler = Compiler()

if not path.exists(compiler.output_folder):
	makedirs(compiler.output_folder)

with open('Programs/Test.Chip8', 'r') as f,\
	 open(path.join(compiler.output_folder, 'TEST'), 'wb') as out:
	for i in f:
		line = i.strip("\n")
		if line:
			print("Command:", line)
			if line[0] != '#':
				out.write(compiler.compile(line))
			else:
				print('Comment', line)



