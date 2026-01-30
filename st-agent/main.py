from agent import Agent

agent = Agent()

# -----------------------------
# Task 1: Time in Cape Town + UTC
# -----------------------------
print("\n=== Multi-Step Task 1: Time in Cape Town + UTC ===")
tool_calls1 = agent.mock_model("What time is it in Cape Town and what is that in UTC?")
results1 = agent.run_tool_sequence(tool_calls1)

final_time = results1[0].get("time", "unknown")
final_utc = results1[1].get("utc_time", "unknown")
print("Agent final output:", results1)
print(f"Final Answer: The time in Cape Town is {final_time}, which is {final_utc} UTC.")

# -----------------------------
# Task 2: 18% of 24,500
# -----------------------------
print("\n=== Multi-Step Task 2: 18% of 24,500 ===")
tool_calls2 = agent.mock_model("What is 18% of 24,500?")
results2 = agent.run_tool_sequence(tool_calls2)

calc_result = results2[0].get("result", "unknown")
print("Agent final output:", results2)
print(f"Final Answer: 18% of 24,500 is {calc_result}. Calculation: 24500 * 0.18 = {calc_result}")
