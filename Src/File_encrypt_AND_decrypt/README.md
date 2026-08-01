*****************************************************************************************
******************************    G U I D E    ******************************************

This program contains the ability of reading file and perform given tasks like encryption and decryption.

# Information
- Original data will be in *.txt format only
- New generate key will be saved in "secret.key" (If we try to create the new key again then new key will replace the old key)
- Encrypted file will be saved in "*_encrypted.enc" 
- Decrypted file wiil be saved in "*_decrypted.dnc""
- To run this program: you have to use the terminal with the argument





*****************************  E X E C U T I O N   ****************************************

#    First and most important Step of this program. You only have to do it once, you can create new key too but the same key will need to  perform task (encryption/decryption).

python main.py G 				# To generate the key, you can create it as much as you want; it will replace the old key and store in secret.key file
python main.py genkey   			# Same but lengthy 


#    For encryption of original file (Only .txt files are allowed in this program as a original file)

python main.py E file.txt			# Encrypt the *.txt file and save the encrypted data in *_encrypted.enc file
python main.py encrypt file.txt 		#Same but full word encrypt


#    For decryption of encrypted file (_encrypted.enc)

python main.py D file_encrypted.enc 		# Decrypt the *_encrypted.enc file and save the decrypted data in *_decrypted.dnc (The data will be same as original file "*.txt" but since the file decrypted we have to name it like this)
python main.py decrypt file_encrypted.enc







********************************   L I M I T A T I O N   ************************************** 
- Original file must be in .txt format
- Same key will be used to decrypt the encrypted file. If you create new key then we can create new encrypted data and decrypt that but for old encrypted data; we cannot decrypt because the key is new.
- No program to encrypt the decrypted data since the decrypted data has different extension and only .txt file can be encrypted.
- You can't change the encrypted data; it will cause the error while you decrypt
