
# train.py
import json

# Sample training data: hours studied and exam marks
hours = [1, 2, 3, 4, 5]
marks = [20, 30, 40, 50, 60]

# Simple linear model: marks = slope * hours + intercept
slope = (
    sum((x - sum(hours) / len(hours)) *
        (y - sum(marks) / len(marks))
        for x, y in zip(hours, marks))
    / sum((x - sum(hours) / len(hours)) ** 2 for x in hours)
)

intercept = sum(marks) / len(marks) - slope * sum(hours) / len(hours)

model = {"slope": slope, "intercept": intercept}

with open("model.json", "w") as file:
    json.dump(model, file)

prediction = slope * 6 + intercept
print(f"Model trained successfully!")
print(f"Predicted marks for 6 hours: {prediction:.1f}")
