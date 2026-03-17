from models.question import Question, QuestionMeta, QuestionOption
from models.career import Career, CareerTrait, CareerTag, CareerReason, CareerRole
from models.career_roadmap import CareerRoadmap
from database import db


def get_fallback_catalog():
    questions = [
        {
            "id": "path",
            "text": "Which career paths do you want to explore right now?",
            "type": "single",
            "required": True,
            "why": "We use this to filter recommendations so you see technical, non-technical, or both.",
            "options": [
                {
                    "label": "Technical",
                    "value": "technical",
                    "detail": "Engineering, data, and software-heavy roles.",
                    "traits": {"technical_interest": 0.9, "coding": 0.7},
                },
                {
                    "label": "Non-Technical",
                    "value": "non-technical",
                    "detail": "Business, creative, people, and operations roles.",
                    "traits": {"people_focus": 0.7, "business": 0.6},
                },
                {
                    "label": "Both",
                    "value": "both",
                    "detail": "Show a full mix across the spectrum.",
                    "traits": {"versatility": 0.8},
                },
            ],
        },
        {
            "id": "interests",
            "text": "Which domains spark your curiosity the most?",
            "type": "multi",
            "required": True,
            "why": "Your interests are a strong signal for long-term motivation.",
            "options": [
                {"label": "AI and Machine Learning", "value": "ai", "traits": {"data": 0.7, "research": 0.6}},
                {"label": "Web and Product Experiences", "value": "web", "traits": {"product": 0.7, "design": 0.4}},
                {"label": "Mobile Apps", "value": "mobile", "traits": {"product": 0.5, "coding": 0.5}},
                {"label": "Data and Analytics", "value": "data", "traits": {"data": 0.8, "analytical": 0.6}},
                {"label": "Cybersecurity", "value": "security", "traits": {"analytical": 0.7, "systems": 0.6}},
                {"label": "Cloud and Infrastructure", "value": "cloud", "traits": {"systems": 0.7, "reliability": 0.6}},
                {"label": "Design and Creative", "value": "design", "traits": {"creativity": 0.8, "design": 0.8}},
                {"label": "Marketing and Growth", "value": "marketing", "traits": {"marketing": 0.8, "communication": 0.6}},
                {"label": "Business and Strategy", "value": "business", "traits": {"business": 0.8, "leadership": 0.5}},
                {"label": "People and Culture", "value": "people", "traits": {"empathy": 0.8, "communication": 0.6}},
                {"label": "Education and Training", "value": "education", "traits": {"teaching": 0.8, "communication": 0.6}},
                {"label": "Finance and Investing", "value": "finance", "traits": {"finance": 0.8, "analytical": 0.6}},
            ],
        },
        {
            "id": "workstyle",
            "text": "Which work style sounds most energizing?",
            "type": "single",
            "required": True,
            "why": "Work style helps match you with the right team environments.",
            "options": [
                {"label": "Deep focus time", "value": "focus", "detail": "Long stretches of independent work.", "traits": {"focus": 0.8}},
                {"label": "Collaborative sprints", "value": "team", "detail": "Fast-paced teamwork and alignment.", "traits": {"collaboration": 0.8, "communication": 0.6}},
                {"label": "Mixed", "value": "mixed", "detail": "A balance of solo and team time.", "traits": {"adaptability": 0.7}},
            ],
        },
        {
            "id": "problem_type",
            "text": "What kind of problems do you most enjoy solving?",
            "type": "multi",
            "required": True,
            "why": "Problem preferences map to career families.",
            "options": [
                {"label": "Building new products", "value": "build", "traits": {"product": 0.7, "creativity": 0.4}},
                {"label": "Optimizing systems", "value": "optimize", "traits": {"systems": 0.7, "analytical": 0.6}},
                {"label": "Helping people succeed", "value": "people_help", "traits": {"empathy": 0.7, "leadership": 0.4}},
                {"label": "Analyzing complex data", "value": "data", "traits": {"data": 0.8, "analytical": 0.6}},
                {"label": "Telling stories and crafting messages", "value": "story", "traits": {"writing": 0.8, "creativity": 0.5}},
                {"label": "Planning and organizing operations", "value": "ops", "traits": {"organization": 0.8, "leadership": 0.4}},
            ],
        },
        {
            "id": "coding_interest",
            "text": "How much do you enjoy coding or technical problem solving?",
            "type": "scale",
            "trait": "coding",
            "required": True,
            "why": "This decides how technical your recommendations should be.",
            "minLabel": "Not at all",
            "maxLabel": "Love it",
            "evidenceHigh": "You enjoy coding and technical problem solving.",
            "evidenceLow": "You prefer roles with less coding.",
        },
        {
            "id": "language_preference",
            "text": "If you are technical, which languages do you prefer or want to learn?",
            "type": "multi",
            "required": False,
            "why": "Language preference helps route you to the right technical specializations.",
            "options": [
                {"label": "Python", "value": "python", "traits": {"data": 0.4, "coding": 0.3}},
                {"label": "JavaScript or TypeScript", "value": "javascript", "traits": {"product": 0.4, "coding": 0.3}},
                {"label": "Java or Kotlin", "value": "java", "traits": {"systems": 0.3, "coding": 0.3}},
                {"label": "C# or .NET", "value": "csharp", "traits": {"systems": 0.3, "coding": 0.3}},
                {"label": "C or C++", "value": "cpp", "traits": {"systems": 0.5, "analytical": 0.3}},
                {"label": "Go", "value": "go", "traits": {"systems": 0.5, "reliability": 0.4}},
                {"label": "Rust", "value": "rust", "traits": {"systems": 0.6, "analytical": 0.4}},
                {"label": "SQL", "value": "sql", "traits": {"data": 0.5, "analytical": 0.4}},
                {"label": "Swift or Objective-C", "value": "swift", "traits": {"product": 0.4, "coding": 0.3}},
            ],
        },
        {
            "id": "math_comfort",
            "text": "How comfortable are you with math and quantitative reasoning?",
            "type": "scale",
            "trait": "analytical",
            "required": True,
            "why": "Many data and engineering roles depend on quantitative strength.",
            "minLabel": "Not comfortable",
            "maxLabel": "Very comfortable",
            "evidenceHigh": "You are confident with quantitative reasoning.",
            "evidenceLow": "You prefer roles that are less math-heavy.",
        },
        {
            "id": "creativity",
            "text": "How important is creativity in your day-to-day work?",
            "type": "scale",
            "trait": "creativity",
            "required": True,
            "why": "Creative drive guides design, marketing, and product roles.",
            "minLabel": "Not important",
            "maxLabel": "Essential",
            "evidenceHigh": "You want creativity to be a core part of your work.",
        },
        {
            "id": "communication",
            "text": "How much do you enjoy communicating ideas and influencing others?",
            "type": "scale",
            "trait": "communication",
            "required": True,
            "why": "Communication strength aligns with leadership, marketing, and client-facing paths.",
            "minLabel": "Not much",
            "maxLabel": "A lot",
            "evidenceHigh": "You enjoy communicating and influencing others.",
        },
        {
            "id": "people_focus",
            "text": "How much do you like working directly with people?",
            "type": "scale",
            "trait": "people_focus",
            "required": True,
            "why": "People-oriented roles need strong interpersonal energy.",
            "minLabel": "Prefer solo",
            "maxLabel": "Love people work",
            "evidenceHigh": "You like working directly with people.",
        },
        {
            "id": "leadership",
            "text": "How excited are you to lead or coordinate teams?",
            "type": "scale",
            "trait": "leadership",
            "required": True,
            "why": "Leadership intent helps match you to management, product, and strategy roles.",
            "minLabel": "Not interested",
            "maxLabel": "Very excited",
            "evidenceHigh": "You are open to leading or coordinating teams.",
        },
        {
            "id": "organization",
            "text": "How much do you enjoy planning, organizing, and process building?",
            "type": "scale",
            "trait": "organization",
            "required": True,
            "why": "Operational roles rely on planning and process ownership.",
            "minLabel": "Not much",
            "maxLabel": "A lot",
            "evidenceHigh": "You enjoy organizing and building processes.",
        },
        {
            "id": "design_interest",
            "text": "How interested are you in visual design or user experience?",
            "type": "scale",
            "trait": "design",
            "required": True,
            "why": "Design interest indicates fit for UX, product, and creative roles.",
            "minLabel": "Not interested",
            "maxLabel": "Very interested",
            "evidenceHigh": "You are drawn to visual design and user experience.",
        },
        {
            "id": "writing_interest",
            "text": "How much do you enjoy writing or storytelling?",
            "type": "scale",
            "trait": "writing",
            "required": True,
            "why": "Writing ability powers content, marketing, and knowledge roles.",
            "minLabel": "Not much",
            "maxLabel": "A lot",
            "evidenceHigh": "You enjoy writing and storytelling.",
        },
        {
            "id": "business_interest",
            "text": "How interested are you in business strategy and market thinking?",
            "type": "scale",
            "trait": "business",
            "required": True,
            "why": "Business interest helps match you to strategy, operations, and growth roles.",
            "minLabel": "Not interested",
            "maxLabel": "Very interested",
            "evidenceHigh": "You are interested in business and market strategy.",
        },
        {
            "id": "marketing_interest",
            "text": "How interested are you in branding, positioning, or growth marketing?",
            "type": "scale",
            "trait": "marketing",
            "required": True,
            "why": "Marketing interest aligns with growth, brand, and go-to-market paths.",
            "minLabel": "Not interested",
            "maxLabel": "Very interested",
            "evidenceHigh": "You are interested in branding and growth marketing.",
        },
        {
            "id": "data_interest",
            "text": "How excited are you about working with data, dashboards, or analytics?",
            "type": "scale",
            "trait": "data",
            "required": True,
            "why": "Data enthusiasm is crucial for analytics and research roles.",
            "minLabel": "Not excited",
            "maxLabel": "Very excited",
            "evidenceHigh": "You are excited about working with data and analytics.",
        },
        {
            "id": "systems_interest",
            "text": "How interested are you in systems, infrastructure, or reliability?",
            "type": "scale",
            "trait": "systems",
            "required": True,
            "why": "Systems interest supports cloud, DevOps, and backend engineering paths.",
            "minLabel": "Not interested",
            "maxLabel": "Very interested",
            "evidenceHigh": "You are interested in systems and infrastructure work.",
        },
        {
            "id": "teaching_interest",
            "text": "How much do you enjoy teaching or mentoring others?",
            "type": "scale",
            "trait": "teaching",
            "required": True,
            "why": "Teaching interest matters for education, enablement, and coaching careers.",
            "minLabel": "Not much",
            "maxLabel": "A lot",
            "evidenceHigh": "You enjoy teaching or mentoring others.",
        },
        {
            "id": "risk_tolerance",
            "text": "How comfortable are you with ambiguity and risk?",
            "type": "scale",
            "trait": "entrepreneurship",
            "required": True,
            "why": "Entrepreneurial comfort influences startup, innovation, and leadership roles.",
            "minLabel": "Prefer stability",
            "maxLabel": "Enjoy risk",
            "evidenceHigh": "You are comfortable with ambiguity and risk.",
        },
        {
            "id": "hands_on",
            "text": "Do you prefer building things hands-on or more strategic work?",
            "type": "single",
            "required": True,
            "why": "This helps balance maker roles with strategy roles.",
            "options": [
                {"label": "Hands-on building", "value": "hands_on", "detail": "I like to build and ship.", "traits": {"maker": 0.8}},
                {"label": "Strategic planning", "value": "strategy", "detail": "I like planning and direction.", "traits": {"strategy": 0.8, "business": 0.4}},
                {"label": "Both", "value": "both", "detail": "I want a balance.", "traits": {"maker": 0.5, "strategy": 0.5}},
            ],
        },
        {
            "id": "collaboration",
            "text": "How do you prefer to collaborate?",
            "type": "single",
            "required": True,
            "why": "Collaboration style influences team fit and career environment.",
            "options": [
                {"label": "Small tight-knit team", "value": "small", "detail": "A few people, high trust.", "traits": {"collaboration": 0.6}},
                {"label": "Larger cross-functional teams", "value": "large", "detail": "Many roles working together.", "traits": {"collaboration": 0.8, "communication": 0.5}},
                {"label": "Mostly independent", "value": "solo", "detail": "Prefer solo ownership.", "traits": {"focus": 0.7}},
            ],
        },
        {
            "id": "impact",
            "text": "What kind of impact motivates you most?",
            "type": "single",
            "required": True,
            "why": "Impact type helps distinguish between mission-driven and commercial paths.",
            "options": [
                {"label": "Helping people directly", "value": "help", "detail": "Care, education, or community impact.", "traits": {"empathy": 0.8}},
                {"label": "Building successful products", "value": "product", "detail": "Creating something that scales.", "traits": {"product": 0.7}},
                {"label": "Driving revenue or growth", "value": "growth", "detail": "Business impact and market wins.", "traits": {"business": 0.6, "marketing": 0.5}},
                {"label": "Innovation and discovery", "value": "innovation", "detail": "Pushing into new ideas.", "traits": {"research": 0.6, "entrepreneurship": 0.4}},
            ],
        },
        {
            "id": "goal",
            "text": "What is your career goal over the next 1-2 years?",
            "type": "text",
            "required": False,
            "why": "We will use this to tailor your roadmap later.",
            "placeholder": "Example: Become a junior data analyst and work on real dashboards.",
        },
    ]

    careers = [
        {
            "name": "Software Engineer",
            "path": "technical",
            "tags": ["web", "mobile", "cloud"],
            "summary": "Builds scalable software products and platforms.",
            "traits": {"coding": 0.8, "systems": 0.6, "product": 0.5, "analytical": 0.6, "maker": 0.7},
            "roles": ["Frontend Engineer", "Backend Engineer", "Full-Stack Engineer"],
            "roadmap": ["Learn a core language", "Build 2-3 portfolio projects", "Ship a real app with users"],
        },
        {
            "name": "Data Analyst",
            "path": "technical",
            "tags": ["data", "finance"],
            "summary": "Turns data into insights with dashboards and analysis.",
            "traits": {"data": 0.8, "analytical": 0.7, "communication": 0.5, "organization": 0.4},
            "roles": ["BI Analyst", "Product Analyst", "Reporting Analyst"],
            "roadmap": ["Master SQL + spreadsheets", "Build a dashboard portfolio", "Practice storytelling with data"],
        },
        {
            "name": "Data Scientist",
            "path": "technical",
            "tags": ["ai", "data"],
            "summary": "Builds predictive models and experiments with ML.",
            "traits": {"data": 0.8, "analytical": 0.8, "research": 0.6, "coding": 0.6},
            "roles": ["ML Scientist", "Applied Data Scientist", "Research Analyst"],
            "roadmap": ["Learn Python + statistics", "Build ML projects", "Showcase experiments and insights"],
        },
        {
            "name": "Machine Learning Engineer",
            "path": "technical",
            "tags": ["ai", "cloud"],
            "summary": "Deploys ML models into production systems.",
            "traits": {"coding": 0.8, "systems": 0.7, "data": 0.7, "reliability": 0.6},
            "roles": ["MLOps Engineer", "Applied ML Engineer", "ML Platform Engineer"],
            "roadmap": ["Strengthen Python + ML basics", "Learn cloud deployment", "Ship an ML app end-to-end"],
        },
        {
            "name": "Cybersecurity Analyst",
            "path": "technical",
            "tags": ["security"],
            "summary": "Protects systems, audits risks, and responds to threats.",
            "traits": {"analytical": 0.7, "systems": 0.6, "focus": 0.6, "reliability": 0.6},
            "roles": ["SOC Analyst", "Security Engineer", "Threat Analyst"],
            "roadmap": ["Learn security fundamentals", "Practice labs and CTFs", "Document security case studies"],
        },
        {
            "name": "Cloud or DevOps Engineer",
            "path": "technical",
            "tags": ["cloud"],
            "summary": "Builds and maintains reliable infrastructure.",
            "traits": {"systems": 0.8, "reliability": 0.7, "coding": 0.5, "organization": 0.5},
            "roles": ["DevOps Engineer", "Site Reliability Engineer", "Platform Engineer"],
            "roadmap": ["Learn Linux + networking", "Deploy apps on cloud", "Automate infrastructure pipelines"],
        },
        {
            "name": "Product Manager",
            "path": "hybrid",
            "tags": ["web", "business"],
            "summary": "Defines product vision and aligns teams to deliver it.",
            "traits": {"product": 0.8, "leadership": 0.7, "communication": 0.7, "business": 0.6},
            "roles": ["Associate PM", "Product Owner", "Growth PM"],
            "roadmap": ["Study product discovery", "Run user interviews", "Ship a feature with metrics"],
        },
        {
            "name": "UX or Product Designer",
            "path": "non-technical",
            "tags": ["design", "web"],
            "summary": "Designs user experiences and visual systems.",
            "traits": {"design": 0.8, "creativity": 0.7, "empathy": 0.6, "communication": 0.5},
            "roles": ["UX Designer", "UI Designer", "Interaction Designer"],
            "roadmap": ["Learn design fundamentals", "Build case studies", "Conduct user research"],
        },
        {
            "name": "Digital Marketer",
            "path": "non-technical",
            "tags": ["marketing", "business"],
            "summary": "Grows audiences and drives product adoption.",
            "traits": {"marketing": 0.8, "communication": 0.7, "creativity": 0.6, "business": 0.5},
            "roles": ["Growth Marketer", "Content Marketer", "Performance Marketer"],
            "roadmap": ["Learn marketing channels", "Run a campaign", "Analyze performance metrics"],
        },
        {
            "name": "Business Analyst",
            "path": "non-technical",
            "tags": ["business", "finance"],
            "summary": "Improves business decisions through analysis.",
            "traits": {"business": 0.7, "analytical": 0.7, "organization": 0.6, "communication": 0.5},
            "roles": ["Strategy Analyst", "Operations Analyst", "Insights Analyst"],
            "roadmap": ["Learn business frameworks", "Build reporting models", "Present recommendations"],
        },
        {
            "name": "People Operations",
            "path": "non-technical",
            "tags": ["people"],
            "summary": "Builds a strong culture and employee experience.",
            "traits": {"empathy": 0.8, "communication": 0.7, "organization": 0.6, "leadership": 0.5},
            "roles": ["HR Generalist", "Talent Partner", "People Ops Manager"],
            "roadmap": ["Learn HR fundamentals", "Practice interviewing", "Design onboarding flows"],
        },
        {
            "name": "Sales or Business Development",
            "path": "non-technical",
            "tags": ["business", "marketing"],
            "summary": "Builds partnerships and drives revenue.",
            "traits": {"communication": 0.8, "business": 0.7, "leadership": 0.5, "marketing": 0.5},
            "roles": ["Account Executive", "Sales Development Rep", "Partnerships Manager"],
            "roadmap": ["Learn consultative selling", "Practice discovery calls", "Track pipeline metrics"],
        },
        {
            "name": "Project or Operations Manager",
            "path": "non-technical",
            "tags": ["business"],
            "summary": "Keeps cross-functional work moving smoothly.",
            "traits": {"organization": 0.8, "leadership": 0.6, "communication": 0.6, "strategy": 0.5},
            "roles": ["Project Manager", "Operations Lead", "Program Manager"],
            "roadmap": ["Learn project frameworks", "Run a cross-team project", "Track delivery metrics"],
        },
        {
            "name": "Content Strategist",
            "path": "non-technical",
            "tags": ["marketing", "education"],
            "summary": "Creates messaging, content systems, and storytelling.",
            "traits": {"writing": 0.8, "creativity": 0.7, "communication": 0.6, "marketing": 0.5},
            "roles": ["Content Designer", "Brand Strategist", "Editorial Lead"],
            "roadmap": ["Build a content portfolio", "Define a messaging system", "Analyze content performance"],
        },
        {
            "name": "Learning and Development",
            "path": "non-technical",
            "tags": ["education", "people"],
            "summary": "Designs training programs and knowledge systems.",
            "traits": {"teaching": 0.8, "communication": 0.6, "empathy": 0.6, "organization": 0.5},
            "roles": ["Trainer", "Instructional Designer", "Enablement Specialist"],
            "roadmap": ["Build a learning plan", "Teach a workshop", "Measure learner outcomes"],
        },
        {
            "name": "Finance Analyst",
            "path": "non-technical",
            "tags": ["finance", "business"],
            "summary": "Analyzes financial performance and risk.",
            "traits": {"finance": 0.8, "analytical": 0.7, "organization": 0.6},
            "roles": ["FP&A Analyst", "Risk Analyst", "Investment Analyst"],
            "roadmap": ["Learn financial modeling", "Build a finance case study", "Present insights to stakeholders"],
        },
    ]

    return {"questions": questions, "careers": careers}


