from xml.dom import minidom
import sys
import os
import codecs
import nodescreator
import subprocess
import buildpaths
import instgen

def buildOperationCall(node, predicateXML, docXML, operationImp, importedMch, operationName, impName, posMut, inputs, isTheOutput, universalOutputs, changedVariables):
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
    calledOperation, operationInputs, operationOutputs, calledMachineName = getMchWithTheCalledOperation(operationImp, buildpaths.graphgen.nodedata[node],
                                                                                                         importedMch)
    if isTheOutput:
        hasWhile = False
        operationIBXML = getOperationIBXML(impName, operationName, calledOperation,
                                                                             operationImp, operationInputs, operationOutputs)
        calledOperationImp = getImpWithCalledOperation(calledOperation, calledMachineName)
        for i in range(len(calledOperationImp.getElementsByTagName('Operation_Call'))):
            solveInsideOperationCall(calledOperationImp.parentNode.parentNode.parentNode, calledOperationImp)
        if calledOperationImp.getElementsByTagName("While") != []:
            hasWhile = True
        operationIBXML = changeMachineWithImplementation(calledOperationImp, operationIBXML, docXML)
        auxXML = modifyPredicateXML(predicateXML, operationIBXML)
        output = make_Sub_Calculus(operationIBXML, auxXML)
        if hasWhile == True:
            output = output.getElementsByTagName('Tag')
            for out in output:
                if out.getAttribute('goalTag') == "End of loop":
                    output = out.getElementsByTagName('Body')[0]
                    changedVariables = changeVariablesNames(output, inputs, universalOutputs, changedVariables)
                    naryPredNode = nodescreator.createNaryPred(output.firstChild.nextSibling.lastChild.previousSibling.cloneNode(10),
                                                               output.firstChild.nextSibling.firstChild.nextSibling.cloneNode(10), '&', docXML)
                    predicateXML.replaceChild(naryPredNode, predicateXML.firstChild.nextSibling)
        else:
            predicateXML.replaceChild(output.firstChild.firstChild.nextSibling.lastChild.previousSibling.cloneNode(10),
                              predicateXML.firstChild.nextSibling)
    else:
        operationIBXML = getOperationIBXML(impName, operationName, calledOperation,
                                                                             operationImp, operationInputs, operationOutputs)
        auxXML = modifyPredicateXML(predicateXML, operationIBXML, posMut)
        output = make_Sub_Calculus(operationIBXML, auxXML)
        predicateXML.replaceChild(output.firstChild.firstChild.nextSibling.lastChild.previousSibling.cloneNode(10),
                              predicateXML.firstChild.nextSibling)
    os.remove("encodeddocumentinput.xml")
    os.remove("encodeddocumentoutput.xml")
    os.remove(impName+".ibxml")
    return predicateXML, changedVariables

def changeVariablesNames(predicate, inputs, outputs, previousChangedId, posMut = []):
    '''
    '''
    allId = predicate.getElementsByTagName('Id')
    changedId = []
    auxlist = []
    changeMutablePos = []
    for Id in allId:
        if Id.getAttribute('value') not in inputs:
            if Id.getAttribute('value') not in outputs:
                if Id.getAttribute('value') not in previousChangedId:
                    if Id.getAttribute('value') in posMut:
                        for mutposition in range(len(posMut)):
                            if posMut[mutposition] == Id.getAttribute('value'):
                                changeMutablePos.append(mutposition)                                
                    Id.setAttribute('value', Id.getAttribute('value')+'1')
                    while (Id.getAttribute('value') in previousChangedId):
                        Id.setAttribute('value', Id.getAttribute('value')+'1')
                    changedId.append(Id.getAttribute('value'))
                    for position in changeMutablePos:
                        posMut[position] = Id.getAttribute('value')
    for Id in changedId:
        if Id not in auxlist:
            auxlist.append(Id)
    return previousChangedId + auxlist

