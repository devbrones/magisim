provide legal information as well as cleartext licensing information , some libraries are LGPL or GPL

Instructions on how to write open source extensions and how to properly share your code.

instructions on how to write proprietary extensions and how to obfuscate or compile to pyc. We should also include instructions on how to properly license the extensions as well as how to publish the extensions on the marketplace (we need to check the licenses as well as create a stable marketplace with payment?! Fuck that....) - SaaS sucks balls! How can users protect their code? Should they et.c. Maybe recommend that users do not obfuscate their code? we cant control third party developers without restricting the end user. which we do NOT want to do! 

Provide documentation about different extension features - i.e. the workplace I/O system and node system.

extensions need to have a descriptor:

```python

class ExtensionMeta:
	name: str = "EXTENSION NAME"
	uuid: str = "7b7584a4-86ea-4076-9da4-1c3813605059"
	authors: list = ["AUTHOR1","AUTHOR2"]
	version: str = "0.0.1-<optional: alpha>-<optional: devel>" 
	qtVersion: str = "5.15"
	license: str = "LGPL3"
	description: str = """ multiline description here """
	# nhr meta
	class ExtensionType:
		types: list = [simulator, renderer ... ] # list of classes
		layoutCompat: bool = False
		hasNodes: list = [("NODENAME1", simulator),("NODENAME2", simulator) ...]
	# ...

```

that contains metadata about the extension so that we can recognise what is going on :3

we also need to declare classes for the different ExtensionMeta.ExtensionType.types types:
- simulator
- renderer
- workspace
- editor
- input
- output
- analyser
- telemetry -- this one is a bit sussy, however it is important that we have this
these are basically scopes, that let us recognise what the extension wants to do, and give it permissions to do such, these will be shown to the user on the first import, allowing the user to see what the extension wants to do.



