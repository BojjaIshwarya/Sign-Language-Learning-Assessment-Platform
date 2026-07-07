from ai.assessment import assess_sign

result = assess_sign(
    expected_label="A",
    predicted_label="B",
    confidence=0.96
)

print(result)
