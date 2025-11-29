## accml-less — A Hands-On Device Interface on Top of accml

A familiar workbench for accelerator physicists, built on a cleaner frame.

accml-less gives you the ability to handle accelerator devices directly —
power converters, RF amps, magnets, diagnostics — in the interactive way many users know from the MATLAB Middle Layer.

Under the hood, though, it stands on the much more structured foundation of accml, the Accelerator Middle Layer.

If accml is the clean recipe-driven kitchen,
then accml-less is the training bench where you can grab the tools yourself
but still stay close enough to the real workflow to move on to accml later.

## Why accml-less Exists

[accml](https://github.com/python-accelerator-middle-layer/accml) 
speaks in structured messages — tiny command cards that a
measurement or execution engine carries out cleanly and predictably. 
That’s the preferred interface for building durable, maintainable
applications.

But many accelerator physicists prefer to start at the device level,
adjusting knobs and reading values as if standing right in front of
the machine.

`accml-less provides` exactly that:\
a device-oriented interface, familiar to MML users, but far better
structured and fully compatible with the concepts of accml.

It also lets a single device object switch — invisibly — between:
* a simulation engine,
* a digital twin,
* the real machine.

## Installation
pip install accml-less

## How It Fits Together

Here is the simplified architecture:

                 ┌───────────────────────────┐
                 │       accml-less          │
                 │   (device-level API)      │
                 └─────────────┬─────────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │      Combined Views       │
                 │     (design + device)     │
                 └─────────────┬─────────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │        View Facades       │
                 │    (direct to backend)    │
                 └─────────────┬─────────────┘
                               │
         ┌─────────────────────┴─────────────────────┐
         │            View Implementations           │
         │  - direct backend access                  │
         │  - or value conversion (via translator)   │
         └─────────────────────┬─────────────────────┘
                               │
                     ┌─────────┴──────────┐
                     │   Backend Proxies  │
                     │     (e.g. PyAT)    | 
                     └─────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │ simulation │ twin │ machine │
                └─────────────────────────────┘


This device interface is built on the same liaison and 
translation services that accml uses — just arranged so
users can interact as if they were turning knobs 
themselves.

## Who This Is For

`accml-less` is intended for accelerator physicists who want
immediate, device-level interaction — especially those coming 
from MML — while staying close to the structured patterns of 
accml.

### What You Should Use It For
 
* experimenting with accml
* quick exploratory tasks
* familiar device-level workflows
* toggling between simulation, twin, and machine with a single 
  device handle

### What You Should Not Use It For 

`accml-less` is not the interface for large-scale, reproducible 
accelerator applications. Those belong in the clean, 
message-based world of accml itself.

Think of `accml-less` as the friendly workbench — not the full 
production line.

## Documentation

For conceptual background:

* Design of `accml` and `accml-less` (see docs/design.md)
* Design Flaws & Trade-offs of accml-less (see docs/design_flaws.md)

These documents explain how the device abstraction works,
why some trade-offs are unavoidable,
and why accml remains the preferred long-term interface.

