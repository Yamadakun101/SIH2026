/**
 * CRIMENET-AI — CHRONOLOGICAL TIMELINE RECONSTRUCTION
 * Multi-source event synthesis across telecom, physical CCTV, banking, and FASTag sensors
 */

const timelineViewer = {
  container: null,
  activeFilter: 'all',

  init(events) {
    this.container = document.getElementById("timelineStream");
    if (!this.container) return;
    this.setupFilters();
    this.render(events);
  },

  setupFilters() {
    const filterBar = document.getElementById("timelineFilters");
    if (!filterBar) return;

    filterBar.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", () => {
        filterBar.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        this.activeFilter = chip.dataset.tfilter;
        
        let filtered = SYNTHETIC_DATA.timeline;
        if (this.activeFilter !== 'all') {
          filtered = filtered.filter(e => e.category === this.activeFilter);
        }
        this.render(filtered);
      });
    });
  },

  render(events) {
    if (!this.container) return;

    if (!events || events.length === 0) {
      this.container.innerHTML = `<div style="padding: 20px; color: #64748b; text-align: center;">No events recorded under this category.</div>`;
      return;
    }

    this.container.innerHTML = events.map(evt => {
      return `
        <div class="timeline-event-item" onclick="app.inspectNodeById('${evt.entityId}')">
          <div class="t-time-col">${evt.time}</div>
          <div class="t-node-marker"></div>
          <div class="t-content-card">
            <div class="t-title">
              <span>${evt.title}</span>
              <span class="badge" style="font-size: 9px;">${evt.source}</span>
            </div>
            <p class="t-desc">${evt.desc}</p>
            <div class="t-tags">
              ${evt.tags.map(t => `<span style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">#${t}</span>`).join('')}
              <span style="color: #2563eb; margin-left: auto; font-weight: 500;">Click to inspect node →</span>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }
};
