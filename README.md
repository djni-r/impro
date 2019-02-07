
Version 0.2.0

Software music improvisation. Essentially it is a software that improvises, 
i.e. goes between random notes and responses to the notes that were played 
before, given certain sounds and rules. The rules are hardcoded, but the 
choices of the notes happen on a semi-stochastic basis. It does not use ML or Deep Learning at this point.

Changes from the previous version:

- Implemeted minimal GUI
- Aded extra sounds that can be played as samples
- Changed the library that plays sounds from sounddevice to playsound
- which in turn made sounds legato, because of asynchronous play
- made some practical changes in the code

Dependencies are not included in the source code.

There is no executable at this point, but I might add it to the distro repository later.

The bare GUI has three buttons, Piano, Cello, Xylo, you can press it to start playing, and press again to stop.
To add extra sounds, create a folder in vendor/resources/misc_sounds and add sounds in it.
When starting the program, add the folder name as a command-line argument.
More than one folder can be added, but only one of them can be used at one time.

The extra sounds will appear along the primary buttons, named same as the files. These buttons can only start the sound, but not stop it.

>>>>>>>>>>>>>>>>>>>>

Version 0.1.0

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
