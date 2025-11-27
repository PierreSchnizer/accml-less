# accml-less: A perhaps too rich interface to the Accelerator middle layer

[accml](https://github.com/python-accelerator-middle-layer/accml) 
is based on interacting with an accelerator, twin or machine based
on structured messages. Its core interaction with the machine is
a command or measurement execution engine.

There seems to be a common demand to provide an interface based
on a device library. These devices can be built based on the 
infrastructure and services `accml` provides.

These devices, however, couple together different aspects that 
accml set out to only couple loosely by exchanging structured
messages.

Therefore, this interface is based on a separate package. 

This packages is seen to aid experimenting with accml in the 
way that a considerable amount of people are used to. 

It is still advised to build well maintainable applications on 
the interface that `accml` provides.

