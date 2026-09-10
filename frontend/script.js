let currentProfile = {};


// -------------------------------
// LOAD PROFILE
// -------------------------------

async function loadProfile() {

    try {

        const response = await fetch("/api/profile");

        currentProfile = await response.json();

        document.getElementById("score").innerText =
            currentProfile.overall_wellness_score || 0;

    } catch (error) {

        console.log(error);

    }
}


// -------------------------------
// PAGE SWITCHING
// -------------------------------

function hideAll() {

    document
        .querySelectorAll(".section")
        .forEach(section => {
            section.classList.add("hidden");
        });
}


function showHome() {

    hideAll();

    document
        .getElementById("chatSection")
        .classList.remove("hidden");

    document.getElementById("pageTitle").innerText =
        "Good day 🌿";

}


function showCheckin() {

    hideAll();

    document
        .getElementById("checkinSection")
        .classList.remove("hidden");

    document.getElementById("pageTitle").innerText =
        "Daily Check-in 📋";

}


function showPattern() {

    hideAll();

    document
        .getElementById("patternSection")
        .classList.remove("hidden");

    document.getElementById("pageTitle").innerText =
        "Wellness Pattern 🧠";

}


function showSmallChange() {

    hideAll();

    document
        .getElementById("changeSection")
        .classList.remove("hidden");

    document.getElementById("pageTitle").innerText =
        "One Small Change 🌱";

}


// -------------------------------
// CHAT
// -------------------------------

function handleEnter(event) {

    if (event.key === "Enter") {

        sendMessage();

    }

}


async function sendMessage() {

    const input =
        document.getElementById("messageInput");

    const message = input.value.trim();

    if (!message) return;


    addMessage("You", message, "user");

    input.value = "";


    addMessage(
        "MediMateAI",
        "Thinking... 🌿",
        "bot"
    );


    try {

        const response = await fetch(
            "/api/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        const result = await response.json();


        removeThinking();


        if (result.status === "error") {

            addMessage(
                "MediMateAI",
                result.message,
                "bot"
            );

            return;
        }


        let text =
            result.response || "I couldn't generate a response.";


        text +=
            "\n\n🌱 Suggested Action: " +
            (result.suggested_action || "—");


        if (result.follow_up_question) {

            text +=
                "\n\n❓ " +
                result.follow_up_question;

        }


        if (result.safety_note) {

            text +=
                "\n\n⚠️ " +
                result.safety_note;

        }


        addMessage(
            "MediMateAI",
            text,
            "bot"
        );


    } catch (error) {

        removeThinking();

        addMessage(
            "MediMateAI",
            "Unable to connect to the server.",
            "bot"
        );

    }

}


function addMessage(name, text, type) {

    const chat =
        document.getElementById("chatBox");


    const div =
        document.createElement("div");

    div.className =
        "message " + type;


    const strong =
        document.createElement("strong");

    strong.innerText = name;


    const p =
        document.createElement("p");

    p.innerText = text;


    div.appendChild(strong);

    div.appendChild(p);


    chat.appendChild(div);

    chat.scrollTop =
        chat.scrollHeight;

}


function removeThinking() {

    const messages =
        document.querySelectorAll(".message.bot");

    messages.forEach(message => {

        if (message.innerText.includes("Thinking...")) {

            message.remove();

        }

    });

}


// -------------------------------
// DAILY CHECK-IN
// -------------------------------

async function submitCheckin() {

    const data = {

        sleep_hours:
            Number(document.getElementById("sleep").value),

        water:
            Number(document.getElementById("water").value),

        activity_minutes:
            Number(document.getElementById("activity").value),

        stress_level:
            Number(document.getElementById("stress").value),

        goal_completed:
            document.getElementById("goalCompleted").value === "true",

        feeling:
            document.getElementById("feeling").value

    };


    const response =
        await fetch(
            "/api/checkin",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


    const result =
        await response.json();


    document.getElementById("checkinResult").innerHTML = `

        <div class="result-card">

            <h3>✅ Check-in Saved</h3>

            <p>
                Today's wellness score:
                <strong>${result.score}/100</strong>
            </p>

            <p>
                Your information has been added
                to your wellness history.
            </p>

        </div>

    `;


    document.getElementById("score").innerText =
        result.score;

}


// -------------------------------
// PATTERN DETECTOR
// -------------------------------

async function analyzePattern() {

    const resultBox =
        document.getElementById("patternResult");


    resultBox.innerHTML =
        "<p>Analyzing your wellness pattern... 🧠</p>";


    const response =
        await fetch("/api/pattern");


    const result =
        await response.json();


    if (result.status === "error") {

        resultBox.innerHTML =
            `<p>${result.message}</p>`;

        return;
    }


    resultBox.innerHTML = `

        <div class="result-card">

            <h3>💪 Strongest Area</h3>

            <p>
                ${result.strongest_area}
            </p>


            <h3>🎯 Needs Attention</h3>

            <p>
                ${result.area_needing_attention}
            </p>


            <h3>🧠 Pattern</h3>

            <p>
                ${result.pattern}
            </p>


            <h3>🌱 Recommended Focus</h3>

            <p>
                ${result.recommended_focus}
            </p>

        </div>

    `;

}


// -------------------------------
// ONE SMALL CHANGE
// -------------------------------

async function getSmallChange() {

    const resultBox =
        document.getElementById("changeResult");


    resultBox.innerHTML =
        "<p>Creating your personalized action... 🌱</p>";


    const response =
        await fetch("/api/small-change");


    const result =
        await response.json();


    if (result.status === "error") {

        resultBox.innerHTML =
            `<p>${result.message}</p>`;

        return;

    }


    resultBox.innerHTML = `

        <div class="result-card">

            <h3>
                🌱 ${result.title}
            </h3>

            <div class="small-action">
                ${result.action}
            </div>

            <p>
                <strong>Duration:</strong>
                ${result.duration}
            </p>

            <p>
                <strong>Difficulty:</strong>
                ⭐ ${result.difficulty}
            </p>

            <p>
                <strong>Frequency:</strong>
                ${result.frequency}
            </p>

            <p>
                <strong>Why:</strong>
                ${result.reason}
            </p>

        </div>

    `;

}


// -------------------------------
// START
// -------------------------------

loadProfile();