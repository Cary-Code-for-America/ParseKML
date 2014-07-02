#!/usr/bin/python

#a var used when we find our folder
foundFolder = 0

#a var to know when we are in a description sequence
processDescription = 0

#a var to count number of projects
projCount = 0

#open files for reading and writing
fo = open("/Users/robertca/Projects/CaryKML/CaryDevelopment-20140616.kml","r")
fw = open("/Users/robertca/Projects/CaryKML/rezoning-20140616.kml","w")

#write the inital link of the fixed kml file
fw.write("<?xml version=\"1.0\" encoding=\"utf-8\"?><kml xmlns=\"http://earth.google.com/kml/2.1\">" + "\n")

#examine each line in the file we are reading from
for line in fo:
	#print line
	#if the link contains our folder name
	if (line.find("kml_ft_CaryDevelopment_Rezoning_Case") > -1):
		#set our flag to 1
		foundFolder = 1
		print "FOLDER FOUND!!\n"

	#if we have found our folder
	if (foundFolder == 1):
		#if the line is a description tag, we need to process differently
		if (line.find("<description>") > -1):
			#we need to process the description
			processDescription = 0

		#If the process flag is set
		if (processDescription == 1):
			#process the line that has the sitesubplans URL in it
			if (line.find("sitesubplans") > -1):
				#strip of the newline
				dline = line.strip()
				#remove the begining 4 and last 5 table tags
				dline = dline[4:-5]
				#write a correct description line to our output file, only the URL in the decription
				fw.write("<description>"+dline+"</description>"+"\n")
				#print line.strip()

		#when not processing the description	
		if (processDescription == 0):
			#print line.strip()
			#write the line to our new file
			fw.write(line)

		#when we find the end of the description
		if (line.find("</description>") > -1):
			#we are done processing description stuff
			processDescription = 0
			projCount += 1

		#when we find the end of the folder			
		if (line.find("</Folder") > -1):
			#set the foundFolder to false
			foundFolder = 0
			#tell the world
			print "END OF FOLDER FOUND!\n"
			#write the final line of our fixed kml file
			fw.write("</kml>" + "\n")
			print str(projCount) + " projects found\n"
			#and we are DONE!
			exit()
		
