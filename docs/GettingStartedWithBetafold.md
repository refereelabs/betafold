# Getting Started with Betafold

**betafold** is a physics engine designed to simulate the behavior of a particle using data learned and output determined by processing via a transformer deep learning architecture.

### The Hamiltonian in 3D Space

With **betafold**, users can simulate the behavior of particles based on some initial state within some predefined 3D space. The behavior of a particle is defined by its Hamiltonian in a particular increment of 3D space. Let this 3D space be defined as $$P$$ which is bound by $$a$$ such that

$$
P \subseteq \mathbb R^3 \\\\
p_x, p_y, p_z < a \\\\
a \in \mathbb R^3
$$

The Hamiltonian of a particle is defined as 

$$
\hat H = \hat T + \hat V,
$$

where $$\hat T$$ is its kinetic energy and $$\hat V$$ is its potential energy.
\
\
In this case we let $$\hat V = 0$$, so

$$\hat H = \frac {1}{2}m\vec v^2$$


A particle's initial state is captured in the input vector $$I$$ which is defined as

$$
I = (\vec p, \hat H),
$$

where

$$
\vec p \in \matrix P \\\\ 
p_x, p_y, p_z < a \\\\
\hat H = \frac {1}{2}m\vec v_p^2
$$