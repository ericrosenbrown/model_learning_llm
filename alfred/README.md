limitations:
- requires fully observed world
- requires predicates to be specified
- requires ability to reset low-level state based on lifted high-level state
- currently can only handle predicates that are:
	- intersection of true predicates (relax intersection requirement, relax only true predicates descriptions)
- assumes initation set distriubtion is 0/1 (no noise in data collection)
- currently only handles one object of each type in domain
- informed adapation does not accept arguments, only lifted predicates