
(define (domain gripper)

(:types 
   room - object
   gripper - object
)

(:predicates ;
   (pos_robby ?r -room)
   (free ?g -gripper)
   )


(:functions 
   (balls_num ?r -room)
)

   (:action move
       :parameters  (?from ?to - room)
       :precondition (and  (pos_robby ?from))
       :effect (and  (pos_robby ?to)
		     (not (pos_robby ?from))))

   (:action pick
       :parameters (?r -room ?gripper -gripper)
       :precondition  (and (>= (balls_num ?r) 1)
			    (pos_robby ?r) (free ?gripper))
       :effect (and
		    (not (free ?gripper))
		    (decrease (balls_num ?r) 1)))

   (:action drop
       :parameters   ( ?r -room ?gripper -gripper)
       :precondition  (and 
			    (not (free ?gripper)) (pos_robby ?r))
       :effect (and 
		    (free ?gripper)
		    (increase (balls_num ?r) 1)))
)




