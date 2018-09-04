from xml.dom import minidom
import instgen
from collections import defaultdict
import nodescreator
import os

'''
minidom: Module responsible of manipulating a xml file in a tree.
instgen: Module to generate every instruction.
defaultdict: Module of dicts
'''

"""
Starting the process of building a graph, passing the BXML file

Note: While building our graph of the implementation, after the initialisation, there will exists at least an END and a CONDITION node.
Every node added to the graph manipulates the END node

The '*' in some comments means that the END node will be manipulated

This file is also used to build graphs of the called operations. But in this case, the first and the last node are a little bit different.
"""

"""
Initialisation of the dicts (graphs)

nodemap: the dict used as a graph. The first node is always the call and last node always the end.
nodetype: this dict contains if the node is a condition, while, instruction, call, skip. It guide us while making the predicate for the inputs.
nodecond: this dict contains if the previous node was false or true. It guide us while making the predicate for the inputs.
nodeiva: this dict contains the invariant of the while's
"""
nodemap = defaultdict(list)  # Graph dict
nodetype = dict()  # Dict of the type of the nodes
nodedata = dict()  # Dict of the data of the nodes
nodecond = dict()  # Dict of the previous condition of the node. If the parent is a Condition node we know if the
# path comes from the True or the False condition.
nodeinva = dict()  # Dict with the invariant of the while and where it end.


def startMap(node, opmch, importedMch, seesMch, refinementMch, directory):
    '''
    Function responsible for the initialisation of the map.
    
    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    '''
    # Initialisation of the Graph, the first node is always the Call
    nodemap[str(len(nodemap) + 1)].append('0')  # Initialisation with 0, None.
    solveFirstNodeData(node, opmch, importedMch, seesMch, refinementMch, directory)
    nodecond[str(len(nodecond) + 1)] = "True"
    nodeinva[str(len(nodeinva) + 1)] = ""
    nodemap[str(len(nodemap) + 1)].append(str(len(nodemap) - 1))
    nodecond[str(len(nodecond) + 1)] = "True"


