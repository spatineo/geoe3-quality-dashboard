import xml.etree.ElementTree as ET

# Documentation: https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support

# https://inspire.ec.europa.eu/reports/ImplementingRules/metadata/MD_IR_and_ISO_20081219.pdf

ns = {
    '':       'http://www.isotc211.org/2005/gmd',
    'csw':    'http://www.opengis.net/cat/csw/2.0.2',
    'gmd':    'http://www.isotc211.org/2005/gmd',
    'gco':    'http://www.isotc211.org/2005/gco',
    'gml':    'http://www.opengis.net/gml',
    'gmx':    'http://www.isotc211.org/2005/gmx',
    'xsi':    'http://www.w3.org/2001/XMLSchema-instance',
    'xlink':  'http://www.w3.org/1999/xlink',
    'geonet': 'http://www.fao.org/geonetwork'
}

tree = ET.parse('example-metadata/Dataset MD Bui-ES-5.xml')
root = tree.getroot()

metadataRoot = root.find('.//MD_Metadata', ns)
print(metadataRoot)

#print(root)
#result = root.findall('.//MD_Metadata//date', ns)
#print(result)

publication = metadataRoot.findall(
 #   "identificationInfo[1]/*/citation/*/date[./*/dateType/*/text()='revision']/*/date"
   "identificationInfo/*/citation/*/date/[CI_Date/foo='2015-12-15']"
, ns)

## TODO: figure out a better library for this to work
## * It needs to work with the type of xpath queries that are in the INSPIRE document

print(publication)