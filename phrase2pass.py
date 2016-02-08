import re
symbols = ['!','@','#','%','&']
pass_length = 12
pharse = raw_input("Pharse for the site password :\n")
if len(pharse) < 1:
  print "Don't ya f#$k with me"
  exit()
  
text = pharse.lower()
# Using regex to filer alphabets
alpha = re.findall('[a-z]*',text)
# Now second filter is to remove all empty string in list
alpha = filter(None,alpha)

def find_whole(temp_list,(init,end)):
  for item in temp_list:
    if init <= len(item) <= end:
      return item
    
# Finding a whole word within lower,upper bound given in tupple
whole_1 = find_whole(alpha,(4,5))
if whole_1 is None:
  whole_1 = find_whole(alpha,(3,5)) 
if whole_1 is None:
  whole_1 = find_whole(alpha,(2,5)) 
if whole_1 in alpha:
  alpha.remove(whole_1)
  
text  = ''.join(alpha)
if whole_1 is not None:
  pass_length = pass_length - len(whole_1)
else:
  whole_1 = ''

def _to_numb(temp):
  temp_numb = ''
  for char in temp:
    temp_numb = temp_numb + str(ord(char)%10)
  return temp_numb  

def _resize(temp,size):
  if len(temp) < size :
    return _resize(temp+temp,size)
  elif len(temp) > size :
    temp = temp[:size]
  return temp
  
def _shuffle(temp):
  o = temp[1::2]
  e = temp[0::2]
  return o+e

def _numericAlpha(temp,parts):
  cut = len(temp)/parts
  numbers = _to_numb(_resize(temp[:cut],pass_length/parts))
  alpha = _resize(temp[cut:],pass_length/parts)
  return alpha,numbers
  
def _trapSymbol(temp):
  parts  = 3
  cut = len(temp)/parts
  alpha,numbers = _numericAlpha(temp[:2*cut],parts)
  trap_symbol = _confuse_symbol_(temp[2*cut:],parts)
  return numbers+alpha+trap_symbol
  
def _caps(temp):
  alpha,numbers = _numericAlpha(temp,2)
  if len(whole_1) < 1:
    return alpha[0:len(alpha)/2] + numbers + alpha[len(alpha)/2:].upper()
  else:
    return numbers + alpha.upper()
  
  
def _confuse_symbol_(temp,parts):
  to_symbol = _resize(temp,pass_length/parts)
  trap_symbol = ''
  for char in to_symbol:
    idx = ord(char)%10
    if idx >= len(symbols):
      idx = idx - len(symbols) -1
    trap_symbol = trap_symbol + symbols[idx]
  return trap_symbol
  
def _fully_loaded(temp):
  parts = 4
  cut = len(temp)/parts
  alpha,numbers = _numericAlpha(temp[:2*cut],parts)
  caps = _resize(temp[2*cut:3*cut],pass_length/parts).upper()
  trap_symbol = _confuse_symbol_(temp[3*cut:],parts)
  return numbers+alpha+trap_symbol+caps
  
def generate(temp,mode):
  if mode == 'X':
    return ''.join(_numericAlpha(temp,2))
  elif mode == 'Y':
    return _caps(temp)    
  elif mode == 'Z':
    return _trapSymbol(temp)
  elif mode == 'Z+':
    return _fully_loaded(temp)
  else:
    return None

print _resize(whole_1+generate(text,'X'),pass_length+len(whole_1)),"<=alphanumeric"
print _resize(whole_1+generate(text,'Y'),pass_length+len(whole_1)),"<=CAPSnumeric"
print _resize(whole_1+generate(text,'Z'),pass_length+len(whole_1)),"<=alphanumeric+symbol"
print _resize(whole_1+generate(text,'Z+'),pass_length+len(whole_1)),"<=alphanumeric+symbol+caps"
print _shuffle(_resize(whole_1+generate(text,'Z+'),pass_length+len(whole_1))),"Secret sauce"