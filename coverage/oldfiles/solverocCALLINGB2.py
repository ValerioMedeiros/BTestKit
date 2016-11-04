from xml.dom import minidom
import sys
import os
import codecs
import nodescreator
import subprocess

def buildOperationCall(node, predicateXML, docXML, operationImp, importedMch, operationName, impName, posMut):
    '''
    Return the predicate of a called operation

    Input:
    operationImp: The operation of the implementation (the one being evaluated)
    node: The node with the type "Call"
    importedMch: All imported machines
    operationName: The name of the operation of the implementation (the one being evaluated)
    predicateXML: The predicate until now in form of a XML tree
    docXML: The XML document
    posMut: All variables quantified inside the while
    impName: The name of the implementation

    Return:
    predicateXML: The predicate until now in form of a XML tree
    '''
    calledOperationName, operationInputs, operationOutputs, calledMachineName = getMchWithTheCalledOperation(operationImp, node, importedMch, operationName)
    operationIBXML, operationInputs, operationOutputs = getOperationIBXML(impName, operationName, calledOperationName, operationImp, operationInputs, operationOutputs)
    #auxXML = modifyPredicateXML(predicateXML, operationIBXML)
    auxXML = predicateXML
    output = make_Sub_Calculus(operationIBXML, auxXML)
    predicateXML.replaceChild(solveOutputPredicate(output, docXML, posMut, calledOperationName, operationInputs, operationOutputs, calledMachineName),
                              predicateXML.firstChild.nextSibling)
    #os.remove("encodeddocumentinput.xml")
    #os.remove("encodeddocumentoutput.xml")
    #os.remove(impName+".ibxml")
    return predicateXML

def getMchWithTheCalledOperation(operationImp, node, importedMch, ImpOperationName):
    '''
    Return properties of the called operation.

    Input:
    operationImp: The operation of the implementation (the one being evaluated)
    node: The node with the type "Call"
    importedMch: All imported machines
    ImpOperationName: The name of the operation of the implementation (the one being evaluated)

    Return:
    calledOperationName : The name of the called operation
    calledOperationInputsInTheImp : The inputs of the called operation in the implementation
    calledOperationOutputsInTheImp : The outputs of the called operation in the implementation
    '''
    calledop = operationImp.getElementsByTagName("Operation_Call")
    for op in calledop:
        opname = op.getElementsByTagName("Name")[0].firstChild.nextSibling.getAttribute("value")
        for mch in importedMch:
            operations = mch.getElementsByTagName("Operation")
            for operation in operations:
                if operation.getAttribute("name") == opname:
                    calledMachineName = mch.firstChild.getAttribute('name')
                    calledOperationName = operation.getAttribute("name")
                    calledOperationInputsInTheImp = op.getElementsByTagName("Input_Parameters")[0]
                    calledOperationOutputsIntheImp = op.getElementsByTagName("Output_Parameters")[0]
    return calledOperationName, calledOperationInputsInTheImp, calledOperationOutputsIntheImp, calledMachineName

def checkPuts(Parameters, ImpParameters):
    '''
    Return if the operation is the same (check only the inputs or the outputs)

    Input:
    Parameters: The outputs or the inputs of the machine
    ImpParameters: The outputs or the inputs of the implementation
    
    Return:
    ans: True means that the parameters are equal, False that are different (this is used to know if the same)
    '''
    ans = True
    IDs = Parameters.getElementsByTagName('Id')
    ImpIDs = ImpParameters.getElementsByTagName('Id')
    for i in range(len(IDs)):
        if IDs[i].getAttribute('value') != ImpIDs[i].getAttribute('value'):
            ans = False
    return ans

def checkOperationCall(operationCalls, operationImp, calledOperationName, operationInputs, operationOutputs):
    '''
    Check if exist the operation called in the operation call, if true, return the called operation, else return None

    Input:
    operationImp: The operation of the implementation (the one being evaluated)
    calledOperationName: The name of the operation of the called operation
    operationCalls: All the Operation Calls of the operation being evaluated
    operationInputs: The inputs of the called operation in the implementation
    operationOutputs: The outputs of the called operation in the implementation

    Return:
    operationCall if the called operation is found, otherwise return None and an error is raised
    '''
    for operationCall in operationCalls:
        for child in operationCall.childNodes:
            if child.nodeType != child.TEXT_NODE:
                if child.tagName == "Operation":
                    if child.getAttribute('name') == calledOperationName:
                        okayOperation = True
                        inputIDs = child.parentNode.getElementsByTagName("Input_Parameters")[0]
                        outputIDs = child.parentNode.getElementsByTagName("Output_Parameters")[0]
                        if inputIDs != None:
                            okayInputs = checkPuts(inputIDs, operationInputs)
                        else:
                            okayInputs = True
                        if outputIDs != None:
                            okayOutputs = checkPuts(outputIDs, operationOutputs)
                        else:
                            okayOutputs = True
                        if okayOperation == True & okayInputs == True & okayOutputs == True:
                            inputsCalledOperation = child.getElementsByTagName('Input_Parameters')[0]
                            outputsCalledOperation = child.getElementsByTagName('Output_Parameters')[0]
                            return operationCall, inputsCalledOperation, outputsCalledOperation
    return None, None, None

