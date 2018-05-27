from des64v1 import cipher, reverse_cipher, tobits, frombits

text = 'BONJOUR!'
key = 'aa00df8'

print('encryption key: ', key)
print('text before encryption: ', text)

bin_text = tobits(text)
bin_key = tobits(key)

print('#### CIPHERING ####')
bin_result = cipher(bin_text, bin_key)
result = frombits(bin_result)

print('text after encryption: ', result)

print('#### DECIPHERING ####')
bin_text2 = reverse_cipher(bin_result, bin_key)
text2 = frombits(bin_text2)
print('text after deciphering: ', text2)

input()
