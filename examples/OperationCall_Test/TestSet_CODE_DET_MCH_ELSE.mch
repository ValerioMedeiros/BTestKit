MACHINE
    TestSet_CODE_DET_MCH_ELSE

OPERATIONS
    verdict <-- TEST_0_opDET_MCH_ELSE =
        ANY kk WHERE kk : BOOL THEN verdict := kk END;

    verdict <-- TEST_1_opDET_MCH_ELSE =
        ANY kk WHERE kk : BOOL THEN verdict := kk END
END