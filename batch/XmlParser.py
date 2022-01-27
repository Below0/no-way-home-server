import xml.etree.ElementTree as elemTree

class XmlParser:
    def parse(self, xml, fields):
            
        xml_tree = elemTree.fromstring(xml)
        items = xml_tree.find('./body/items').findall('item')

        item_list = []
        
        for item in items:
            contents = {}
            for field in fields:
                contents[field] = item.findtext(field)
            item_list.append(contents)

        return item_list