def solveFirstNodeData(node, opmch, importedMch, seesMch, refinementMch, directory):
    doc = minidom.getDOMImplementation()
    docXML = doc.createDocument(None, "Scapegoat", None)
    if opmch.getElementsByTagName("Precondition") != []:
        nodedata[str(len(nodedata) + 1)] = opmch.getElementsByTagName("Precondition")[0].cloneNode(20)
        nodetype[str(len(nodetype) + 1)] = "Condition"
    else:
        nodetype[str(len(nodetype) + 1)] = "PreconditionTrue"
        nodedata[str(len(nodedata) + 1)] = None
    for child in opmch.parentNode.parentNode.childNodes:  # In the machine of the Implementation
        if child.nodeType != child.TEXT_NODE:
            if child.tagName == 'Invariant' or child.tagName == 'Properties' or child.tagName == 'Constraints' or\
                            child.tagName == 'Values':
                if nodetype[str(len(nodetype))] == "Condition":
                    if child.firstChild.nextSibling.tagName == "Attr":
                        if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                            nodedata[str(len(nodedata))].appendChild(
                                child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10))
                            nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                        else:
                            nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10),
                                nodedata[str(len(nodedata))], '&', docXML)
                    else:
                        if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                            nodedata[str(len(nodedata))].appendChild(child.firstChild.nextSibling.cloneNode(10))
                            nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                        else:
                            nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                child.firstChild.nextSibling.cloneNode(10),
                                nodedata[str(len(nodedata))], '&', docXML)
                else:
                    nodedata[str(len(nodedata))] = child.cloneNode(20)
                    nodetype[str(len(nodetype))] = "Condition"
            elif child.tagName == 'Assertions':
                if nodetype[str(len(nodetype))] == "Condition":
                    if child.firstChild.nextSibling.tagName == "Attr":
                        count = 3
                    else:
                        count = 1
                    for i in range(len(child.childNodes)):
                        if child.childNodes.item(i).nodeType != child.childNodes.item(i).TEXT_NODE:
                            if i >= count:
                                if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                    nodedata[str(len(nodedata))].appendChild(child.childNodes.item(count).cloneNode(10))
                                    nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                                else:
                                    nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                        child.childNodes.item(count).cloneNode(10),
                                        nodedata[str(len(nodedata))], '&', docXML)
                else:
                    nodedata[str(len(nodedata))] = child
                    nodetype[str(len(nodetype))] = "Condition"
            elif child.tagName == 'Sets':
                solveSets(child, docXML)
    SolveFirstNodeImportedAndSees(importedMch, directory)
    SolveFirstNodeImportedAndSees(seesMch, directory)
    for child in node.parentNode.parentNode.childNodes:  # In the Implementation
        if child.nodeType != child.TEXT_NODE:
            if child.tagName == 'Invariant' or child.tagName == 'Properties' or child.tagName == 'Constraints' or child.tagName == 'Values':
                if nodetype[str(len(nodetype))] == "Condition":
                    if child.firstChild.nextSibling.tagName == "Attr":
                        if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                            nodedata[str(len(nodedata))].appendChild(
                                child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10))
                            nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                        else:
                            nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10),
                                nodedata[str(len(nodedata))], '&', docXML)
                    else:
                        if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                            nodedata[str(len(nodedata))].appendChild(child.firstChild.nextSibling.cloneNode(10))
                            nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                        else:
                            nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                child.firstChild.nextSibling.cloneNode(10),
                                nodedata[str(len(nodedata))], '&', docXML)
                else:
                    nodedata[str(len(nodedata))] = child.cloneNode(20)
                    nodetype[str(len(nodetype))] = "Condition"
            elif child.tagName == 'Assertions':
                if nodetype[str(len(nodetype))] == "Condition":
                    if child.firstChild.nextSibling.tagName == "Attr":
                        count = 3
                    else:
                        count = 1
                    for i in range(len(child.childNodes)):
                        if child.childNodes.item(i).nodeType != child.childNodes.item(i).TEXT_NODE:
                            if i >= count:
                                if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                    nodedata[str(len(nodedata))].appendChild(child.childNodes.item(count).cloneNode(10))
                                    nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                                else:
                                    nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                        child.childNodes.item(count).cloneNode(10),
                                        nodedata[str(len(nodedata))], '&', docXML)
                else:
                    nodedata[str(len(nodedata))] = child.cloneNode(20)
                    nodetype[str(len(nodetype))] = "Condition"
            elif child.tagName == 'Sets':
                solveSets(child, docXML)
    for ref in refinementMch: #For the refinement
        for child in ref.firstChild.childNodes:
            if child.nodeType != child.TEXT_NODE:
                if child.tagName == 'Invariant' or child.tagName == 'Properties' or child.tagName == 'Constraints' or child.tagName == 'Values':
                    if nodetype[str(len(nodetype))] == "Condition":
                        if child.firstChild.nextSibling.tagName == "Attr":
                            if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                nodedata[str(len(nodedata))].appendChild(
                                    child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10))
                                nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                            else:
                                nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                    child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10),
                                    nodedata[str(len(nodedata))], '&', docXML)
                        else:
                            if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                nodedata[str(len(nodedata))].appendChild(child.firstChild.nextSibling.cloneNode(10))
                                nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                            else:
                                nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                    child.firstChild.nextSibling.cloneNode(10),
                                    nodedata[str(len(nodedata))], '&', docXML)
                    else:
                        nodedata[str(len(nodedata))] = child.cloneNode(20)
                        nodetype[str(len(nodetype))] = "Condition"
                elif child.tagName == 'Assertions':
                    if nodetype[str(len(nodetype))] == "Condition":
                        if child.firstChild.nextSibling.tagName == "Attr":
                            count = 3
                        else:
                            count = 1
                        for i in range(len(child.childNodes)):
                            if child.childNodes.item(i).nodeType != child.childNodes.item(i).TEXT_NODE:
                                if i >= count:
                                    if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                        nodedata[str(len(nodedata))].appendChild(
                                            child.childNodes.item(count).cloneNode(10))
                                        nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                                    else:
                                        nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                            child.childNodes.item(count).cloneNode(10),
                                            nodedata[str(len(nodedata))], '&', docXML)
                    else:
                        nodedata[str(len(nodedata))] = child.cloneNode(20)
                        nodetype[str(len(nodetype))] = "Condition"
                elif child.tagName == 'Sets':
                    solveSets(child, docXML)
    if nodedata['1'] is None:
        firstTrue = docXML.createElement('Id')
        firstTrue.setAttribute('value', 'TRUE')
        firstTrue.appendChild(docXML.createTextNode('\n'))
        firstTrue.appendChild(docXML.createElement('Attr'))
        firstTrue.appendChild(docXML.createTextNode('\n'))
        secondTrue = docXML.createElement('Id')
        secondTrue.setAttribute('value', 'TRUE')
        secondTrue.appendChild(docXML.createTextNode('\n'))
        secondTrue.appendChild(docXML.createElement('Attr'))
        secondTrue.appendChild(docXML.createTextNode('\n'))
        nodedata['1'] = nodescreator.createExpComparison(firstTrue, secondTrue, '=', docXML)


