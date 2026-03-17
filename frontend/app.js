const fallbackQuestions = [
    {
        id: "path",
        text: "Which career paths do you want to explore right now?",
        type: "single",
        required: true,
        why: "We use this to filter recommendations so you see technical, non-technical, or both.",
        options: [
            {
                label: "Technical",
                value: "technical",
                detail: "Engineering, data, and software-heavy roles.",
                traits: { technical_interest: 0.9, coding: 0.7 }
            },
            {
                label: "Non-Technical",
                value: "non-technical",
                detail: "Business, creative, people, and operations roles.",
                traits: { people_focus: 0.7, business: 0.6 }
            },
            {
                label: "Both",
                value: "both",
                detail: "Show a full mix across the spectrum.",
                traits: { versatility: 0.8 }
            }
        ]
    },
    {
        id: "interests",
        text: "Which domains spark your curiosity the most?",
        type: "multi",
        required: true,
        why: "Your interests are a strong signal for long-term motivation.",
        options: [
            { label: "AI and Machine Learning", value: "ai", traits: { data: 0.7, research: 0.6 } },
            { label: "Web and Product Experiences", value: "web", traits: { product: 0.7, design: 0.4 } },
            { label: "Mobile Apps", value: "mobile", traits: { product: 0.5, coding: 0.5 } },
            { label: "Data and Analytics", value: "data", traits: { data: 0.8, analytical: 0.6 } },
            { label: "Cybersecurity", value: "security", traits: { analytical: 0.7, systems: 0.6 } },
            { label: "Cloud and Infrastructure", value: "cloud", traits: { systems: 0.7, reliability: 0.6 } },
            { label: "Design and Creative", value: "design", traits: { creativity: 0.8, design: 0.8 } },
            { label: "Marketing and Growth", value: "marketing", traits: { marketing: 0.8, communication: 0.6 } },
            { label: "Business and Strategy", value: "business", traits: { business: 0.8, leadership: 0.5 } },
            { label: "People and Culture", value: "people", traits: { empathy: 0.8, communication: 0.6 } },
            { label: "Education and Training", value: "education", traits: { teaching: 0.8, communication: 0.6 } },
            { label: "Finance and Investing", value: "finance", traits: { finance: 0.8, analytical: 0.6 } }
        ]
    },
    {
        id: "workstyle",
        text: "Which work style sounds most energizing?",
        type: "single",
        required: true,
        why: "Work style helps match you with the right team environments.",
        options: [
            { label: "Deep focus time", value: "focus", detail: "Long stretches of independent work.", traits: { focus: 0.8 } },
            { label: "Collaborative sprints", value: "team", detail: "Fast-paced teamwork and alignment.", traits: { collaboration: 0.8, communication: 0.6 } },
            { label: "Mixed", value: "mixed", detail: "A balance of solo and team time.", traits: { adaptability: 0.7 } }
        ]
    },
    {
        id: "problem_type",
        text: "What kind of problems do you most enjoy solving?",
        type: "multi",
        required: true,
        why: "Problem preferences map to career families.",
        options: [
            { label: "Building new products", value: "build", traits: { product: 0.7, creativity: 0.4 } },
            { label: "Optimizing systems", value: "optimize", traits: { systems: 0.7, analytical: 0.6 } },
            { label: "Helping people succeed", value: "people_help", traits: { empathy: 0.7, leadership: 0.4 } },
            { label: "Analyzing complex data", value: "data", traits: { data: 0.8, analytical: 0.6 } },
            { label: "Telling stories and crafting messages", value: "story", traits: { writing: 0.8, creativity: 0.5 } },
            { label: "Planning and organizing operations", value: "ops", traits: { organization: 0.8, leadership: 0.4 } }
        ]
    },
    {
        id: "coding_interest",
        text: "How much do you enjoy coding or technical problem solving?",
        type: "scale",
        trait: "coding",
        required: true,
        why: "This decides how technical your recommendations should be.",
        minLabel: "Not at all",
        maxLabel: "Love it",
        evidenceHigh: "You enjoy coding and technical problem solving.",
        evidenceLow: "You prefer roles with less coding."
    },
    {
        id: "language_preference",
        text: "If you are technical, which languages do you prefer or want to learn?",
        type: "multi",
        required: false,
        why: "Language preference helps route you to the right technical specializations.",
        options: [
            { label: "Python", value: "python", traits: { data: 0.4, coding: 0.3 } },
            { label: "JavaScript or TypeScript", value: "javascript", traits: { product: 0.4, coding: 0.3 } },
            { label: "Java or Kotlin", value: "java", traits: { systems: 0.3, coding: 0.3 } },
            { label: "C# or .NET", value: "csharp", traits: { systems: 0.3, coding: 0.3 } },
            { label: "C or C++", value: "cpp", traits: { systems: 0.5, analytical: 0.3 } },
            { label: "Go", value: "go", traits: { systems: 0.5, reliability: 0.4 } },
            { label: "Rust", value: "rust", traits: { systems: 0.6, analytical: 0.4 } },
            { label: "SQL", value: "sql", traits: { data: 0.5, analytical: 0.4 } },
            { label: "Swift or Objective-C", value: "swift", traits: { product: 0.4, coding: 0.3 } }
        ]
    },
    {
        id: "math_comfort",
        text: "How comfortable are you with math and quantitative reasoning?",
        type: "scale",
        trait: "analytical",
        required: true,
        why: "Many data and engineering roles depend on quantitative strength.",
        minLabel: "Not comfortable",
        maxLabel: "Very comfortable",
        evidenceHigh: "You are confident with quantitative reasoning.",
        evidenceLow: "You prefer roles that are less math-heavy."
    },
    {
        id: "creativity",
        text: "How important is creativity in your day-to-day work?",
        type: "scale",
        trait: "creativity",
        required: true,
        why: "Creative drive guides design, marketing, and product roles.",
        minLabel: "Not important",
        maxLabel: "Essential",
        evidenceHigh: "You want creativity to be a core part of your work."
    },
    {
        id: "communication",
        text: "How much do you enjoy communicating ideas and influencing others?",
        type: "scale",
        trait: "communication",
        required: true,
        why: "Communication strength aligns with leadership, marketing, and client-facing paths.",
        minLabel: "Not much",
        maxLabel: "A lot",
        evidenceHigh: "You enjoy communicating and influencing others."
    },
    {
        id: "people_focus",
        text: "How much do you like working directly with people?",
        type: "scale",
        trait: "people_focus",
        required: true,
        why: "People-oriented roles need strong interpersonal energy.",
        minLabel: "Prefer solo",
        maxLabel: "Love people work",
        evidenceHigh: "You like working directly with people."
    },
    {
        id: "leadership",
        text: "How excited are you to lead or coordinate teams?",
        type: "scale",
        trait: "leadership",
        required: true,
        why: "Leadership intent helps match you to management, product, and strategy roles.",
        minLabel: "Not interested",
        maxLabel: "Very excited",
        evidenceHigh: "You are open to leading or coordinating teams."
    },
    {
        id: "organization",
        text: "How much do you enjoy planning, organizing, and process building?",
        type: "scale",
        trait: "organization",
        required: true,
        why: "Operational roles rely on planning and process ownership.",
        minLabel: "Not much",
        maxLabel: "A lot",
        evidenceHigh: "You enjoy organizing and building processes."
    },
    {
        id: "design_interest",
        text: "How interested are you in visual design or user experience?",
        type: "scale",
        trait: "design",
        required: true,
        why: "Design interest indicates fit for UX, product, and creative roles.",
        minLabel: "Not interested",
        maxLabel: "Very interested",
        evidenceHigh: "You are drawn to visual design and user experience."
    },
    {
        id: "writing_interest",
        text: "How much do you enjoy writing or storytelling?",
        type: "scale",
        trait: "writing",
        required: true,
        why: "Writing ability powers content, marketing, and knowledge roles.",
        minLabel: "Not much",
        maxLabel: "A lot",
        evidenceHigh: "You enjoy writing and storytelling."
    },
    {
        id: "business_interest",
        text: "How interested are you in business strategy and market thinking?",
        type: "scale",
        trait: "business",
        required: true,
        why: "Business interest helps match you to strategy, operations, and growth roles.",
        minLabel: "Not interested",
        maxLabel: "Very interested",
        evidenceHigh: "You are interested in business and market strategy."
    },
    {
        id: "marketing_interest",
        text: "How interested are you in branding, positioning, or growth marketing?",
        type: "scale",
        trait: "marketing",
        required: true,
        why: "Marketing interest aligns with growth, brand, and go-to-market paths.",
        minLabel: "Not interested",
        maxLabel: "Very interested",
        evidenceHigh: "You are interested in branding and growth marketing."
    },
    {
        id: "data_interest",
        text: "How excited are you about working with data, dashboards, or analytics?",
        type: "scale",
        trait: "data",
        required: true,
        why: "Data enthusiasm is crucial for analytics and research roles.",
        minLabel: "Not excited",
        maxLabel: "Very excited",
        evidenceHigh: "You are excited about working with data and analytics."
    },
    {
        id: "systems_interest",
        text: "How interested are you in systems, infrastructure, or reliability?",
        type: "scale",
        trait: "systems",
        required: true,
        why: "Systems interest supports cloud, DevOps, and backend engineering paths.",
        minLabel: "Not interested",
        maxLabel: "Very interested",
        evidenceHigh: "You are interested in systems and infrastructure work."
    },
    {
        id: "teaching_interest",
        text: "How much do you enjoy teaching or mentoring others?",
        type: "scale",
        trait: "teaching",
        required: true,
        why: "Teaching interest matters for education, enablement, and coaching careers.",
        minLabel: "Not much",
        maxLabel: "A lot",
        evidenceHigh: "You enjoy teaching or mentoring others."
    },
    {
        id: "risk_tolerance",
        text: "How comfortable are you with ambiguity and risk?",
        type: "scale",
        trait: "entrepreneurship",
        required: true,
        why: "Entrepreneurial comfort influences startup, innovation, and leadership roles.",
        minLabel: "Prefer stability",
        maxLabel: "Enjoy risk",
        evidenceHigh: "You are comfortable with ambiguity and risk."
    },
    {
        id: "hands_on",
        text: "Do you prefer building things hands-on or more strategic work?",
        type: "single",
        required: true,
        why: "This helps balance maker roles with strategy roles.",
        options: [
            { label: "Hands-on building", value: "hands_on", detail: "I like to build and ship.", traits: { maker: 0.8 } },
            { label: "Strategic planning", value: "strategy", detail: "I like planning and direction.", traits: { strategy: 0.8, business: 0.4 } },
            { label: "Both", value: "both", detail: "I want a balance.", traits: { maker: 0.5, strategy: 0.5 } }
        ]
    },
    {
        id: "collaboration",
        text: "How do you prefer to collaborate?",
        type: "single",
        required: true,
        why: "Collaboration style influences team fit and career environment.",
        options: [
            { label: "Small tight-knit team", value: "small", detail: "A few people, high trust.", traits: { collaboration: 0.6 } },
            { label: "Larger cross-functional teams", value: "large", detail: "Many roles working together.", traits: { collaboration: 0.8, communication: 0.5 } },
            { label: "Mostly independent", value: "solo", detail: "Prefer solo ownership.", traits: { focus: 0.7 } }
        ]
    },
    {
        id: "impact",
        text: "What kind of impact motivates you most?",
        type: "single",
        required: true,
        why: "Impact type helps distinguish between mission-driven and commercial paths.",
        options: [
            { label: "Helping people directly", value: "help", detail: "Care, education, or community impact.", traits: { empathy: 0.8 } },
            { label: "Building successful products", value: "product", detail: "Creating something that scales.", traits: { product: 0.7 } },
            { label: "Driving revenue or growth", value: "growth", detail: "Business impact and market wins.", traits: { business: 0.6, marketing: 0.5 } },
            { label: "Innovation and discovery", value: "innovation", detail: "Pushing into new ideas.", traits: { research: 0.6, entrepreneurship: 0.4 } }
        ]
    },
    {
        id: "goal",
        text: "What is your career goal over the next 1-2 years?",
        type: "text",
        required: false,
        why: "We will use this to tailor your roadmap later.",
        placeholder: "Example: Become a junior data analyst and work on real dashboards."
    }
];

