(define (problem problem_name) (:domain domain_name)
(:objects 
   g1 g2 - gripper
   r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 - room
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
   (= (balls_num r10) 0)
   (= (balls_num r11) 0)
   (pos_robby r2)
   (free g1)
   (free g2)
)

(:goal (and
   (= (balls_num r2) 2)
   (= (balls_num r3) 2)
   (= (balls_num r4) 2)
   (= (balls_num r5) 2)
   (= (balls_num r6) 2)
   (= (balls_num r7) 2)
   (= (balls_num r8) 2)
   (= (balls_num r9) 2)
   (= (balls_num r10) 2)
   (= (balls_num r11) 2)
))

)
