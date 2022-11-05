from xml.dom.minidom import parseString, parse, Node
import re
import bs4 as bs

class Hypertree(object):
    """ generated source for class Hypertree """
    root = Node()
    indent = 1

    def __init__(self, root, indent):
        """ generated source for method __init__ """
        self.root = root
        self.indent = indent

    def prime(self):
        """ generated source for method prime """
        children = self.root.childNodes
        first = children.item(0)
        self.root = first
        return self

    def head(self, n): #remove all simple trees from the last descendant
        """ generated source for method head """
        children = self.root.childNodes
        i = children.Length
        while i > n:
            self.root.removeChild(children.item(children.Length - 1))
            i = children.Length
        return self

    def tail(self, n): #remove all simple trees from the first descendant
        """ generated source for method tail """
        children = self.root.childNodes
        i = children.length
        while i > n:
            self.root.removeChild(children.item(0))
            i = children.getLength()
        return self

    def simpleTree(self, n):
        """ generated source for method simpleTree """
        self.head(n)
        self.tail(1)
        return self

    def print_(self, indent=1):
        """ generated source for method print_ """
        print("   " * indent, end="")
        print("[Tag: " + self.root.tagName, end="")
        attributes = self.root.attributes.items()
        if attributes != None:
            for attribute in attributes:
                print(", Attribute: " + attribute[0] + " = " + attribute[1], end="")
        
        children = self.root.childNodes
        if children.length == 1:
            child = children.item(0)
            if child.nodeType == child.TEXT_NODE:
                value = child.nodeValue.replace("[\n\r]", "")
                if value != "":
                    print(", Value: " + value,  end="")

        print ("]")

        for child in self.root.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                # child.print_(child, indent+1)
                # Hypertree tree = new Hypertree(child, indent + 1);
				# tree.print();
                tree = Hypertree(child, indent + 1)    
                tree.print_(indent + 1)

def htmlParser(file):
    with open(file, 'r') as f:
        soup = bs.BeautifulSoup(f, 'html.parser', from_encoding="utf-8")
        soup.prettify()
    return str(soup)

    
def cleanFile(fpath):

    with open(fpath,'r+') as f:

        file = f.read()
            
        # Replacing the pattern with the string
        # in the file data
        # file = re.sub(">\\s*<", "><", file)
        # file = re.sub("<br>", "<br />", file)
        # file = re.sub("<BR>", "<BR />", file)
        # file = re.sub("<hr>", "<hr />", file)
        # file = re.sub("<HR>", "<HR />", file)
        # file = re.sub(" &amp ", "&amp;", file)
        # file = re.sub("&amp ", "&amp;", file)
        # file = re.sub(" &amp", "&amp;", file)
        # file = re.sub("&nbsp", "", file)
        file = re.sub('\<!DOCTYPE.*?>','',file, flags=re.DOTALL)

        # Setting the position to the top
        # of the page to insert data
        f.seek(0)
            
        # Writing replaced data in the file
        f.write(file)

        # Truncating the file size
        f.truncate()

        # Closing the file
        f.close()
    
    file = bytearray(file, "utf-8")
    return file

def main():
    """ generated source for method main """
    # dom = parse("testcase.html")
    fpath = "testcase.html"
    file = cleanFile(fpath)
    file = htmlParser(fpath)
    doc = parseString(file)
    root = doc.documentElement
    tree = Hypertree(root, 1)
    tree.print_(1)
    print("")
    # tree.prime()
    # tree.print_()
    # print("")
    # tree.head(2)
    # tree.print_(0)
    # print("")
    # tree.tail(1)
    # tree.print_(0)
    # print("")
    # tree.simpleTree(2)
    # tree.print_(0)
    # print("")

if __name__ == '__main__':
    main()