const fallbackCareers = [
    {
        name: "Software Engineer",
        path: "technical",
        tags: ["web", "mobile", "cloud"],
        summary: "Builds scalable software products and platforms.",
        traits: { coding: 0.8, systems: 0.6, product: 0.5, analytical: 0.6, maker: 0.7 },
        roles: ["Frontend Engineer", "Backend Engineer", "Full-Stack Engineer"],
        roadmap: ["Learn a core language", "Build 2-3 portfolio projects", "Ship a real app with users"]
    },
    {
        name: "Data Analyst",
        path: "technical",
        tags: ["data", "finance"],
        summary: "Turns data into insights with dashboards and analysis.",
        traits: { data: 0.8, analytical: 0.7, communication: 0.5, organization: 0.4 },
        roles: ["BI Analyst", "Product Analyst", "Reporting Analyst"],
        roadmap: ["Master SQL + spreadsheets", "Build a dashboard portfolio", "Practice storytelling with data"]
    },
    {
        name: "Data Scientist",
        path: "technical",
        tags: ["ai", "data"],
        summary: "Builds predictive models and experiments with ML.",
        traits: { data: 0.8, analytical: 0.8, research: 0.6, coding: 0.6 },
        roles: ["ML Scientist", "Applied Data Scientist", "Research Analyst"],
        roadmap: ["Learn Python + statistics", "Build ML projects", "Showcase experiments and insights"]
    },
    {
        name: "Machine Learning Engineer",
        path: "technical",
        tags: ["ai", "cloud"],
        summary: "Deploys ML models into production systems.",
        traits: { coding: 0.8, systems: 0.7, data: 0.7, reliability: 0.6 },
        roles: ["MLOps Engineer", "Applied ML Engineer", "ML Platform Engineer"],
        roadmap: ["Strengthen Python + ML basics", "Learn cloud deployment", "Ship an ML app end-to-end"]
    },
    {
        name: "Cybersecurity Analyst",
        path: "technical",
        tags: ["security"],
        summary: "Protects systems, audits risks, and responds to threats.",
        traits: { analytical: 0.7, systems: 0.6, focus: 0.6, reliability: 0.6 },
        roles: ["SOC Analyst", "Security Engineer", "Threat Analyst"],
        roadmap: ["Learn security fundamentals", "Practice labs and CTFs", "Document security case studies"]
    },
    {
        name: "Cloud or DevOps Engineer",
        path: "technical",
        tags: ["cloud"],
        summary: "Builds and maintains reliable infrastructure.",
        traits: { systems: 0.8, reliability: 0.7, coding: 0.5, organization: 0.5 },
        roles: ["DevOps Engineer", "Site Reliability Engineer", "Platform Engineer"],
        roadmap: ["Learn Linux + networking", "Deploy apps on cloud", "Automate infrastructure pipelines"]
    },
    {
        name: "Product Manager",
        path: "hybrid",
        tags: ["web", "business"],
        summary: "Defines product vision and aligns teams to deliver it.",
        traits: { product: 0.8, leadership: 0.7, communication: 0.7, business: 0.6 },
        roles: ["Associate PM", "Product Owner", "Growth PM"],
        roadmap: ["Study product discovery", "Run user interviews", "Ship a feature with metrics"]
    },
    {
        name: "UX or Product Designer",
        path: "non-technical",
        tags: ["design", "web"],
        summary: "Designs user experiences and visual systems.",
        traits: { design: 0.8, creativity: 0.7, empathy: 0.6, communication: 0.5 },
        roles: ["UX Designer", "UI Designer", "Interaction Designer"],
        roadmap: ["Learn design fundamentals", "Build case studies", "Conduct user research"]
    },
    {
        name: "Digital Marketer",
        path: "non-technical",
        tags: ["marketing", "business"],
        summary: "Grows audiences and drives product adoption.",
        traits: { marketing: 0.8, communication: 0.7, creativity: 0.6, business: 0.5 },
        roles: ["Growth Marketer", "Content Marketer", "Performance Marketer"],
        roadmap: ["Learn marketing channels", "Run a campaign", "Analyze performance metrics"]
    },
    {
        name: "Business Analyst",
        path: "non-technical",
        tags: ["business", "finance"],
        summary: "Improves business decisions through analysis.",
        traits: { business: 0.7, analytical: 0.7, organization: 0.6, communication: 0.5 },
        roles: ["Strategy Analyst", "Operations Analyst", "Insights Analyst"],
        roadmap: ["Learn business frameworks", "Build reporting models", "Present recommendations"]
    },
    {
        name: "People Operations",
        path: "non-technical",
        tags: ["people"],
        summary: "Builds a strong culture and employee experience.",
        traits: { empathy: 0.8, communication: 0.7, organization: 0.6, leadership: 0.5 },
        roles: ["HR Generalist", "Talent Partner", "People Ops Manager"],
        roadmap: ["Learn HR fundamentals", "Practice interviewing", "Design onboarding flows"]
    },
    {
        name: "Sales or Business Development",
        path: "non-technical",
        tags: ["business", "marketing"],
        summary: "Builds partnerships and drives revenue.",
        traits: { communication: 0.8, business: 0.7, leadership: 0.5, marketing: 0.5 },
        roles: ["Account Executive", "Sales Development Rep", "Partnerships Manager"],
        roadmap: ["Learn consultative selling", "Practice discovery calls", "Track pipeline metrics"]
    },
    {
        name: "Project or Operations Manager",
        path: "non-technical",
        tags: ["business"],
        summary: "Keeps cross-functional work moving smoothly.",
        traits: { organization: 0.8, leadership: 0.6, communication: 0.6, strategy: 0.5 },
        roles: ["Project Manager", "Operations Lead", "Program Manager"],
        roadmap: ["Learn project frameworks", "Run a cross-team project", "Track delivery metrics"]
    },
    {
        name: "Content Strategist",
        path: "non-technical",
        tags: ["marketing", "education"],
        summary: "Creates messaging, content systems, and storytelling.",
        traits: { writing: 0.8, creativity: 0.7, communication: 0.6, marketing: 0.5 },
        roles: ["Content Designer", "Brand Strategist", "Editorial Lead"],
        roadmap: ["Build a content portfolio", "Define a messaging system", "Analyze content performance"]
    },
    {
        name: "Learning and Development",
        path: "non-technical",
        tags: ["education", "people"],
        summary: "Designs training programs and knowledge systems.",
        traits: { teaching: 0.8, communication: 0.6, empathy: 0.6, organization: 0.5 },
        roles: ["Trainer", "Instructional Designer", "Enablement Specialist"],
        roadmap: ["Build a learning plan", "Teach a workshop", "Measure learner outcomes"]
    },
    {
        name: "Finance Analyst",
        path: "non-technical",
        tags: ["finance", "business"],
        summary: "Analyzes financial performance and risk.",
        traits: { finance: 0.8, analytical: 0.7, organization: 0.6 },
        roles: ["FP&A Analyst", "Risk Analyst", "Investment Analyst"],
        roadmap: ["Learn financial modeling", "Build a finance case study", "Present insights to stakeholders"]
    }
];

