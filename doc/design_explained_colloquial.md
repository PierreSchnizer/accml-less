# Design of accml-less 

If you’ve ever worked with a real accelerator, you know the first thing you meet is not an elegant abstraction or a well-behaved mathematical object.
You meet **devices** — power converters that sulk when you push them too fast, RF amplifiers that have opinions about stability, diagnostics that only tell the truth when they feel like it.
And if you’re coming from the MATLAB Middle Layer (MML), you’re used to poking these devices directly: “Give me that current,” “Set that phase,” “Try not to explode.”

`accml-less` embraces this world — but gives it a good cleaning first.

The Core Idea: A Friendly Device Layer

The heart of accml-less is simple: 
**it gives you device access that looks and feels like the real 
accelerator.**
A power converter in `accml-less` behaves like a power converter.
An RF system behaves like an RF system.
When you call a method, it acts like you’re turning the knobs on 
the actual machine.

But unlike MML — where half the magic happens through a global
state that quietly decides what machine you’re talking to — 
`accml-less` makes this business **structural**.

A **device factory** creates all device objects and hands each of
them a small *service object*.
Whenever you call a device method, the device checks that service 
and asks:

>  “Hey, boss — who am I talking to right now? \
   The simulator? \
  The digital twin? \
  Or the real hardware?”

And the service answers.
The device switches backend accordingly, and the method call goes where it should.

This is still a device-level interface, with *side effects* just like 
MML: calling a method can poke a real magnet or drive a real RF chain.

But now the plumbing is at least tidy — not hidden in global variables, 
but contained in one well-defined service.

## A Bridge from MML, Not a Replacement for accml

`accml-less` exists for a very specific reason: \
it gives accelerator physicists coming from MML a familiar landing pad.

You get a device interface that is:
* direct,
* concrete,
* easy to tinker with,
* good for debugging,
* and close to the way the machine actually reacts.

This makes it excellent for:
* playing with simulations,
* sanity-checking hardware behaviour,
* writing quick exploratory scripts,
* and talking directly to real devices in a hands-on way.

But here is the part we want to say explicitly and without apology:


>   **For serious software, 
>   accml is the preferred interface.**


`accml` is built around clean abstractions:
no hidden state, no backend switching in the middle of a method call,
no device objects carrying side-effects like little land mines.
It is uniform, view-based, deterministic, and engineered to work 
the same way whether you run it on the machine, the digital twin, 
or a big simulation code.

`accml-less` is useful — but it’s not the architectural core.
Think of it as the set of hand tools you keep on the front 
workbench because they’re comfortable and familiar.
`accml` is the machine shop in the back where the serious, 
precise fabrication happens.

## Why Keep accml-less at All?

Because sometimes you don’t want the machine shop. \
Sometimes you want to tap a pipe and listen for the echo. \
When debugging real apparatus, or when ramping up new students,
or when replicating the MML workflow, a thin layer that exposes 
the machine’s “raw personality” is exactly what you need.

`accml-less` gives you that, but without the old MML quirks:
* The interface is cleaner.
* The layout is more structured.
* The backend switching is controlled and semi-visible.
* Devices are produced consistently by a factory.
* There is no mysterious global state deciding the fate of your
 calls.

You get the benefits of MML’s device-centric approach, but with 
some engineering discipline.

## The Recommended Path

Use `accml-less` to get started, to explore, to debug, to talk 
to devices the way hardware actually talks back.

But when you write larger applications — \
when you need determinism, \
when you need clean separation of concerns, \
when you want to write code that lasts — 

> **move to accml.** \
> It’s the real architecture.