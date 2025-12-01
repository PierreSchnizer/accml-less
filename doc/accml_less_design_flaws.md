# accml-less limitations


##  1. A Tale of Two Workshops

accml is built around the idea of *handing a recipe to a very 
competent craft-person*.\
You write a clean list of steps; the execution engine carries\
them out.
Everything is tidy, deterministic, and reproducible.

`accml-less` is different.\
It puts you in front of the bench.\
You pick up the tools yourself — or worse, reach around the 
craft-person and try to move their hands.

Sure, it works.\
But it’s easy to get your fingers caught.

## 2. Why This Causes Trouble

Because accml-less behaves like direct device access, it must 
solve several problems at once:

### 2.1 One device, many realities

A “Quadrupole” in AT isn’t the same kind of creature as a quadrupole
power converter in the real machine. One object may map to several 
simulation elements, or vice versa.


### 2.2 Switching destinations on the fly

Users expect the same device object to behave the same way whether
it talks to:

* a simulation engine,
* a digital twin,
* the real machine.

That means every device has to check a multiplexer on each call 
and figure out where reality currently resides.


### 2.3 Explaining what will happen

If changing one device property actually writes numbers into several
simulation elements, the user should be able to inspect that.\
That’s harder than it sounds.

That is why `accml`, which uses explicit messages and clear 
separation, avoids these troubles entirely.


### 3. Why the Implementation Looks Complicated

To make the device illusion work, `accml-less` uses four layers:

1. *Combined View* — the dual device/beam-dynamics interface
2. *View Facade* — bundles view implementations and routes calls
3. *View Implementation* — does backend-specific work
4. *Backend Proxy* — ensures a uniform API for all backends

This may look like overkill, but each layer solves a distinct problem.\
Skip one, and you get spaghetti.

## 4. What Could Be Improved
### 4.1 Clearer vocabulary

“Device” and “design” views are generic terms. A more destinct 
name would be:

* **Device view**
* **Beam Dynamics view**

Likewise, renaming *target/native* to *source/target* might match 
normal engineering terminology better.


## 5. What Cannot Be Improved

Some limitations are baked into the concept:

* **Destination switching has unavoidable side effects**\
  If one object talks to multiple worlds, its behavior will depend  
  on which world is active.\
  This is the price of convenience.
* **The four-layer implementation is necessary**\
  Removing layers merges responsibilities and makes everything
  fragile.

You *could* collapse things by skipping the backend proxy and 
letting view implementations talk directly to a backend.\
But you’d be breaking the clean separation of concerns — and 
inviting chaos.


## End Note

`accml-less` is not meant to be perfect.\
It’s meant to be *useful* — a friendly workbench where accelerator 
physicists can experiment freely, while still standing close enough
to the `accml` model that they can graduate to the real thing when
ready.

`accml` is the production interface.\
`accml-less` is the apprenticeship bench.

Both are necessary — as long as you don’t try to use a hammer on 
the RF amplifier.

# Flaws of the `accml-less` design (zero's version)

`accml` is designed around the flow of messages: 
These are  commands which come from the user side and get executed
by some measurement execution engine. Or data flows back to the user.

It follows how large scale work shops work: the input is a good 
description of the end product or a work instruction how to make
it. The work steps actually executed depend on then specifics of 
the used work bench. The work instruction is carried out by a 
sufficiently experienced person.

`accml-less` puts the user in front of the work bench. It lets the
user handle the tools: but even further the user does expect them
to work the same or similar independent on where it works.

A better picture would be: the user steps behind the craft-person
working at this work bench and tries to get the job done 
moving  the craft-person hands. 


## Implementation challenges

The above requirements need to address:

1. provide devices which expose different views
2. each view needs to interact with the backend in question:
   be it a simulation engine, a twin or the real machine. 
   Furthermore, it shall be changeable by the user interacting 
   at a single stop.
3. mapping the user interaction to the appropriate device and
   value of the back end.

The tasks above need to take into account:The *simulation engine*,
the *twin* or the*real world accelerator* consist of a set of 
*entities*. In the simulation engine these are typically called
*elements* whereas for the twin or *real world accelerator* these
are called *devices*. It is important to note that the elements of 
a simulation engine *do not* always map to a single element. The 
same applies to devices.

Now when the user handles the device, it can result that changes
made to some of its properties need to be delivered to different
elements.

So the challenge is:
* give the user access to the device
* but let the user inspect what will happen when the device 
  properties gets changed. 

Due to the challenges listed above `accml` is designed to 
interact with an accelerator or even command or measurement 
execution engines. Its rather like handing in a "work instruction"
to a production work shop.

## Current implementation

The devices made available to the user follow the following object 
hierarchy:

1. *combined views*: with these the user interacts. 
   These are the design and device view. 
2. *view facades*: They contain all the different
   *view implementations* with their respective backend. 
   Each *view facade* has been given a reference to the 
   *destination multiplexer*. Each time it executes a method call
   it will probe it to see to which destination the call needs to 
   be redirected to.
3. These *view_implementations* now interact with their backend.
   The view implementation comes in two flavours:
    * *ViewWithBackend* interacts directly with the backend. 
      It is the one used when the backend has the same view 
      as the view used here
    * *ViewWithConversion* finds out with which property of the 
      backends needs to be converted. Furthermore, it recalculates
      the value.
4. Finally: the *Backend*. Here a slim proxy is required so that 
   the `accml-less` interacts with the backend in a standardised
   way. Currently such a proxy exists for PyAT.

The required information for level 1--3 are obtained from the 
*liaison manager* and *translator service*.


## What can be improved

* Improve terminology:
  * naming the views: *design* and *device* sound very general. 
    As long as this repository intends to be similar to MML 
    one could stick with *device* and call the other *beam dynamics*.
  
  * naming *target* and *native* view: would be *source* and *target*
    be more natural


## What can not be improved:

* Side effects due to *multiplexer switching*. This is considered
  to be core demand to `accml-less`.
* The 4 layers implementing the actual devices. The current form
  addresses the following concerns
  1. Combined view: make it clear on the user interface side 
     which properties belong to which view
  2. View facade: this collects the different available view 
     implementations and passes the incoming request on to the
     appropriate view implementation.
  3. View implementation: passes the request on to the back end.
  4. Back end: to provide a consistent interface to the view 
     implementation.
  
If required a backend could be implemented directly using the 
view implementation. It is not recommended as it seems to violate
the design principle *separation of concerns*. 


## Todo's 

* Implement view facades
* Add test implementations for real machine and twin
* Find out if the conversion_capsule is needed. Could one just go 
  a head using the liaison and translation manager directly?
* Find out what "probing" the different devices should provide.
* Find out which parts should be moved to accml. 
   * backend interface
   * backend implementation of the pyat calculation engine