let questions = [];
let careers = [];
let backendAvailable = false;

const state = {
    index: 0,
    answers: {},
    traitSums: {},
    traitCounts: {},
    evidence: {},
    selectedTags: [],
    currentQuestion: null,
    history: []
};

const questionTitle = document.getElementById("question-title");
const questionWhy = document.getElementById("question-why");
const questionBody = document.getElementById("question-body");
const progressLabel = document.getElementById("progress-label");
const progressFill = document.getElementById("progress-fill");
const nextBtn = document.getElementById("next-btn");
const backBtn = document.getElementById("back-btn");
const resultPanel = document.getElementById("result-panel");
const resultList = document.getElementById("result-list");
const resultSummary = document.getElementById("result-summary");
const traitGrid = document.getElementById("trait-grid");
const externalPanel = document.getElementById("external-panel");
const externalList = document.getElementById("external-list");
const externalSkills = document.getElementById("external-skills");
const externalJobs = document.getElementById("external-jobs");

function addTrait(trait, value, evidenceText) {
    if (!state.traitSums[trait]) {
        state.traitSums[trait] = 0;
        state.traitCounts[trait] = 0;
    }
    state.traitSums[trait] += value;
    state.traitCounts[trait] += 1;

    if (evidenceText) {
        if (!state.evidence[trait]) state.evidence[trait] = [];
        state.evidence[trait].push(evidenceText);
    }
}

