#include <stdio.h>
#include <stdlib.h>

#include "runTest_CLAUSE_NONDET_MCH_CASE.h"

int main(int argc, char **argv)
{
    bool result;
    runTest_CLAUSE_NONDET_MCH_CASE__testAll(&result);
    if (result == true){
<<<<<<< HEAD
        printf("The translation of the implementation Arm is well performed and achieved Clause Coverage");
=======
        printf("The translation of the implementation IMP_OC_NONDET_MCH_CASE is well performed and achievedClause Coverage");
>>>>>>> origin/coverage
    }
    else{
        printf("The translation of the implementation IMP_OC_NONDET_MCH_CASE is NOT well performed");    
    }
    return 0;
}