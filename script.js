/* ═══════════════════════════════════════════════
   THEME TOGGLE
═══════════════════════════════════════════════ */
(function initTheme() {
  const saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
})();

const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    window.dispatchEvent(new CustomEvent('themechange', { detail: { theme: next } }));
  });
}

/* ═══════════════════════════════════════════════
   GALAXY CANVAS
═══════════════════════════════════════════════ */
(function initGalaxy() {
  const canvas = document.getElementById('galaxyCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, stars = [], shootingStars = [];
  const STAR_COUNT = 180;

  function isLight() {
    return document.documentElement.getAttribute('data-theme') === 'light';
  }

  function getStarPalette() {
    return isLight()
      ? ['#6366f1', '#818cf8', '#4f46e5', '#a5b4fc']
      : ['#a5b4fc', '#c4b5fd', '#e0e7ff', '#ffffff'];
  }

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = canvas.parentElement ? canvas.parentElement.offsetHeight : window.innerHeight;
  }

  function randomStar() {
    const palette = getStarPalette();
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.5 + 0.3,
      alpha: Math.random() * 0.6 + 0.3,
      speed: Math.random() * 0.004 + 0.001,
      phase: Math.random() * Math.PI * 2,
      color: palette[Math.floor(Math.random() * palette.length)],
    };
  }

  function createShootingStar() {
    const angle = (Math.random() * 30 + 15) * (Math.PI / 180);
    return {
      x: Math.random() * W * 0.8,
      y: Math.random() * H * 0.35,
      len: Math.random() * 160 + 80,
      speed: Math.random() * 7 + 5,
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
      if (shootingStars.length < 3 && Math.random() < 0.6) {
        shootingStars.push(createShootingStar());
      }
    }, 2200);
    requestAnimationFrame(draw);
  }

  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    const light = isLight();

    // Subtle background nebula in dark mode
    if (!light) {
      const g1 = ctx.createRadialGradient(W * 0.25, H * 0.35, 0, W * 0.25, H * 0.35, W * 0.45);
      g1.addColorStop(0, 'rgba(99,102,241,0.08)');
      g1.addColorStop(1, 'transparent');
      ctx.fillStyle = g1;
      ctx.fillRect(0, 0, W, H);

      const g2 = ctx.createRadialGradient(W * 0.75, H * 0.65, 0, W * 0.75, H * 0.65, W * 0.4);
      g2.addColorStop(0, 'rgba(167,139,250,0.06)');
      g2.addColorStop(1, 'transparent');
      ctx.fillStyle = g2;
      ctx.fillRect(0, 0, W, H);
    }

    // Stars
    for (const s of stars) {
      const pulse = Math.sin(t * 0.001 * s.speed * 60 + s.phase);
      const a = s.alpha * (0.65 + 0.35 * pulse);
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = s.color;
      ctx.globalAlpha = light ? a * 0.5 : a;
      ctx.fill();
    }

    // Shooting stars
    const shootColor = light ? '99,102,241' : '165,180,252';
    for (let i = shootingStars.length - 1; i >= 0; i--) {
      const ss = shootingStars[i];
      ctx.save();
      const grad = ctx.createLinearGradient(ss.x, ss.y, ss.x - ss.dx * ss.len, ss.y - ss.dy * ss.len);
      grad.addColorStop(0, `rgba(${shootColor},${ss.life * 0.9})`);
      grad.addColorStop(1, `rgba(${shootColor},0)`);
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

  window.addEventListener('resize', () => {
    resize();
    stars = Array.from({ length: STAR_COUNT }, randomStar);
  });

  window.addEventListener('themechange', () => {
    stars = Array.from({ length: STAR_COUNT }, randomStar);
  });

  init();
})();

/* ═══════════════════════════════════════════════
   TYPING ANIMATION
═══════════════════════════════════════════════ */
(function initTyping() {
  const el = document.getElementById('typingText');
  if (!el) return;
  const phrases = [
    'AI & Machine Learning Specialist',
    'Data Science & Vision Developer',
    'IIT Madras NPTEL Certified',
    'B.Tech CSE (AI) Undergrad',
  ];
  let pi = 0, ci = 0, deleting = false;

  function type() {
    const phrase = phrases[pi];
    if (!deleting) {
      el.textContent = phrase.slice(0, ci + 1);
      ci++;
      if (ci === phrase.length) {
        deleting = true;
        setTimeout(type, 2000);
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
    setTimeout(type, deleting ? 50 : 80);
  }

  setTimeout(type, 1000);
})();

/* ═══════════════════════════════════════════════
   NAVBAR — Scroll & Active Link
═══════════════════════════════════════════════ */
const navbar  = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;

  // Scrolled navbar state
  if (navbar) {
    navbar.classList.toggle('scrolled', scrollY > 30);
  }

  // Back to top button visibility
  if (backToTop) {
    backToTop.classList.toggle('visible', scrollY > 400);
  }

  // Active section indicator
  let current = '';
  const isBottom = (window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 60);

  if (isBottom) {
    const lastSection = sections[sections.length - 1];
    if (lastSection) current = lastSection.id;
  } else {
    sections.forEach(sec => {
      const top = sec.offsetTop - 120;
      const height = sec.offsetHeight;
      if (scrollY >= top && scrollY < top + height) {
        current = sec.id;
      }
    });
  }

  navLinks.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
  });
}, { passive: true });

