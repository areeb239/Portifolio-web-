/* ═══════════════════════════════════════════════
   THEME TOGGLE
═══════════════════════════════════════════════ */
(function initTheme() {
  const saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
})();

const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

/* ═══════════════════════════════════════════════
   GALAXY CANVAS
═══════════════════════════════════════════════ */
(function initGalaxy() {
  const canvas = document.getElementById('galaxyCanvas');
  const ctx = canvas.getContext('2d');
  let W, H, stars, shootingStars;
  const STAR_COUNT = 220;

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function randomStar() {
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.5 + 0.2,
      alpha: Math.random() * 0.7 + 0.2,
      speed: Math.random() * 0.004 + 0.001,
      phase: Math.random() * Math.PI * 2,
      color: ['#a5b4fc', '#c4b5fd', '#e0e7ff', '#ffffff'][Math.floor(Math.random() * 4)],
    };
  }

  function createShootingStar() {
    const angle = (Math.random() * 30 + 15) * (Math.PI / 180);
    return {
      x: Math.random() * W * 0.7,
      y: Math.random() * H * 0.3,
      len: Math.random() * 180 + 80,
      speed: Math.random() * 8 + 6,
      alpha: 1,
      angle,
      dx: Math.cos(angle),
      dy: Math.sin(angle),
      life: 1,
    };
  }

  function init() {
    resize();
    stars = Array.from({ length: STAR_COUNT }, randomStar);
    shootingStars = [];
    setInterval(() => {
      if (shootingStars.length < 4 && Math.random() < 0.6) {
        shootingStars.push(createShootingStar());
      }
    }, 2000);
    requestAnimationFrame(draw);
  }

  function getThemeBg() {
    return document.documentElement.getAttribute('data-theme') === 'light'
      ? 'rgba(245,247,255,0)'
      : 'rgba(8,12,24,0)';
  }

  function draw(t) {
    ctx.clearRect(0, 0, W, H);

    // Nebula glow
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    if (isDark) {
      const g1 = ctx.createRadialGradient(W * 0.25, H * 0.3, 0, W * 0.25, H * 0.3, W * 0.5);
      g1.addColorStop(0, 'rgba(99,102,241,0.07)');
      g1.addColorStop(1, 'transparent');
      ctx.fillStyle = g1; ctx.fillRect(0, 0, W, H);

      const g2 = ctx.createRadialGradient(W * 0.8, H * 0.7, 0, W * 0.8, H * 0.7, W * 0.4);
      g2.addColorStop(0, 'rgba(167,139,250,0.05)');
      g2.addColorStop(1, 'transparent');
      ctx.fillStyle = g2; ctx.fillRect(0, 0, W, H);
    }

    // Stars
    for (const s of stars) {
      const pulse = Math.sin(t * 0.001 * s.speed * 60 + s.phase);
      const a = s.alpha * (0.6 + 0.4 * pulse);
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = s.color;
      ctx.globalAlpha = a;
      ctx.fill();
    }

    // Shooting stars
    for (let i = shootingStars.length - 1; i >= 0; i--) {
      const ss = shootingStars[i];
      ctx.save();
      const grad = ctx.createLinearGradient(ss.x, ss.y, ss.x - ss.dx * ss.len, ss.y - ss.dy * ss.len);
      grad.addColorStop(0, `rgba(165,180,252,${ss.life * 0.9})`);
      grad.addColorStop(1, 'rgba(165,180,252,0)');
      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.5;
      ctx.globalAlpha = ss.life;
      ctx.beginPath();
      ctx.moveTo(ss.x, ss.y);
      ctx.lineTo(ss.x - ss.dx * ss.len, ss.y - ss.dy * ss.len);
      ctx.stroke();
      ctx.restore();

      ss.x += ss.dx * ss.speed;
      ss.y += ss.dy * ss.speed;
      ss.life -= 0.022;
      if (ss.life <= 0) shootingStars.splice(i, 1);
    }

    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', () => { resize(); stars = Array.from({ length: STAR_COUNT }, randomStar); });
  init();
})();

/* ═══════════════════════════════════════════════
   TYPING ANIMATION
═══════════════════════════════════════════════ */
(function initTyping() {
  const el = document.getElementById('typingText');
  const phrases = [
    'AI & Machine Learning Enthusiast',
    'Data Science Learner',
    'Future AI Engineer',
  ];
  let pi = 0, ci = 0, deleting = false;

  function type() {
    const phrase = phrases[pi];
    if (!deleting) {
      el.textContent = phrase.slice(0, ci + 1);
      ci++;
      if (ci === phrase.length) {
        deleting = true;
        setTimeout(type, 1800);
        return;
      }
    } else {
      el.textContent = phrase.slice(0, ci - 1);
      ci--;
      if (ci === 0) {
        deleting = false;
        pi = (pi + 1) % phrases.length;
      }
    }
    setTimeout(type, deleting ? 55 : 80);
  }

  setTimeout(type, 1200);
})();

