limitations:
- requires fully observed world
- requires predicates to be specified
- requires ability to reset low-level state based on lifted high-level state
- currently can only handle predicates that are:
	- intersection of true predicates (relax intersection requirement, relax only true predicates descriptions)
		- in order to relax to negated predicates, we need to add not predicates, add it to high-level state, and make it so that lifted sets of predicates with argument bindings can be identified as equal up to naming.
- assumes initation set distriubtion is 0/1 (no noise in data collection)
- currently only handles one object of each type in domain