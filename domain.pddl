(define (domain power1-domain)
(:requirements  :strips :typing :numeric-fluents)
(:predicates  (timenow_t0000)
 (timenow_t0030)
 (timenow_t0100)
 (timenow_t0130)
 (timenow_t0200)
 (timenow_t0230)
 (timenow_t0300)
 (timenow_t0330)
 (timenow_t0400)
 (timenow_t0430)
 (timenow_t0500)
 (timenow_t0530)
 (timenow_t0600)
 (timenow_t0630)
 (timenow_t0700)
 (timenow_t0730)
 (timenow_t0800)
 (timenow_t0830)
 (timenow_t0900)
 (timenow_t0930)
 (timenow_t1000)
 (timenow_t1030)
 (timenow_t1100)
 (timenow_t1130)
 (timenow_t1200)
 (timenow_t1230)
 (timenow_t1300)
 (timenow_t1330)
 (timenow_t1400)
 (timenow_t1430)
 (timenow_t1500)
 (timenow_t1530)
 (timenow_t1600)
 (timenow_t1630)
 (timenow_t1700)
 (timenow_t1730)
 (timenow_t1800)
 (timenow_t1830)
 (timenow_t1900)
 (timenow_t1930)
 (timenow_t2000)
 (timenow_t2030)
 (timenow_t2100)
 (timenow_t2130)
 (timenow_t2200)
 (timenow_t2230)
 (timenow_t2300)
 (timenow_t2330)
 (timenow_t2400)
)
(:functions   (value_n13)
  (value_n14)
  (value_n15)
  (value_n16)
  (value_n17)
  (value_n18)
  (value_n19)
  (value_n20)
  (value_n21)
  (value_n22)
  (value_n23)
  (value_n24)
  (value_n25)
  (value_n26)
  (stored_units_s0)
  (stored_capacity_s0)
  (funds_s0)
  (objective_s0)
  (value_n0)
  (value_n1)
  (value_n2)
  (value_n3)
  (value_n4)
  (value_n5)
  (value_n6)
  (value_n7)
  (value_n8)
  (value_n9)
  (value_n10)
  (value_n11)
  (value_n12)
)
(:action pump_water_up__t0000__n7__s0
	:parameters ()
	:precondition (and (>= (+ (*   (funds_s0) 1.0) -7.34999942779541 ) 0.0)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t0000))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 7.34999942779541)
))
(:action advance_time__t0000__t0030
	:parameters ()
	:precondition (and  (timenow_t0000))
	:effect (and 
			(not (timenow_t0000))			(timenow_t0030)
))
(:action advance_time__t0030__t0100
	:parameters ()
	:precondition (and  (timenow_t0030))
	:effect (and 
			(timenow_t0100)			(not (timenow_t0030))
))
(:action pump_water_up__t0030__n7__s0
	:parameters ()
	:precondition (and (>= (+ (*   (funds_s0) 1.0) -7.34999942779541 ) 0.0)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t0030))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 7.34999942779541)
))
(:action generate__t0030__n7__s0
	:parameters ()
	:precondition (and  (timenow_t0030)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 7.0)
))
(:action generate__t0000__n7__s0
	:parameters ()
	:precondition (and  (timenow_t0000)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 7.0)
))
(:action generate__t0100__n7__s0
	:parameters ()
	:precondition (and  (timenow_t0100)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 7.0)
))
(:action advance_time__t0100__t0130
	:parameters ()
	:precondition (and  (timenow_t0100))
	:effect (and 
			(timenow_t0130)			(not (timenow_t0100))
))
(:action pump_water_up__t0100__n7__s0
	:parameters ()
	:precondition (and  (timenow_t0100)(>= (+ (*   (funds_s0) 1.0) -7.34999942779541 ) 0.0)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 7.34999942779541)
))
(:action pump_water_up__t0130__n6__s0
	:parameters ()
	:precondition (and  (timenow_t0130)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -6.299999713897705 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 6.299999713897705)
))
(:action advance_time__t0130__t0200
	:parameters ()
	:precondition (and  (timenow_t0130))
	:effect (and 
			(timenow_t0200)			(not (timenow_t0130))
))
(:action generate__t0130__n6__s0
	:parameters ()
	:precondition (and  (timenow_t0130)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 6.0)			(decrease (stored_units_s0) 1.0)
))
(:action pump_water_up__t0200__n6__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -6.299999713897705 ) 0.0) (timenow_t0200))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 6.299999713897705)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t0200__t0230
	:parameters ()
	:precondition (and  (timenow_t0200))
	:effect (and 
			(timenow_t0230)			(not (timenow_t0200))
))
(:action generate__t0200__n6__s0
	:parameters ()
	:precondition (and  (timenow_t0200)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 6.0)			(decrease (stored_units_s0) 1.0)
))
(:action generate__t0230__n6__s0
	:parameters ()
	:precondition (and  (timenow_t0230)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 6.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t0230__t0300
	:parameters ()
	:precondition (and  (timenow_t0230))
	:effect (and 
			(timenow_t0300)			(not (timenow_t0230))
))
(:action pump_water_up__t0230__n6__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -6.299999713897705 ) 0.0) (timenow_t0230))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 6.299999713897705)
))
(:action generate__t0300__n5__s0
	:parameters ()
	:precondition (and  (timenow_t0300)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (funds_s0) 5.0)			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t0300__t0330
	:parameters ()
	:precondition (and  (timenow_t0300))
	:effect (and 
			(timenow_t0330)			(not (timenow_t0300))
))
(:action pump_water_up__t0300__n5__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -5.25 ) 0.0) (timenow_t0300))
	:effect (and 
			(decrease (funds_s0) 5.25)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action pump_water_up__t0330__n4__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -4.199999809265137 ) 0.0) (timenow_t0330))
	:effect (and 
			(decrease (funds_s0) 4.199999809265137)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t0330__n4__s0
	:parameters ()
	:precondition (and  (timenow_t0330)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 4.0)
))
(:action advance_time__t0330__t0400
	:parameters ()
	:precondition (and  (timenow_t0330))
	:effect (and 
			(timenow_t0400)			(not (timenow_t0330))
))
(:action generate__t0400__n3__s0
	:parameters ()
	:precondition (and  (timenow_t0400)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 3.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t0400__t0430
	:parameters ()
	:precondition (and  (timenow_t0400))
	:effect (and 
			(not (timenow_t0400))			(timenow_t0430)
))
(:action pump_water_up__t0400__n3__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -3.1499998569488525 ) 0.0) (timenow_t0400))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 3.1499998569488525)
))
(:action advance_time__t0430__t0500
	:parameters ()
	:precondition (and  (timenow_t0430))
	:effect (and 
			(timenow_t0500)			(not (timenow_t0430))
))
(:action generate__t0430__n3__s0
	:parameters ()
	:precondition (and  (timenow_t0430)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 3.0)			(decrease (stored_units_s0) 1.0)
))
(:action pump_water_up__t0430__n3__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -3.1499998569488525 ) 0.0) (timenow_t0430))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 3.1499998569488525)
))
(:action advance_time__t0500__t0530
	:parameters ()
	:precondition (and  (timenow_t0500))
	:effect (and 
			(timenow_t0530)			(not (timenow_t0500))
))
(:action pump_water_up__t0500__n4__s0
	:parameters ()
	:precondition (and  (timenow_t0500)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -4.199999809265137 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 4.199999809265137)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t0500__n4__s0
	:parameters ()
	:precondition (and  (timenow_t0500)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 4.0)
))
(:action pump_water_up__t0530__n5__s0
	:parameters ()
	:precondition (and  (timenow_t0530)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -5.25 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 5.25)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t0530__t0600
	:parameters ()
	:precondition (and  (timenow_t0530))
	:effect (and 
			(timenow_t0600)			(not (timenow_t0530))
))
(:action generate__t0530__n5__s0
	:parameters ()
	:precondition (and  (timenow_t0530)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (funds_s0) 5.0)			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)
))
(:action generate__t0600__n9__s0
	:parameters ()
	:precondition (and  (timenow_t0600)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 9.0)
))
(:action advance_time__t0600__t0630
	:parameters ()
	:precondition (and  (timenow_t0600))
	:effect (and 
			(timenow_t0630)			(not (timenow_t0600))
))
(:action pump_water_up__t0600__n9__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t0600)(>= (+ (*   (funds_s0) 1.0) -9.449999809265137 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 9.449999809265137)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t0630__n13__s0
	:parameters ()
	:precondition (and  (timenow_t0630)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (funds_s0) 13.0)			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t0630__t0700
	:parameters ()
	:precondition (and  (timenow_t0630))
	:effect (and 
			(timenow_t0700)			(not (timenow_t0630))
))
(:action pump_water_up__t0630__n13__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t0630)(>= (+ (*   (funds_s0) 1.0) -13.649999618530273 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 13.649999618530273)
))
(:action pump_water_up__t0700__n18__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t0700)(>= (+ (*   (funds_s0) 1.0) -18.899999618530273 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 18.899999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t0700__t0730
	:parameters ()
	:precondition (and  (timenow_t0700))
	:effect (and 
			(timenow_t0730)			(not (timenow_t0700))
))
(:action generate__t0700__n18__s0
	:parameters ()
	:precondition (and  (timenow_t0700)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 18.0)
))
(:action pump_water_up__t0730__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t0730)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t0730__n19__s0
	:parameters ()
	:precondition (and  (timenow_t0730)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action advance_time__t0730__t0800
	:parameters ()
	:precondition (and  (timenow_t0730))
	:effect (and 
			(timenow_t0800)			(not (timenow_t0730))
))
(:action generate__t0800__n19__s0
	:parameters ()
	:precondition (and  (timenow_t0800)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action advance_time__t0800__t0830
	:parameters ()
	:precondition (and  (timenow_t0800))
	:effect (and 
			(not (timenow_t0800))			(timenow_t0830)
))
(:action pump_water_up__t0800__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0) (timenow_t0800))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t0830__t0900
	:parameters ()
	:precondition (and  (timenow_t0830))
	:effect (and 
			(timenow_t0900)			(not (timenow_t0830))
))
(:action pump_water_up__t0830__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0) (timenow_t0830))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t0830__n19__s0
	:parameters ()
	:precondition (and  (timenow_t0830)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action advance_time__t0900__t0930
	:parameters ()
	:precondition (and  (timenow_t0900))
	:effect (and 
			(timenow_t0930)			(not (timenow_t0900))
))
(:action pump_water_up__t0900__n19__s0
	:parameters ()
	:precondition (and  (timenow_t0900)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t0900__n19__s0
	:parameters ()
	:precondition (and  (timenow_t0900)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action pump_water_up__t0930__n19__s0
	:parameters ()
	:precondition (and  (timenow_t0930)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t0930__t1000
	:parameters ()
	:precondition (and  (timenow_t0930))
	:effect (and 
			(timenow_t1000)			(not (timenow_t0930))
))
(:action generate__t0930__n19__s0
	:parameters ()
	:precondition (and  (timenow_t0930)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action advance_time__t1000__t1030
	:parameters ()
	:precondition (and  (timenow_t1000))
	:effect (and 
			(timenow_t1030)			(not (timenow_t1000))
))
(:action generate__t1000__n19__s0
	:parameters ()
	:precondition (and  (timenow_t1000)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action pump_water_up__t1000__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1000)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1030__n19__s0
	:parameters ()
	:precondition (and  (timenow_t1030)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action pump_water_up__t1030__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1030)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1030__t1100
	:parameters ()
	:precondition (and  (timenow_t1030))
	:effect (and 
			(timenow_t1100)			(not (timenow_t1030))
))
(:action pump_water_up__t1100__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1100)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1100__t1130
	:parameters ()
	:precondition (and  (timenow_t1100))
	:effect (and 
			(timenow_t1130)			(not (timenow_t1100))
))
(:action generate__t1100__n19__s0
	:parameters ()
	:precondition (and  (timenow_t1100)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action pump_water_up__t1130__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1130)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1130__n19__s0
	:parameters ()
	:precondition (and  (timenow_t1130)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action advance_time__t1130__t1200
	:parameters ()
	:precondition (and  (timenow_t1130))
	:effect (and 
			(timenow_t1200)			(not (timenow_t1130))
))
(:action generate__t1200__n19__s0
	:parameters ()
	:precondition (and  (timenow_t1200)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action advance_time__t1200__t1230
	:parameters ()
	:precondition (and  (timenow_t1200))
	:effect (and 
			(not (timenow_t1200))			(timenow_t1230)
))
(:action pump_water_up__t1200__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0) (timenow_t1200))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1230__t1300
	:parameters ()
	:precondition (and  (timenow_t1230))
	:effect (and 
			(timenow_t1300)			(not (timenow_t1230))
))
(:action pump_water_up__t1230__n18__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -18.899999618530273 ) 0.0) (timenow_t1230))
	:effect (and 
			(decrease (funds_s0) 18.899999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1230__n18__s0
	:parameters ()
	:precondition (and  (timenow_t1230)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 18.0)
))
(:action advance_time__t1300__t1330
	:parameters ()
	:precondition (and  (timenow_t1300))
	:effect (and 
			(timenow_t1330)			(not (timenow_t1300))
))
(:action pump_water_up__t1300__n18__s0
	:parameters ()
	:precondition (and  (timenow_t1300)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -18.899999618530273 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 18.899999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1300__n18__s0
	:parameters ()
	:precondition (and  (timenow_t1300)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 18.0)
))
(:action pump_water_up__t1330__n18__s0
	:parameters ()
	:precondition (and  (timenow_t1330)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -18.899999618530273 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 18.899999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1330__n18__s0
	:parameters ()
	:precondition (and  (timenow_t1330)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 18.0)
))
(:action advance_time__t1330__t1400
	:parameters ()
	:precondition (and  (timenow_t1330))
	:effect (and 
			(timenow_t1400)			(not (timenow_t1330))
))
(:action generate__t1400__n18__s0
	:parameters ()
	:precondition (and  (timenow_t1400)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 18.0)
))
(:action advance_time__t1400__t1430
	:parameters ()
	:precondition (and  (timenow_t1400))
	:effect (and 
			(timenow_t1430)			(not (timenow_t1400))
))
(:action pump_water_up__t1400__n18__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1400)(>= (+ (*   (funds_s0) 1.0) -18.899999618530273 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 18.899999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1430__t1500
	:parameters ()
	:precondition (and  (timenow_t1430))
	:effect (and 
			(timenow_t1500)			(not (timenow_t1430))
))
(:action pump_water_up__t1430__n18__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1430)(>= (+ (*   (funds_s0) 1.0) -18.899999618530273 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 18.899999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1430__n18__s0
	:parameters ()
	:precondition (and  (timenow_t1430)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 18.0)
))
(:action pump_water_up__t1500__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1500)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1500__t1530
	:parameters ()
	:precondition (and  (timenow_t1500))
	:effect (and 
			(timenow_t1530)			(not (timenow_t1500))
))
(:action generate__t1500__n19__s0
	:parameters ()
	:precondition (and  (timenow_t1500)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action pump_water_up__t1530__n20__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1530)(>= (+ (*   (funds_s0) 1.0) -21.0 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 21.0)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1530__n20__s0
	:parameters ()
	:precondition (and  (timenow_t1530)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (funds_s0) 20.0)			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t1530__t1600
	:parameters ()
	:precondition (and  (timenow_t1530))
	:effect (and 
			(timenow_t1600)			(not (timenow_t1530))
))
(:action pump_water_up__t1600__n23__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1600)(>= (+ (*   (funds_s0) 1.0) -24.149999618530273 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 24.149999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1600__t1630
	:parameters ()
	:precondition (and  (timenow_t1600))
	:effect (and 
			(not (timenow_t1600))			(timenow_t1630)
))
(:action generate__t1600__n23__s0
	:parameters ()
	:precondition (and  (timenow_t1600)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 23.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t1630__t1700
	:parameters ()
	:precondition (and  (timenow_t1630))
	:effect (and 
			(timenow_t1700)			(not (timenow_t1630))
))
(:action pump_water_up__t1630__n25__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -26.249998092651367 ) 0.0) (timenow_t1630))
	:effect (and 
			(decrease (funds_s0) 26.249998092651367)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1630__n25__s0
	:parameters ()
	:precondition (and  (timenow_t1630)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 25.0)
))
(:action advance_time__t1700__t1730
	:parameters ()
	:precondition (and  (timenow_t1700))
	:effect (and 
			(timenow_t1730)			(not (timenow_t1700))
))
(:action pump_water_up__t1700__n26__s0
	:parameters ()
	:precondition (and  (timenow_t1700)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -27.299999237060547 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 27.299999237060547)
))
(:action generate__t1700__n26__s0
	:parameters ()
	:precondition (and  (timenow_t1700)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (funds_s0) 26.0)			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t1730__t1800
	:parameters ()
	:precondition (and  (timenow_t1730))
	:effect (and 
			(timenow_t1800)			(not (timenow_t1730))
))
(:action generate__t1730__n25__s0
	:parameters ()
	:precondition (and  (timenow_t1730)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 25.0)
))
(:action pump_water_up__t1730__n25__s0
	:parameters ()
	:precondition (and  (timenow_t1730)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -26.249998092651367 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 26.249998092651367)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1800__t1830
	:parameters ()
	:precondition (and  (timenow_t1800))
	:effect (and 
			(timenow_t1830)			(not (timenow_t1800))
))
(:action pump_water_up__t1800__n24__s0
	:parameters ()
	:precondition (and (>= (+ (*   (funds_s0) 1.0) -25.19999885559082 ) 0.0)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1800))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 25.19999885559082)
))
(:action generate__t1800__n24__s0
	:parameters ()
	:precondition (and  (timenow_t1800)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 24.0)			(decrease (stored_units_s0) 1.0)
))
(:action pump_water_up__t1830__n22__s0
	:parameters ()
	:precondition (and (>= (+ (*   (funds_s0) 1.0) -23.099998474121094 ) 0.0)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1830))
	:effect (and 
			(decrease (funds_s0) 23.099998474121094)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1830__n22__s0
	:parameters ()
	:precondition (and  (timenow_t1830)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 22.0)
))
(:action advance_time__t1830__t1900
	:parameters ()
	:precondition (and  (timenow_t1830))
	:effect (and 
			(timenow_t1900)			(not (timenow_t1830))
))
(:action generate__t1900__n21__s0
	:parameters ()
	:precondition (and  (timenow_t1900)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 21.0)			(decrease (stored_units_s0) 1.0)
))
(:action pump_water_up__t1900__n21__s0
	:parameters ()
	:precondition (and (>= (+ (*   (funds_s0) 1.0) -22.049999237060547 ) 0.0)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1900))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 22.049999237060547)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t1900__t1930
	:parameters ()
	:precondition (and  (timenow_t1900))
	:effect (and 
			(timenow_t1930)			(not (timenow_t1900))
))
(:action pump_water_up__t1930__n20__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t1930)(>= (+ (*   (funds_s0) 1.0) -21.0 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 21.0)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t1930__n20__s0
	:parameters ()
	:precondition (and  (timenow_t1930)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (funds_s0) 20.0)			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t1930__t2000
	:parameters ()
	:precondition (and  (timenow_t1930))
	:effect (and 
			(timenow_t2000)			(not (timenow_t1930))
))
(:action generate__t2000__n19__s0
	:parameters ()
	:precondition (and  (timenow_t2000)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 19.0)
))
(:action pump_water_up__t2000__n19__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -19.94999885559082 ) 0.0) (timenow_t2000))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (funds_s0) 19.94999885559082)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t2000__t2030
	:parameters ()
	:precondition (and  (timenow_t2000))
	:effect (and 
			(not (timenow_t2000))			(timenow_t2030)
))
(:action advance_time__t2030__t2100
	:parameters ()
	:precondition (and  (timenow_t2030))
	:effect (and 
			(timenow_t2100)			(not (timenow_t2030))
))
(:action pump_water_up__t2030__n18__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -18.899999618530273 ) 0.0) (timenow_t2030))
	:effect (and 
			(decrease (funds_s0) 18.899999618530273)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t2030__n18__s0
	:parameters ()
	:precondition (and  (timenow_t2030)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 18.0)
))
(:action advance_time__t2100__t2130
	:parameters ()
	:precondition (and  (timenow_t2100))
	:effect (and 
			(timenow_t2130)			(not (timenow_t2100))
))
(:action pump_water_up__t2100__n16__s0
	:parameters ()
	:precondition (and  (timenow_t2100)(>= (+ (*   (funds_s0) 1.0) -16.799999237060547 ) 0.0)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(decrease (funds_s0) 16.799999237060547)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action generate__t2100__n16__s0
	:parameters ()
	:precondition (and  (timenow_t2100)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 16.0)
))
(:action advance_time__t2130__t2200
	:parameters ()
	:precondition (and  (timenow_t2130))
	:effect (and 
			(timenow_t2200)			(not (timenow_t2130))
))
(:action pump_water_up__t2130__n14__s0
	:parameters ()
	:precondition (and  (timenow_t2130)(>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -14.69999885559082 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 14.69999885559082)
))
(:action generate__t2130__n14__s0
	:parameters ()
	:precondition (and  (timenow_t2130)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 14.0)
))
(:action pump_water_up__t2200__n12__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0) (timenow_t2200)(>= (+ (*   (funds_s0) 1.0) -12.59999942779541 ) 0.0))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 12.59999942779541)
))
(:action advance_time__t2200__t2230
	:parameters ()
	:precondition (and  (timenow_t2200))
	:effect (and 
			(timenow_t2230)			(not (timenow_t2200))
))
(:action generate__t2200__n12__s0
	:parameters ()
	:precondition (and  (timenow_t2200)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 12.0)			(decrease (stored_units_s0) 1.0)
))
(:action generate__t2230__n10__s0
	:parameters ()
	:precondition (and  (timenow_t2230)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (funds_s0) 10.0)			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)
))
(:action pump_water_up__t2230__n10__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -10.5 ) 0.0) (timenow_t2230))
	:effect (and 
			(decrease (funds_s0) 10.5)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))
