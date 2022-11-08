#Arshjit Pelia 0374870
#COSC 4806

import os, re
import bs4 as bs
from xml.dom.minidom import parseString, Node
from tkinter import filedialog

# Tree structure consists of a root (node object) and a depth counter (integer)
# The class is used to create a tree structure from a DOM object (root) and to traverse the tree
# Also, functions of class are used to perform WEBOQL operations on the tree structure (e.g. head, tail, prime)
# lastly, the printing function is used to print the tree structure in the console by recursively traversing the tree from the node object
# Hypertree Class

class Htree(object):
    root = Node()
    DEPTH = 0
    def __init__(self, root, DEPTH):
        self.root = root
        self.DEPTH = DEPTH

# peforming the prime operation on the tree structure retrives the first subtree of the argument
# subtrees of t are the trees at the end of arcs which stem from the root of t
    def prime(self):
        children = self.root.childNodes
        if children.length == 0:
            return None
        else:
            return Htree(children.item(0), self.DEPTH)

# performing the tail operation on the tree structure retrives the trees obtained by chopping prefixes of tree (i.e. all subtrees except the first)
    def tail(self):
        children = self.root.childNodes
        if children.length == 0:
            return None
        else:
            return Htree(children.item(1), self.DEPTH)

# performing the head operation on the tree structure retrives the first x simple trees of the argument. If x is not specified then only the first simple tree
# simple trees of a tree t are the trees that are composed of an arc that stems from the root of t and its sub-tree
    def head(self, n =1):
        children = self.root.childNodes
        if children.length == 0:
            return None
        else:
            if n == 1:
                return Htree(children.item(0), self.DEPTH)
            else:
                return Htree(children.item(0), self.DEPTH).head(n - 1)
                
# printing the tree structure in the console by recursively traversing the tree from the node object
# the function uses the DEPTH counter to print depth of the tree and DEPTH the output
    def print_(self, DEPTH=1):
        # if root object is not document object then print tag name
        # if self.root.nodeType != Node.DOCUMENT_NODE:
        if self.root.nodeType == Node.DOCUMENT_NODE:
            print("<Document Object>")
        else:
            print("   " * DEPTH, end="")
            print("[Tag: " + self.root.tagName, end="")
        # retrieve attributes of the node object and print them
            attributes = self.root.attributes.items()
            if attributes != None:
                for attribute in attributes:
                    print(", Attributes: " + attribute[0] + " = " + attribute[1], end="")
        
        # check for text content of the node object and print it
        # also check for text seperated by br tags and print them
            if self.root.hasChildNodes():
                print(", Text: ", end=" ")
                for i in self.root.childNodes:
                    if i.nodeType == i.TEXT_NODE:
                        if i.nodeValue and not re.match(r'^\s+$', i.nodeValue) and i.nodeValue != ' ':
                            print(i.nodeValue, end=" ")
                    if i.nodeType == i.ELEMENT_NODE and i.tagName == "br":
                        #check if nodeValue exists
                        if i.nodeValue:
                            print(i.nextSibling.nodeValue, end=" ")

            print ("]")
# recursively traverse the tree structure and repeat the process for each child node
        for child in self.root.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                tree = Htree(child, DEPTH + 1)    
                tree.print_(DEPTH + 1)

# function to select a file from the file explorer, parse the file and return the html content AS A STRING
def parseHTML(file):
    with open(file, 'r') as f:
        soup = bs.BeautifulSoup(f, 'html.parser', from_encoding="utf-8")
        soup.prettify()
    return str(soup)

# function to select a file from the file explorer
def selectfile():
    filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("html files","*.html"),("all files","*.*")))
    return filepath

# start function to loop the program for multiple operations on the tree
# function to print the tree and then allow the user to select whether to perform prime, head, or tail functions on the tree and then print the tree again after the function is performed
# continously loops with the new tree until the user decides to quit
def start(tree, action):
    print()
    if (action != "invalid"):
        print("Tree after " + action + " operation:")
        print()
        tree.print_()
        print("")
    print("Enter 'p' to prime the tree, 'h' to head the tree, 't' to tail the tree, rs to restart or 'q' to quit")
    print("")
    choice = input("Enter your choice: ")
    if choice == 'p':
        tree = tree.prime()
        start(tree, "prime")
    elif choice == 'h':
        n = input("Enter the number of nodes to head: ")
        tree = tree.head(int(n))
        start(tree, "head")
    elif choice == 't':
        tree = tree.tail()
        start(tree, "tail")
    elif choice == 'q':
        print("Program terminated!")
        exit()
    elif choice == 'rs':
        main()
    else:
        print("Invalid input. try again")
        start(tree, "invalid")

# main function
# Begiins by calling the selectfile function to select a file from the file explorer and then parses the file and returns the html content AS A STRING
# creates a DOM object from the html content and then creates a tree structure from the DOM object
# finally, calls the start function to loop the program for multiple operations on the tree
def main():
    # get file path from user
    # fpath = input("Enter file path: ")
    fpath = selectfile()
    # get file name from user
    # fname = input("Enter file name: ")
    fname = os.path.basename(fpath)
    # parse the html file
    html = parseHTML(fpath)
    # parse the html file into a DOM object
    dom = parseString(html)
    # create a tree structure from the DOM object
    tree = Htree(dom, 0)
    # call start function to loop the program for multiple operations on the tree
    print()
    print("Program started for file: " + fname)
    print("")
    start(tree, "Creation")

if __name__ == "__main__":
    main()