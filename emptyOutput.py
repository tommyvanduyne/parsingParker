
import os
def main():
	foldersToEmpty = ["results","ngrams","outputs"]
	for folderName in foldersToEmpty:
		for fileName in os.listdir(folderName):
			filePath = os.path.join(folderName,fileName)
			try:
				if (os.path.isfile(filePath)):
					os.unlink(filePath)
			except Exception as e:
				print (e)	
	


if __name__ == "__main__":
    main()

