# Design of accml-less 

When you work with an accelerator, the first things you interact
with are the **devices**: power converters, RF amplifiers, 
diagnostics, and all the other components that make the machine 
run.

If you’re used to the MATLAB Middle Layer (MML), the world is 
organized around these devices. You read settings, 
write settings, and see how the hardware responds. It’s a very 
direct way of working — close to the metal.

`accml-less` keeps that spirit, but tidies it up.

## The Core Idea: A Familiar and Friendly Device Layer

The core abstraction in accml-less is simply the **device**.
A power converter object behaves like a power converter.\
An RF object behaves like an RF station. \
You interact with them in a straightforward, device-oriented 
way that mirrors the feel of talking to the machine.

But the design repairs one of the long-standing quirks of MML.\
In MML, a (hidden) global variable quietly decides whether your
device call goes to the real machine, the simulator, or a model.
In `accml-less`, this becomes an explicit, structured mechanism.

All device objects are created by a *device factory*, and each
device receives a small *service handle*.
Whenever you call a method, the device checks that service:

* “Am I talking to the real machine?”
* “Am I talking to the digital twin?”
* “Am I talking to a simulator?”

The service answers, and the device routes the call accordingly.\
This means the interface remains close to hardware, but the 
internal routing is clean and easy to reason about.

It is still a device-level API with side effects — reading and
writing real values when connected to hardware — but at least the
machinery behind it is structured and visible.

## A Bridge from MML — Not a Replacement for accml

`accml-less` exists to give accelerator physicists a familiar 
starting point.
If you learned accelerator control through MML, this layer will 
feel natural: concrete, device-first, and immediately usable for exploring the machine or a model of it.

It’s excellent for:
* quick checks,
* exploratory scripts,
* hardware debugging,
* and interacting with simulations in a hands-on way.

But we want to say this explicitly:

> **For larger applications and clean software structure, use accml.**

accml provides the architectural clarity:

no backend switching hidden inside device calls, no implicit 
state, no device objects that secretly behave differently 
depending on context. 

It uses explicit views, rewriting, and well-defined patterns
— a cleaner base for scalable software.

`accml-less` is the bridge.\
`accml` is the design.

## Why Keep accml-less?

Because sometimes, especially during debugging or commissioning, 
you need an interface that stays close to the way the machine 
actually behaves.

You want to read a property, write a property, and immediately
see the effect.
You want to interact with the simulator and the real machine 
using roughly the same device-style commands.

`accml-less` gives you that, but with improvements over MML:

* a more structured layout,
* consistent creation of devices via a factory,
* backend switching handled explicitly by a service,
* and no reliance on global variables.

You get the familiarity without the mess.

## Recommended Use

Use `accml-less` when you need direct device-style interaction 
— especially for debugging, commissioning, or reproducing 
MML-like workflows.

When building larger, maintainable applications or tools, move to
accml, which provides the cleaner, more robust architectural 
foundation.