# Design of accml-less

**NB** the design and architecture of `accml-less` is
currently being explored: so expect changes.

## Core abstraction

### API based on devices

Core abstraction of `accml-less` is a device that 
shall provide an interface close to the devices 
existing in the real machine.

Given that the device was appropriately instantiated,
the same device shall be the API independently if 
in the end a real world machine is addressed, 
its representation in a simulation engine or 
its representation in a digital twin.

### API Devices as start or debug tool

These devices exist to facilitate debugging or 
interaction with the machine. These are ment to get
the user started. 

Complex scripts or applications are best developed using
only the functionality that `accml` provides.

Reason: the interface provided there is designed to 
be small and slim. Thus it is expected to be 
more flexible and thus better to maintain.