/* ═══════════════════════════════════════════════
   HAMBURGER MENU
═══════════════════════════════════════════════ */
const hamburger = document.getElementById('hamburger');
const navLinksEl = document.getElementById('navLinks');

if (hamburger && navLinksEl) {
  hamburger.addEventListener('click', () => {
    const open = navLinksEl.classList.toggle('open');
    hamburger.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Close on nav link click
  navLinksEl.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navLinksEl.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });

  // Close on click outside
  document.addEventListener('click', e => {
    if (navbar && !navbar.contains(e.target)) {
      navLinksEl.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ═══════════════════════════════════════════════
   SCROLL REVEAL (IntersectionObserver)
═══════════════════════════════════════════════ */
const revealEls = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  revealEls.forEach(el => revealObserver.observe(el));
} else {
  revealEls.forEach(el => el.classList.add('visible'));
}

/* ═══════════════════════════════════════════════
   BACK TO TOP
═══════════════════════════════════════════════ */
if (backToTop) {
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* ═══════════════════════════════════════════════
   CERTIFICATE LIGHTBOX MODAL
═══════════════════════════════════════════════ */
(function initCertModal() {
  const modal = document.getElementById('certModal');
  const openThumb = document.getElementById('certThumbWrap');
  const openBtn = document.getElementById('viewCertBtn');
  const closeBtn = document.getElementById('modalClose');

  if (!modal) return;

  function openModal() {
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    if (closeBtn) closeBtn.focus();
  }

  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (openThumb) {
    openThumb.addEventListener('click', openModal);
    openThumb.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openModal();
      }
    });
  }

  if (openBtn) {
    openBtn.addEventListener('click', openModal);
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  // Backdrop click close
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  // Escape key close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      closeModal();
    }
  });
})();

/* ═══════════════════════════════════════════════
   CONTACT FORM VALIDATION & INTERACTION
═══════════════════════════════════════════════ */
(function initForm() {
  const form      = document.getElementById('contactForm');
  const nameEl    = document.getElementById('name');
  const emailEl   = document.getElementById('email');
  const msgEl     = document.getElementById('message');
  const success   = document.getElementById('formSuccess');
  const submitBtn = document.getElementById('submitBtn');

  if (!form || !nameEl || !emailEl || !msgEl) return;

  let hasSubmitted = false;

  function setError(inputEl, errorId, msg) {
    inputEl.classList.toggle('error', !!msg);
    const errSpan = document.getElementById(errorId);
    if (errSpan) errSpan.textContent = msg;
  }

  function validateEmail(val) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  }

  function validate(showAll = false) {
    let valid = true;
    const n = nameEl.value.trim();
    const e = emailEl.value.trim();
    const m = msgEl.value.trim();

    if (!n) {
      if (showAll) setError(nameEl, 'nameError', 'Please enter your name.');
      valid = false;
    } else if (n.length < 2) {
      if (showAll) setError(nameEl, 'nameError', 'Name must be at least 2 characters.');
      valid = false;
    } else {
      setError(nameEl, 'nameError', '');
    }

    if (!e) {
      if (showAll) setError(emailEl, 'emailError', 'Please enter your email.');
      valid = false;
    } else if (!validateEmail(e)) {
      if (showAll) setError(emailEl, 'emailError', 'Please enter a valid email address.');
      valid = false;
    } else {
      setError(emailEl, 'emailError', '');
    }

    if (!m) {
      if (showAll) setError(msgEl, 'messageError', 'Please enter a message.');
      valid = false;
    } else if (m.length < 8) {
      if (showAll) setError(msgEl, 'messageError', 'Message should be at least 8 characters.');
      valid = false;
    } else {
      setError(msgEl, 'messageError', '');
    }

    return valid;
  }

  // Validate on blur
  [nameEl, emailEl, msgEl].forEach(el => {
    el.addEventListener('blur', () => {
      validate(true);
    });
    // On live input, only clear errors if already triggered
    el.addEventListener('input', () => {
      if (hasSubmitted || el.classList.contains('error')) {
        validate(false);
      }
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    hasSubmitted = true;
    if (!validate(true)) return;

    if (submitBtn) {
      submitBtn.disabled = true;
      const textSpan = submitBtn.querySelector('.btn-text');
      if (textSpan) textSpan.textContent = 'Sending Message…';
    }

    // Simulate reliable dispatch
    setTimeout(() => {
      form.reset();
      hasSubmitted = false;
      if (success) success.classList.add('show');
      if (submitBtn) {
        submitBtn.disabled = false;
        const textSpan = submitBtn.querySelector('.btn-text');
        if (textSpan) textSpan.textContent = 'Send Message';
      }
      [nameEl, emailEl, msgEl].forEach(el => el.classList.remove('error'));
      ['nameError', 'emailError', 'messageError'].forEach(id => {
        const span = document.getElementById(id);
        if (span) span.textContent = '';
      });
      setTimeout(() => {
        if (success) success.classList.remove('show');
      }, 6000);
    }, 1000);
  });
})();

/* ═══════════════════════════════════════════════
   SKILL TAG MICRO-INTERACTIONS
═══════════════════════════════════════════════ */
document.querySelectorAll('.skill-tag').forEach(tag => {
  tag.addEventListener('mouseenter', function() {
    this.style.transition = 'all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)';
  });
  tag.addEventListener('mouseleave', function() {
    this.style.transition = '';
  });
});
