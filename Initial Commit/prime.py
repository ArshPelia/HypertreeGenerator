from sqlalchemy import null
from sympy import fps
from treelib import Tree, Node
import re
from xml.dom.minidom import parseString, parse
from tkinter import filedialog
import bs4 as bs
from colorama import Fore, Back, Style

indent = 1

def selectfile():
    filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("html files","*.html"),("all files","*.*")))
    return filepath

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

def get_firstSubtree(node):
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            return child
    return null

def getSimpleTree(node):
    tree = Tree()
    tree.create_node(node.tagName, node.tagName)
    id = 1
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            tree.create_node(child.tagName, id, parent=node.tagName, data=child)
            id += 1
    return tree

def get_firstxsimpletrees(node, x = 2):
    subtrees = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            subtrees.append(child)
            if len(subtrees) == x:
                return subtrees
    return subtrees

def htmlParser(file):
    with open(file, 'r') as f:
        soup = bs.BeautifulSoup(f, 'html.parser', from_encoding="utf-8")
        soup.prettify()
    return str(soup)

def main():
    fpath = "testcase.html"
    file = cleanFile(fpath)
    file = htmlParser(fpath)
    doc = parseString(file)
    root = doc.documentElement
    body = doc.getElementsByTagName("body")[0]
    head = doc.getElementsByTagName("head")[0]
    table = doc.getElementsByTagName("table")[0]

    print("")
    print(Fore.GREEN +"Prime of root:")
    print(Style.RESET_ALL)
    subtree = get_firstSubtree(root)
    print_tree(subtree)

    print("")
    print(Fore.RED +"Prime of body:")
    print(Style.RESET_ALL)
    subtree = get_firstSubtree(body)
    print_tree(subtree)

    print("")
    print(Fore.BLUE +"Prime of head:")
    print(Style.RESET_ALL)
    subtree = get_firstSubtree(head)
    print_tree(subtree)

    print("")
    print(Fore.YELLOW +"Prime of table:")
    print(Style.RESET_ALL)
    subtree = get_firstSubtree(table)
    print_tree(subtree)

    # print_tree(root)

if __name__ == "__main__":
    main()