(:action advance_time__t2230__t2300
	:parameters ()
	:precondition (and  (timenow_t2230))
	:effect (and 
			(timenow_t2300)			(not (timenow_t2230))
))
(:action generate__t2300__n6__s0
	:parameters ()
	:precondition (and  (timenow_t2300)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 6.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t2300__t2330
	:parameters ()
	:precondition (and  (timenow_t2300))
	:effect (and 
			(timenow_t2330)			(not (timenow_t2300))
))
(:action pump_water_up__t2300__n6__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -6.299999713897705 ) 0.0) (timenow_t2300))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 6.299999713897705)
))
(:action pump_water_up__t2330__n3__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -3.1499998569488525 ) 0.0) (timenow_t2330))
	:effect (and 
			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)			(decrease (funds_s0) 3.1499998569488525)
))
(:action generate__t2330__n3__s0
	:parameters ()
	:precondition (and  (timenow_t2330)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(increase (funds_s0) 3.0)			(decrease (stored_units_s0) 1.0)
))
(:action advance_time__t2330__t2400
	:parameters ()
	:precondition (and  (timenow_t2330))
	:effect (and 
			(timenow_t2400)			(not (timenow_t2330))
))
(:action generate__t2400__n1__s0
	:parameters ()
	:precondition (and  (timenow_t2400)(>= (+ (*   (stored_units_s0) 1.0) -1.0 ) 0.0))
	:effect (and 
			(increase (stored_capacity_s0) 1.0)			(decrease (stored_units_s0) 1.0)			(increase (funds_s0) 1.0)
))
(:action pump_water_up__t2400__n1__s0
	:parameters ()
	:precondition (and (>= (+ (*   (stored_capacity_s0) 1.0) -1.0 ) 0.0)(>= (+ (*   (funds_s0) 1.0) -1.0499999523162842 ) 0.0) (timenow_t2400))
	:effect (and 
			(decrease (funds_s0) 1.0499999523162842)			(increase (stored_units_s0) 1.0)			(decrease (stored_capacity_s0) 1.0)
))


)