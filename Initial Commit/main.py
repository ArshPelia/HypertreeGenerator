from sqlalchemy import null
from treelib import Tree, Node
import re
from xml.dom.minidom import getDOMImplementation, parseString, parse
import tkinter as tk
from tkinter import filedialog


filepath = ""
success = "False"
root = ""
body = ""
head = ""
table = ""

def createGUI(output=""):
    root = tk.Tk()
    root.title("HTML to Hypertree")
    root.geometry("500x500")
    root.resizable(False, False)

    # Create the file selection button
    button = tk.Button(root, text="Select File", command=selectfile)
    button.pack()

    label = tk.Label(root, text="Filpath: " + filepath)
    label.pack()

    label1 = tk.Label(root, text="Tree Generated: " + success)
    label1.pack()

    # Create the output text box
    # text = tk.Text(root, height=10, width=50)
    # text.pack()

    # Create the output button
    button1 = tk.Button(root, text="Generate Hypertree", command=generate_Tree(filepath))
    button1.pack()

    # Create the output button
    button2 = tk.Button(root, text="Print Hypertree", command=print_tree(root))
    button2.pack()

    root.mainloop()

def selectfile():
    filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("html files","*.html"),("all files","*.*")))
    return filepath

def generate_Tree(fpath):
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
    doc = parseString(file)
    root = doc.documentElement
    body = doc.getElementsByTagName("body")[0]
    head = doc.getElementsByTagName("head")[0]
    table = doc.getElementsByTagName("table")[0]
    success = "True"
    # return file

def print_tree(node, level=0):

    print("   " * level, end="")

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
    createGUI()

if __name__ == "__main__":
    main()