function getTraitScore(trait) {
    if (!state.traitCounts[trait]) return 0.4;
    return Math.min(1, state.traitSums[trait] / state.traitCounts[trait]);
}

function renderProgress() {
    progressLabel.textContent = `Question ${state.index + 1} of ${questions.length}`;
    const percent = ((state.index + 1) / questions.length) * 100;
    progressFill.style.width = `${percent}%`;
}

function renderQuestion() {
    const q = state.currentQuestion || questions[state.index];
    if (!q) return;
    renderProgress();
    questionTitle.textContent = q.text;
    questionWhy.textContent = `Why we ask: ${q.why}`;
    questionBody.innerHTML = "";

    nextBtn.disabled = q.required;
    backBtn.disabled = state.index === 0;

    const savedAnswer = state.answers[q.id];

    if (q.type === "single") {
        const grid = document.createElement("div");
        grid.className = "option-grid";
        q.options.forEach((option) => {
            const card = document.createElement("div");
            card.className = "option";
            if (savedAnswer === option.value) card.classList.add("selected");
            card.innerHTML = `
                <div class="option-title">${option.label}</div>
                <div class="option-detail">${option.detail || ""}</div>
            `;
            card.addEventListener("click", () => {
                state.answers[q.id] = option.value;
                [...grid.children].forEach((child) => child.classList.remove("selected"));
                card.classList.add("selected");
                nextBtn.disabled = false;
            });
            grid.appendChild(card);
        });
        questionBody.appendChild(grid);
        if (savedAnswer) nextBtn.disabled = false;
    }

    if (q.type === "multi") {
        const chips = document.createElement("div");
        chips.className = "chips";
        if (q.id === "interests" || q.options?.length > 8) {
            chips.classList.add("scrollable");
        }
        const selected = new Set(savedAnswer || []);
        q.options.forEach((option) => {
            const chip = document.createElement("div");
            chip.className = "chip";
            chip.textContent = option.label;
            if (selected.has(option.value)) chip.classList.add("selected");
            chip.addEventListener("click", () => {
                if (selected.has(option.value)) {
                    selected.delete(option.value);
                    chip.classList.remove("selected");
                } else {
                    selected.add(option.value);
                    chip.classList.add("selected");
                }
                state.answers[q.id] = [...selected];
                nextBtn.disabled = q.required && selected.size === 0;
            });
            chips.appendChild(chip);
        });
        questionBody.appendChild(chips);
        if (savedAnswer && savedAnswer.length) nextBtn.disabled = false;
    }

    if (q.type === "scale") {
        const scale = document.createElement("div");
        scale.className = "scale";
        const input = document.createElement("input");
        input.type = "range";
        input.min = 1;
        input.max = 5;
        input.step = 1;
        input.value = savedAnswer || 3;
        input.addEventListener("input", () => {
            state.answers[q.id] = Number(input.value);
            nextBtn.disabled = false;
        });
        scale.appendChild(input);
        const labels = document.createElement("div");
        labels.className = "scale-labels";
        labels.innerHTML = `<span>${q.minLabel}</span><span>${q.maxLabel}</span>`;
        scale.appendChild(labels);
        questionBody.appendChild(scale);
        if (savedAnswer) nextBtn.disabled = false;
    }

    if (q.type === "text") {
        const area = document.createElement("textarea");
        area.className = "textarea-input";
        area.placeholder = q.placeholder || "";
        area.value = savedAnswer || "";
        area.addEventListener("input", () => {
            state.answers[q.id] = area.value;
            nextBtn.disabled = q.required && !area.value.trim();
        });
        questionBody.appendChild(area);
        if (!q.required) nextBtn.disabled = false;
    }
}

