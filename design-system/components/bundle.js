/* @ds-bundle: {"format":4,"namespace":"VikDS","components":[{"name":"Button"},{"name":"Eyebrow"},{"name":"Pill"},{"name":"Card"},{"name":"CompanyMark"},{"name":"ProofStat"},{"name":"Stat"},{"name":"Callout"},{"name":"CodeBlock"},{"name":"Nav"}]} */
(function () {
  var React = window.React, h = React.createElement;
  function cx() { return Array.prototype.slice.call(arguments).filter(Boolean).join(' '); }
  function tone(t) { return t ? 'vk-tone-' + t : ''; }

  function Button(p) {
    var cls = cx('vk-root', 'vk-btn', 'vk-btn-' + (p.variant || 'primary'), p.className);
    var tag = p.href ? 'a' : 'button';
    return h(tag, { className: cls, href: p.href, onClick: p.onClick, type: p.href ? undefined : 'button' }, p.children);
  }

  function Eyebrow(p) {
    var v = p.variant || 'box';
    return h('div', { className: cx('vk-root', 'vk-eyebrow-' + v, v === 'box' && tone(p.tone || 'green'), p.className) }, p.children);
  }

  function Pill(p) {
    var v = p.variant || 'outline';
    var tag = p.href ? 'a' : 'span';
    return h(tag, { className: cx('vk-root', 'vk-pill', 'vk-pill-' + v, tone(p.tone), p.className), href: p.href }, p.children);
  }

  function Card(p) {
    var tag = p.href ? 'a' : 'div';
    var tier = p.tier || 'primary';
    if (tier === 'secondary') {
      return h(tag, { className: cx('vk-root', 'vk-card', 'vk-card-secondary', tone(p.tone || 'green'), p.className), href: p.href },
        h('div', { className: 'vk-card-2-main' },
          h('h3', null, p.title),
          p.subtitle && h('div', { className: 'vk-card-sub' }, p.subtitle)),
        p.href && h('div', { className: 'vk-card-open' }, p.cta || 'Open', ' ', h('span', null, '\u2192')));
    }
    return h(tag, { className: cx('vk-root', 'vk-card', tone(p.tone || 'green'), p.className), href: p.href },
      p.image && h('div', { className: 'vk-card-media' }, h('img', { src: p.image, alt: p.imageAlt || '', loading: 'lazy' })),
      h('div', { className: 'vk-card-body-wrap' },
        p.number && h('div', { className: 'vk-card-num ds-dot' }, p.number),
        h('h3', null, p.title),
        p.subtitle && h('div', { className: 'vk-card-sub' }, p.subtitle),
        p.children && h('div', { className: 'vk-card-body' }, p.children),
        p.tags && h('div', { className: 'vk-card-tags' }, p.tags.map(function (t) { return h(Pill, { key: t }, t); })),
        p.href && h('div', { className: 'vk-card-open' }, p.cta || 'Open', ' ', h('span', null, '\u2192'))));
  }

  function CompanyMark(p) {
    // logoHasName: the logo already contains the company name, so the name is not repeated as text
    var showName = !(p.logo && p.logoHasName);
    return h('div', { className: cx('vk-root', 'vk-mark', p.className) },
      p.logo && h('span', { className: 'vk-mark-plate' }, h('img', { src: p.logo, alt: p.logoHasName ? p.name : '', height: 32 })),
      h('div', { className: 'vk-mark-text' },
        showName && h('div', { className: 'vk-mark-name' }, p.name),
        p.description && h('div', { className: 'vk-mark-desc' }, p.description)));
  }

  function ProofStat(p) {
    var bars = p.from != null && p.to != null;
    var max = Math.max(p.from || 0, p.to || 0) || 1;
    return h('div', { className: cx('vk-root', 'vk-proof', tone(p.tone || 'green'), p.className) },
      h('div', { className: 'vk-proof-num' }, p.value),
      h('div', { className: 'vk-proof-label' }, p.label),
      bars && h('div', { className: 'vk-proof-bars', 'aria-hidden': 'true' },
        h('span', { className: 'vk-proof-bar vk-proof-from', style: { width: (100 * p.from / max) + '%' } }),
        h('span', { className: 'vk-proof-bar vk-proof-to', style: { width: (100 * p.to / max) + '%' } })),
      p.context && h('div', { className: 'vk-proof-ctx' }, p.context));
  }

  function Stat(p) {
    return h('div', { className: cx('vk-root', 'vk-stat', tone(p.tone), p.className) },
      h('div', { className: 'vk-stat-num' }, p.value),
      h('div', { className: 'vk-stat-label' }, p.label),
      p.context && h('div', { className: 'vk-stat-ctx' }, p.context),
      p.caption && h('div', { className: 'vk-stat-cap' }, p.caption));
  }

  function Callout(p) {
    return h('div', { className: cx('vk-root', 'vk-callout', tone(p.tone), p.className) },
      p.title && h('span', { className: 'vk-callout-title' }, p.title), p.children);
  }

  function CodeBlock(p) {
    if (p.prompt) {
      return h('pre', { className: cx('vk-root', 'vk-prompt', p.className) },
        h('span', { className: 'vk-prompt-label' }, p.label || 'PROMPT'), p.children);
    }
    return h('pre', { className: cx('vk-root', 'vk-code', p.className) }, p.children);
  }

  function Nav(p) {
    return h('nav', { className: cx('vk-root', 'vk-nav', p.className) },
      h('div', { className: 'vk-nav-in' },
        h('a', { className: 'vk-nav-logo', href: p.homeHref || '#' }, p.brand || 'Vik', h('span', null, '.'), p.brandTail || 'Bharadwaj'),
        h('div', { className: 'vk-nav-links' }, (p.links || []).map(function (l) {
          return h('a', { key: l.href, href: l.href, 'aria-current': l.active ? 'page' : undefined }, l.label);
        }))));
  }

  window.VikDS = { Button: Button, Eyebrow: Eyebrow, Pill: Pill, Card: Card, CompanyMark: CompanyMark, ProofStat: ProofStat, Stat: Stat, Callout: Callout, CodeBlock: CodeBlock, Nav: Nav };
})();