def solveInsideOperationCall(calledImp, calledOperationImp):
    '''
    This function deal with the different calling of a machine (deterministic and non-deterministic) and implementation (with operation call or without)
    Only enters here if the called operation is non-deterministic.

    Inputs:
    calledImp: The called implementation
    calledOperationImp: The called operation TREE in the implementation
    '''
    importedMch = list()
    for childnode in calledImp.getElementsByTagName("Machine")[0].childNodes:
        if childnode.nodeType != childnode.TEXT_NODE:
            if childnode.tagName == "Imports":
                importedMchTree = calledImp.getElementsByTagName("Imports")[0] #Getting all Imports branch
                importedMchTree = importedMchTree.getElementsByTagName("Referenced_Machine")[0] #Getting all referenced machine
                importedMchTree = importedMchTree.getElementsByTagName("Name")#Getting all names of imported machines
                for name in importedMchTree:
                    importedMch.append(minidom.parse(name.firstChild.data+".bxml")) #Getting the imported machine
    operationCall = calledOperationImp.getElementsByTagName('Operation_Call')[0]
    mchInsideCalledOperation, mchInsideOperationInputs, mchInsideOperationOutputs, mchInsideCalledMachineName = getMchWithTheCalledOperation(calledImp, operationCall,
                                                                                                                     importedMch)
    if not(testDeterminism(mchInsideCalledOperation)):
        impCalledOperation = getImpWithCalledOperation(mchInsideCalledOperation, mchInsideCalledMachineName)
        if impCalledOperation.getElementsByTagName('Operation_Call') != []:
            solveInsideOperationCall(impCalledOperation.parentNode.parentNode.parentNode, impCalledOperation)
            calledOperationImp = changeOperationCallWithOperationMachine(operationCall, impCalledOperation,
                                                                         mchInsideOperationInputs, mchInsideOperationOutputs)
        else:
            calledOperationImp = changeOperationCallWithOperationMachine(operationCall, impCalledOperation,
                                                                         mchInsideOperationInputs, mchInsideOperationOutputs)        
    else:
        calledOperationImp = changeOperationCallWithOperationMachine(operationCall, mchInsideCalledOperation,
                                                                     mchInsideOperationInputs, mchInsideOperationOutputs)

def changeOperationCallWithOperationMachine(operationCall, calledOperationMachine, mchOperationInputs, mchOperationOutputs):
    '''
    This function change the operation call in the implementation for the body of the operation in the machine.
    Only enters here if the called operation is deterministic after the previous is non-deterministic (nested operation calls).

    Inputs:
    operationCall: The operation call branch in the implementation
    calledOperationMachine: The called machine
    mchOperationInputs: The inputs of the operation in the implementation
    mchOperationOutputs: The outputs of the operation in the implementation

    Return:
    substitution: The predicate with the swaped operations
    '''
    for child in calledOperationMachine.childNodes:
        if child.nodeType != child.TEXT_NODE:
            if child.tagName == "Output_Parameters":
                calledOperationMachineOutputs = child.getElementsByTagName('Id')
                operationOutputs = mchOperationOutputs.getElementsByTagName('Id')
                allId = child.parentNode.getElementsByTagName('Body')[0]
                allId = allId.getElementsByTagName('Id')
                for i in range(len(calledOperationMachineOutputs)):
                    for Id in allId:
                        if Id.getAttribute('value') == calledOperationMachineOutputs[i].getAttribute('value'):
                            Id.parentNode.replaceChild(operationOutputs[i].cloneNode(10), Id)
            if child.tagName == "Input_Parameters":
                calledOperationMachineInputs = child.getElementsByTagName('Id')
                operationInputs = mchOperationInputs.getElementsByTagName('Id')
                allId = child.parentNode.getElementsByTagName('Body')[0]
                allId = allId.getElementsByTagName('Id')
                for i in range(len(calledOperationMachineInputs)):
                    for Id in allId:
                        if Id.getAttribute('value') == calledOperationMachineInputs[i].getAttribute('value'):
                            Id.parentNode.replaceChild(operationInputs[i].cloneNode(10), Id)
    substitution = operationCall.parentNode
    substitution.replaceChild(calledOperationMachine.getElementsByTagName('Body')[0].firstChild.nextSibling.cloneNode(10), operationCall)
    return substitution
    