function applyAnswerToTraits(question, answer) {
    if (!answer) return;

    if (question.type === "single") {
        const option = question.options.find((opt) => opt.value === answer);
        if (option && option.traits) {
            Object.entries(option.traits).forEach(([trait, value]) => addTrait(trait, value));
        }
    }

    if (question.type === "multi") {
        answer.forEach((value) => {
            const option = question.options.find((opt) => opt.value === value);
            if (option && option.traits) {
                Object.entries(option.traits).forEach(([trait, v]) => addTrait(trait, v));
            }
        });
        if (question.id === "interests") {
            state.selectedTags = answer.slice();
        }
    }

    if (question.type === "scale") {
        const normalized = Number(answer) / 5;
        if (question.trait) {
            addTrait(
                question.trait,
                normalized,
                normalized >= 0.8 ? question.evidenceHigh : normalized <= 0.4 ? question.evidenceLow : ""
            );
        }
    }
}

function rebuildTraitScores() {
    state.traitSums = {};
    state.traitCounts = {};
    state.evidence = {};
    state.selectedTags = [];

    questions.forEach((question) => {
        applyAnswerToTraits(question, state.answers[question.id]);
    });
}

function computeFit(career) {
    const traitEntries = Object.entries(career.traits);
    let score = 0;
    const weights = career.weights || {};
    let weightTotal = 0;
    traitEntries.forEach(([trait, required]) => {
        const userValue = getTraitScore(trait);
        const weight = weights[trait] || 1;
        score += Math.max(0, 1 - Math.abs(required - userValue)) * weight;
        weightTotal += weight;
    });

    if (state.selectedTags.some((tag) => career.tags.includes(tag))) {
        score += 0.3;
    }
    return score / (Math.max(weightTotal, traitEntries.length) + 0.3);
}

