/* triple_else_else_else
 * Author: Diego Oliveira
 * Creation date: 04/11/2016
 */
MACHINE
    triple_else_else_else

OPERATIONS
    res1, res2, res3 <-- optriple_else_else_else(xx, yy, zz)=
    PRE xx : NAT & yy : NAT & zz : NAT
    THEN
        IF xx < 5 THEN
            IF yy < 5 THEN
                IF zz < 5 THEN
                    res1 := 0 || res2 := 0 || res3 := 0
                ELSE
                    res1 := 0 || res2 := 0 || res3 := zz
                END
            ELSE
                IF zz < 5 THEN
                    res1 := 0 || res2 := yy || res3 := 0
                ELSE
                    res1 := 0 || res2 := yy || res3 := zz
                END
            END
        ELSE
           IF yy < 5 THEN
                IF zz < 5 THEN
                    res1 := xx || res2 := 0 || res3 := 0
                ELSE
                    res1 := xx || res2 := 0 || res3 := zz
                END
            ELSE
                IF zz < 5 THEN
                    res1 := xx || res2 := yy || res3 := 0
                ELSE
                    res1 := xx || res2 := yy || res3 := zz
                END
            END
        END
    END
END
