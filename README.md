Software music improvisation. Essentially it is a software that improvises, 
i.e. goes between random notes and responses to the notes that were played 
before, given certain sounds and rules. The rules are hardcoded, but the 
choices of the notes happen on a semi-stochastic basis.

The first release version 0.1.0 has many unimplemented features left for later.
It comes with just three types of sounds, piano, cello and xylo. It can only be
initiated at the start with command line arguments, which can be any combination
of piano, cello and xylo. For now I'm leaving it without explanations for how it
actually works.

Some things I plan to implement:
- GUI
- Rhythm (the class already exists)
- improvisations in a particular key
- legato sounds
- add more types of sounds
- more control for the user
- refinement of the probabilities
- visual aspect
- and much more...

Dependencies and the actual sounds are not included in the source code.

To use the software (ONLY ON MACs) 
go to https://github.com/makar-y/impro-dist,
download it,
drag the 'play' file from the 'play' folder into the terminal window,
and add the sounds you want to play, any combination,
e.g. /path/to/executable/play piano cello xylo
or .../play piano cello
or .../play piano piano xylo
etc

To exit, use control-C