def changeMachineWithImplementation(calledOperation, operationIBXML, docXML):
    '''
    This function change the operation call in the machine for the body of the operation in the implementation.
    Only enters here if the called operation is non-deterministic.

    Inputs:
    calledOperation: The called operation TREE in the non-deterministic machine operation
    operationIBXML: The IBXML with the operation call of the non-deterministic machine
    docXML: The xml document

    Return:
    operationIBXML: The IBXML with the implementation instead of the operation call
    '''
    operation = operationIBXML.getElementsByTagName('Operation')[0]
    for operationchild in operation.childNodes:
        if operationchild.nodeType != operationchild.TEXT_NODE:
            if operationchild.tagName == "Body":
                for calledOperationChild in calledOperation.childNodes:
                    if calledOperationChild.nodeType != calledOperationChild.TEXT_NODE:
                        if calledOperationChild.tagName == "Body":
                            operationchild.parentNode.replaceChild(calledOperationChild, operationchild)
    allAssig = operationIBXML.getElementsByTagName('Assignement_Sub')
    for assig in allAssig:
        newAssig = docXML.createElement('Simple_Assignement_Sub')
        for assigchilds in assig.childNodes:
            newAssig.appendChild(assigchilds.cloneNode(10))
        assig.parentNode.replaceChild(newAssig, assig)
    return operationIBXML

def getImpWithCalledOperation(calledOperation, calledMachineName):
    '''
    Function to return the operation in the implementation of a given machine.
    Only enters here if a non-deterministic operation was found then the algorithm get the implementation (that is deterministic).

    Inputs:
    calledOperation: The called operation TREE in the non-deterministic machine operation
    calledMachineName: The name of the machine that has the non-deterministic machine operation
    
    Return:
    If the algorithm found an implementation version of the non-deterministic operation it returns the operation, otherwise return None.
    '''
    for file in os.listdir('/Users/Diego Oliveira/Documents/BTestBox/coverage/'):
        if file.endswith(".bxml"):
            bxmlfile = minidom.parse(file)
            root = bxmlfile.firstChild
            if root.getAttribute('type') == 'implementation':
                abstraction = root.getElementsByTagName('Abstraction')[0]
                if abstraction.firstChild.data == calledMachineName:
                    importedImplementationOperations = root.getElementsByTagName('Operation')
                    for importedImplementationOperation in importedImplementationOperations:
                        if importedImplementationOperation.getAttribute('name') == calledOperation.getAttribute('name'):
                            return importedImplementationOperation
    return None

def modifyPredicateXML(predicateXML, operationIBXML, posMut = []):
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
                if ID.getAttribute('value') not in posMut:
                    ID.parentNode.replaceChild(IDibxml.cloneNode(10), ID)
    return predicateXML

def getMchWithTheCalledOperation(operationImp, calledop, importedMch):
    '''
    Return properties of the called operation.

    Input:
    operationImp: The operation of the implementation (the one being evaluated)
    node: The node with the type "Call"
    importedMch: All imported machines

    Return:
    calledOperationName : The name of the called operation
    calledOperationInputsInTheImp : The inputs of the called operation in the implementation
    calledOperationOutputsInTheImp : The outputs of the called operation in the implementation
    '''
    opname = calledop.getElementsByTagName("Name")[0].firstChild.nextSibling.getAttribute("value")
    for mch in importedMch:
        operations = mch.getElementsByTagName("Operation")
        for operation in operations:
            if operation.getAttribute("name") == opname:
                calledMachineName = mch.firstChild.getAttribute('name')
                if calledop.getElementsByTagName("Input_Parameters") != []:
                    calledOperationInputsInTheImp = calledop.getElementsByTagName("Input_Parameters")[0]
                else:
                    calledOperationInputsInTheImp = []
                if calledop.getElementsByTagName("Output_Parameters") != []:
                    calledOperationOutputsIntheImp = calledop.getElementsByTagName("Output_Parameters")[0]
                else:
                    calledOperationInputsInTheImp = []
                return operation, calledOperationInputsInTheImp, calledOperationOutputsIntheImp, calledMachineName
    return None, None, None, None