def getOperationIBXML(impName, operationName, calledOperationName, operationImp, operationInputs, operationOutputs):
    '''
    Return the IBXML tree of the implementation operation. The IBXML is a XML file that contains the substitution of the Operation Call.

    Input:
    impName: The name of the implementation
    operationImp: The operation of the implementation (the one being evaluated)
    operationName: The name of the operation of the implementation (the one being evaluated)
    calledOperationName: The name of the operation of the called operation
    operationInputs: The inputs of the called operation in the implementation
    operationOutputs: The outputs of the called operation in the implementation

    Return:
    operationIBXML: The IBXML of the implementation.
    The IBXML is a XML file that contains the substitution of the Operation Call.
    '''
    args = ["/Program Files (x86)/Atelier B full 4.4.0-beta.2/bbin/win32/pog.exe"]
    args.append("-i")
    args.append(impName+".bxml")
    p = subprocess.call(args)
    ibxml = minidom.parse(impName+".ibxml")
    for child in ibxml.firstChild.childNodes:
        if child.nodeType != child.TEXT_NODE:
            if child.tagName == "Operations":
                for operation in child.childNodes:
                    if operation.nodeType != operation.TEXT_NODE:
                        if operation.getAttribute('name') == operationName:
                            operationCalls = operation.getElementsByTagName('Operation_Call')
                            operationIBXML, inputsCalledOperation, outputsCalledOperation = checkOperationCall(operationCalls, operationImp, calledOperationName, operationInputs, operationOutputs)
                            if operationIBXML != None:
                                return operationIBXML, inputsCalledOperation, outputsCalledOperation
    return None, None, None

def modifyPredicateXML(predicateXML, operationIBXML):
    '''
    Return the predicate of a called operation

    Input:
    operationIBXML: The operation in form of a XML tree (the operation call is already replaced)
    predicateXML: The predicate until now in form of a XML tree

    Return:
    predicateXML: The predicate until now in form of a XML tree
    '''
    IDsInPredicate = predicateXML.getElementsByTagName('Id')
    IDsInIBXML = operationIBXML.getElementsByTagName('Output_Parameters')[0]
    IDsInIBXML = IDsInIBXML.getElementsByTagName('Id')
    for ID in IDsInPredicate:
        for IDibxml in IDsInIBXML:
            if ID.getAttribute('value') == IDibxml.getAttribute('value'):
                ID.setAttribute('tag', IDibxml.getAttribute('tag'))
    return predicateXML

def solveOutputPredicate_If_Sub(subst, pred, docXML, posMut):
    '''
    Solve the If_Sub that is returned as output

    Input:
    subst: The substitution
    pred: The predicate that the substituion will happen
    docXML: The XML document
    posMut: The quantified variables inside the while

    Return:
    newPred: The predicate with everything already replaced (final predicate of the operation call)
    '''
    condition = subst.childNodes.item(3)
    condition = condition.firstChild.nextSibling
    body = subst.childNodes.item(5)
    body = body.firstChild.nextSibling
    newPred = makePredicateInstruction(body, pred.cloneNode(10), posMut, docXML)
    newPred = nodescreator.createBinaryPred(condition, newPred, docXML)
    if subst.lastChild.previousSibling.tagName == "Else":
        bodyElse = subst.childNodes.item(7)
        bodyElse = bodyElse.firstChild.nextSibling
        newPredElse = makePredicateInstruction(bodyElse, pred.cloneNode(10), posMut, docXML)
        binaryPredElse = nodescreator.createBinaryPred(nodescreator.createUnaryNode(condition.cloneNode(10), docXML), newPredElse, docXML)
        newPred = nodescreator.createNaryPred(newPred, binaryPredElse, docXML)
    return newPred

def solveOutputPredicate_LET_Sub(subst, pred, docXML, posMut):
    '''
    Solve the Select that is returned as output

    Input:
    subst: The substitution
    pred: The predicate taht the substituition happen
    docXML: The XML document
    posMut: The quantified variables inside the while

    Return:
    FinalPred: The predicate with everything already replaced (final predicate of the operation call)
    '''
    for childnode in subst.childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            if childnode.tagName == "Values":
                for value in childnode.childNodes:
                    if value.nodeType != childnode.TEXT_NODE:
                        variable = value.getAttribute('ident')
                        changevalue = value.childNodes.item(3)
                        thenPred = subst.getElementsByTagName('Then')[0]
                        allID = thenPred.getElementsByTagName('Id')
                        for ID in allID:
                            if ID.getAttribute("value") == variable:
                                ID.parentNode.replaceChild(changevalue.cloneNode(10), ID)
            if childnode.tagName == "Then":
                newPred = makePredicateInstruction(childnode.firstChild.nextSibling.cloneNode(10), pred.cloneNode(10), posMut, docXML)
    return newPred
    