def solveSets(setsClause, docXML):
    allSet = setsClause.getElementsByTagName('Set')
    for set in allSet:
        if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
            nodedata[str(len(nodedata))].appendChild(set.cloneNode(20))
            nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
        else:
            nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                set.cloneNode(10),
                nodedata[str(len(nodedata))], '&', docXML)

def SolveFirstNodeImportedAndSees(machines, directory):
    for dcmt in machines:  # In the other imported machines
        for mch in dcmt.childNodes:
            for child in mch.childNodes:
                if child.nodeType != child.TEXT_NODE:
                    if child.tagName == 'Invariant' or child.tagName == 'Properties' or child.tagName == 'Constraints' or child.tagName == 'Values':
                        if nodetype[str(len(nodetype))] == "Condition":
                            doc = minidom.getDOMImplementation()
                            docXML = doc.createDocument(None, "Scapegoat", None)
                            if child.firstChild.nextSibling.tagName == "Attr":
                                if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                    nodedata[str(len(nodedata))].appendChild(
                                        child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10))
                                    nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                                else:
                                    nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                        child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10),
                                        nodedata[str(len(nodedata))], '&', docXML)
                            else:
                                if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                    nodedata[str(len(nodedata))].appendChild(child.firstChild.nextSibling.cloneNode(10))
                                    nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                                else:
                                    nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                        child.firstChild.nextSibling.cloneNode(10),
                                        nodedata[str(len(nodedata))], '&', docXML)
                        else:
                            nodedata[str(len(nodedata))] = child.cloneNode(20)
                            nodetype[str(len(nodetype))] = "Condition"
                    elif child.tagName == 'Assertions':
                        if nodetype[str(len(nodetype))] == "Condition":
                            doc = minidom.getDOMImplementation()
                            docXML = doc.createDocument(None, "Scapegoat", None)
                            if child.firstChild.nextSibling.tagName == "Attr":
                                count = 3
                            else:
                                count = 1
                            for i in range(len(child.childNodes)):
                                if child.childNodes.item(i).nodeType != child.childNodes.item(i).TEXT_NODE:
                                    if i >= count:
                                        if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                            nodedata[str(len(nodedata))].appendChild(
                                                child.childNodes.item(count).cloneNode(10))
                                            nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                                        else:
                                            nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                                child.childNodes.item(count).cloneNode(10),
                                                nodedata[str(len(nodedata))], '&', docXML)
                        else:
                            nodedata[str(len(nodedata))] = child.cloneNode(20)
                            nodetype[str(len(nodetype))] = "Condition"
                    elif child.tagName == 'Sets':
                        doc = minidom.getDOMImplementation()
                        docXML = doc.createDocument(None, "Scapegoat", None)
                        solveSets(child, docXML)
        imp = getImpWithImportedMch(dcmt, directory)
        for child in imp.firstChild.childNodes:
            if child.nodeType != child.TEXT_NODE:
                if child.tagName == 'Invariant' or child.tagName == 'Properties' or child.tagName == 'Constraints' or child.tagName == 'Values':
                    if nodetype[str(len(nodetype))] == "Condition":
                        doc = minidom.getDOMImplementation()
                        docXML = doc.createDocument(None, "Scapegoat", None)
                        if child.firstChild.nextSibling.tagName == "Attr":
                            if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                nodedata[str(len(nodedata))].appendChild(
                                    child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10))
                                nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                            else:
                                nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                    child.firstChild.nextSibling.nextSibling.nextSibling.cloneNode(10),
                                    nodedata[str(len(nodedata))], '&', docXML)
                        else:
                            if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                nodedata[str(len(nodedata))].appendChild(child.firstChild.nextSibling.cloneNode(10))
                                nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                            else:
                                nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                    child.firstChild.nextSibling.cloneNode(10),
                                    nodedata[str(len(nodedata))], '&', docXML)
                    else:
                        nodedata[str(len(nodedata))] = child.cloneNode(20)
                        nodetype[str(len(nodetype))] = "Condition"
                elif child.tagName == 'Assertions':
                    if nodetype[str(len(nodetype))] == "Condition":
                        doc = minidom.getDOMImplementation()
                        docXML = doc.createDocument(None, "Scapegoat", None)
                        if child.firstChild.nextSibling.tagName == "Attr":
                            count = 3
                        else:
                            count = 1
                        for i in range(len(child.childNodes)):
                            if child.childNodes.item(i).nodeType != child.childNodes.item(i).TEXT_NODE:
                                if i >= count:
                                    if nodedata[str(len(nodedata))].tagName == 'Nary_Pred':
                                        nodedata[str(len(nodedata))].appendChild(
                                            child.childNodes.item(count).cloneNode(10))
                                        nodedata[str(len(nodedata))].appendChild(docXML.createTextNode('\n'))
                                    else:
                                        nodedata[str(len(nodedata))] = nodescreator.createNaryPred(
                                            child.childNodes.item(count).cloneNode(10),
                                            nodedata[str(len(nodedata))], '&', docXML)
                    else:
                        nodedata[str(len(nodedata))] = child.cloneNode(20)
                        nodetype[str(len(nodetype))] = "Condition"
                elif child.tagName == 'Sets':
                    doc = minidom.getDOMImplementation()
                    docXML = doc.createDocument(None, "Scapegoat", None)
                    solveSets(child, docXML)


