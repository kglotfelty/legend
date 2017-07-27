# Creates a legend in CIAO Chips plotting package


CIAO's ChIPS plotting package contains the basic plotting elements
but does not provide a built-in legend creation routine.  




Limitiations

- Only a single plot in a single frame can be present
- Moving/resizing the legend is very painful.
- Users must call the .update() method if any changes are made to the
  parent plots properties.
- Only curves are supported -- not histograms.

