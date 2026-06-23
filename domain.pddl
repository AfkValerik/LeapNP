(define (domain instance_12_3-domain)
(:requirements  :strips :typing :numeric-fluents)
(:functions   (max_int)
  (value_c0)
  (value_c1)
  (value_c2)
  (value_c3)
  (value_c4)
  (value_c5)
  (value_c6)
  (value_c7)
  (value_c8)
  (value_c9)
  (value_c10)
  (value_c11)
)
(:action decrement__c9
	:parameters ()
	:precondition (and (>= (+ (*   (value_c9) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c9) 1.0)
))
(:action decrement__c7
	:parameters ()
	:precondition (and (>= (+ (*   (value_c7) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c7) 1.0)
))
(:action decrement__c8
	:parameters ()
	:precondition (and (>= (+ (*   (value_c8) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c8) 1.0)
))
(:action decrement__c5
	:parameters ()
	:precondition (and (>= (+ (*   (value_c5) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c5) 1.0)
))
(:action decrement__c6
	:parameters ()
	:precondition (and (>= (+ (*   (value_c6) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c6) 1.0)
))
(:action decrement__c4
	:parameters ()
	:precondition (and (>= (+ (*   (value_c4) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c4) 1.0)
))
(:action decrement__c1
	:parameters ()
	:precondition (and (>= (+ (*   (value_c1) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c1) 1.0)
))
(:action decrement__c2
	:parameters ()
	:precondition (and (>= (+ (*   (value_c2) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c2) 1.0)
))
(:action decrement__c0
	:parameters ()
	:precondition (and (>= (+ (*   (value_c0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c0) 1.0)
))
(:action increment__c11
	:parameters ()
	:precondition (and (>= (+ (*   (value_c11) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c11) 1.0)
))
(:action increment__c7
	:parameters ()
	:precondition (and (>= (+ (*   (value_c7) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c7) 1.0)
))
(:action increment__c8
	:parameters ()
	:precondition (and (>= (+ (*   (value_c8) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c8) 1.0)
))
(:action decrement__c11
	:parameters ()
	:precondition (and (>= (+ (*   (value_c11) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c11) 1.0)
))
(:action increment__c9
	:parameters ()
	:precondition (and (>= (+ (*   (value_c9) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c9) 1.0)
))
(:action increment__c10
	:parameters ()
	:precondition (and (>= (+ (*   (value_c10) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c10) 1.0)
))
(:action increment__c3
	:parameters ()
	:precondition (and (>= (+ (*   (value_c3) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c3) 1.0)
))
(:action increment__c4
	:parameters ()
	:precondition (and (>= (+ (*   (value_c4) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c4) 1.0)
))
(:action increment__c5
	:parameters ()
	:precondition (and (>= (+ (*   (value_c5) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c5) 1.0)
))
(:action increment__c6
	:parameters ()
	:precondition (and (>= (+ (*   (value_c6) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c6) 1.0)
))
(:action increment__c0
	:parameters ()
	:precondition (and (>= (+ (*   (value_c0) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c0) 1.0)
))
(:action increment__c1
	:parameters ()
	:precondition (and (>= (+ (*   (value_c1) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c1) 1.0)
))
(:action increment__c2
	:parameters ()
	:precondition (and (>= (+ (*   (value_c2) -1.0) 23.0 ) 0.0))
	:effect (and 
			(increase (value_c2) 1.0)
))
(:action decrement__c10
	:parameters ()
	:precondition (and (>= (+ (*   (value_c10) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c10) 1.0)
))
(:action decrement__c3
	:parameters ()
	:precondition (and (>= (+ (*   (value_c3) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (value_c3) 1.0)
))


)