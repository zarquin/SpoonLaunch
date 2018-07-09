# SpoonLaunch
software for using Launchpad to control SpoonFight

## Using a Launchpad Pro to control Spoonfight.

there are several different functions that are done on the launchpad to control Spoonfight.

they are:
* Start and stop each of the tracks
* Set the playback mode of each of the slices in each track
* Set the volume level of each of the tracks.
* Set all tracks to jump to a particular slice for playback.
* Load a new loop into a track.

### Launchpad Pro Layout
Below is the general layout of the launchpad with some indicators to show what they do.

```
    0      1   2   3   4   5   6   7   8      9
             +---+---+---+---+---+---+---+---+ 
             | . |   | . |   |   |   |   |   |  <-  ALL SLICE JUMP       
Track Stop   +---+---+---+---+---+---+---+---+ 
       \/      SLICES
      +---+  +---+---+---+---+---+---+---+---+  +---+
TRK 1 | 1 |  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |  | M | <-Track Playback Mode
      +---+  +---+---+---+---+---+---+---+---+  +---+
TRK 2 | 2 |  |   |   |   |   |   |   |   |   |  | M | <-Track Playback Mode
      +---+  +---+---+---+---+---+---+---+---+  +---+
TRK 3 | 3 |  |   |   |   |   |   | . |   |   |  | M | <-Track Playback Mode
      +---+  +---+---+---+---+---+---+---+---+  +---+
TRK 4 | 4 |  |   |   |   |   |   |   |   |   |  | M | <-Track Playback Mode
      +---+  +---+---+---+---+---+---+---+---+  +---+
      |   |  |   |   |   |   |   |   |   |   |  |   |  5
      +---+  +---+---+---+---+---+---+---+---+  +---+
      | V |  | P | M | S | R | D | H |   |   |  |   |  <- Hold Buttons
      +---+  +---+---+---+---+---+---+---+---+  +---+
      |   |  |   |   |   |   |   |   |   |   |  |   |  7
      +---+  +---+---+---+---+---+---+---+---+  +---+
      | . |  |   |   |   |   |   |   |   |   |  | . |  8
      +---+  +---+---+---+---+---+---+---+---+  +---+
      
             +---+---+---+---+---+---+---+---+ 
  LOAD ->    | L1| L2| L3| L4|   |   |   |   |         9
             +---+---+---+---+---+---+---+---+ 

```
### Slice buttons
Pressing the slice buttons (the top 4 rows of 8 ) rotates each slice through the slice playback modes.
The modes and the colours are:
* Play : Green
* Mute : Red
* Skip : Off
* Reverse : ??
* Random : Dark Blue
* Half :  Pink
* Double : Light Blue

### Track Playback Mode
Pressing the track playback mode button (on the right) rotates the playback mode of that track.  
The modes are:
* Play : Green
* Reverse : 
* Random : 
* Stop : Off

Pressing the Track Stop button stops the playback of that track.  Pressing it again while stopped sets the slice playback of that track back to the start.

### All Slice Jump
Pressing these buttons will cause all tracks to jump to that slice position

### Hold Buttons
Press and hold one of these buttons to allow the faster changing of the slice modes.  
e.g. press and hold the Reverse button (pink) and then press the slices you want to change to that mode to change them straight away.  (Rather than having to cycle through all the modes for that slice)

The Volume hold button in the left most column lets you set the volume for each track.  While the volume hold button is held donw, pressing the right most track slice button sets the track volume to max, while pressing the left most slice button sets the volume to minimum.  

### Track Load buttons
These buttons let you load a new audio file into a particular track.
HOlding down L1 lets you select a new file for Track one, and L4 is for track four.

To load a new file, hold down the button for the track you want to change, then press the appropriate slice button that matches teh file index (as defined in the patch file) that you want to load.
