#!/usr/bin/python

#a var used when we find our folder
foundFolder = 0

#a var to know when we are in a description sequence
processDescription = 0

#a var to know when we need to process coordinates
processCoordinates = 0

#a var to know when we need to grab the next line
grabNextLine = 0

#a var to store our description
descLine = ""

#a var to store our comment
commentLine = ""

#a var to flag the folder
foundFolder = 0

#a string var for lines of text
line = ""

#a var to count number of projects
projCount = 0

#open files for reading and writing
fo = open("/Users/robertca/Downloads/CFA/kml/CaryDevelopment-20140409.kml","r")
fw = open("/Users/robertca/Downloads/CFA/polyCoords_20140409_REZ.js","w")

#write the inital link of the fixed kml file
#fw.write("<?xml version=\"1.0\" encoding=\"utf-8\"?><kml xmlns=\"http://earth.google.com/kml/2.1\">" + "\n")

#examine each line in the file we are reading from
for line in fo:
	#print line
	#if the link contains our folder name
	if (line.find("kml_ft_CaryDevelopment_Rezoning_Case") > -1):
		#set our flag to 1
		foundFolder = 1
		print "FOLDER FOUND!!\n"
		processCoordinates = 0
		processDescription = 0

	#if we have found our folder
	if (foundFolder == 1):
		#if the line is a description tag, we need to process differently
		if (line.find("<name>") > -1):
			#we need to process the description
			processDescription = 1

		#If the process flag is set
		if (processDescription == 1):
			#process the line that has the sitesubplans URL in it
			dline = line.strip()
			descLine = dline[6:-7]

			#check to see if the description line has an 's in it
			if (descLine.find("'s") > -1):
				#we need to fix the 's in the line as it breaks the syntax, change 's to just s.
				descLine.replace("'s", "s")

			#if we've seen the Comments tag, the next line is some data we want, let's take that
			if (grabNextLine == 1):
				#strip off the newline
				dline = line.strip()
				#remove the beginning 4 and last 5 table tags
				dline = dline[4:-5]
				#store this in a new var
				commentLine = dline
				#check the line for 's and change to just s or we get error!
				if (commentLine.find("'s") > -1):
					commentLine = commentLine.replace("'", "")

				#don't repeat this
				grabNextLine = 0

			#Looking for the <th>Comments</th>, then setting up to grab the next line because it has info related to the project	
			if (line.find("<th>ID</th>") > -1):
				#set the flag - grab the comments on the next pass
				grabNextLine = 1

		#when not processing the description	
		#if (processDescription == 0):
			#print line.strip()
			#write the line to our new file
			#fw.write(line)

		#when we find the end of the description
		if (line.find("</description>") > -1):
			#we are done processing description stuff
			processDescription = 0
			projCount += 1

		if (line.find('name="ProjectName"') > -1):
			projName = line.strip()
			projName = projName[31:-13]
			#print "Project: " + projName
			#check the project name for 's, change it to just s
			if (projName.find("'s") > -1):
				projName = projName.replace("'", "")

		if (line.find("<coordinates>") > -1):
			processCoordinates = 1
			processDescription = 0

		def pair_list(list_):
			return[list_[i:i+2] for i in xrange(0, len(list_), 2)]

		if (processCoordinates == 1):			
			fw.write("L.polygon([\n")
			dline = line.strip()
			dline = dline[13:-14]
			dline = dline.replace(",0 ", ",")
			coords = dline.split(",")
			#coords = coords.pop()
			#print coords
			newList = pair_list(coords)
			newList.pop()
			for element in newList:
				fw.write("\t[" + element[1] + ", " + element[0] + "],\n")
			fw.write("],{\n")
			fw.write("color: '#0df',\n")
			fw.write("fillColor: '#0df',\n")
			fw.write("fillOpacity: 0.5\n")
   			fw.write("}).addTo(map).bindPopup('<a href=\"http://www.townofcary.org/Departments/Planning_Department/Public_Hearing_Cases/Rezoning_Cases.htm\" target=\"_blank\">" + projName + "</a><br>ID: " + commentLine + "');\n\n")
			processCoordinates = 0

		#when we find the end of the folder			
		if (line.find("</Folder") > -1):
			#set the foundFolder to false
			foundFolder = 0
			#tell the world
			print "END OF FOLDER FOUND!\n"
			#write the final line of our fixed kml file
			#fw.write("</kml>" + "\n")
			print str(projCount) + " projects found\n"
			#and we are DONE!
			exit()
		