def getImpWithImportedMch(importedMch, directory):
    for file in os.listdir(directory):
        if file.endswith(".bxml"):
            bxmlfile = minidom.parse(directory + os.sep + file)
            root = bxmlfile.firstChild
            if root.getAttribute('type') == 'implementation':
                abstraction = root.getElementsByTagName('Abstraction')[0]
                if abstraction.firstChild.data == importedMch.firstChild.getAttribute('name'):
                    return bxmlfile
    return None


def mapAssig(node):
    """
    Adding an Instruction node to the Graph.

    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the assignement
    """
    nodetype[str(len(nodetype) + 1)] = "Instruction"
    nodedata[str(len(nodedata) + 1)] = node
    nodemap[str(len(nodemap) + 1)].append(str(len(nodemap) - 1))
    nodecond[str(len(nodecond) + 1)] = "True"
    nodeinva[str(len(nodemap) - 1)] = instgen.make_inst(node.childNodes.item(3))


def mapIf(node, opmch):
    """
    Adding an If to the Graph.

    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the If
    """
    thenNodeList = list()
    # If Condition
    for testenode in node.childNodes:
        if testenode.nodeType != testenode.TEXT_NODE:
            if testenode.tagName == "Condition":
                condition = testenode
    # condition = node.childNodes.item(3)
    condition = condition.childNodes.item(1)
    nodetype[str(len(nodetype) + 1)] = "Condition"
    nodedata[str(len(nodedata) + 1)] = condition
    nodeinva[str(len(nodeinva) + 1)] = ""
    conditionNode = str(len(nodemap))  # To add in the END*
    nodemap[str(len(nodemap) + 1)].append(conditionNode)  # Adding in the END* node
    # Then
    nodecond[str(int(conditionNode) + 1)] = "True"
    for testenode in node.childNodes:
        if testenode.nodeType != testenode.TEXT_NODE:
            if testenode.tagName == "Then":
                then = testenode
                makeMap(then, opmch)
    # then = node.childNodes.item(5)
    # makeMap(then, opmch)
    thenNode = str(len(nodemap) - 1)  # To add in the END*
    thenNodeList = nodemap[str(len(nodemap))]  # To add in the END*
    nodecond[str(int(thenNode) + 1)] = "True and False"
    # Else
    if node.lastChild.previousSibling.tagName == "Else":  # Check if the ELSE exists
        nodecond[str(int(thenNode) + 1)] = "False"
        for testenode in node.childNodes:
            if testenode.nodeType != testenode.TEXT_NODE:
                if testenode.tagName == "Else":
                    makeMap(testenode, opmch)
        # makeMap(node.childNodes.item(7), opmch)
        elseNode = str(len(nodemap) - 1)  # To add in the END*
    # Connecting the END node
    if node.lastChild.previousSibling.tagName == "Else":
        for thennode in thenNodeList:
            if thennode not in nodemap[str(len(nodemap))]:
                nodemap[str(len(nodemap))].append(thennode)  # Adding in the END
        aux = nodemap[str(int(elseNode) + 1)]
        nodemap[str(int(thenNode) + 1)] = [conditionNode]
        for key in aux:
            if key not in nodemap[str(len(nodemap))]:
                nodemap[str(len(nodemap))].append(key)
    else:
        nodemap[str(len(nodemap))].append(conditionNode)  # Adding in the END


