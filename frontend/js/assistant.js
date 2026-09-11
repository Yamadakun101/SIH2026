/**
 * CRIMENET-AI — CASE-AWARE INVESTIGATIVE ASSISTANT
 * Rule-based local reasoning engine simulating NLP entity Q&A on synthetic intelligence graph
 */

const aiAssistant = {
  messagesContainer: null,
  chatInput: null,
  chatHistory: [],

  init() {
    this.messagesContainer = document.getElementById("chatMessages");
    this.chatInput = document.getElementById("chatInput");
    
    // Add Welcome Greeting
    if (this.chatHistory.length === 0) {
      this.addMessage("ai", `Hello Inspector Verma. I am your Case AI Assistant for investigation <strong>DL-2026-0412</strong>. I have indexed 18 synthetic entities, 22 multi-modal graph links, CDR logs, FASTag records, and CCTV optical detections.<br><br>You can click any suggested query below or ask specific questions regarding suspect associations, timeline anomalies, vehicle movements, or financial trails.`);
    }
  },

  handleUserSubmit(event) {
    if (event) event.preventDefault();
    const query = this.chatInput.value.trim();
    if (!query) return;

    this.processQuery(query);
    this.chatInput.value = "";
  },

  askPreset(queryText) {
    this.processQuery(queryText);
  },

  processQuery(query) {
    this.addMessage("user", query);

    // Show AI typing indicator
    const typingId = "typing-" + Date.now();
    this.addMessage("ai", `<span id="${typingId}"><em>Analyzing synthetic knowledge graph and correlation paths...</em></span>`);

    setTimeout(() => {
      const response = this.generateResponse(query);
      const typingEl = document.getElementById(typingId);
      if (typingEl && typingEl.parentElement) {
        typingEl.parentElement.innerHTML = response;
      }
    }, 450);
  },

  generateResponse(query) {
    const q = query.toLowerCase();

    if (q.includes("rakesh") || q.includes("central") || q.includes("suspect")) {
      return SYNTHETIC_DATA.aiResponses["rakesh"];
    } else if (q.includes("phone") || q.includes("cdr") || q.includes("call") || q.includes("number")) {
      return SYNTHETIC_DATA.aiResponses["phone"];
    } else if (q.includes("disappearance") || q.includes("before") || q.includes("happened") || q.includes("timeline")) {
      return SYNTHETIC_DATA.aiResponses["disappearance"];
    } else if (q.includes("strongest") || q.includes("evidence") || q.includes("best lead")) {
      return SYNTHETIC_DATA.aiResponses["strongest"];
    } else if (q.includes("people") || q.includes("how many") || q.includes("persons") || q.includes("associate")) {
      return SYNTHETIC_DATA.aiResponses["people"];
    } else if (q.includes("car") || q.includes("vehicle") || q.includes("swift") || q.includes("sedan") || q.includes("dl 01")) {
      return SYNTHETIC_DATA.aiResponses["vehicle"];
    } else if (q.includes("money") || q.includes("transaction") || q.includes("bank") || q.includes("50,000") || q.includes("imps")) {
      return SYNTHETIC_DATA.aiResponses["money"];
    } else if (q.includes("cctv") || q.includes("camera")) {
      return "Two optical CCTV detections are logged: (1) CCTV-DU-019 at 16:15 capturing victim Pooja Sharma boarding White Sedan DL 01 AX 4492 near Arts Faculty, and (2) CCTV-KG-084 at 18:42 capturing the vehicle passing Kashmere Gate ISBT toward the outer highway.";
    } else {
      return SYNTHETIC_DATA.aiResponses["default"];
    }
  },

  addMessage(sender, htmlContent) {
    if (!this.messagesContainer) return;

    const wrapper = document.createElement("div");
    wrapper.className = `msg-wrapper ${sender}`;
    
    const avatar = document.createElement("div");
    avatar.className = "msg-avatar";
    avatar.innerText = sender === "user" ? "IV" : "AI";

    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";
    bubble.innerHTML = htmlContent;

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    this.messagesContainer.appendChild(wrapper);

    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    this.chatHistory.push({ sender, htmlContent });
  },

  clearChat() {
    this.chatHistory = [];
    if (this.messagesContainer) {
      this.messagesContainer.innerHTML = "";
    }
    this.init();
  }
};
