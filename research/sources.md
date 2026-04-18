data = [
    ["Chris Walker", "YouTube", "[https://youtube.com/@chriswalker](https://youtube.com/@chriswalker)", "Strong B2B demand generation expert"],
    ["Dave Gerhardt", "LinkedIn", "[https://linkedin.com/in/davegerhardt](https://linkedin.com/in/davegerhardt)", "Strong B2B branding expert"],
    ["Alex Hormozi", "YouTube", "[https://youtube.com/@AlexHormozi](https://youtube.com/@AlexHormozi)", "Great content hooks and offers"]
]

with open("research/sources.md", "w") as f:
    f.write("# Sources\n\n")
    f.write("| Expert | Platform | Link | Why Chosen |\n")
    f.write("|---|---|---|---|\n")

```
for row in data:
    f.write(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |\n")
```

print("sources.md created successfully!")