import React, { useState } from 'react';
import { 
  Clock, 
  PhoneCall, 
  CreditCard, 
  Video, 
  Camera, 
  MapPin, 
  ShieldCheck, 
  Filter 
} from 'lucide-react';

export default function TimelineView({ timelineData, onSelectEntity }) {
  const [selectedCategory, setSelectedCategory] = useState('ALL');

  const filteredEvents = selectedCategory === 'ALL'
    ? timelineData
    : timelineData.filter((evt) => evt.category === selectedCategory);

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'TELECOM':
        return <PhoneCall size={13} />;
      case 'BANKING':
        return <CreditCard size={13} />;
      case 'CCTV':
        return <Video size={13} />;
      case 'ANPR':
        return <Camera size={13} />;
      default:
        return <Clock size={13} />;
    }
  };

  return (
    <div className="timeline-container">
      {/* Filter Bar */}
      <div className="timeline-filter-bar">
        <Filter size={15} color="var(--text-secondary)" />
        <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          Filter Event Feed:
        </span>

        {['ALL', 'TELECOM', 'BANKING', 'CCTV', 'ANPR'].map((cat) => (
          <button
            key={cat}
            className={`header-btn ${selectedCategory === cat ? 'primary' : ''}`}
            onClick={() => setSelectedCategory(cat)}
            style={{ fontSize: '0.75rem', padding: '0.3rem 0.65rem' }}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Timeline List */}
      <div className="timeline-list">
        {filteredEvents.map((evt) => (
          <div key={evt.id} className="timeline-event-item">
            {/* Round Marker */}
            <div className="timeline-event-marker">
              {getCategoryIcon(evt.category)}
            </div>

            {/* Event Content Card */}
            <div className="timeline-event-card">
              <div className="timeline-event-top">
                <span className="timeline-event-time">
                  {evt.time} • <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>{evt.date}</span>
                </span>
                <span className="badge verified" style={{ fontSize: '0.68rem' }}>
                  <ShieldCheck size={11} />
                  {evt.confidence}% Confidence
                </span>
              </div>

              <h3 className="timeline-event-title">{evt.title}</h3>
              <p className="timeline-event-desc">{evt.description}</p>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderTop: '1px solid var(--border-light)', paddingTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                  <MapPin size={13} color="var(--info-blue)" />
                  <span>{evt.location}</span>
                </div>
                <div style={{ fontFamily: 'monospace', fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                  Source: {evt.source_id}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
