function animateCounter(elementId, start, end, duration) {
  const counter = document.getElementById(elementId);
  console.log(counter);
  let startTime = null;

  const step = (currentTime) => {
    if (startTime === null) startTime = currentTime;
    const progress = currentTime - startTime;
    const increment = Math.min(Math.floor(progress / (duration / end)), end);

    counter.textContent = increment + (increment === end ? "+" : ""); // Append '+' at the end

    if (increment < end) {
      requestAnimationFrame(step);
    }
  };

  requestAnimationFrame(step);
}

// Start the animation when the cards are in view
document.addEventListener("DOMContentLoaded", () => {
  // Use Intersection Observer to trigger the animations when the cards are in view
  const options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.1,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounter("projects-completed", 0, 10, 5000); // Projects Completed
        animateCounter("happy-clients", 0, 20, 5000); // Happy Clients
        observer.unobserve(entry.target); // Stop observing after animation
      }
    });
  }, options);

  const targets = document.querySelectorAll(".stat-card"); // Target all statistic cards
  targets.forEach((target) => observer.observe(target)); // Observe each card
});
