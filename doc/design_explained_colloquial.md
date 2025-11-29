# Design of `accml-less`

## 1. Why We Need a Middle Layer at All

If you talk to accelerator physicists long enough, you notice 
that most of the work boils down to nudging a lot of specialized
gadgets — power converters, RF amplifiers, vacuum gauges, 
BPM electronics — each of which speaks its own little dialect.

Yet simulations speak a *different* dialect: Twiss parameters, 
lattice functions, normalized coordinates, quantities the hardware
has never heard of.

So how do you write code that can talk to both worlds without
losing your mind?

That’s where *accml*, the Accelerator Middle Layer, comes in. It 
treats the whole accelerator — the big humming machine or its 
digital twin or a simulation — as a workshop run on **small messages**. 
Every instruction is one neat, tiny card:

```python3
Cmd(dev_id, prop_id, value, behaviour_on_failure)
```

Like leaving a note on the craft-person’s bench: “Turn this knob
to here; if it sticks, stop.” The beauty is that you can write a 
whole recipe — a work instruction — and the machine, twin, or 
simulator all know how to carry it out.

accml is the clean interface: compact, structured, and predictable.

## 2. The Two Worlds: Hardware and Beam Dynamics

Here comes the catch. The accelerator you can touch and the 
accelerator you simulate don’t live in the same coordinate system.

* The **device view** sees magnet currents, RF phases, temperatures.
* The **design (beam dynamics) view** sees Courant–Snyder parameters, 
   optics functions, normalised coordinates.

If you don’t separate these worlds carefully, you quickly end up 
in a tangle of unit conversions, coordinate transforms, and 
off-by-a-factor-of-two disasters.

That’s why accml introduces **views**.

A view is simply, “the way this kind of thing thinks.”\
The device view thinks like hardware.\
The design view thinks like the physics.\

## 3. The Three Helpers: Liaison, Translation, Rewriting

To make views actually work in practice, accml relies on three pieces of machinery:

### 3.1 Liaison Manager — the cross-reference book

It tells us which design-view element corresponds to which device-view device.\
One-to-one? Fine.\
One-to-many? Still fine.\
Many-to-one? Also fine.\
Real accelerators aren’t tidy; `accml` accepts that.

### 3.2 Translation Service — the mapping engine 

Once we know *what corresponds to what, we still have to convert values:
units, coordinate transforms, sometimes derived physics quantities.

3.3 Command Rewriter — the interpreter

This one listens to your high-level work instruction and rewrites every
command into the right view for whatever destination you use: simulation, 
twin, real hardware.

Together, these three let you write one recipe that works everywhere.

4. Work Instructions — Recipes for the Accelerator

A work instruction is exactly what it sounds like:\
a list of small steps carried out in order, each step a simple 
command.

Accelerator physicists know these as response-matrix measurements,
orbit correction scans, tune-kicks — all sequences of “set something,
measure something, repeat.”

`accml` allows you to package these sequences in a tidy, replayable, 
auditable form.\
Like dropping a well-written recipe into the workshop, and the 
craft-person knows exactly what to do.

5. Execution Engines — the Conductor

Execution engines are responsible for running the recipe:

1. Read the next command
2. Rewrite it to the right view
3. Send it to the right destination
4. Record the system state

Crucially, the engine doesn’t care *what* the destination is — real, twin, or simulation.
The views and rewrites take care of everything.

## 6. Enter `accml-less` — the Training Bench

accml is clean.\
In fact, it’s very clean.\
Clean interfaces are great for automation, execution engines, and
reproducibility — but sometimes you want to poke devices directly.

Accelerator physicists coming from the MATLAB Middle Layer (MML) are used to a very immediate style:

```matlab
setsp('QF', 12.1)
readpv('BPMx')
```

`accml` doesn’t expose that kind of raw, device-level interface.\
That’s where *accml-less* comes in.

Think of accml-less as a *training bench*, the place where you can
put your hands directly on the knobs — or at least on a very 
convincing mock-up of the knobs — without abandoning all discipline.

It is:

* familiar to anyone used to MML,
* cleaner and more structured than MML,
* but still fundamentally device-oriented,
* and able to switch under the hood between simulation, twin, and 
  real hardware.

`accml-less` is the starter kit; `accml` is the production system.

## 7. How accml-less Works Under the Hood

`accml-less` has a job: let users handle devices directly, while 
secretly routing those calls to wherever the accelerator currently
“lives.”

That leads to a layered structure:

### 7.1 Combined Views (what the user sees)

A device object exposes its properties in both device-view and
design-view form.\ 
This is the handle the user grabs onto.

### 7.2 View Facades (the selector)

Each combined view holds a set of view implementations and a 
reference to a *destination multiplexer*, which decides whether
you’re talking to a simulation, a twin, or the real machine today.

This replaces MML’s global variable with something cleaner and 
more modular.

### 7.3 View Implementations (the workers)

Two flavors:

* **ViewWithBackend** — backend already works in this view
* **ViewWithConversion** — needs value conversion via the translator

### 7.4 Backend Proxies (the translators to each world)

A slim layer ensuring accml-less talks to any backend in a 
consistent way.\
Today: PyAT backend exists.
Tomorrow: more can be added.

All these layers rely on the liaison manager and translator service.

### 8. Trade-offs Built into accml-less

Some things cannot be avoided:

* **Side effects when switching destinations**\
  Because accml-less allows one device object to magically talk to
  different backends, switching destinations inevitably causes 
  invisible changes in behavior.\
  This is by design.

* **The multi-layer device implementation**\
  It looks heavier than MML, but it preserves clear separation of concerns.

`accml-less` is not meant to replace `accml` — it’s meant to get new users
comfortable, productive, and confident before they graduate to the cleaner, 
message-based world of accml.


# Design of accml-less (earlier version) 

If you’ve ever worked with a real accelerator, you know the first
thing you meet is not an elegant abstraction or a well-behaved 
mathematical object.
You meet **devices** — power converters that sulk when you push 
them too fast, RF amplifiers that have opinions about stability, 
diagnostics that only tell the truth when they feel like it.
And if you’re coming from the MATLAB Middle Layer (MML), you’re 
used to poking these devices directly: “Give me that current,” 
“Set that phase,” “Try not to explode.”

`accml-less` embraces this world — but gives it a good cleaning first.

## The Core Idea: A Friendly Device Layer

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