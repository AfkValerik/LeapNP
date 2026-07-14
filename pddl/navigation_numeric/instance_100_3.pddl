(define (problem instance_100_3)
  (:domain navigation-numeric)
  (:objects
    rock1 rock2 rock3 - rock
	agent1 - agent
  )

  (:init
	(= (maxx) 100)
	(= (minx) 1)
	(= (maxy) 100)
	(= (miny) 1)
	(= (x agent1) 50)
	(= (y agent1) 5)
	(= (x rock1) 3)
	(= (y rock1) 2)
	(= (xend rock1) 90)
	(= (yend rock1) 2)
	(= (x rock2) 2)
	(= (y rock2) 2)
	(= (xend rock2) 2)
	(= (yend rock2) 90)
	(= (x rock3) 91)
	(= (y rock3) 2)
	(= (xend rock3) 91)
	(= (yend rock3) 90)


  )

  (:goal (and 
    (>= (x agent1) 45)
    (<= (x agent1) 55)
	(>= (y agent1) 1)
	(<= (y agent1) 10)
  ))

  
  

  
)