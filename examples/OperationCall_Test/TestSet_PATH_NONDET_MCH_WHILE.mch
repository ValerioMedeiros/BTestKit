MACHINE
    TestSet_PATH_NONDET_MCH_WHILE

OPERATIONS
    verdict <-- TEST_0_opNONDET_MCH_WHILE =
        ANY kk WHERE kk : BOOL THEN verdict := kk END;

    verdict <-- TEST_1_opNONDET_MCH_WHILE =
        ANY kk WHERE kk : BOOL THEN verdict := kk END
END