by moving the exponential calculations from the cpu (cuda kernel cannot run numpy functions) to using eulers number as a variable and then performing the equations, resulted in a 3000x speed (it/s) increase.


Should we switch to qt or pyside2?

PRO:
- Easy to develop using qtcreator or qtdesigner.
- lots of users in the professional workspace thx. to autodesk!
- plenty of libraries and modules.
- support for nodes - allows us to visualise the workflow.
- fast as fuck (built with cpp)
- uses opengl instead of javascript (which we will love)
- might be easier to support in the future
- LOTS OF THEMING SUPPORT!
- cross platform maybeeeeE?
- easy to create extensions for
- https://github.com/jchanvfx/NodeGraphQt

AGAINST:
- Fucking large library, which means large executable (not really a problem)
- gradio is important for experience in the programming world, since it is being used by all major AI and computation workflows.
- We would have to write a separate server program and a separate client program, and create communication methods between them, API using flask or django - web bottleneck.
- we have NO experience in qt.