def mapCase(node, opmch):
    """
    Adding a Case to the Graph:

    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the Case_Sub in the BXML tree
    """
    # First part of the condition for everycase
    for testenode in node.childNodes:
        if testenode.nodeType != testenode.TEXT_NODE:
            if testenode.tagName == "Value":
                firstconditionpart = testenode.firstChild.nextSibling
    # firstconditionpart = node.childNodes.item(3).firstChild.nextSibling
    # The condition of every other case
    for testenode in node.childNodes:
        if testenode.nodeType != testenode.TEXT_NODE:
            if testenode.tagName == "Choices":
                choices = testenode.childNodes
    # choices = node.childNodes.item(5).childNodes
    allThenNodes = list()
    for choice in choices:
        case = minidom.getDOMImplementation()
        caseXML = case.createDocument(None, "Scapegoat", None)
        caseCondition = caseXML.documentElement
        if choice.nodeType != choice.TEXT_NODE:
            for child in choice.childNodes:
                if child.nodeType != choice.TEXT_NODE:
                    if child.tagName == "Value":
                        caseCondition.appendChild(nodescreator.createExpComparison(firstconditionpart.cloneNode(10),
                                                                                   child.firstChild.nextSibling.cloneNode(
                                                                                       10), '=', caseXML))
            if len(caseCondition.childNodes) > 1:
                condition = nodescreator.createNaryPred(caseCondition.childNodes.item(0),
                                                        caseCondition.childNodes.item(1), 'or', caseXML)
                for i in range(len(caseCondition.childNodes)):
                    if i > 1:
                        condition.appendChild(caseCondition.childNodes.item(i).cloneNode(10))
                        condition.appendChild(caseXML.createTextNode('\n'))
            else:
                condition = caseCondition.firstChild
            nodetype[str(len(nodetype) + 1)] = "Condition"
            nodedata[str(len(nodedata) + 1)] = condition
            nodeinva[str(len(nodeinva) + 1)] = ""
            conditionNode = str(len(nodemap))  # To add in the END
            nodemap[str(len(nodemap) + 1)].append(conditionNode)  # Adding in the END* node
            # Then
            nodecond[str(int(conditionNode) + 1)] = "True"
            then = choice.getElementsByTagName('Then')[0]
            makeMap(then, opmch)
            thenNode = str(len(nodemap) - 1)  # To add in the END*
            nodecond[str(int(thenNode) + 1)] = "False"
            # Conecting an condition in the other (nested if's)
            for thennode in nodemap[str(int(thenNode) + 1)]:
                if thennode not in allThenNodes:
                    allThenNodes.append(thennode)
            nodemap[str(int(thenNode) + 1)] = [conditionNode]
    if node.lastChild.previousSibling.tagName == "Else":
        # body = node.lastChild.previousSibling.firstChild.nextSibling
        # body = body.childNodes.item(3)
        for testenode in node.childNodes:
            if testenode.nodeType != testenode.TEXT_NODE:
                if testenode.tagName == "Else":
                    for childTestNode in testenode.childNodes:
                        if childTestNode.nodeType != childTestNode.TEXT_NODE:
                            if childTestNode.tagName == "Choice":
                                for childChildTestNode in childTestNode.childNodes:
                                    if childChildTestNode.nodeType != childChildTestNode.TEXT_NODE:
                                        if childChildTestNode.tagName == "Then":
                                            body = childChildTestNode
        nodecond[str(int(thenNode) + 1)] = "False"
        makeMap(body, opmch)
        elseNode = str(len(nodemap) - 1)  # To add in the END*
    else:
        allThenNodes.append(conditionNode)
    # Conecting the END
    nodecond[str(len(nodemap))] = "True and False"
    for thennode in allThenNodes:
        if thennode not in nodemap[str(len(nodemap))]:
            nodemap[str(len(nodemap))].append(thennode)


