(define (problem problem_name) (:domain domain_name)
(:objects 
   g1 g2 - gripper
   r1 r2 - room
)

(:init
   (= (balls_num r1) 80)
   (= (balls_num r2) 0)
   (pos_robby r2)
   (free g1)
   (free g2)
)

(:goal (and
   (= (balls_num r2) 80)
))

)
