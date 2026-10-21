/* @ds-bundle: {"format":4,"namespace":"VikDS","components":[{"name":"Button"},{"name":"Eyebrow"},{"name":"Pill"},{"name":"Card"},{"name":"Stat"},{"name":"Callout"},{"name":"CodeBlock"},{"name":"Nav"}]} */
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
    return h(tag, { className: cx('vk-root', 'vk-card', tone(p.tone || 'green'), p.className), href: p.href },
      p.number && h('div', { className: 'vk-card-num ds-dot' }, p.number),
      h('h3', null, p.title),
      p.subtitle && h('div', { className: 'vk-card-sub' }, p.subtitle),
      p.children && h('div', { className: 'vk-card-body' }, p.children),
      p.tags && h('div', { className: 'vk-card-tags' }, p.tags.map(function (t) { return h(Pill, { key: t }, t); })),
      p.href && h('div', { className: 'vk-card-open' }, p.cta || 'Open', ' ', h('span', null, '→')));
  }

  function Stat(p) {
    return h('div', { className: cx('vk-root', 'vk-stat', tone(p.tone), p.className) },
      h('div', { className: 'vk-stat-num' }, p.value),
      h('div', { className: 'vk-stat-label' }, p.label),
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

  window.VikDS = { Button: Button, Eyebrow: Eyebrow, Pill: Pill, Card: Card, Stat: Stat, Callout: Callout, CodeBlock: CodeBlock, Nav: Nav };
})();