function buildReasons(career) {
    const reasons = [];
    Object.entries(career.traits)
        .sort((a, b) => getTraitScore(b[0]) - getTraitScore(a[0]))
        .slice(0, 3)
        .forEach(([trait]) => {
            const evidence = state.evidence[trait];
            if (evidence && evidence.length) {
                reasons.push(evidence[0]);
            } else {
                reasons.push(`You show strength in ${trait.replace(/_/g, " ")}.`);
            }
        });

    const matchingTag = state.selectedTags.find((tag) => career.tags.includes(tag));
    if (matchingTag) {
        reasons.push(`Your interest in ${matchingTag.replace(/_/g, " ")} aligns with this path.`);
    }
    return reasons.slice(0, 4);
}

async function renderResults() {
    if (backendAvailable) {
        await renderResultsFromBackend();
        return;
    }
    rebuildTraitScores();
    const preference = state.answers.path || "both";
    let filtered = careers;
    if (preference === "technical") {
        filtered = careers.filter((career) => career.path !== "non-technical");
    }
    if (preference === "non-technical") {
        filtered = careers.filter((career) => career.path !== "technical");
    }

    const ranked = filtered
        .map((career) => ({ ...career, score: computeFit(career) }))
        .sort((a, b) => b.score - a.score)
        .slice(0, 6);

    resultSummary.textContent =
        "Based on your answers, here are the career paths that match your signals and interests.";

    traitGrid.innerHTML = "";
    Object.keys(state.traitSums)
        .map((trait) => ({ trait, score: getTraitScore(trait) }))
        .sort((a, b) => b.score - a.score)
        .slice(0, 8)
        .forEach(({ trait, score }) => {
            const card = document.createElement("div");
            card.className = "trait-card";
            card.innerHTML = `
                <strong>${trait.replace(/_/g, " ")}</strong>
                <div class="trait-bar"><span style="width:${Math.round(score * 100)}%"></span></div>
            `;
            traitGrid.appendChild(card);
        });

    resultList.innerHTML = "";
    ranked.forEach((career) => {
        const reasons = buildReasons(career);
        const card = document.createElement("div");
        card.className = "result-card";
        card.innerHTML = `
            <div>
                <h3>${career.name}</h3>
                <div class="result-meta">
                    <span class="pill">${career.path.replace("-", " ")}</span>
                    <span>Fit Score: ${(career.score * 100).toFixed(0)}%</span>
                </div>
            </div>
            <p>${career.summary}</p>
            <div>
                <strong>Why this fits you</strong>
                <ul class="list">${reasons.map((r) => `<li>${r}</li>`).join("")}</ul>
            </div>
            <div>
                <strong>Example roles</strong>
                <ul class="list">${career.roles.map((r) => `<li>${r}</li>`).join("")}</ul>
            </div>
            <div>
                <strong>Next steps</strong>
                <ul class="list">${career.roadmap.map((r) => `<li>${r}</li>`).join("")}</ul>
            </div>
        `;
        resultList.appendChild(card);
    });

    const topScore = ranked.length ? ranked[0].score : 0;
    if (topScore < 0.55) {
        loadExternalSuggestions().then(renderExternalSuggestions);
    } else {
        externalPanel.classList.add("hidden");
        externalList.innerHTML = "";
    }

    resultPanel.classList.remove("hidden");
    document.getElementById("question-card").classList.add("hidden");
    document.querySelector(".nav").classList.add("hidden");
    document.querySelector(".progress").classList.add("hidden");
}