def solveOutputPredicate_Nary_Sub(subst, pred, docXML, posMut):
    '''
    Solve the Nary_Sub that is returned as output

    Input:
    subst: The substitution
    pred: The predicate taht the substituition happen
    docXML: The XML document
    posMut: The quantified variables inside the while

    Return:
    FinalPred: The predicate with everything already replaced (final predicate of the operation call)
    '''
    FinalPred = docXML.createElement('Predicate')
    for childnode in subst.childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            if childnode.tagName != 'Attr':
                newPred = makePredicateInstruction(childnode.cloneNode(10), pred.cloneNode(10), posMut, docXML)
                if FinalPred.hasChildNodes():
                    if FinalPred.firstChild.nextSibling.tagName == "Nary_Sub":
                        FinalPred.firstChild.nextSibling.appendChild(newPred)
                        FinalPred.firstChild.nextSibling.appendChild(docXML.createTextNode('\n'))
                    else:
                        naryNode = nodescreator.createNaryPred(FinalPred.firstChild.nextSibling, newPred,  '&', docXML)
                        FinalPred.insertBefore(naryNode, FinalPred.firstChild.nextSibling)
                else:
                    FinalPred.appendChild(docXML.createTextNode('\n'))
                    FinalPred.appendChild(newPred)
                    FinalPred.appendChild(docXML.createTextNode('\n'))
    return FinalPred.firstChild.nextSibling

def testDeterminism(subst):
    if subst.getElementsByTagName('Select') != [] or subst.tagName == 'Select':
        return False
    if subst.getElementsByTagName('Nary_Sub') != []:
        if len(subst.getElementsByTagName('Nary_Sub')) > 1:
            for element in subst.getElementsByTagName('Nary_Sub'):
                if element.getAttribute('op') == 'CHOICE':
                    return False
        else:
            if subst.getElementsByTagName('Nary_Sub').getAttribute('op') == "CHOICE":
                return False
    if (subst.tagName == 'Nary_Sub' and subst.getAttribute('op') == "CHOICE"):
        return False
    if subst.getElementsByTagName('ANY_Sub') != [] or subst.tagName == 'ANY_Sub':
        return False
    if subst.getElementsByTagName('Becomes_In') != [] or subst.tagName == 'Becomes_In':
        return False
    if subst.getElementsByTagName('Becomes_Such_That') != [] or subst.tagName == 'Becomes_Such_That':
        return False
    return True

def makePredicateInstruction(subst, pred, posMut, docXML):
    if subst.tagName == "Simple_Assignement_Sub":
        pred = changeVariableInPred(pred, subst, posMut)
    if subst.tagName == "If_Sub":
        pred = solveOutputPredicate_If_Sub(subst, pred, docXML, posMut)
    if subst.tagName == "Nary_Sub":
        pred = solveOutputPredicate_Nary_Sub(subst, pred, docXML, posMut)
    if subst.tagName == "LET_Sub":
        pred = solveOutputPredicate_LET_Sub(subst, pred, docXML, posMut)
    return pred

def getCalledOperationImplementation(calledOperationName, operationInputs, operationOutputs, calledMachineName):
    for file in os.listdir('/Users/Diego Oliveira/Documents/BTestBox/coverage/'):
        if file.endswith(".bxml"):
            bxmlfile = minidom.parse(file)
            root = bxmlfile.firstChild
            if root.getAttribute('type') == 'implementation':
                abstraction = root.getElementsByTagName('Abstraction')[0]
                if abstraction.firstChild.data == calledMachineName:
                    importedImplementationOperations = root.getElementsByTagName('Operation')
                    for importedImplementationOperation in importedImplementationOperations:
                        if importedImplementationOperation.getAttribute('name') == calledOperationName:
                            okayOperation = True
                            inputIDs = importedImplementationOperation.getElementsByTagName("Input_Parameters")[0]
                            outputIDs = importedImplementationOperation.getElementsByTagName("Output_Parameters")[0]
                            if inputIDs != None:
                                okayInputs = checkPuts(inputIDs, operationInputs)
                            else:
                                okayInputs = True
                            if outputIDs != None:
                                okayOutputs = checkPuts(outputIDs, operationOutputs)
                            else:
                                okayOutputs = True
                            if okayOperation == True & okayInputs == True & okayOutputs == True:
                                return importedImplementationOperation
    return None
    

