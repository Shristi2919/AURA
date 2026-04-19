$(document).ready(function () {

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    })

    // Siri wave configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp", sync: true },
        out: { effect: "fadeOutUp", sync: true }
    });

    // Mic button click
    $("#MicBtn").click(function () {
        eel.playMicSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        document.body.classList.toggle("listening");
        eel.allCommands()();
    });

    // Win+A hotkey
    function doc_keyUp(e) {
        if (e.key === 'a' && e.metaKey) {
            eel.playMicSound();
            $("#ChatUI").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // Play assistant with text message
    function PlayAssistant(message) {
        if (message != "") {
            $("#ChatUI").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicButton").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // Toggle mic and send button
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicButton").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicButton").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    $("#chatbox").keypress(function (e) {
        if (e.which == 13) {
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

});

// Text input effects
const input = document.getElementById("chatbox");
let typingTimer;

input.addEventListener("input", () => {
    document.body.classList.add("typing");
    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
        document.body.classList.remove("typing");
    }, 600);
});

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && input.value.trim() !== "") {
        let message = input.value;
        const wave = document.createElement("div");
        wave.className = "wave";
        document.getElementById("TextInput").appendChild(wave);
        setTimeout(() => wave.remove(), 600);
        input.value = "";
    }
});