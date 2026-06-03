(define (problem p_3_20) (:domain gripper)
(:objects 
   g1 g2 - gripper
   r1 r2 r3 - room
)

(:init
   (= (balls_num r1) 20)
   (= (balls_num r2) 0)
   (= (balls_num r3) 0)
   (pos_robby r2)
   (free g1)
   (free g2)
)

(:goal (and
   (= (balls_num r2) 10)
   (= (balls_num r3) 10)
))

)