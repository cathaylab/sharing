## TOPIC
* [What is markov chain?](https://en.wikipedia.org/wiki/Markov_chain)
	1. 無記憶: 下一狀態的機率分布只能由當前狀態決定
	2. 有現狀態 + 轉移機率

* What is markov decision process?
	1. agent, states, possible actions, transition probs, rewards
	2. agent’s goal is to find a policy that will maximize rewards over time

* Bellman Optimality Equation & Value Iteration 
	1. estimate the optimal state value of any state s
	2. estimating a potentially infinite sum of discounted future rewards

* Q-Value Iteration
	1. state-action values
	2. Code example

* What is Q-Learning?
	1. agent initially has no idea what the transition probabilities are (it does not know T(s, a, s′))
	2. it does not know what the rewards are going to be either (it does not know R(s, a, s′)).

* Q-Learning using an exploration function

* MDP Example:
	1. car (cold, hot, overheat)
	2. hippo (sleep, running, retrying, dead)
	3. stocks (not hold, holding)