/* ═══════════════════════════════════════════════
   NAVBAR — scroll + active link
═══════════════════════════════════════════════ */
const navbar  = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');

window.addEventListener('scroll', () => {
  // Scrolled class
  navbar.classList.toggle('scrolled', window.scrollY > 40);

  // Back to top
  document.getElementById('backToTop').classList.toggle('visible', window.scrollY > 400);

  // Active nav link
  let current = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 100) current = sec.id;
  });
  navLinks.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
  });
}, { passive: true });

/* ═══════════════════════════════════════════════
   HAMBURGER MENU
═══════════════════════════════════════════════ */
const hamburger = document.getElementById('hamburger');
const navLinksEl = document.getElementById('navLinks');

hamburger.addEventListener('click', () => {
  const open = navLinksEl.classList.toggle('open');
  hamburger.classList.toggle('open', open);
  hamburger.setAttribute('aria-expanded', open);
});

// Close on link click
navLinksEl.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    navLinksEl.classList.remove('open');
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', false);
  });
});

// Close on outside click
document.addEventListener('click', e => {
  if (!navbar.contains(e.target)) {
    navLinksEl.classList.remove('open');
    hamburger.classList.remove('open');
  }
});

/* ═══════════════════════════════════════════════
   SCROLL REVEAL
═══════════════════════════════════════════════ */
const revealEls = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

revealEls.forEach(el => revealObserver.observe(el));

/* ═══════════════════════════════════════════════
   BACK TO TOP
═══════════════════════════════════════════════ */
document.getElementById('backToTop').addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* ═══════════════════════════════════════════════
   SMOOTH SCROLL (for older browsers)
═══════════════════════════════════════════════ */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

/* ═══════════════════════════════════════════════
   CONTACT FORM VALIDATION
═══════════════════════════════════════════════ */
(function initForm() {
  const form    = document.getElementById('contactForm');
  const nameEl  = document.getElementById('name');
  const emailEl = document.getElementById('email');
  const msgEl   = document.getElementById('message');
  const success = document.getElementById('formSuccess');
  const submitBtn = document.getElementById('submitBtn');

  function setError(inputEl, errorId, msg) {
    inputEl.classList.toggle('error', !!msg);
    document.getElementById(errorId).textContent = msg;
  }

  function validateEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  function validate() {
    let valid = true;
    const n = nameEl.value.trim();
    const e = emailEl.value.trim();
    const m = msgEl.value.trim();

    if (!n) { setError(nameEl, 'nameError', 'Name is required.'); valid = false; }
    else if (n.length < 2) { setError(nameEl, 'nameError', 'Name must be at least 2 characters.'); valid = false; }
    else setError(nameEl, 'nameError', '');

    if (!e) { setError(emailEl, 'emailError', 'Email is required.'); valid = false; }
    else if (!validateEmail(e)) { setError(emailEl, 'emailError', 'Enter a valid email address.'); valid = false; }
    else setError(emailEl, 'emailError', '');

    if (!m) { setError(msgEl, 'messageError', 'Message is required.'); valid = false; }
    else if (m.length < 10) { setError(msgEl, 'messageError', 'Message must be at least 10 characters.'); valid = false; }
    else setError(msgEl, 'messageError', '');

    return valid;
  }

  // Live validation
  [nameEl, emailEl, msgEl].forEach(el => {
    el.addEventListener('input', validate);
    el.addEventListener('blur', validate);
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!validate()) return;

    // Simulate sending
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').textContent = 'Sending…';

    setTimeout(() => {
      form.reset();
      success.classList.add('show');
      submitBtn.disabled = false;
      submitBtn.querySelector('.btn-text').textContent = 'Send Message';
      [nameEl, emailEl, msgEl].forEach(el => el.classList.remove('error'));
      ['nameError','emailError','messageError'].forEach(id => {
        document.getElementById(id).textContent = '';
      });
      setTimeout(() => success.classList.remove('show'), 5000);
    }, 1200);
  });
})();

/* ═══════════════════════════════════════════════
   SKILL TAG HOVER RIPPLE (subtle micro-interaction)
═══════════════════════════════════════════════ */
document.querySelectorAll('.skill-tag').forEach(tag => {
  tag.addEventListener('mouseenter', function() {
    this.style.transition = 'all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)';
  });
  tag.addEventListener('mouseleave', function() {
    this.style.transition = '';
  });
});
