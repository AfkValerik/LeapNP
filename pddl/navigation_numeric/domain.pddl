(define (domain navigation-numeric)
    (:requirements :typing :fluents :negative-preconditions :disjunctive-preconditions)
    (:types thing - object
        agent rock - thing)


    (:functions
        (maxx) ;; bounds
        (maxy) ;; bounds
        (miny) ;; bounds
        (minx) ;; bounds
        (x ?t - thing) ;; x coordinate of the location for ?t
        (y ?t - thing) ;; y coordinate of the location for ?t
        (xend ?r - rock)
        (yend ?r - rock)
        
    )

    ;; Move an agent to a neighboring location
    (:action move_up
     :parameters (?a - agent)
     :precondition (and (<= (+ (y ?a) 1) (maxy))
        (forall (?r - rock) (or (>= (x ?a) (xend ?r))
                                (<= (x ?a) (x ?r))
                                (>= (+ (y ?a) 1) (yend ?r))
                                (<= (+ (y ?a) 1) (y ?r))))) ;; rocks are not allowed to be in the same location as the agent
     :effect (and
    		(increase (y ?a) 1)))

    (:action move_down
     :parameters (?a - agent)
     :precondition (and (>= (- (y ?a) 1) (miny))
        (forall (?r - rock) (or  (>= (x ?a) (xend ?r))
                                (<= (x ?a) (x ?r))
                                (>= (- (y ?a) 1) (yend ?r))
                                (<= (- (y ?a) 1) (y ?r)))))
     :effect (and
    		(decrease (y ?a) 1)))

    (:action move_right
     :parameters (?a - agent)
     :precondition (and (<= (+ (x ?a) 1) (maxx))
        (forall (?r - rock) (or (>= (+ (x ?a) 1) (xend ?r))
                                (<= (+ (x ?a) 1) (x ?r))
                                (>= (y ?a) (yend ?r))
                                (<= (y ?a) (y ?r)))))
     :effect (and
    		(increase (x ?a) 1)))

    (:action move_left
     :parameters (?a - agent)
     :precondition (and (>= (- (x ?a) 1) (minx))
                (forall (?r - rock) (or (>= (- (x ?a) 1) (xend ?r))
                                 (<= (- (x ?a) 1) (x ?r))
                                 (>= (y ?a) (yend ?r))
                                 (<= (y ?a) (y ?r)))))
     :effect (and
    		(decrease (x ?a) 1)))

  
    
)
