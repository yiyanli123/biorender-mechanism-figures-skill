const track = document.querySelector('#collections');
const slides = Array.from(track.querySelectorAll('.collection'));
const tabs = Array.from(document.querySelectorAll('.category-nav a'));
const controls = document.querySelector('.slider-controls');
const slider = controls.querySelector('input');
const previous = controls.querySelector('[data-previous]');
const next = controls.querySelector('[data-next]');
const count = controls.querySelector('output');
const status = document.querySelector('[role="status"]');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const last = slides.length - 1;
let active = 0;
let target = null;
let scrollFrame = null;

function update(index) {
  active = index;
  const title = slides[index].querySelector('strong').textContent.trim();
  tabs.forEach((tab, n) => {
    if (n === index) tab.setAttribute('aria-current', 'true');
    else tab.removeAttribute('aria-current');
  });
  previous.disabled = index === 0;
  next.disabled = index === last;
  slider.value = index + 1;
  slider.setAttribute('aria-valuetext', title);
  count.value = `${index + 1} / ${slides.length}`;
  status.textContent = `${title}, ${index + 1} of ${slides.length}`;
}

function goTo(index, animate = true) {
  const destination = Math.max(0, Math.min(last, index));
  const behavior = animate && !reducedMotion.matches ? 'smooth' : 'instant';
  target = behavior === 'smooth' ? destination : null;
  track.scrollTo({left: destination * track.clientWidth, behavior});
  update(destination);
}

tabs.forEach((tab, index) => {
  tab.addEventListener('click', event => {
    event.preventDefault();
    goTo(index);
  });
});

previous.addEventListener('click', () => goTo(active - 1));
next.addEventListener('click', () => goTo(active + 1));
slider.addEventListener('input', () => goTo(Number(slider.value) - 1, false));

track.addEventListener('keydown', event => {
  if (event.target !== track || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
  event.preventDefault();
  if (event.key === 'Home') goTo(0);
  else if (event.key === 'End') goTo(last);
  else goTo(active + (event.key === 'ArrowRight' ? 1 : -1));
});

track.addEventListener('pointerdown', () => { target = null; });
track.addEventListener('wheel', () => { target = null; }, {passive: true});
track.addEventListener('scroll', () => {
  if (scrollFrame !== null) return;
  scrollFrame = requestAnimationFrame(() => {
    scrollFrame = null;
    const position = track.scrollLeft / track.clientWidth;
    const index = Math.max(0, Math.min(last, Math.round(position)));
    if (target !== null && Math.abs(position - target) < 0.01) target = null;
    if (target === null && index !== active) update(index);
  });
}, {passive: true});

new ResizeObserver(() => goTo(active, false)).observe(track);
slider.max = slides.length;
controls.hidden = false;
track.dataset.enhanced = '';
const linkedIndex = slides.findIndex(slide => `#${slide.id}` === location.hash);
goTo(Math.max(0, linkedIndex), false);
