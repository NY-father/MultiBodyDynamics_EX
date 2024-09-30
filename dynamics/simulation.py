# dynamics/simulation.py

from pydy.system import System
from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame, Point, RigidBody, inertia, Lagrangian, KanesMethod
import numpy as np
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self, settings, bodies, joints, loads):
        self.time_step = settings['time_step']
        self.duration = settings['duration']
        self.bodies = bodies        # List of BodyItem objects
        self.joints = joints        # List of Joint objects
        self.loads = loads          # List of Load objects

    def run(self):
        try:
            # Step 1: Check if joints are defined
            if not self.joints:
                raise ValueError("No joints defined in the system.")

            # Step 2: Define generalized coordinates and speeds
            num_joints = len(self.joints)
            q = dynamicsymbols('q1:%d' % (num_joints + 1))  # q1, q2, ..., qn
            u = dynamicsymbols('u1:%d' % (num_joints + 1))  # u1, u2, ..., un

            # Step 3: Define Reference Frames
            N = ReferenceFrame('N')  # Inertial frame
            frames = [N]
            for i in range(num_joints):
                frames.append(frames[i].orientnew('F{}'.format(i+1), 'Axis', (q[i], N.z)))

            # Step 4: Define Points and Orientations
            points = [Point('O')]
            points[0].set_vel(N, 0)
            for i in range(num_joints):
                # Access points via the 'body' attribute
                body_item = self.bodies[i]
                p = points[i].locatenew('P{}'.format(i+1), body_item.body.point2 - body_item.body.point1)
                p.set_vel(N, points[i].v2pt_theory(points[i], N, frames[i]))
                points.append(p)

            # Step 5: Define Rigid Bodies
            rigid_bodies = []
            for i, body_item in enumerate(self.bodies):
                mass = body_item.body.mass
                inertia_val = body_item.body.inertia
                # Assuming planar motion, inertia tensor simplifies
                body_inertia = inertia(N, 0, 0, inertia_val)
                body = RigidBody('Body{}'.format(i+1), points[i+1], frames[i+1], (mass, body_inertia))
                rigid_bodies.append(body)

            # Step 6: Define Forces (Loads)
            forces = []
            for load in self.loads:
                torque = load.torque
                joint = load.joint  # Assuming 'joint' is a reference to a Joint object

                # Find the corresponding point for the joint
                joint_point = None
                for p in points:
                    if p.name == joint.position.name:
                        joint_point = p
                        break
                if joint_point:
                    forces.append((joint_point, torque * N.z))
                else:
                    print(f"Warning: Joint point {joint.position} not found among points.")

            # Step 7: Create Lagrangian
            kinetic = sum([body.kinetic_energy for body in rigid_bodies])
            potential = sum([body.potential_energy for body in rigid_bodies])
            L = Lagrangian(N, kinetic - potential)

            # Step 8: Apply Lagrange's Equations using KanesMethod
            kanes_method = KanesMethod(N, q_ind=q, u_ind=u)
            fr, frstar = kanes_method.kanes_equations(L, forces)

            # Step 9: Formulate the System
            system = System(fr, frstar, kanes_method)

            # Step 10: Integrate the Equations of Motion
            t = np.linspace(0, self.duration, int(self.duration / self.time_step) + 1)
            initial_conditions = np.zeros(2 * num_joints)  # Assuming zero initial displacement and velocity

        except AttributeError as e:
            print(f"Attribute Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Step 11: Visualize or Process Results
        self.visualize(solution, t)

    def visualize(self, solution, t):
        # Implement visualization of the simulation results
        plt.figure(figsize=(10, 6))
        for i in range(len(solution.q)):
            plt.plot(t, solution.q[i], label=f'θ{i+1}')
        plt.xlabel('Time (s)')
        plt.ylabel('Generalized Coordinates (Radians)')
        plt.title('Simulation Results')
        plt.legend()
        plt.grid(True)
        plt.show()
