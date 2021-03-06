
class environment:
    def __init__(self):
        self.width = 5
        self.height = 5
        self.state = [(i,j) for i in range(self.height) for j in range(self.width)]
        self.reward = [[0.]*self.width for _ in range(self.height)]
        self.reward[2][2] = 1.
        self.reward[1][2] = -1.
        self.reward[2][1] = -1.
        self.discount_factor = 0.9
        self.move_step = [(-1,0),(1,0),(0,-1),(0,1)] #상,하,좌,우

    def _step(self, state, action):
        # 동작 수행
        # 다음 상태와 리워드 반환
        next_state = self.state_after_action(state, action)
        immediate_reward = self.reward[next_state[0]][next_state[1]]
        return next_state, immediate_reward

    def _reset(self):
        # 환경 초기화
        return NotImplementedError

    def _render(self):
        # 화면으로 보여주기
        return NotImplementedError

    def state_after_action(self, state, action):
        step = self.move_step[action]
        return self.check_boundary([state[0] + step[0], state[1] + step[1]])

    def check_boundary(self, state):
        state[0] = (0 if state[0] < 0 else self.width - 1
                    if state[0] > self.width - 1 else state[0])
        state[1] = (0 if state[1] < 0 else self.height - 1
                    if state[1] > self.height - 1 else state[1])
        return state

class value_iter_agent:
    def __init__(self, env):
        self.env = env
        self.value_table = [[0.] * self.env.width for _ in range(self.env.height)]
        self.possible_actions = [0, 1, 2, 3] # 상, 하, 좌, 우

    def value_iter(self):
        # k+1 가치함수 테이블 선언
        new_value_table = [[0.] * self.env.width for _ in range(self.env.height)]

        # k 가치함수 테이블에서 k+1 가치함수 테이블 값 구하기
        for state in self.env.state:
            if state == (2, 2):
                ## Q. 해당 터미널 스테이트의 가치는 높을수록 좋은 것이 아닌가?
                new_value_table[2][2] = 0.0
                continue

            value_list = []
            # 벨만 기대 방정식
            for action in self.possible_actions:
                next_state, reward = self.env._step(state, action)
                new_value = reward + self.env.discount_factor * self.value_table[next_state[0]][next_state[1]]
                value_list.append(new_value)
            new_value_table[state[0]][state[1]] = round(max(value_list), 2)
        self.value_table = new_value_table

if __name__ == "__main__":
    env = environment()
    agent = value_iter_agent(env)

    agent.value_table

    for i in range(10):
        agent.value_iter()
