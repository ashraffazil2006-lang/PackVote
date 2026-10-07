// src/components/Loading.jsx
export default function Loading() {
  const steps = [
    { label: 'Analyzing group preferences', done: true },
    { label: 'Running K-Means clustering', done: true },
    { label: 'Computing KNN experience scores', done: false, active: true },
    { label: 'Evaluating destination suitability', done: false },
    { label: 'Predicting accommodation costs', done: false },
    { label: 'Ranking recommendations', done: false },
  ];

  return (
    <div className="loading-container">
      <div className="spinner" />
      <p className="loading-text">
        Our ML models are working on your group's perfect trip...
      </p>
      <div className="loading-steps">
        {steps.map((step, i) => (
          <div
            key={i}
            className={`loading-step ${step.active ? 'active' : ''} ${step.done ? 'done' : ''}`}
            style={{ animationDelay: `${i * 0.12}s` }}
          >
            <div className="step-dot" />
            <span>
              {step.done ? '✓ ' : step.active ? '⟳ ' : ''}
              {step.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
