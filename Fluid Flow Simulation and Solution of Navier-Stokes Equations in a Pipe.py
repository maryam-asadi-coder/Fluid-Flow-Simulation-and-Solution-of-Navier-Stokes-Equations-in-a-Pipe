import numpy as np
import matplotlib.pyplot as plt

# Constants
nu = 1e-6  # Kinematic viscosity (m^2/s)
rho = 1000  # Density of fluid (kg/m^3)
L = 1.0  # Length of the pipe (m)
dx = 0.01  # Spatial step (m)
dt = 0.001  # Time step (s), reduced to improve stability
T_max = 2.0  # Maximum time (s)

# Discretization
Nx = int(L / dx)  # Number of spatial points
Nt = int(T_max / dt)  # Number of time steps

# Velocity field (initial condition: constant velocity across the pipe)
u = np.zeros(Nx)
u[int(Nx/4):int(3*Nx/4)] = 1.0  # Initial velocity in the middle

# Pressure field (initial condition: no pressure gradient)
p = np.zeros(Nx)

# Velocity at the boundary (no slip condition)
u[0] = 0  # Velocity at the inlet (m/s)
u[-1] = 0  # Velocity at the outlet (m/s)

# Function to compute pressure gradient
def compute_pressure_gradient(p, dx):
    dp_dx = np.zeros_like(p)
    for i in range(1, len(p)-1):
        dp_dx[i] = (p[i+1] - p[i-1]) / (2*dx)
    return dp_dx

# Function to compute the velocity update based on Navier-Stokes
def update_velocity(u, p, nu, dx, dt, rho):
    u_new = u.copy()
    dp_dx = compute_pressure_gradient(p, dx)  # Calculate pressure gradient

    for i in range(1, Nx-1):
        # Central difference for velocity gradient
        du_dx = (u[i+1] - u[i-1]) / (2 * dx)

        # Navier-Stokes equation (simplified)
        u_new[i] = u[i] - dt * (u[i] * du_dx + dp_dx[i] / rho) + nu * dt * (u[i+1] - 2*u[i] + u[i-1]) / dx**2

    return u_new

# Time-stepping loop
u_history = []
for t in range(Nt):
    u = update_velocity(u, p, nu, dx, dt, rho)
    u_history.append(u.copy())

# Convert u_history to a numpy array for easy plotting
u_history = np.array(u_history)

# Plot results
plt.figure(figsize=(12, 6))

# Plot velocity profiles over time
plt.subplot(1, 2, 1)
for i in range(0, Nt, Nt//10):
    plt.plot(np.linspace(0, L, Nx), u_history[i], label=f"t = {i*dt:.2f}s")
plt.xlabel("Position (m)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity Profiles Over Time")
plt.legend()

# Plot velocity at the final time step
plt.subplot(1, 2, 2)
plt.plot(np.linspace(0, L, Nx), u_history[-1], label="Final velocity profile")
plt.xlabel("Position (m)")
plt.ylabel("Velocity (m/s)")
plt.title("Final Velocity Profile")
plt.legend()

plt.tight_layout()
plt.show()
