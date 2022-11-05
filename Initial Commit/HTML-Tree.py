from htmldom import htmldom
from sqlalchemy import null
from treelib import Tree, Node
import re
from xml.dom.minidom import getDOMImplementation, parseString, parse
from tkinter import filedialog

# impl = getDOMImplementation()

# newdoc = impl.createDocument(None, "ROOT", None)
# top_element = newdoc.documentElement
# text = newdoc.createTextNode('Some textual content.')
# top_element.appendChild(text)
# Opening the file in read and write mode
    # "C:/Users/apeli/OneDrive/Documents/School/Year 4/Web Database Management/A1/testcase.html"
    # "C:/Users/apeli/OneDrive/Documents/School/Year 4/Web Database Management/A1-Example/Java-Example/HTML-to-Hypertree-master/sample2.html"
    # "C:/Users/apeli/OneDrive/Documents/School/Year 4/Web Database Management/A1-Example/java-Example/assignment.html"
    #with open("C:/Users/apeli/OneDrive/Documents/School/Year 4/Web Database Management/A1-Example/example-fixed.html",'r+') as f:

indent = 1

def selectfile():
    filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("html files","*.html"),("all files","*.*")))
    return filepath

def cleanFile(fpath):
    with open(fpath,'r+') as f:

        # Reading the file data and store
        # it in a file variable
        file = f.read()
            
        # Replacing the pattern with the string
        # in the file data
        file = re.sub(">\\s*<", "><", file)
        file = re.sub("<br>", "<br />", file)
        file = re.sub("<BR>", "<BR />", file)
        file = re.sub("<hr>", "<hr />", file)
        file = re.sub("<HR>", "<HR />", file)
        file = re.sub("&amp", "&amp;", file)
        file = re.sub("&nbsp", "", file)
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

def printIndentation(level):
    print("   " * level, end="")

def print_tree(node, level=0):
    printIndentation(level)

    print("[Tag: " + node.tagName, end="")
    attributes = node.attributes.items()
    if attributes != null:
        for attribute in attributes:
            print(", Attribute: " + attribute[0] + " = " + attribute[1], end="")
    
    children = node.childNodes
    if children.length == 1:
        child = children.item(0)
        if child.nodeType == child.TEXT_NODE:
            value = child.nodeValue.replace("[\n\r]", "")
            if value != "":
                print(", Value: " + value,  end="")

    print ("]")

    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            print_tree(child, level+1)

def main():
    fpath = selectfile()
    file = cleanFile(fpath)
    doc = parseString(file)
    root = doc.documentElement
    tree = Tree()
    tree.create_node(root, 0)  # root node
    print_tree(root)

if __name__ == "__main__":
    main()
