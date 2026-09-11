import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Filter, 
  MapPin, 
  Clock, 
  CreditCard, 
  PhoneCall, 
  Video, 
  Car
} from 'lucide-react';

export default function TimelineView({ timelineData, onSelectEntity }) {
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [activeEventIndex, setActiveEventIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const scrollContainerRef = useRef(null);

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
      }, 2600);
    }
    return () => clearInterval(interval);
  }, [isPlaying, filteredEvents.length]);

  // Smooth scroll active card into view
  useEffect(() => {
    if (scrollContainerRef.current) {
      const activeElement = scrollContainerRef.current.querySelector(`.timeline-branch-col:nth-child(${activeEventIndex + 1})`);
      if (activeElement) {
        activeElement.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      }
    }
  }, [activeEventIndex]);

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'TELECOM':
        return <PhoneCall size={13} />;
      case 'FINANCIAL':
      case 'BANKING':
        return <CreditCard size={13} />;
      case 'SURVEILLANCE':
      case 'CCTV':
        return <Video size={13} />;
      case 'CONVEYANCE':
      case 'ANPR':
        return <Car size={13} />;
      default:
        return <Clock size={13} />;
    }
  };

  const handlePrev = () => {
    setActiveEventIndex((prev) => Math.max(prev - 1, 0));
  };

  const handleNext = () => {
    setActiveEventIndex((prev) => Math.min(prev + 1, filteredEvents.length - 1));
  };

  return (
    <div className="horizontal-branching-timeline-container">
      {/* Top Filter & Control Header */}
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
            Chronological Sequence: Event {activeEventIndex + 1} of {filteredEvents.length}
          </div>
        </div>

        {/* Category Filters */}
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

      {/* Alternating Horizontal Timeline Tree (Matching Hand-Drawn Sketch) */}
      <div className="branching-scroll-wrapper" ref={scrollContainerRef}>
        <div className="branching-timeline-canvas">
          
          {/* Continuous Center Horizontal Spine Axis Line */}
          <div className="central-horizontal-spine" />

          {/* Event Columns with Alternating Top / Bottom Stem Connectors */}
          <div className="timeline-branches-row">
            {filteredEvents.map((evt, idx) => {
              const isTop = idx % 2 === 0; // Even above, Odd below
              const isCurrent = idx === activeEventIndex;
              const isCompleted = idx <= activeEventIndex;

              return (
                <div 
                  key={evt.id}
                  className={`timeline-branch-col ${isTop ? 'branch-top' : 'branch-bottom'} ${isCurrent ? 'active-branch' : ''}`}
                  onClick={() => {
                    setActiveEventIndex(idx);
                    setIsPlaying(false);
                  }}
                >
                  {/* Top Card Area (if isTop) */}
                  {isTop ? (
                    <div className="branch-card-container top-position">
                      <div className={`timeline-event-card-box ${isCurrent ? 'current-card' : ''}`}>
                        <div className="card-top-row">
                          <span className="gov-badge-match">
                            {evt.match_pct}% Match
                          </span>
                          <span className="event-time-badge">
                            {evt.time}
                          </span>
                        </div>

                        <h4 className="event-card-title">{evt.title}</h4>
                        <p className="event-card-description">{evt.description}</p>

                        <div className="event-card-footer">
                          <div className="event-location-text">
                            <MapPin size={12} color="var(--gov-navy)" />
                            <span>{evt.location}</span>
                          </div>
                          <span className="event-source-tag">{evt.source}</span>
                        </div>
                      </div>

                      {/* Vertical Stem Line going DOWN to center axis */}
                      <div className="stem-connector-line stem-down" />
                    </div>
                  ) : (
                    <div className="branch-placeholder top-placeholder" />
                  )}

                  {/* Node Dot on the Central Axis */}
                  <div className="center-node-anchor">
                    <div className={`axis-node-dot ${isCurrent ? 'current-dot' : ''} ${isCompleted ? 'completed-dot' : ''}`}>
                      {getCategoryIcon(evt.category)}
                    </div>
                    <div className="axis-node-timestamp">{evt.time}</div>
                  </div>

                  {/* Bottom Card Area (if not isTop) */}
                  {!isTop ? (
                    <div className="branch-card-container bottom-position">
                      {/* Vertical Stem Line going UP to center axis */}
                      <div className="stem-connector-line stem-up" />

                      <div className={`timeline-event-card-box ${isCurrent ? 'current-card' : ''}`}>
                        <div className="card-top-row">
                          <span className="gov-badge-match">
                            {evt.match_pct}% Match
                          </span>
                          <span className="event-time-badge">
                            {evt.time}
                          </span>
                        </div>

                        <h4 className="event-card-title">{evt.title}</h4>
                        <p className="event-card-description">{evt.description}</p>

                        <div className="event-card-footer">
                          <div className="event-location-text">
                            <MapPin size={12} color="var(--gov-navy)" />
                            <span>{evt.location}</span>
                          </div>
                          <span className="event-source-tag">{evt.source}</span>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="branch-placeholder bottom-placeholder" />
                  )}
                </div>
              );
            })}
          </div>

        </div>
      </div>
    </div>
  );
}
