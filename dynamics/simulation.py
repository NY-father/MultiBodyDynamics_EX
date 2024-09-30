from pydy.system import System
from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame, Point, RigidBody, inertia, KanesMethod
from sympy import symbols
import numpy as np
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self, settings, bodies, joints, loads):
        self.time_step = settings['time_step']
        self.duration = settings['duration']
        self.bodies = bodies        # BodyItem 객체들의 리스트
        self.joints = joints        # Joint 객체들의 리스트
        self.loads = loads          # Load 객체들의 리스트

    def run(self):
        try:
            # Step 1: 조인트가 정의되었는지 확인
            if not self.joints:
                raise ValueError("시스템에 조인트가 정의되지 않았습니다.")

            # Step 2: 일반화 좌표(q)와 일반화 속도(u) 정의
            num_bodies = len(self.bodies)
            q = dynamicsymbols(f'q1:{num_bodies + 1}')  # q1, q2, ..., qn
            u = dynamicsymbols(f'u1:{num_bodies + 1}')  # u1, u2, ..., un

            # Step 3: 기준 프레임 정의
            N = ReferenceFrame('N')  # 관성 프레임
            frames = [N]
            for i in range(num_bodies):
                parent_frame = frames[i]  # 이전 프레임을 부모로 설정
                Fi = parent_frame.orientnew(f'F{i+1}', 'Axis', (q[i], N.z))
                Fi.set_ang_vel(parent_frame, u[i] * N.z)
                frames.append(Fi)

            # Step 4: 점과 위치 정의
            points = [Point('O')]
            points[0].set_vel(N, 0)
            for i in range(num_bodies):
                body_item = self.bodies[i]
                length = body_item.body.length
                p = points[i].locatenew(f'P{i+1}', length * frames[i+1].x)
                p.v2pt_theory(points[i], N, frames[i+1])
                points.append(p)

            # Step 5: 강체 정의
            rigid_bodies = []
            for i, body_item in enumerate(self.bodies):
                mass = body_item.body.mass
                inertia_val = body_item.body.inertia
                body_inertia = inertia(frames[i+1], 0, 0, inertia_val)
                body = RigidBody(f'Body{i+1}', points[i+1], frames[i+1], mass, (body_inertia, points[i+1]))
                rigid_bodies.append(body)

            # Step 6: 힘(하중) 정의
            forces = []
            for load in self.loads:
                torque = load.torque
                joint_index = self.joints.index(load.joint)
                forces.append((frames[joint_index + 1], torque * N.z))

            # 중력 추가
            g = symbols('g')
            gravity = -g * N.y
            for body in rigid_bodies:
                mass = body.mass
                center_of_mass = body.masscenter
                forces.append((center_of_mass, mass * gravity))

            # Step 7: KanesMethod 적용 (kd_eqs 포함)
            kinematic_differential_equations = [qi.diff(symbols('t')) - ui for qi, ui in zip(q, u)]
            km = KanesMethod(N, q_ind=q, u_ind=u, kd_eqs=kinematic_differential_equations)
            fr, frstar = km.kanes_equations(loads=forces, bodies=rigid_bodies)

            # Step 8: 수치적분 준비
            from sympy.utilities.lambdify import lambdify
            from scipy.integrate import odeint

            # 상태 변수와 파라미터 정의
            state_vars = q + u
            parameters = [g]

            # rhs_func 생성
            rhs_func = lambdify(state_vars + parameters, km.rhs(), modules='numpy')

            # 초기 조건 설정 (좌표와 속도 모두 0)
            initial_conditions = np.zeros(len(q) + len(u))

            t = np.linspace(0, self.duration, int(self.duration / self.time_step) + 1)

            # 중력 상수 값 지정 (예: 9.81 m/s^2)
            g_val = 9.81

            # 방정식 적분
            def equations(y, t):
                # y를 q와 u로 분할
                q_vals = y[:len(q)]
                u_vals = y[len(q):]
                # 입력 값 생성 (상수 포함)
                input_vals = np.concatenate((q_vals, u_vals, [g_val]))
                # dydt 계산 (dq/dt와 du/dt 모두 포함)
                dydt = rhs_func(*input_vals)
                dydt = np.array(dydt).flatten()
                return dydt

            solution = odeint(equations, initial_conditions, t)

        except AttributeError as e:
            import traceback
            print(f"Attribute Error: {e}")
            traceback.print_exc()
            return
        except Exception as e:
            import traceback
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            return

        # Step 9: 결과 시각화 또는 처리
        self.visualize(solution, t)

    def visualize(self, solution, t):
        plt.figure(figsize=(10, 6))
        num_coordinates = len(self.bodies)
        for i in range(num_coordinates):
            plt.plot(t, solution[:, i], label=f'θ{i+1}')
        plt.xlabel('시간 (초)')
        plt.ylabel('일반화 좌표 (라디안)')
        plt.title('시뮬레이션 결과')
        plt.legend()
        plt.grid(True)
        plt.show()
