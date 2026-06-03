(define (problem problem_name) (:domain domain_name)
(:objects 
   g1 g2 - gripper
   r1 r2 r3 r4 r5 r6 r7 - room
)

(:init
   (= (balls_num r1) 20)
   (= (balls_num r2) 0)
   (= (balls_num r3) 0)
   (= (balls_num r4) 0)
   (= (balls_num r5) 0)
   (= (balls_num r6) 0)
   (= (balls_num r7) 0)
   (pos_robby r2)
   (free g1)
   (free g2)
)

(:goal (and
   (= (balls_num r2) 5)
   (= (balls_num r3) 5)
   (= (balls_num r4) 3)
   (= (balls_num r5) 3)
   (= (balls_num r6) 2)
   (= (balls_num r7) 2)
))

)
