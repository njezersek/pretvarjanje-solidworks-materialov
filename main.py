import xml.etree.ElementTree as ET
import re

vhodnaDatoteka = "primeri/SolidWorks DIN Materials.xml"
izhodnaMapa = "izhod"

# odpri datoteko z Solodworks materiali
tree = ET.parse(vhodnaDatoteka)

# definicije atributov
# za pot do elementa se uporablja Xpath (https://www.w3schools.com/xml/xpath_syntax.asp)
atributi = {
	# <Creo ime>:                   (<pot do elementa>, <ime atributa>, <prefix>, <sufix>, <Type>, 	<Access>, <Description>)
	"PTC_MATERIAL_DESCRIPTION":		(".//xhatch",		"name",			"'",		"'",	"String","Full",     ""),
	"PTC_YOUNG_MODULUS":			(".//EX",			"value",		"",			"MPa",	"Real",	"Full",     "")
}

# poišči vse materiale
materials = tree.findall(".//material")

# sprehodi se čez vse materiale
for material in materials:
	ime = material.get("name")
	ime_datoteke = re.sub(r'\W+', '', ime) # odstarni vse ne alfanumerične znake
	
	# ustvari novo datoteko
	izhod = open(izhodnaMapa+"/"+ime_datoteke+".mtl", "w")
	izhod.write(ime_datoteke + " = { \n\n")
	izhod.write("Name" + " = " + ime_datoteke + "\n\n")
	izhod.write("PARAMETERS = \n")

	# sprehodi se čez vse atribute materiala
	prvi = True
	for atribut,opis in atributi.items():
		el = material.find(opis[0])
		if el is not None: # če je element najden
			parameterString = "{\n" if prvi else ",\n{\n" # prvi parameter pred seboj nima vejice
			prvi = False
			parameterString += "  Name = " + atribut + "\n"
			parameterString += "  Type = " + opis[4] + "\n"
			parameterString += "  Default = " +  opis[2] + el.attrib[opis[1]] + opis[3] + "\n"
			parameterString += "  Access = " + opis[5] + "\n"
			if opis[6] : parameterString += "  Description = " + opis[6] + "\n"
			parameterString += "}"
			izhod.write(parameterString)
	
	izhod.write("\n\n} \n")
	izhod.close()
	# ustavi se po prvem materialu (to daj stran na koncno verzijo)
	break