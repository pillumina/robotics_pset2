import Agent
import Env
import Policy
import State
import time


############################################################
## initialize the state, policy, discount and agent
agent = Agent.Agent(6,6,0)
policy = Policy.Policy()
init_state = State.State(1, 4, 6)
discount = 0.9

############################################################

############################################################
## 3(c) 3(e)
# agent.plot_trajectory(policy, init_state, 0)
# value = agent.policy_eval(policy, 0.9)
# print("The value of trajectory in 3(c) is, ", value[6][1][4])
############################################################



###########################################################
## 3(g), 3(h), 3(i)  Policy Iteration
start_time = time.time()

opt_policy, opt_value = agent.policy_iter(policy, discount)

end_time = time.time()
diff_time = end_time - start_time

print("3(i) running time: ", diff_time, "s")

agent.plot_trajectory(opt_policy, init_state, 0)
###########################################################

###########################################################
# # 4(b), 4(c)   Value Iteration
#
# start_time = time.time()
# opt_policy, opt_value = agent.value_iter(discount)
# end_time = time.time()
# diff_time = end_time - start_time
# print ("4(c) running time: ", diff_time, "s")
# agent.plot_trajectory(opt_policy, init_state, 0)
###########################################################


###########################################################
## 5(a) Recompute 3(c) with pe=25%
# agent.plot_trajectory(policy, init_state, 0.25)
# value = agent.policy_eval(policy, 0.9)
# print("The value of trajectory in 5(a) is, ", value[6][1][4])
###########################################################

###########################################################
## 5(b) Modified reward function
# agent.plot_trajectory(policy, init_state, 0.25)
# value = agent.policy_eval(policy, True, 0.9)
# print("The value of trajectory in 5(a) is, ", value[6][1][4])
###########################################################