def mapWhile(node, opmch):
    """
    Adding an While to the Graph


    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the while
    """
    # WhileCondition
    for childnode in node.childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            if childnode.tagName == 'Condition':
                condition = childnode.cloneNode(10)
                condition = condition.childNodes.item(1)
    nodetype[str(len(nodetype) + 1)] = "ConditionWhile"
    nodedata[str(len(nodedata) + 1)] = condition
    nodeinva[str(len(nodeinva) + 1)] = ""
    conditionNode = str(len(nodemap))  # To Connect at the END*
    nodemap[str(len(nodemap) + 1)].append(conditionNode)
    for childnode in node.childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            if childnode.tagName == 'Invariant':
                nodeinva[conditionNode] = childnode.cloneNode(10)
    # WhileBody
    nodecond[str(int(conditionNode) + 1)] = "True"
    for childnode in node.childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            if childnode.tagName == 'Body':
                body = childnode.cloneNode(10)
    makeMap(body, opmch)
    bodyNode = str(len(nodemap) - 1)  # To connect at the END*
    # Connecting the while nodes
    nodemap[conditionNode].append(bodyNode)
    nodemap[str(int(bodyNode) + 1)] = [conditionNode]
    nodecond[str(int(bodyNode) + 1)] = "False"


def mapSkip(node):
    """
    Adding a SKIP to the Graph

    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the Skip
    """
    nodetype[str(len(nodetype) + 1)] = "Skip"
    nodedata[str(len(nodedata) + 1)] = node
    nodemap[str(len(nodemap) + 1)].append(str(len(nodemap) - 1))
    nodecond[str(len(nodecond) + 1)] = "True"
    nodeinva[str(len(nodeinva) + 1)] = ""


