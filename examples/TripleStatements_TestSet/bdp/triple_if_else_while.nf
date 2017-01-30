﻿Normalised(
THEORY MagicNumberX IS
  MagicNumber(Machine(triple_if_else_while))==(3.5)
END
&
THEORY UpperLevelX IS
  First_Level(Machine(triple_if_else_while))==(Machine(triple_if_else_while));
  Level(Machine(triple_if_else_while))==(0)
END
&
THEORY LoadedStructureX IS
  Machine(triple_if_else_while)
END
&
THEORY ListSeesX IS
  List_Sees(Machine(triple_if_else_while))==(?)
END
&
THEORY ListUsesX IS
  List_Uses(Machine(triple_if_else_while))==(?)
END
&
THEORY ListIncludesX IS
  Inherited_List_Includes(Machine(triple_if_else_while))==(?);
  List_Includes(Machine(triple_if_else_while))==(?)
END
&
THEORY ListPromotesX IS
  List_Promotes(Machine(triple_if_else_while))==(?)
END
&
THEORY ListExtendsX IS
  List_Extends(Machine(triple_if_else_while))==(?)
END
&
THEORY ListVariablesX IS
  External_Context_List_Variables(Machine(triple_if_else_while))==(?);
  Context_List_Variables(Machine(triple_if_else_while))==(?);
  Abstract_List_Variables(Machine(triple_if_else_while))==(?);
  Local_List_Variables(Machine(triple_if_else_while))==(?);
  List_Variables(Machine(triple_if_else_while))==(?);
  External_List_Variables(Machine(triple_if_else_while))==(?)
END
&
THEORY ListVisibleVariablesX IS
  Inherited_List_VisibleVariables(Machine(triple_if_else_while))==(?);
  Abstract_List_VisibleVariables(Machine(triple_if_else_while))==(?);
  External_List_VisibleVariables(Machine(triple_if_else_while))==(?);
  Expanded_List_VisibleVariables(Machine(triple_if_else_while))==(?);
  List_VisibleVariables(Machine(triple_if_else_while))==(?);
  Internal_List_VisibleVariables(Machine(triple_if_else_while))==(?)
END
&
THEORY ListInvariantX IS
  Gluing_Seen_List_Invariant(Machine(triple_if_else_while))==(btrue);
  Gluing_List_Invariant(Machine(triple_if_else_while))==(btrue);
  Expanded_List_Invariant(Machine(triple_if_else_while))==(btrue);
  Abstract_List_Invariant(Machine(triple_if_else_while))==(btrue);
  Context_List_Invariant(Machine(triple_if_else_while))==(btrue);
  List_Invariant(Machine(triple_if_else_while))==(btrue)
END
&
THEORY ListAssertionsX IS
  Expanded_List_Assertions(Machine(triple_if_else_while))==(btrue);
  Abstract_List_Assertions(Machine(triple_if_else_while))==(btrue);
  Context_List_Assertions(Machine(triple_if_else_while))==(btrue);
  List_Assertions(Machine(triple_if_else_while))==(btrue)
END
&
THEORY ListCoverageX IS
  List_Coverage(Machine(triple_if_else_while))==(btrue)
END
&
THEORY ListExclusivityX IS
  List_Exclusivity(Machine(triple_if_else_while))==(btrue)
END
&
THEORY ListInitialisationX IS
  Expanded_List_Initialisation(Machine(triple_if_else_while))==(skip);
  Context_List_Initialisation(Machine(triple_if_else_while))==(skip);
  List_Initialisation(Machine(triple_if_else_while))==(skip)
END
&
THEORY ListParametersX IS
  List_Parameters(Machine(triple_if_else_while))==(?)
END
&
THEORY ListInstanciatedParametersX END
&
THEORY ListConstraintsX IS
  List_Context_Constraints(Machine(triple_if_else_while))==(btrue);
  List_Constraints(Machine(triple_if_else_while))==(btrue)
END
&
THEORY ListOperationsX IS
  Internal_List_Operations(Machine(triple_if_else_while))==(?);
  List_Operations(Machine(triple_if_else_while))==(?)
END
&
THEORY ListInputX END
&
THEORY ListOutputX END
&
THEORY ListHeaderX END
&
THEORY ListOperationGuardX END
&
THEORY ListPreconditionX END
&
THEORY ListSubstitutionX END
&
THEORY ListConstantsX IS
  List_Valuable_Constants(Machine(triple_if_else_while))==(?);
  Inherited_List_Constants(Machine(triple_if_else_while))==(?);
  List_Constants(Machine(triple_if_else_while))==(?)
END
&
THEORY ListSetsX IS
  Context_List_Enumerated(Machine(triple_if_else_while))==(?);
  Context_List_Defered(Machine(triple_if_else_while))==(?);
  Context_List_Sets(Machine(triple_if_else_while))==(?);
  List_Valuable_Sets(Machine(triple_if_else_while))==(?);
  Inherited_List_Enumerated(Machine(triple_if_else_while))==(?);
  Inherited_List_Defered(Machine(triple_if_else_while))==(?);
  Inherited_List_Sets(Machine(triple_if_else_while))==(?);
  List_Enumerated(Machine(triple_if_else_while))==(?);
  List_Defered(Machine(triple_if_else_while))==(?);
  List_Sets(Machine(triple_if_else_while))==(?)
END
&
THEORY ListHiddenConstantsX IS
  Abstract_List_HiddenConstants(Machine(triple_if_else_while))==(?);
  Expanded_List_HiddenConstants(Machine(triple_if_else_while))==(?);
  List_HiddenConstants(Machine(triple_if_else_while))==(?);
  External_List_HiddenConstants(Machine(triple_if_else_while))==(?)
END
&
THEORY ListPropertiesX IS
  Abstract_List_Properties(Machine(triple_if_else_while))==(btrue);
  Context_List_Properties(Machine(triple_if_else_while))==(btrue);
  Inherited_List_Properties(Machine(triple_if_else_while))==(btrue);
  List_Properties(Machine(triple_if_else_while))==(btrue)
END
&
THEORY ListSeenInfoX END
&
THEORY ListANYVarX END
&
THEORY ListOfIdsX IS
  List_Of_Ids(Machine(triple_if_else_while)) == (? | ? | ? | ? | ? | ? | ? | ? | triple_if_else_while);
  List_Of_HiddenCst_Ids(Machine(triple_if_else_while)) == (? | ?);
  List_Of_VisibleCst_Ids(Machine(triple_if_else_while)) == (?);
  List_Of_VisibleVar_Ids(Machine(triple_if_else_while)) == (? | ?);
  List_Of_Ids_SeenBNU(Machine(triple_if_else_while)) == (?: ?)
END
&
THEORY TCIntRdX IS
  predB0 == OK;
  extended_sees == KO;
  B0check_tab == KO;
  local_op == OK;
  abstract_constants_visible_in_values == KO;
  project_type == SOFTWARE_TYPE;
  event_b_deadlockfreeness == KO;
  variant_clause_mandatory == KO;
  event_b_coverage == KO;
  event_b_exclusivity == KO;
  genFeasibilityPO == KO
END
)
