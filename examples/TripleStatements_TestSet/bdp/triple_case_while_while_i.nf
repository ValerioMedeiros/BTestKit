﻿Normalised(
THEORY MagicNumberX IS
  MagicNumber(Implementation(triple_case_while_while_i))==(3.5)
END
&
THEORY UpperLevelX IS
  First_Level(Implementation(triple_case_while_while_i))==(Machine(triple_case_while_while));
  Level(Implementation(triple_case_while_while_i))==(1);
  Upper_Level(Implementation(triple_case_while_while_i))==(Machine(triple_case_while_while))
END
&
THEORY LoadedStructureX IS
  Implementation(triple_case_while_while_i)
END
&
THEORY ListSeesX IS
  List_Sees(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListIncludesX IS
  List_Includes(Implementation(triple_case_while_while_i))==(?);
  Inherited_List_Includes(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListPromotesX IS
  List_Promotes(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListExtendsX IS
  List_Extends(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListVariablesX IS
  External_Context_List_Variables(Implementation(triple_case_while_while_i))==(?);
  Context_List_Variables(Implementation(triple_case_while_while_i))==(?);
  Abstract_List_Variables(Implementation(triple_case_while_while_i))==(?);
  Local_List_Variables(Implementation(triple_case_while_while_i))==(?);
  List_Variables(Implementation(triple_case_while_while_i))==(?);
  External_List_Variables(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListVisibleVariablesX IS
  Inherited_List_VisibleVariables(Implementation(triple_case_while_while_i))==(?);
  Abstract_List_VisibleVariables(Implementation(triple_case_while_while_i))==(?);
  External_List_VisibleVariables(Implementation(triple_case_while_while_i))==(?);
  Expanded_List_VisibleVariables(Implementation(triple_case_while_while_i))==(?);
  List_VisibleVariables(Implementation(triple_case_while_while_i))==(?);
  Internal_List_VisibleVariables(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListInvariantX IS
  Gluing_Seen_List_Invariant(Implementation(triple_case_while_while_i))==(btrue);
  Expanded_List_Invariant(Implementation(triple_case_while_while_i))==(btrue);
  Abstract_List_Invariant(Implementation(triple_case_while_while_i))==(btrue);
  Context_List_Invariant(Implementation(triple_case_while_while_i))==(btrue);
  List_Invariant(Implementation(triple_case_while_while_i))==(btrue)
END
&
THEORY ListAssertionsX IS
  Expanded_List_Assertions(Implementation(triple_case_while_while_i))==(btrue);
  Abstract_List_Assertions(Implementation(triple_case_while_while_i))==(btrue);
  Context_List_Assertions(Implementation(triple_case_while_while_i))==(btrue);
  List_Assertions(Implementation(triple_case_while_while_i))==(btrue)
END
&
THEORY ListCoverageX IS
  List_Coverage(Implementation(triple_case_while_while_i))==(btrue)
END
&
THEORY ListExclusivityX IS
  List_Exclusivity(Implementation(triple_case_while_while_i))==(btrue)
END
&
THEORY ListInitialisationX IS
  Expanded_List_Initialisation(Implementation(triple_case_while_while_i))==(skip);
  Context_List_Initialisation(Implementation(triple_case_while_while_i))==(skip);
  List_Initialisation(Implementation(triple_case_while_while_i))==(skip)
END
&
THEORY ListParametersX IS
  List_Parameters(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListInstanciatedParametersX END
&
THEORY ListConstraintsX IS
  List_Constraints(Implementation(triple_case_while_while_i))==(btrue);
  List_Context_Constraints(Implementation(triple_case_while_while_i))==(btrue)
END
&
THEORY ListOperationsX IS
  Internal_List_Operations(Implementation(triple_case_while_while_i))==(optriple_case_while_while);
  List_Operations(Implementation(triple_case_while_while_i))==(optriple_case_while_while)
END
&
THEORY ListInputX IS
  List_Input(Implementation(triple_case_while_while_i),optriple_case_while_while)==(xx,yy,zz)
END
&
THEORY ListOutputX IS
  List_Output(Implementation(triple_case_while_while_i),optriple_case_while_while)==(res1,res2,res3)
END
&
THEORY ListHeaderX IS
  List_Header(Implementation(triple_case_while_while_i),optriple_case_while_while)==(res1,res2,res3 <-- optriple_case_while_while(xx,yy,zz))
END
&
THEORY ListPreconditionX IS
  Own_Precondition(Implementation(triple_case_while_while_i),optriple_case_while_while)==(btrue);
  List_Precondition(Implementation(triple_case_while_while_i),optriple_case_while_while)==(xx: NAT & yy: NAT & zz: NAT)
END
&
THEORY ListSubstitutionX IS
  Expanded_List_Substitution(Implementation(triple_case_while_while_i),optriple_case_while_while)==(xx: NAT & yy: NAT & zz: NAT | @(ii,jj).(ii:=0;jj:=0;(ii: INT | res2:=ii);(jj: INT | res3:=jj);(not(xx = 1) & xx = 0 ==> ((xx: INT | res1:=xx);WHILE ii<yy DO WHILE jj<zz DO (jj+1: INT & jj: INT & 1: INT | res3:=jj+1);(jj+1: INT & jj: INT & 1: INT | jj:=jj+1) INVARIANT 0<=jj & jj<=zz & res3 = jj VARIANT zz-jj END;(ii+1: INT & ii: INT & 1: INT | res2:=ii+1);(ii+1: INT & ii: INT & 1: INT | ii:=ii+1) INVARIANT 0<=ii & ii<=yy & res2 = ii & 0<=jj & jj<=zz & res3 = jj & (ii>0 => res3 = zz) & (not(ii>0) => res3 = 0) VARIANT yy-ii END) [] not(xx = 0) & xx = 1 ==> ((xx: INT | res1:=xx);WHILE ii<yy DO WHILE jj<zz DO (jj+1: INT & jj: INT & 1: INT | res3:=jj+1);(jj+1: INT & jj: INT & 1: INT | jj:=jj+1) INVARIANT 0<=jj & jj<=zz & res3 = jj VARIANT zz-jj END;(ii+1: INT & ii: INT & 1: INT | res2:=ii+1);(ii+1: INT & ii: INT & 1: INT | ii:=ii+1) INVARIANT 0<=ii & ii<=yy & res2 = ii & 0<=jj & jj<=zz & res3 = jj & (ii>0 => res3 = zz) & (not(ii>0) => res3 = 0) VARIANT yy-ii END) [] not(xx = 0) & not(xx = 1) ==> ((xx: INT | res1:=xx);WHILE ii<yy DO WHILE jj<zz DO (jj+1: INT & jj: INT & 1: INT | res3:=jj+1);(jj+1: INT & jj: INT & 1: INT | jj:=jj+1) INVARIANT 0<=jj & jj<=zz & res3 = jj VARIANT zz-jj END;(ii+1: INT & ii: INT & 1: INT | res2:=ii+1);(ii+1: INT & ii: INT & 1: INT | ii:=ii+1) INVARIANT 0<=ii & ii<=yy & res2 = ii & 0<=jj & jj<=zz & res3 = jj & (ii>0 => res3 = zz) & (not(ii>0) => res3 = 0) VARIANT yy-ii END))));
  List_Substitution(Implementation(triple_case_while_while_i),optriple_case_while_while)==(VAR ii,jj IN ii:=0;jj:=0;res2:=ii;res3:=jj;CASE xx OF EITHER 0 THEN res1:=xx;WHILE ii<yy DO WHILE jj<zz DO res3:=jj+1;jj:=jj+1 INVARIANT 0<=jj & jj<=zz & res3 = jj VARIANT zz-jj END;res2:=ii+1;ii:=ii+1 INVARIANT 0<=ii & ii<=yy & res2 = ii & 0<=jj & jj<=zz & res3 = jj & (ii>0 => res3 = zz) & (not(ii>0) => res3 = 0) VARIANT yy-ii END OR 1 THEN res1:=xx;WHILE ii<yy DO WHILE jj<zz DO res3:=jj+1;jj:=jj+1 INVARIANT 0<=jj & jj<=zz & res3 = jj VARIANT zz-jj END;res2:=ii+1;ii:=ii+1 INVARIANT 0<=ii & ii<=yy & res2 = ii & 0<=jj & jj<=zz & res3 = jj & (ii>0 => res3 = zz) & (not(ii>0) => res3 = 0) VARIANT yy-ii END ELSE res1:=xx;WHILE ii<yy DO WHILE jj<zz DO res3:=jj+1;jj:=jj+1 INVARIANT 0<=jj & jj<=zz & res3 = jj VARIANT zz-jj END;res2:=ii+1;ii:=ii+1 INVARIANT 0<=ii & ii<=yy & res2 = ii & 0<=jj & jj<=zz & res3 = jj & (ii>0 => res3 = zz) & (not(ii>0) => res3 = 0) VARIANT yy-ii END END END END)
END
&
THEORY ListConstantsX IS
  List_Valuable_Constants(Implementation(triple_case_while_while_i))==(?);
  Inherited_List_Constants(Implementation(triple_case_while_while_i))==(?);
  List_Constants(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListSetsX IS
  Context_List_Enumerated(Implementation(triple_case_while_while_i))==(?);
  Context_List_Defered(Implementation(triple_case_while_while_i))==(?);
  Context_List_Sets(Implementation(triple_case_while_while_i))==(?);
  List_Own_Enumerated(Implementation(triple_case_while_while_i))==(?);
  List_Valuable_Sets(Implementation(triple_case_while_while_i))==(?);
  Inherited_List_Enumerated(Implementation(triple_case_while_while_i))==(?);
  Inherited_List_Defered(Implementation(triple_case_while_while_i))==(?);
  Inherited_List_Sets(Implementation(triple_case_while_while_i))==(?);
  List_Enumerated(Implementation(triple_case_while_while_i))==(?);
  List_Defered(Implementation(triple_case_while_while_i))==(?);
  List_Sets(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListHiddenConstantsX IS
  Abstract_List_HiddenConstants(Implementation(triple_case_while_while_i))==(?);
  Expanded_List_HiddenConstants(Implementation(triple_case_while_while_i))==(?);
  List_HiddenConstants(Implementation(triple_case_while_while_i))==(?);
  External_List_HiddenConstants(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListPropertiesX IS
  Abstract_List_Properties(Implementation(triple_case_while_while_i))==(btrue);
  Context_List_Properties(Implementation(triple_case_while_while_i))==(btrue);
  Inherited_List_Properties(Implementation(triple_case_while_while_i))==(btrue);
  List_Properties(Implementation(triple_case_while_while_i))==(btrue)
END
&
THEORY ListValuesX IS
  Values_Subs(Implementation(triple_case_while_while_i))==(aa: aa);
  List_Values(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListSeenInfoX END
&
THEORY ListIncludedOperationsX END
&
THEORY InheritedEnvX IS
  Operations(Implementation(triple_case_while_while_i))==(Type(optriple_case_while_while) == Cst(btype(INTEGER,?,?)*btype(INTEGER,?,?)*btype(INTEGER,?,?),btype(INTEGER,?,?)*btype(INTEGER,?,?)*btype(INTEGER,?,?)))
END
&
THEORY ListVisibleStaticX END
&
THEORY ListOfIdsX IS
  List_Of_Ids(Implementation(triple_case_while_while_i)) == (? | ? | ? | ? | optriple_case_while_while | ? | ? | ? | triple_case_while_while_i);
  List_Of_HiddenCst_Ids(Implementation(triple_case_while_while_i)) == (? | ?);
  List_Of_VisibleCst_Ids(Implementation(triple_case_while_while_i)) == (?);
  List_Of_VisibleVar_Ids(Implementation(triple_case_while_while_i)) == (? | ?);
  List_Of_Ids_SeenBNU(Implementation(triple_case_while_while_i)) == (?: ?)
END
&
THEORY VariablesLocEnvX IS
  Variables_Loc(Implementation(triple_case_while_while_i),optriple_case_while_while, 1) == (Type(ii) == Lvl(btype(INTEGER,?,?));Type(jj) == Lvl(btype(INTEGER,?,?)))
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
&
THEORY ListLocalOperationsX IS
  List_Local_Operations(Implementation(triple_case_while_while_i))==(?)
END
&
THEORY ListLocalInputX END
&
THEORY ListLocalOutputX END
&
THEORY ListLocalHeaderX END
&
THEORY ListLocalPreconditionX END
&
THEORY ListLocalSubstitutionX END
&
THEORY TypingPredicateX IS
  TypingPredicate(Implementation(triple_case_while_while_i))==(btrue)
END
&
THEORY ImportedVariablesListX END
&
THEORY ListLocalOpInvariantX END
)
