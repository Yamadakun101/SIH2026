import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Filter, 
  MapPin, 
  Clock, 
  ShieldCheck, 
  CreditCard, 
  PhoneCall, 
  Video, 
  Camera, 
  Car,
  Crosshair,
  ArrowRight
} from 'lucide-react';

export default function TimelineView({ timelineData, onSelectEntity }) {
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [activeEventIndex, setActiveEventIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const filteredEvents = selectedCategory === 'ALL'
    ? timelineData
    : timelineData.filter((evt) => evt.category === selectedCategory);

  // Auto playback
  useEffect(() => {
    let interval = null;
    if (isPlaying) {
      interval = setInterval(() => {
        setActiveEventIndex((prev) => {
          if (prev >= filteredEvents.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, 2400);
    }
    return () => clearInterval(interval);
  }, [isPlaying, filteredEvents.length]);

  const currentEvent = filteredEvents[activeEventIndex] || filteredEvents[0];

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'TELECOM':
        return <PhoneCall size={14} />;
      case 'FINANCIAL':
      case 'BANKING':
        return <CreditCard size={14} />;
      case 'SURVEILLANCE':
      case 'CCTV':
        return <Video size={14} />;
      case 'CONVEYANCE':
      case 'ANPR':
        return <Car size={14} />;
      default:
        return <Clock size={14} />;
    }
  };

  const handlePrev = () => {
    setActiveEventIndex((prev) => Math.max(prev - 1, 0));
  };

  const handleNext = () => {
    setActiveEventIndex((prev) => Math.min(prev + 1, filteredEvents.length - 1));
  };

  return (
    <div className="horizontal-timeline-container">
      {/* Top Filter & Playback Toolbar */}
      <div className="timeline-top-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <div className="playback-controls">
            <button 
              className="control-btn" 
              onClick={handlePrev}
              disabled={activeEventIndex === 0}
              title="Previous Event"
            >
              <SkipBack size={14} />
            </button>
            <button 
              className={`control-btn play-btn ${isPlaying ? 'active' : ''}`}
              onClick={() => setIsPlaying(!isPlaying)}
              title={isPlaying ? 'Pause Auto-Playback' : 'Play Timeline Sequence'}
            >
              {isPlaying ? <Pause size={14} /> : <Play size={14} />}
            </button>
            <button 
              className="control-btn" 
              onClick={handleNext}
              disabled={activeEventIndex === filteredEvents.length - 1}
              title="Next Event"
            >
              <SkipForward size={14} />
            </button>
          </div>

          <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            Event {activeEventIndex + 1} of {filteredEvents.length}
          </div>
        </div>

        {/* Category Filter Chips */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          <Filter size={13} color="var(--text-secondary)" />
          {['ALL', 'FINANCIAL', 'SURVEILLANCE', 'CONVEYANCE', 'TELECOM'].map((cat) => (
            <button
              key={cat}
              className={`gov-badge-subtle ${selectedCategory === cat ? 'active-filter' : ''}`}
              onClick={() => {
                setSelectedCategory(cat);
                setActiveEventIndex(0);
                setIsPlaying(false);
              }}
              style={{ cursor: 'pointer', border: '1px solid var(--border-medium)' }}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Main Horizontal Track Rail */}
      <div className="horizontal-track-wrapper">
        <div className="horizontal-track-line">
          {/* Progress fill */}
          <div 
            className="horizontal-track-progress"
            style={{
              width: `${(activeEventIndex / Math.max(filteredEvents.length - 1, 1)) * 100}%`
            }}
          />

          {/* Milestone Step Nodes */}
          {filteredEvents.map((evt, idx) => {
            const isCompleted = idx <= activeEventIndex;
            const isCurrent = idx === activeEventIndex;

            return (
              <div
                key={evt.id}
                className={`horizontal-step-node ${isCurrent ? 'current' : ''} ${isCompleted ? 'completed' : ''}`}
                style={{
                  left: `${(idx / Math.max(filteredEvents.length - 1, 1)) * 100}%`
                }}
                onClick={() => {
                  setActiveEventIndex(idx);
                  setIsPlaying(false);
                }}
              >
                {/* Node Pill Marker */}
                <div className="step-marker-circle">
                  {getCategoryIcon(evt.category)}
                </div>

                {/* Step Time & Short Label Above/Below */}
                <div className="step-label-box">
                  <div className="step-time-text">{evt.time}</div>
                  <div className="step-category-pill">{evt.category}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Active Event Spotlight Card */}
      {currentEvent && (
        <div className="active-event-spotlight-card">
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '0.65rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', marginBottom: '0.25rem' }}>
                <span className="gov-badge-match">
                  {currentEvent.match_pct}% Evidence Match Score
                </span>
                <span className="gov-badge-subtle">
                  {currentEvent.category} EVENT
                </span>
              </div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                {currentEvent.title}
              </h3>
            </div>

            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--gov-navy)' }}>
                {currentEvent.time}
              </div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                {currentEvent.date}
              </div>
            </div>
          </div>

          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.55, marginBottom: '0.85rem' }}>
            {currentEvent.description}
          </p>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderTop: '1px solid var(--border-light)', paddingTop: '0.65rem', fontSize: '0.78rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-secondary)' }}>
              <MapPin size={14} color="var(--gov-navy)" />
              <span><strong>Location:</strong> {currentEvent.location}</span>
            </div>

            <div style={{ fontFamily: 'monospace', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
              Source Record: <strong>{currentEvent.source}</strong>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