def get_catalog():
    try:
        questions = Question.query.filter_by(active=True).order_by(Question.difficulty).all()
        careers = Career.query.all()
    except Exception:
        db.session.rollback()
        return get_fallback_catalog()

    if not questions or not careers:
        return get_fallback_catalog()

    question_payload = []
    for q in questions:
        meta = db.session.get(QuestionMeta, q.question_id)
        options = QuestionOption.query.filter_by(question_id=q.question_id).all()
        option_payload = [
            {
                "label": o.label,
                "value": o.value,
                "detail": o.detail,
                "traits": o.traits or {},
            }
            for o in options
        ]
        question_payload.append(
            {
                "id": q.category or q.trait or f"q_{q.question_id}",
                "text": q.question_text,
                "type": q.response_type,
                "difficulty": q.difficulty,
                "required": bool(meta.required) if meta else True,
                "why": meta.why if meta else "",
                "minLabel": meta.min_label if meta else None,
                "maxLabel": meta.max_label if meta else None,
                "evidenceHigh": meta.evidence_high if meta else None,
                "evidenceLow": meta.evidence_low if meta else None,
                "placeholder": meta.placeholder if meta else None,
                "options": option_payload if option_payload else None,
            }
        )

    career_payload = []
    for career in careers:
        traits = CareerTrait.query.filter_by(career_id=career.career_id).all()
        tags = CareerTag.query.filter_by(career_id=career.career_id).all()
        reasons = CareerReason.query.filter_by(career_id=career.career_id).order_by(CareerReason.reason_order).all()
        roles = CareerRole.query.filter_by(career_id=career.career_id).order_by(CareerRole.role_order).all()
        roadmap = CareerRoadmap.query.filter_by(career_id=career.career_id).order_by(CareerRoadmap.step_order).all()

        career_payload.append(
            {
                "name": career.career_name,
                "path": career.domain or "general",
                "tags": [t.tag for t in tags],
                "summary": career.description or "",
                "traits": {t.trait: t.required_level for t in traits},
                "weights": {t.trait: t.weight or 1.0 for t in traits},
                "roles": [r.role_title for r in roles],
                "reasons": [r.reason_text for r in reasons],
                "roadmap": [r.description for r in roadmap],
            }
        )

    return {"questions": question_payload, "careers": career_payload}