def mapOperationcall(node):
    """
    Adding a Operation Call to the Graph

    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the Operation_Call
    """
    nodetype[str(len(nodetype) + 1)] = "Call"
    nodedata[str(len(nodedata) + 1)] = node
    nodemap[str(len(nodemap) + 1)].append(str(len(nodemap) - 1))
    nodecond[str(len(nodecond) + 1)] = "True"
    outputs = ""
    for childNode in node.childNodes:
        if childNode.nodeType != childNode.TEXT_NODE:
            if childNode.tagName == "Output_Parameters":
                outputs = instgen.make_outputParameters(childNode)
    nodeinva[str(len(nodeinva) + 1)] = outputs


def mapNary(node, opmch):
    """
    Handling the Nary_Sub and adding every child in the Graph

    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the Nary_Sub
    """
    for childnode in node.childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            makeMapNary(childnode, opmch)


def makeMapNary(node, opmch):
    '''
    Surfing the tree and adding every child of the Nary_Sub node to the Graph

    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: The node of the Nary_Sub
    '''
    tag = node.tagName
    if tag == "Assignement_Sub":
        mapAssig(node)
    if tag == "If_Sub":
        mapIf(node, opmch)
    if tag == "While":
        mapWhile(node, opmch)
    if tag == "VAR_IN":
        makeMap(node, opmch)
    if tag == "Skip":
        mapSkip(node)
    if tag == "Operation_Call":
        mapOperationcall(node)
    if tag == "Case_Sub":
        mapCase(node, opmch)


def makeMap(node, opmch, importedMch=[], seesMch=[], refinementMch = [], directory=[]):
    """
    Surfing the tree and adding every child to the Graph


    Input:
    opmch: The node of the operation in the machine (to get the Precondition)
    node: One of the nodes inside the Tree
    """
    for childnode in node.childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            tag = childnode.tagName
            if tag == "Body":
                if node.tagName == "Operation":
                    startMap(node, opmch, importedMch, seesMch, refinementMch, directory)  # Initialisation of the Graph
                    makeMap(childnode, opmch)
                else:
                    makeMap(childnode, opmch)
            if tag == "Assignement_Sub":
                mapAssig(childnode)
            if tag == "If_Sub":
                mapIf(childnode, opmch)
            if tag == "Nary_Sub":
                mapNary(childnode, opmch)
            if tag == "VAR_IN":
                makeMap(childnode, opmch)
            if tag == "While":
                mapWhile(childnode, opmch)
            if tag == "Skip":
                mapSkip(childnode)
            if tag == "Operation_Call":
                mapOperationcall(childnode)
            if tag == "Case_Sub":
                mapCase(childnode, opmch)