def testDeterminism(operation):
    '''
    Fuction to check if a machine is deterministic or not, if it is return True, if not, return False

    Inputs:
    operation: The machine operation

    Return:
    Returns False if the machine is non deterministic, otherwise return True
    '''
    if operation.getElementsByTagName('Select') != [] or operation.tagName == 'Select':
        return False
    if operation.getElementsByTagName('Nary_Sub') != []:
        if len(operation.getElementsByTagName('Nary_Sub')) > 1:
            for element in operation.getElementsByTagName('Nary_Sub'):
                if element.getAttribute('op') == 'CHOICE':
                    return False
        else:
            if operation.getElementsByTagName('Nary_Sub')[0].getAttribute('op') == "CHOICE":
                return False
    if (operation.tagName == 'Nary_Sub' and operation.getAttribute('op') == "CHOICE"):
        return False
    if operation.getElementsByTagName('ANY_Sub') != [] or operation.tagName == 'ANY_Sub':
        return False
    if operation.getElementsByTagName('Becomes_In') != [] or operation.tagName == 'Becomes_In':
        return False
    if operation.getElementsByTagName('Becomes_Such_That') != [] or operation.tagName == 'Becomes_Such_That':
        return False
    return True

def checkPuts(Parameters, ImpParameters):
    '''
    Return if the operation is the same (check only the inputs or the outputs)

    Input:
    Parameters: The outputs or the inputs of the machine
    ImpParameters: The outputs or the inputs of the implementation
    
    Return:
    ans: True means that the parameters are equal, False that are different (this is used to know if is the same Operation)
    '''
    ans = True
    IDs = Parameters.getElementsByTagName('Id') + Parameters.getElementsByTagName('Integer_Literal')
    ImpIDs = ImpParameters.getElementsByTagName('Id') + ImpParameters.getElementsByTagName('Integer_Literal')
    for i in range(len(IDs)):
        if IDs[i].getAttribute('value') != ImpIDs[i].getAttribute('value'):
            ans = False
    return ans

def checkOperationCall(operationCalls, operationImp, calledOperation, operationInputs, operationOutputs):
    '''
    Check if exist the operation called in the operation call, if true, return the called operation, else return None

    Input:
    operationImp: The operation of the implementation (the one being evaluated)
    calledOperation: The called operation
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
                    if child.getAttribute('name') == calledOperation.getAttribute('name'):
                        okayOperation = True
                if child.tagName == 'Input_Parameters':
                    inputsIDs = child
                    okayInputs = checkPuts(inputsIDs, operationInputs)
                if child.tagName == 'Output_Parameters':
                    outputsIDs = child
                    okayOutputs = checkPuts(outputsIDs, operationOutputs)
                    outputsIDsCalledOperation = child.parentNode.getElementsByTagName('Output_Parameters')[1].cloneNode(10)
        if operationInputs == []:
            okayInputs = True
        if operationOutputs == []:
            okayOutputs = True
        if okayOperation == True & okayInputs == True & okayOutputs == True:
            return operationCall
    return None

def getOperationIBXML(impName, operationName, calledOperation, operationImp, operationInputs, operationOutputs):
    '''
    Return the IBXML tree of the implementation operation. The IBXML is a XML file that contains the substitution of the Operation Call.

    Input:
    impName: The name of the implementation
    operationImp: The operation of the implementation (the one being evaluated)
    operationName: The name of the operation of the implementation (the one being evaluated)
    calledOperation: The called operation
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
                            operationIBXML = checkOperationCall(operationCalls, operationImp, calledOperation, operationInputs, operationOutputs)
                            if operationIBXML != None:
                                return operationIBXML
    return None

def make_Sub_Calculus(calledOperation, predicateXML):
    '''
    Call the exe that make the substitution of the predicate, and return a predicate XML as output

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
    calcSub.appendChild(predicateXML.firstChild.nextSibling.cloneNode(10))
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
    