async function renderResultsFromBackend() {
    try {
        const res = await fetch("http://localhost:5000/recommendations/score", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers: state.answers, limit: 6, offset: 0 }),
        });
        if (!res.ok) throw new Error("recommendation failed");
        const payload = await res.json();

        resultSummary.textContent =
            "Based on your answers, here are the career paths that match your signals and interests.";

        const summaryRes = await fetch("http://localhost:5000/profile/summary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers: state.answers }),
        });
        const summary = summaryRes.ok ? await summaryRes.json() : { traits: [] };

        traitGrid.innerHTML = "";
        (summary.traits || []).slice(0, 8).forEach((item) => {
            const card = document.createElement("div");
            card.className = "trait-card";
            card.innerHTML = `
                <strong>${item.trait.replace(/_/g, " ")}</strong>
                <div class="trait-bar"><span style="width:${Math.round(item.score * 100)}%"></span></div>
            `;
            traitGrid.appendChild(card);
        });

        resultList.innerHTML = "";
        (payload.results || []).forEach((career) => {
            const card = document.createElement("div");
            card.className = "result-card";
            card.innerHTML = `
                <div>
                    <h3>${career.name}</h3>
                    <div class="result-meta">
                        <span class="pill">${career.path.replace("-", " ")}</span>
                        <span>Fit Score: ${(career.fit_score * 100).toFixed(0)}%</span>
                    </div>
                </div>
                <p>${career.summary || ""}</p>
                <div>
                    <strong>Why this fits you</strong>
                    <ul class="list">${(career.reasons || []).map((r) => `<li>${r}</li>`).join("")}</ul>
                </div>
                <div>
                    <strong>Example roles</strong>
                    <ul class="list">${(career.roles || []).map((r) => `<li>${r}</li>`).join("")}</ul>
                </div>
                <div>
                    <strong>Next steps</strong>
                    <ul class="list">${(career.roadmap || []).map((r) => `<li>${r}</li>`).join("")}</ul>
                </div>
            `;
            resultList.appendChild(card);
        });

        const topScore = payload.results?.length ? payload.results[0].fit_score : 0;
        if (topScore < 0.55) {
            loadExternalSuggestions().then(renderExternalSuggestions);
        } else {
            externalPanel.classList.add("hidden");
            externalList.innerHTML = "";
        }

        resultPanel.classList.remove("hidden");
        document.getElementById("question-card").classList.add("hidden");
        document.querySelector(".nav").classList.add("hidden");
        document.querySelector(".progress").classList.add("hidden");
    } catch (error) {
        backendAvailable = false;
        renderResults();
    }
}

