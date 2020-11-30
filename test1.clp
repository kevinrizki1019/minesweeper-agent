(deffacts bomb
    (is-bomb 2 0)
)

(defrule B1
    (not-bomb 2 0)
=>
    (assert (is-bomb 2 2))
    (assert (is-bomb 1 2))
)

(defrule B2
    (not-bomb 2 2)
=>
    (assert (is-bomb 2 0))
    (assert (is-bomb 1 2))
)

(defrule B3
    (not-bomb 1 2)
=>
    (assert (is-bomb 2 2))
    (assert (is-bomb 2 0))
)