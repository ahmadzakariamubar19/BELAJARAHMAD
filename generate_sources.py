import os

experts = [
    {
        "name": "Chris Walker",
        "platform": "YouTube",
        "link": "https://youtube.com/@chriswalker",
        "why": "Strong B2B SaaS demand generation operator",
        "focus": "Demand Gen"
    },
    {
        "name": "Dave Gerhardt",
        "platform": "LinkedIn",
        "link": "https://linkedin.com/in/davegerhardt",
        "why": "Strong B2B brand-led growth strategist",
        "focus": "Brand"
    },
    {
        "name": "Alex Hormozi",
        "platform": "YouTube",
        "link": "https://youtube.com/@AlexHormozi",
        "why": "Excellent hooks and audience capture",
        "focus": "Hooks"
    }
]

os.makedirs("research", exist_ok=True)

with open("research/sources.md", "w") as f:
    f.write("# Sources\n\n")
    f.write("| Expert | Platform | Link | Why Chosen | Focus |\n")
    f.write("|---|---|---|---|---|\n")

    for e in experts:
        f.write(
            f"| {e['name']} | {e['platform']} | {e['link']} | {e['why']} | {e['focus']} |\n"
        )

print("sources.md generated successfully!")