function getInterestLabel(value) {
    const interestQuestion = questions.find((q) => q.id === "interests");
    if (!interestQuestion || !interestQuestion.options) return value;
    const match = interestQuestion.options.find((opt) => opt.value === value);
    return match ? match.label : value;
}

function getExternalQuery() {
    const goal = (state.answers.goal || "").trim();
    if (goal.length > 4) return goal;
    if (state.selectedTags.length) {
        return getInterestLabel(state.selectedTags[0]);
    }
    return "career";
}

async function loadExternalSuggestions() {
    const query = getExternalQuery();
    try {
        const res = await fetch(`http://localhost:5000/external/suggest?q=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error("external fetch failed");
        const data = await res.json();
        return {
            suggestions: data.suggestions || [],
            related_skills: data.related_skills || [],
            related_jobs: data.related_jobs || [],
        };
    } catch (error) {
        return { suggestions: [], related_skills: [], related_jobs: [] };
    }
}

function renderExternalSuggestions(bundle) {
    const suggestions = bundle.suggestions || [];
    const relatedSkills = bundle.related_skills || [];
    const relatedJobs = bundle.related_jobs || [];

    if (!suggestions.length && !relatedSkills.length && !relatedJobs.length) {
        externalPanel.classList.add("hidden");
        externalList.innerHTML = "";
        externalSkills.innerHTML = "";
        externalJobs.innerHTML = "";
        return;
    }

    externalPanel.classList.remove("hidden");
    externalList.innerHTML = "";
    suggestions.forEach((item) => {
        const card = document.createElement("div");
        card.className = "external-card";
        card.innerHTML = `
            <strong>${item.title}</strong>
            <div class="result-meta">Source: ${item.source || "External"}</div>
        `;
        externalList.appendChild(card);
    });

    externalSkills.innerHTML = "";
    relatedSkills.forEach((skill) => {
        const card = document.createElement("div");
        card.className = "external-card";
        card.innerHTML = `
            <strong>${skill.name}</strong>
            <div class="result-meta">Importance: ${skill.level ?? "n/a"}</div>
        `;
        externalSkills.appendChild(card);
    });

    externalJobs.innerHTML = "";
    relatedJobs.forEach((job) => {
        const card = document.createElement("div");
        card.className = "external-card";
        card.innerHTML = `
            <strong>${job.title}</strong>
            <div class="result-meta">Related job family</div>
        `;
        externalJobs.appendChild(card);
    });
}

async function loadCatalog() {
    try {
        const res = await fetch("http://localhost:5000/catalog");
        if (!res.ok) throw new Error("catalog fetch failed");
        const data = await res.json();
        questions = data.questions || [];
        careers = data.careers || [];
        backendAvailable = true;
    } catch (error) {
        questions = fallbackQuestions;
        careers = fallbackCareers;
        backendAvailable = false;
    }

    if (!questions.length || !careers.length) {
        questions = fallbackQuestions;
        careers = fallbackCareers;
        backendAvailable = false;
    }
}

nextBtn.addEventListener("click", () => {
    const q = state.currentQuestion || questions[state.index];
    if (q.required && !state.answers[q.id]) return;

    if (backendAvailable) {
        fetchNextQuestion().then((done) => {
            if (done) renderResults();
        });
        return;
    }

    if (state.index < questions.length - 1) {
        state.index += 1;
        renderQuestion();
    } else {
        renderResults();
    }
});

backBtn.addEventListener("click", () => {
    if (backendAvailable) {
        state.history.pop();
        state.currentQuestion = state.history[state.history.length - 1] || null;
        renderQuestion();
        return;
    }
    if (state.index === 0) return;
    state.index -= 1;
    renderQuestion();
});

async function fetchNextQuestion() {
    try {
        const res = await fetch("http://localhost:5000/questions/next", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers: state.answers }),
        });
        if (!res.ok) throw new Error("question fetch failed");
        const data = await res.json();
        if (data.status === "completed") {
            return true;
        }
        state.currentQuestion = data;
        state.history.push(data);
        renderQuestion();
        return false;
    } catch (error) {
        backendAvailable = false;
        state.currentQuestion = null;
        renderQuestion();
        return false;
    }
}

loadCatalog().then(() => {
    renderQuestion();
    if (backendAvailable) {
        state.history = [];
        fetchNextQuestion();
    }
});
