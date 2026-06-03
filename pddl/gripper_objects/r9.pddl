(define (problem problem_name) (:domain domain_name)
(:objects 
   g1 g2 - gripper
   r1 r2 r3 r4 r5 r6 r7 r8 r9 - room
)

(:init
   (= (balls_num r1) 20)
   (= (balls_num r2) 0)
   (= (balls_num r3) 0)
   (= (balls_num r4) 0)
   (= (balls_num r5) 0)
   (= (balls_num r6) 0)
   (= (balls_num r7) 0)
   (= (balls_num r8) 0)
   (= (balls_num r9) 0)
   (pos_robby r2)
   (free g1)
   (free g2)
)

(:goal (and
   (= (balls_num r2) 3)
   (= (balls_num r3) 3)
   (= (balls_num r4) 3)
   (= (balls_num r5) 3)
   (= (balls_num r6) 2)
   (= (balls_num r7) 2)
   (= (balls_num r8) 2)
   (= (balls_num r9) 2)
))

)
