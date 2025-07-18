import pyperclip
import time
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

credentials, project_id = google.auth.default()

vertexai.init(project="generalpurposeai", location="us-central1")

model = GenerativeModel(model_name="gemini-2.0-flash")

def get_ai_scores(project_details, project_type):
    prompt = f"""I'm a freelance software developer and I have recently recieved a project with requirements: {project_details}
I wish to consult you on the difficulty aspects of the project. You are to give me a score out of 10 for each of the following categories and format it like this:
- Complexity: [Insert Score here]/10
- Time Required: [Insert Score here]/10
- Expertise Needed: [Insert Score here]/10
- Resources: [Insert Score here]/10
Also take into account that it is a {project_type} project. Give the response exactly like above."""
    responses = model.generate_content(prompt)
    return responses.text

# Define base cost and weighting factors
project_costs = {"1": 2, "2": 7.5, "3": 15} 
project_types = """1. Small-Scale Simple Project
2. Medium-Scale Project
3. Large-Scale Project"""
project_input = "0"
project_type = ""
while project_input not in list(project_costs.keys()):
    print(project_types)
    project_input = input("Enter a project number to calculate price for: ")
    if project_input not in list(project_costs.keys()):
        print("Invalid project number entered. Please try again!")
    else:
        if project_input == "1":
            project_type = "Small-scale"
        elif project_input == "2":
            project_type = "Medium-scale"
        else:
            project_type = "Large-scale"
base_cost = project_costs[project_input]
weights = [0.3, 0.3, 0.25, 0.15]  # Weighting for each factor (should sum to 1)

# Get user input for difficulty scores
factors = ["Complexity", "Time Required", "Expertise Needed", "Resources"]
scores = []

time.sleep(1)
print()
project_details = input("Enter the project details as provided by the client: ")
ai_scores = get_ai_scores(project_details, project_type)
complexity = ai_scores.find("Complexity")
project_time = ai_scores.find("Time Required")
expertise = ai_scores.find("Expertise Needed")
resources = ai_scores.find("Resources")
scores.append(int(ai_scores[complexity+12:complexity+13]))
scores.append(int(ai_scores[project_time+15:project_time+16]))
scores.append(int(ai_scores[expertise+18:expertise+19]))
scores.append(int(ai_scores[resources+11:resources+12]))

# Compute total cost
difficulty_multiplier = sum(score * weight for score, weight in zip(scores, weights)) / 10
final_cost = base_cost * (1 + difficulty_multiplier)

time.sleep(2)
print()
source_code = input("Is the source code included with this project? (Y/N) ")
if source_code:
    if project_input == "1":
        final_cost += 0.99
    elif project_input == "2":
        final_cost += 1.99
    else:
        final_cost += 2.99
print()
discount = input("Do you wish to apply a discount? (Y/N) ")
discount_percentage = 0
if discount.upper() == "Y":
    print(f"Current cost before the discount is: £{final_cost:.2f}")
    while True:
        try:
            discount_percentage = int(input("Enter the discount percentage: "))
            final_cost = final_cost * (1 - (discount_percentage / 100))
            break
        except:
            print("The percentage must be a whole number. Please try again!")

time.sleep(3)
print()
print(f"Final Project Cost: £{final_cost:.2f}")

time.sleep(4)
print()
complexity_cost = (scores[0] * weights[0]) / 10
time_cost = (scores[1] * weights[1]) / 10
expertise_cost = (scores[2] * weights[2]) / 10
resources_cost = (scores[3] * weights[3]) / 10
project_breakdown = f"""The Final Project Cost is as follows: £{final_cost:.2f}
Based on the following factors:
Base cost (due to project type) - £{base_cost:.2f}
Complexity score - {scores[0]}/10
Time score - {scores[1]}/10
Expertise score - {scores[2]}/10
Resources score - {scores[3]}/10
Total multiplier - {1 + difficulty_multiplier:.2f}
Source code included - {source_code}
Discount percentage: {discount_percentage}%"""
pyperclip.copy(project_breakdown)
print("Project breakdown copied!")



