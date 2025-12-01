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


## Exposed interface

Each device provides interfaces for the different views:
e.g. a power converter provides a "*device*" view where it 
will handle *set_current*. 

For each view the device provides the following async methods
* read(id_)
* trigger(id_)
* set(id_, value)

These interfaces are similar to what ophyd_async provides 
(please not trigger is only provided per id here). 

## How does it work

Devices shall be retrieved from a device factory. This factory 
generates devices on the information provided by the 
translation service, translation objects and further repositories,
which will be added as needed.

These devices are actually following the facade pattern.
Under the hood these contain the different device implementations 
that this facade will delegate the different method calls to:
simulator, twin or the real machine for example.


When the factory instantiates the device it will add to it a 
multiplexer switcher object. Every time the device recieves a 
trigger, read or set object it will check where the switcher 
object points to and then delegate the method call to the appropriate
method.

Each of these delegates work in their "natural view": e.g. the 
simulator works in the *design* view, whereas a machine will typically
work in a *device* view

Each delegator then will in turn interact with its backend to retrieve
the required data.