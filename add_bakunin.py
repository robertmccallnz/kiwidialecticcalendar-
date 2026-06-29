"""Append Bakunin mō Aotearoa as the final course in the AI Warrior thinkers series."""
import json, pathlib

p = pathlib.Path("/tmp/kdcal/courses.json")
data = json.loads(p.read_text())

bakunin = {
    "title": "Tangi o te Tāheke — Bakunin mō Aotearoa",
    "slug": "bakunin-mo-aotearoa",
    "status": "Upcoming",
    "access": "free_subscriber",
    "calendar_visibility": "public",
    "description": (
        "The final thinker in the AI Warrior series. Mikhail Bakunin's federalist, "
        "anti-authoritarian socialism — rendered for Aotearoa as a Zapatista-style "
        "kaupapa of autonomous communes, mana motuhake, and refusal of the state-capital "
        "machine. Six lessons. The waterfall tears down what dams the awa."
    ),
    "lessons": [
        {
            "title": "Course launch — Tangi o te Tāheke",
            "date": "2026-07-04",
            "time": "19:00",
            "location": "Substack",
            "access": "free_subscriber",
            "calendar_visibility": "public",
            "teaser": "The cry of the waterfall. Why Bakunin, why Aotearoa, why now — and how this course closes the AI Warrior thinkers series.",
            "link": "https://www.kiwidialectic.com/p/bakunin-mo-aotearoa-course-launch"
        },
        {
            "title": "Lesson 1: Ko wai a Bakunin? — the man Marx feared",
            "date": "2026-07-05",
            "time": "19:00",
            "location": "Substack",
            "access": "free_subscriber",
            "calendar_visibility": "public",
            "teaser": "The Russian who split the First International, defended the Paris Commune, and warned that any state — even a workers' state — becomes a new prison.",
            "link": "https://www.kiwidialectic.com/p/bakunin-mo-aotearoa-lesson-1-ko-wai"
        },
        {
            "title": "Lesson 2: Mana motuhake — federation from below, not the state from above",
            "date": "2026-07-12",
            "time": "19:00",
            "location": "Substack",
            "access": "free_subscriber",
            "calendar_visibility": "public",
            "teaser": "Bakunin's free federation read alongside He Whakaputanga and tino rangatiratanga. Power binds upward from the hapū, never downward from Wellington.",
            "link": "https://www.kiwidialectic.com/p/bakunin-mo-aotearoa-lesson-2-mana-motuhake"
        },
        {
            "title": "Lesson 3: Te tāheke — the passion for destruction is also a creative passion",
            "date": "2026-07-19",
            "time": "19:00",
            "location": "Substack",
            "access": "free_subscriber",
            "calendar_visibility": "public",
            "teaser": "How to tear down without nihilism. The waterfall as kaupapa: what falls feeds the awa, what is demolished irrigates the kāinga.",
            "link": "https://www.kiwidialectic.com/p/bakunin-mo-aotearoa-lesson-3-te-taheke"
        },
        {
            "title": "Lesson 4: Caracoles in the kāinga — a Zapatista reading for Aotearoa",
            "date": "2026-07-26",
            "time": "19:00",
            "location": "Substack",
            "access": "free_subscriber",
            "calendar_visibility": "public",
            "teaser": "Chiapas to Ōtepoti. Autonomous councils, mandar obedeciendo, and what a Kiwi caracol looks like — marae, co-ops, learning circles, mutual-aid pātaka.",
            "link": "https://www.kiwidialectic.com/p/bakunin-mo-aotearoa-lesson-4-caracoles"
        },
        {
            "title": "Lesson 5: Refusing the algorithmic Leviathan — anarchism in the age of AI",
            "date": "2026-08-02",
            "time": "19:00",
            "location": "Substack",
            "access": "free_subscriber",
            "calendar_visibility": "public",
            "teaser": "Bakunin called the state a machine. The machine is now literal. How federation, encryption, and refusal apply to platform capital and state AI.",
            "link": "https://www.kiwidialectic.com/p/bakunin-mo-aotearoa-lesson-5-algorithmic-leviathan"
        },
        {
            "title": "Lesson 6: Arm the class — closing the AI Warrior thinkers series",
            "date": "2026-08-09",
            "time": "19:00",
            "location": "Substack",
            "access": "free_subscriber",
            "calendar_visibility": "public",
            "teaser": "From Gramsci to Bakunin in six thinkers. The toolkit, the refrain, the kaupapa for the next decade. E kore e mau te rongo ki te whenua kāore e watea.",
            "link": "https://www.kiwidialectic.com/p/bakunin-mo-aotearoa-lesson-6-arm-the-class"
        }
    ]
}

# Replace if already present, else append
data["courses"] = [c for c in data["courses"] if c.get("slug") != bakunin["slug"]]
data["courses"].append(bakunin)
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("Bakunin course appended. Total courses:", len(data["courses"]))
