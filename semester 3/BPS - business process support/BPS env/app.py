import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Planet data: [size, distance, speed, color, tilt_angle]
PLANETS = {
    'Sun': [20, 0, 0, 'yellow', 0],
    'Mercury': [4, 30, 4.1, 'gray', 7],
    'Venus': [6, 45, 1.6, 'orange', 3],
    'Earth': [7, 65, 1, 'blue', 23.5],
    'Mars': [5, 85, 0.5, 'red', 25],
    'Jupiter': [15, 120, 0.08, 'burlywood', 3],
    'Saturn': [12, 150, 0.03, 'khaki', 27]
}

# Setup 3D plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Initialize planet objects
planets_scatter = {}
orbit_lines = {}

# Create orbit paths and planets
for name, (size, distance, speed, color, tilt) in PLANETS.items():
    if distance > 0:
        theta = np.linspace(0, 2*np.pi, 100)
        # Create tilted orbital path
        x = distance * np.cos(theta)
        y = distance * np.sin(theta)
        z = distance * np.sin(theta) * np.sin(np.radians(tilt))
        orbit_lines[name] = ax.plot(x, y, z, '--', color='gray', alpha=0.3)[0]
    
    planets_scatter[name] = ax.scatter([], [], [], s=size**2, color=color, label=name)

# Set view limits
limit = 180
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_zlim(-limit, limit)

# Add legend
ax.legend(loc='upper right')

def update(frame):
    objects = []
    for name, (size, distance, speed, color, tilt) in PLANETS.items():
        if name != 'Sun':
            # Calculate planet position with tilt
            angle = frame * speed
            x = distance * np.cos(angle)
            y = distance * np.sin(angle)
            z = distance * np.sin(angle) * np.sin(np.radians(tilt))
            planets_scatter[name].set_offsets([[x, y]])
            planets_scatter[name]._offsets3d = ([x], [y], [z])
        objects.append(planets_scatter[name])
    
    # Sun stays at center
    planets_scatter['Sun']._offsets3d = ([0], [0], [0])
    return objects

# Create animation
anim = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    interval=50, blit=False, repeat=True)

# Set title and labels
ax.set_title('3D Solar System', color='white')
ax.set_xlabel('X', color='white')
ax.set_ylabel('Y', color='white')
ax.set_zlabel('Z', color='white')

# Set grid color
ax.xaxis.line.set_color('white')
ax.yaxis.line.set_color('white')
ax.zaxis.line.set_color('white')

plt.show()