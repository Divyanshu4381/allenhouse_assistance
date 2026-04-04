/**
 * Voice Speech Agent Integration (Decoupled Plugin)
 * This script dynamically injects its own UI and CSS.
 * To enable: Include <script src="speech-agent.js"></script> in index.html
 * To disable: Remove the script tag.
 */

(function initSpeechAgent() {
    // 1. Define Styles
    const voiceStyles = `
        .voice-overlay {
            position: absolute;
            top: 64px;
            left: 0;
            width: 100%;
            height: calc(100% - 64px);
            background: #ffffff;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
            padding: 40px;
            text-align: center;
        }
        .voice-active .voice-overlay { display: flex; }
        .voice-active .chatbox, .voice-active .chat-input, .voice-active .chat-footer { display: none; }
        .voice-visualizer { width: 120px; height: 120px; position: relative; margin-bottom: 30px; }
        .voice-pulse {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 80px; height: 80px;
            background: linear-gradient(45deg, #4285f4, #ea4335, #fbbc05, #34a853);
            background-size: 300% 300%; border-radius: 50%;
            animation: geminiGradient 3s ease infinite, geminiPulse 2s infinite;
            box-shadow: 0 0 20px rgba(66, 133, 244, 0.4);
        }
        .voice-pulse.thinking { animation: geminiGradient 1s linear infinite, geminiPulse 0.5s infinite; filter: hue-rotate(90deg); }
        .voice-pulse.speaking { animation: geminiGradient 2s ease infinite, speakingWave 0.6s infinite alternate; }
        @keyframes geminiGradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes geminiPulse { 0% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; } 50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; } 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; } }
        @keyframes speakingWave { from { transform: translate(-50%, -50%) scale(1); border-radius: 50%; } to { transform: translate(-50%, -50%) scale(1.2); border-radius: 40% 60% 50% 50%; } }
        .voice-status { font-size: 1.2rem; font-weight: 500; color: #002147; margin-bottom: 8px; }
        .voice-transcript { font-size: 0.95rem; color: #64748b; max-width: 280px; min-height: 1.4em; margin-bottom: 40px; }
        .voice-controls { display: flex; gap: 20px; }
        .voice-btn {
            padding: 12px 24px; border-radius: 30px; border: 1px solid #e2e8f0;
            background: #f8fafc; cursor: pointer; font-weight: 500;
            display: flex; align-items: center; gap: 8px; transition: all 0.2s;
        }
        .voice-btn:hover { background: #f1f5f9; transform: translateY(-2px); }
        .voice-btn.exit-btn { background: #002147; color: white; border: none; }
        .voice-btn.exit-btn:hover { background: #001833; }
        .voice-toggle-btn {
            width: 48px; height: 48px; background: #f1f5f9; border: none;
            color: #002147; border-radius: 50%; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            transition: all 0.2s; flex-shrink: 0;
        }
        .voice-toggle-btn svg { width: 22px; fill: currentColor; }
        .voice-toggle-btn:hover { background: #e2e8f0; transform: scale(1.05); }
    `;

    // 2. Define HTML Templates
    const voiceOverlayHTML = `
        <div class="voice-visualizer"><div class="voice-pulse" id="voicePulse"></div></div>
        <div class="voice-status" id="voiceStatus">Listening...</div>
        <div class="voice-transcript" id="voiceTranscript">Say something like "Tell me about course fees"</div>
        <div class="voice-controls">
            <button class="voice-btn" id="switchToTextBtn">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 5H4c-1.1 0-1.99.9-1.99 2L2 17c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/></svg>
                Keyboard
            </button>
            <button class="voice-btn exit-btn" id="exitVoiceBtn">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                Stop
            </button>
        </div>
    `;

    const voiceBtnHTML = `
        <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.91.39-.91.88 0 2.76-2.24 5-5 5s-5-2.24-5-5c0-.49-.42-.88-.91-.88-.5 0-.91.41-.91.91 0 3.19 2.45 5.86 5.56 6.32V20c0 .55.45 1 1 1s1-.45 1-1v-1.77c3.11-.45 5.56-3.13 5.56-6.32 0-.5-.41-.91-.91-.91z"/></svg>
    `;

    document.addEventListener("DOMContentLoaded", () => {
        // --- Injection Step ---
        const chatbot = document.querySelector(".chatbot");
        const chatInputContainer = document.querySelector(".chat-input");
        if (!chatbot || !chatInputContainer) return;

        // Inject Styles
        const styleTag = document.createElement("style");
        styleTag.id = "voiceAgentStyles";
        styleTag.textContent = voiceStyles;
        document.head.appendChild(styleTag);

        // Inject Overlay
        const voiceOverlay = document.createElement("div");
        voiceOverlay.id = "voiceOverlay";
        voiceOverlay.className = "voice-overlay";
        voiceOverlay.innerHTML = voiceOverlayHTML;
        chatbot.appendChild(voiceOverlay);

        // Inject Button
        const voiceModeBtn = document.createElement("button");
        voiceModeBtn.id = "voiceModeBtn";
        voiceModeBtn.className = "voice-toggle-btn";
        voiceModeBtn.title = "Voice Agent";
        voiceModeBtn.innerHTML = voiceBtnHTML;
        chatInputContainer.insertBefore(voiceModeBtn, chatInputContainer.firstChild);

        // --- Logic Step ---
        const chatInput = document.getElementById("chatInput");
        const sendBtn = document.getElementById("sendBtn");
        const chatbox = document.getElementById("chatbox");
        
        const voicePulse = document.getElementById("voicePulse");
        const voiceStatus = document.getElementById("voiceStatus");
        const voiceTranscript = document.getElementById("voiceTranscript");
        const switchToTextBtn = document.getElementById("switchToTextBtn");
        const exitVoiceBtn = document.getElementById("exitVoiceBtn");

        let isVoiceMode = false;
        let recognition = null;
        let currentAudio = null;

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-IN';

            recognition.onstart = () => updateVoiceUI("listening");
            recognition.onresult = (event) => {
                let transcript = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                voiceTranscript.textContent = transcript || 'Listening...';
            };
            recognition.onerror = (e) => { if (isVoiceMode) setTimeout(() => startListening(), 2000); };
            recognition.onend = () => {
                if (isVoiceMode && voiceTranscript.textContent.trim() !== "" && !voiceTranscript.textContent.includes("Say something")) {
                    processVoiceInput(voiceTranscript.textContent);
                } else if (isVoiceMode) {
                    startListening();
                }
            };
        }

        function toggleVoiceMode(show) {
            isVoiceMode = show;
            if (show) { chatbot.classList.add("voice-active"); startListening(); }
            else { chatbot.classList.remove("voice-active"); stopVoiceAgent(); }
        }

        function startListening() {
            if (!recognition) return;
            stopAllSpeech();
            voiceTranscript.textContent = 'Say something...';
            updateVoiceUI("listening");
            try { recognition.start(); } catch (e) {}
        }

        function stopVoiceAgent() { if (recognition) recognition.stop(); stopAllSpeech(); }

        function stopAllSpeech() {
            if (currentAudio) { currentAudio.pause(); currentAudio = null; }
            if (window.speechSynthesis) window.speechSynthesis.cancel();
        }

        function updateVoiceUI(state) {
            voicePulse.className = "voice-pulse";
            if (state === "listening") voiceStatus.textContent = "I'm Listening...";
            else if (state === "thinking") { voiceStatus.textContent = "Thinking..."; voicePulse.classList.add("thinking"); }
            else if (state === "speaking") { voiceStatus.textContent = "Allenhouse AI is speaking..."; voicePulse.classList.add("speaking"); }
        }

        async function processVoiceInput(text) {
            updateVoiceUI("thinking");
            try {
                const res = await fetch("/api/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: text })
                });
                const data = await res.json();
                const answer = data.answer || "I'm sorry, I couldn't understand that.";
                appendChatMessage(text, "outgoing");
                appendChatMessage(answer, "incoming");
                await playTTS(answer);
            } catch (error) { setTimeout(() => startListening(), 2000); }
        }

        async function playTTS(text) {
            function prepareTextForSpeech(html) {
                let clean = html.replace(/<[^>]*>?/gm, ' ');
                clean = clean.replace(/\|[\s-]*\|[\s-]*\|[\s-]*\|/g, ' ').replace(/\|/g, ' ');
                clean = clean.replace(/[*#=~]/g, ' ').replace(/\s+/g, ' ').trim();
                return clean;
            }
            const cleanText = prepareTextForSpeech(text);
            if (!cleanText) return;
            updateVoiceUI("speaking");
            voiceTranscript.textContent = cleanText.substring(0, 80) + (cleanText.length > 80 ? "..." : "");
            try {
                const response = await fetch(`/api/tts?text=${encodeURIComponent(cleanText)}`);
                const blob = await response.blob();
                const audioUrl = window.URL.createObjectURL(blob);
                currentAudio = new Audio(audioUrl);
                currentAudio.onended = () => { if (isVoiceMode) startListening(); };
                await currentAudio.play();
            } catch (err) {
                if (window.speechSynthesis) {
                    const utterance = new SpeechSynthesisUtterance(cleanText);
                    utterance.onend = () => { if (isVoiceMode) startListening(); };
                    window.speechSynthesis.speak(utterance);
                } else if (isVoiceMode) startListening();
            }
        }

        function appendChatMessage(message, className) {
            const chatLi = document.createElement("div");
            chatLi.classList.add("chat", className);
            let chatContent = className === "outgoing" ? `<p></p>` : `<div class="bot-avatar"><svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1H3a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73A2 2 0 0 1 12 2zM9 11a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm6 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/></svg></div><p></p>`;
            chatLi.innerHTML = chatContent;
            chatLi.querySelector("p").innerHTML = message;
            chatbox.appendChild(chatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
        }

        voiceModeBtn.addEventListener("click", () => toggleVoiceMode(true));
        switchToTextBtn.addEventListener("click", () => toggleVoiceMode(false));
        exitVoiceBtn.addEventListener("click", () => toggleVoiceMode(false));
        document.querySelector(".chatbot-toggler").addEventListener("click", () => {
            if (!document.body.classList.contains("show-chatbot")) toggleVoiceMode(false);
        });
    });
})();
