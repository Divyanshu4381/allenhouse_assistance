/**
 * Voice Speech Agent Integration
 * This script provides a decoupled Speech-to-Text (STT) and Text-to-Speech (TTS) integration.
 * Removing this `<script>` from HTML cleanly removes the entire feature.
 */

(function initSpeechAgent() {
    // Wait for the DOM to be ready
    document.addEventListener("DOMContentLoaded", () => {
        const chatInput = document.getElementById("chatInput");
        const sendBtn = document.getElementById("sendBtn");
        const chatbox = document.getElementById("chatbox");
        
        if (!chatInput || !sendBtn || !chatbox) {
            console.warn("Speech Agent Error: Required chat UI elements not found.");
            return;
        }

        // State to know if we should speak the NEXT bot reply
        let shouldSpeakResponse = false;

        // If the user types anything manually, we disable voice reply
        chatInput.addEventListener('keydown', () => {
            shouldSpeakResponse = false;
        });

        // If the user clicks the normal send button manually, we disable voice reply
        sendBtn.addEventListener('click', (e) => {
            if (e.isTrusted) {
                shouldSpeakResponse = false;
            }
        });

        // ==========================================
        // 1. Add Microphone UI Element Dynamically
        // ==========================================
        const micBtn = document.createElement("button");
        micBtn.id = "micBtn";
        micBtn.className = "send-btn"; // Borrowing the style of the send button
        micBtn.style.backgroundColor = "#ffb606"; // Distinct Allenhouse yellow for mic
        micBtn.innerHTML = `<svg viewBox="0 0 24 24" style="width: 20px; fill: white;"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.91.39-.91.88 0 2.76-2.24 5-5 5s-5-2.24-5-5c0-.49-.42-.88-.91-.88-.5 0-.91.41-.91.91 0 3.19 2.45 5.86 5.56 6.32V20c0 .55.45 1 1 1s1-.45 1-1v-1.77c3.11-.45 5.56-3.13 5.56-6.32 0-.5-.41-.91-.91-.91z"/></svg>`;
        micBtn.title = "Click to talk (Gemini Style)";
        micBtn.type = "button";
        
        // Insert the mic button right before the send button
        sendBtn.parentNode.insertBefore(micBtn, sendBtn);

        // ==========================================
        // 2. Setup Speech Recognition (STT)
        // ==========================================
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;

        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-IN'; // English - India

            let isRecording = false;

            micBtn.addEventListener("click", () => {
                if (isRecording) {
                    recognition.stop();
                } else {
                    recognition.start();
                }
            });

            recognition.onstart = () => {
                isRecording = true;
                micBtn.style.animation = "geminiVoicePulse 2s linear infinite";
                chatInput.placeholder = "Listening...";
                
                // Add keyframes for Google Gemini style multi-color pulse
                if (!document.getElementById("speechPulseStyle")) {
                    const style = document.createElement('style');
                    style.id = "speechPulseStyle";
                    style.innerHTML = `
                      @keyframes geminiVoicePulse {
                        0% { background: #4285f4; box-shadow: 0 0 0 0 rgba(66, 133, 244, 0.6), 0 0 0 0 rgba(234, 67, 53, 0.4); transform: scale(1); }
                        25% { background: #ea4335; }
                        50% { background: #fbbc05; box-shadow: 0 0 0 12px rgba(251, 188, 5, 0), 0 0 0 24px rgba(52, 168, 83, 0); transform: scale(1.15); }
                        75% { background: #34a853; }
                        100% { background: #4285f4; box-shadow: 0 0 0 0 rgba(66, 133, 244, 0), 0 0 0 0 rgba(234, 67, 53, 0); transform: scale(1); }
                      }
                    `;
                    document.head.appendChild(style);
                }
                
                // Stop any reading voice since user started talking
                window.speechSynthesis.cancel();
                shouldSpeakResponse = false;
            };

            recognition.onresult = (event) => {
                let currentTranscript = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    currentTranscript += event.results[i][0].transcript;
                }
                chatInput.value = currentTranscript;
                chatInput.style.height = '48px';
                chatInput.style.height = chatInput.scrollHeight + 'px';
                sendBtn.disabled = !chatInput.value.trim();
            };

            recognition.onerror = (event) => {
                console.error("Speech Recognition Error: ", event.error);
                resetMicUI();
            };

            recognition.onend = () => {
                resetMicUI();
                // If there's text after listening ends, trigger send and set Voice Mode flag
                if (chatInput.value.trim().length > 0) {
                    shouldSpeakResponse = true; // Yes, we talked! So bot should reply in voice!
                    sendBtn.click(); // Automatically click send
                }
            };

            function resetMicUI() {
                isRecording = false;
                micBtn.style.backgroundColor = "#ffb606";
                micBtn.style.animation = "none";
                chatInput.placeholder = "Enter a message...";
            }
        } else {
            console.warn("Speech Recognition API not supported in this browser.");
            micBtn.style.display = "none";
        }

        // ==========================================
        // 3. Setup Text-to-Speech (TTS) via Local Backend (ElevenLabs Proxy)
        // ==========================================
        async function speakText(text) {
            // Clean text from HTML tags
            const cleanText = text.replace(/<[^>]*>?/gm, ' ').trim();
            if (!cleanText) return;

            try {
                // Call our FastAPI backend endpoint that acts as a proxy to ElevenLabs
                // The backend safely manages the VOICE_API_KEY
                const response = await fetch(`http://127.0.0.1:8001/api/tts?text=${encodeURIComponent(cleanText)}`);
                
                if (!response.ok) {
                    console.error("Failed to fetch TTS audio from ElevenLabs Proxy");
                    return;
                }
                
                const blob = await response.blob();
                const audioUrl = window.URL.createObjectURL(blob);
                const audio = new Audio(audioUrl);
                
                // Play the high-quality ElevenLabs audio voice
                audio.play();
                
            } catch (err) {
                console.error("ElevenLabs proxy playback error:", err);
            }
        }

        // Create an observer to auto-read AI's messages ONLY if voice flow was used
        const observer = new MutationObserver((mutationsList) => {
            for(const mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1 && node.classList.contains('incoming')) {
                            setTimeout(() => {
                                const pNode = node.querySelector('p');
                                if (shouldSpeakResponse && pNode && !pNode.querySelector('.typing')) {
                                    speakText(pNode.innerHTML);
                                    shouldSpeakResponse = false; // Reset after it speaks
                                }
                            }, 100);
                        } else if (node.nodeType === 3 || (node.nodeType === 1 && node.tagName === 'P')) {
                            const parent = node.closest ? node.closest('.incoming') : (node.parentElement && node.parentElement.closest('.incoming'));
                            if (parent) {
                                const pNode = parent.querySelector('p');
                                if (shouldSpeakResponse && pNode && !pNode.querySelector('.typing') && pNode.innerText.trim().length > 0) {
                                   speakText(pNode.innerHTML);
                                   shouldSpeakResponse = false; // Reset after it speaks
                                }
                            }
                        }
                    });
                } else if (mutation.type === 'characterData' || mutation.type === 'childList') {
                     if (mutation.target.nodeName === 'P' && mutation.target.parentElement && mutation.target.parentElement.classList.contains('incoming')) {
                         if (shouldSpeakResponse && !mutation.target.querySelector('.typing')) {
                             speakText(mutation.target.innerHTML);
                             shouldSpeakResponse = false;
                         }
                     }
                }
            }
        });

        observer.observe(chatbox, { childList: true, subtree: true });

        // Preload voices
        if(window.speechSynthesis) {
            window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
        }
    });
})();
