// Konfetti-Bibliothek von CDN laden
(function() {
  var script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js';
  document.head.appendChild(script);
})();

// Kontinuierliches Konfetti für 5 Sekunden
function startConfetti() {
  const duration = 5 * 1000;
  const animationEnd = Date.now() + duration;
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 1000 };
  
  function randomInRange(min, max) {
    return Math.random() * (max - min) + min;
  }
  
  const interval = setInterval(function() {
    const timeLeft = animationEnd - Date.now();
    if(timeLeft <= 0) {
      return clearInterval(interval);
    }
    const particleCount = 50 * (timeLeft / duration);
    // Konfetti mit bunten Farben
    confetti(Object.assign({}, defaults, {
      particleCount,
      origin: { x: Math.random(), y: Math.random() - 0.2 }
    }));
  }, 250);
}

// Einzelne Konfetti-Explosion
function singleConfetti(options = {}) {
  const defaults = {
    particleCount: 150,
    spread: 70,
    origin: { y: 0.6 }
  };
  
  if (typeof confetti === 'function') {
    confetti(Object.assign({}, defaults, options));
  }
}

// Mehrfache Konfetti-Explosionen
function multipleConfetti() {
  if (typeof confetti !== 'function') return;
  
  // Erste Explosion
  confetti({
    particleCount: 150,
    spread: 70,
    origin: { y: 0.6 }
  });
  
  // Zweite Explosion von links
  setTimeout(() => {
    confetti({
      particleCount: 100,
      spread: 60,
      origin: { x: 0.2, y: 0.7 }
    });
  }, 300);
  
  // Dritte Explosion von rechts
  setTimeout(() => {
    confetti({
      particleCount: 100,
      spread: 60,
      origin: { x: 0.8, y: 0.7 }
    });
  }, 600);
}

// Perfekte Punktzahl Konfetti (Extra spektakulär!)
function perfectScoreConfetti() {
  if (typeof confetti !== 'function') return;
  
  // Starte kontinuierliches Konfetti
  startConfetti();
  
  // Zusätzliche große Explosion nach 1 Sekunde
  setTimeout(() => {
    confetti({
      particleCount: 200,
      spread: 90,
      origin: { y: 0.5 },
      colors: ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
    });
  }, 1000);
  
  // Noch eine Explosion nach 2 Sekunden
  setTimeout(() => {
    confetti({
      particleCount: 150,
      spread: 120,
      origin: { y: 0.4 },
      colors: ['#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43', '#54A0FF']
    });
  }, 2000);
}

// Quiz-spezifische Konfetti-Funktion basierend auf Prozentsatz
function celebrateQuizResult(percentage) {
  setTimeout(() => {
    if (percentage === 100) {
      perfectScoreConfetti();
    } else if (percentage >= 80) {
      multipleConfetti();
    } else if (percentage >= 70) {
      startConfetti();
    }
  }, 1000);
}