def mapOperations(operationimp, operationmch, directory, importedMch=[], seesMch=[], refinementMch = []):
    """
    Start function, where we start mapping.

    Input:
    operationmch: The node of the operation in the machine (to get the Precondition)
    operationimp: The node of the operation in the implementation
    directory: The directory with the bxml files
    importedMch: List with the imported machines
    seesMch: List with the seen machines
    refinementMch: List with the refinements
    """

    makeMap(operationimp, operationmch, importedMch, seesMch, refinementMch, directory)
    nodetype[str(len(nodetype) + 1)] = "END"  # Adding a type for the END node
    outputs = None
    for childNode in operationimp.childNodes:
        if childNode.nodeType != childNode.TEXT_NODE:
            if childNode.tagName == "Output_Parameters":
                outputs = childNode.cloneNode(10)
    doc = minidom.getDOMImplementation()
    docXML = doc.createDocument(None, "Scapegoat", None)
    finalOutputXML = docXML.createElement('Output')
    if outputs != None:
        for child in outputs.childNodes:
            if child.nodeType != child.TEXT_NODE:
                outputNode = docXML.createElement('Id')
                outputNode.setAttribute('value', 'output' + child.getAttribute('value'))
                outputNode.appendChild(docXML.createTextNode('\n'))
                outputNode.appendChild(docXML.createElement('Attr'))
                outputNode.appendChild(docXML.createTextNode('\n'))
                outputs.replaceChild(nodescreator.createExpComparison(outputNode, child.cloneNode(10), '=', docXML),
                                     child)
        for output in outputs.childNodes:
            if output.nodeType != output.TEXT_NODE:
                if finalOutputXML.hasChildNodes():
                    if finalOutputXML.firstChild.nextSibling.tagName == 'Nary_Pred':
                        finalOutputXML.firstChild.nextSibling.appendChild(output)
                        finalOutputXML.firstChild.nextSibling.appendChild(docXML.createTextNode('\n'))
                    else:
                        naryPredNode = nodescreator.createNaryPred(finalOutputXML.firstChild.nextSibling, output, '&',
                                                                   docXML)
                        finalOutputXML.replaceChild(naryPredNode, finalOutputXML.firstChild.nextSibling)
                else:
                    finalOutputXML.appendChild(docXML.createTextNode('\n'))
                    finalOutputXML.appendChild(output)
                    finalOutputXML.appendChild(docXML.createTextNode('\n'))
    else:
        firstTrue = docXML.createElement('Id')
        firstTrue.setAttribute('value', 'TRUE')
        firstTrue.appendChild(docXML.createTextNode('\n'))
        firstTrue.appendChild(docXML.createElement('Attr'))
        firstTrue.appendChild(docXML.createTextNode('\n'))
        secondTrue = docXML.createElement('Id')
        secondTrue.setAttribute('value', 'TRUE')
        secondTrue.appendChild(docXML.createTextNode('\n'))
        secondTrue.appendChild(docXML.createElement('Attr'))
        secondTrue.appendChild(docXML.createTextNode('\n'))
        finalOutputXML.appendChild(docXML.createTextNode('\n'))
        finalOutputXML.appendChild(nodescreator.createExpComparison(firstTrue, secondTrue, '=', docXML))
        finalOutputXML.appendChild(docXML.createTextNode('\n'))
    nodedata[str(len(nodedata) + 1)] = finalOutputXML.firstChild.nextSibling  # Adding data for the END node
    nodeinva[str(len(nodeinva) + 1)] = ""
    for key in sorted(nodemap.keys()):
        print(key, nodemap[key], nodetype[key], nodedata[key], nodecond[key], nodeinva[key])

def clearGraphs():
    '''
    Function to clear all graphs (Used to implementations with more then one operation.
    '''
    nodemap.clear()
    nodetype.clear()
    nodedata.clear()
    nodecond.clear()
    nodeinva.clear()


# To test, uncomment the next comment.
'''
impName = "triple_while_while_while_i"
imp = minidom.parse(impName+".bxml")
mch = imp.getElementsByTagName("Abstraction")[0] #Getting the Machine name
mch = minidom.parse(mch.firstChild.data+".bxml") #Getting the machine
operationsimp = imp.getElementsByTagName("Operations")[0] #Surfing until Operations
operationsmch = mch.getElementsByTagName("Operations")[0] #Surfing until Operations in the machine   

for operationImp in operationsimp.childNodes:
        if operationImp.nodeType != operationImp.TEXT_NODE:
            operationMch = operationsmch.firstChild.nextSibling #Jumping a TEXT_NODE
            while operationMch.getAttribute("name") != operationImp.getAttribute("name"): #Surfing to the machine operation equal the imp operation
                operationMch = operationMch.nextSibling.nextSibling #Jumping a TEXT_NODE
            mapOperations(operationImp, operationMch)

for key in sorted(nodemap.keys()):
    print(key, nodemap[key], nodetype[key], nodedata[key], nodecond[key], nodeinva[key])
'''