def solveOutputPredicate(outputXML, docXML, posMut, calledOperationName, operationInputs, operationOutputs, calledMachineName):
    '''
    Solve the Output predicate

    Input:
    outputXML: The output XML after the substitution
    docXML: The XML document
    posMut: The quantified variables inside the while

    Return:
    newPred: The predicate with everything already replaced (final predicate of the operation call)
    '''
    pred = outputXML.firstChild.childNodes.item(1).childNodes.item(3).lastChild.previousSibling
    subst = outputXML.firstChild.childNodes.item(1).childNodes.item(3).firstChild.nextSibling
    if testDeterminism(subst) == False:
        calledOperationImplementation = getCalledOperationImplementation(calledOperationName, operationInputs, operationOutputs, calledMachineName)
        print(calledOperationImplementation)
    else:
        newPred = makePredicateInstruction(subst, pred, posMut, docXML)
    return newPred
        
def changeVariableInPred(predicate, substitution, posMut):
    '''
    Create and return a Binary_Pred node

    Input:
    predicate: The predicate tree inside the IBXML
    substitution: The substitution tree inside the XML
    posMut: The quantified variables inside the while

    Return:
    predicate: The predicate with everything already replaced (final predicate of the operation call)
    '''
    if substitution.tagName == 'Nary_Sub':
        for child in substitution.childNodes:
            if child.nodeType != child.TEXT_NODE:
                variablesId = child.getElementsByTagName("Variables")[0]
                variablesId = variablesId.getElementsByTagName("Id")[0].getAttribute('value')
                values = child.getElementsByTagName("Values")[0]
                values = values.firstChild.nextSibling
                allId = predicate.getElementsByTagName('Id')
                for Id in allId:
                    if Id.getAttribute("value") == variablesId:
                        if Id.getAttribute("value") in posMut:
                            parent = Id.parentNode
                            isInQuant = False
                            while(parent != None):
                                if parent.tagName == "Quantified_Pred":
                                    isInQuant = True
                                parent = parent.parentNode
                            if isInQuant == False:
                                cloneValues = values.cloneNode(5)
                                Id.parentNode.replaceChild(cloneValues, Id)
                        else:
                            cloneValues = values.cloneNode(5)
                            Id.parentNode.replaceChild(cloneValues, Id)
    else:
        variablesId = substitution.getElementsByTagName("Variables")[0]
        variablesId = variablesId.getElementsByTagName("Id")[0].getAttribute('value')
        values = substitution.getElementsByTagName("Values")[0]
        values = values.firstChild.nextSibling
        allId = predicate.getElementsByTagName('Id')
        for Id in allId:
            if Id.getAttribute("value") == variablesId:
                if Id.getAttribute("value") in posMut:
                    parent = Id.parentNode
                    isInQuant = False
                    while(parent != None):
                        if parent.tagName == "Quantified_Pred":
                            isInQuant = True
                        parent = parent.parentNode
                    if isInQuant == False:
                        cloneValues = values.cloneNode(5)
                        Id.parentNode.replaceChild(cloneValues, Id)
                else:
                    cloneValues = values.cloneNode(5)
                    Id.parentNode.replaceChild(cloneValues, Id)
    return predicate
        
    
def make_Sub_Calculus(calledOperation, predicateXML):
    '''
    Call the exe that make the substitution of the predicate, and return it as output

    Input:
    calledOperation: The called operation tree
    predicateXML: The predicate until now

    Return:
    outputXML: The output in a XML tree
    '''
    impl = minidom.getDOMImplementation()
    subCalcXML = impl.createDocument(None, "Sub_Calculus_Father", None)
    root = subCalcXML.documentElement
    calcSub = subCalcXML.createElement("Sub_Calculus")
    root.appendChild(calcSub)
    calcSub.appendChild(calledOperation)
    calcSub.appendChild(predicateXML.firstChild.nextSibling)
    encodeddocument = subCalcXML.toprettyxml(encoding="utf-8")
    f = open("/Users/Diego Oliveira/Documents/BTestBox/coverage/encodeddocumentinput.xml", 'bw')
    f.write(encodeddocument)
    f.close()
    args = "/Users/Diego Oliveira/AtelierB/installatelierb/bbin/win32/substitution_calculus_pred.exe"
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    output, errors = p.communicate()
    if p.returncode==0:
        print("Calculus_pred executed successfully")
        #print(output)
    else:
        print("Calculus_pred - error reported and the return code is "+str(p.returncode))
        #print(output)
        print(errors)
    f = open("/Users/Diego Oliveira/Documents/BTestBox/coverage/encodeddocumentoutput.xml", 'bw')
    f.write(output)
    f.close()
    outputXML = minidom.parse("encodeddocumentoutput.xml")
    return outputXML
    