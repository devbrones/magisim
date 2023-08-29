by moving the exponential calculations from the cpu (cuda kernel cannot run numpy functions) to using eulers number as a variable and then performing the equations, resulted in a 3000x speed (it/s) increase.

