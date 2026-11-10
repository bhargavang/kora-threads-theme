/*
  <kora-shop-the-look>: links the numbered hotspots on the look image to the
  numbered product list next to it.
  - Tap or click a hotspot: its product is highlighted (and scrolled into
    view on narrow screens). Tap again to clear.
  - Hover or focus a product in the list: its hotspot lights up.
*/

if (!customElements.get('kora-shop-the-look')) {
  class KoraShopTheLook extends HTMLElement {
    connectedCallback() {
      this.hotspots = Array.from(this.querySelectorAll('.kora-look__hotspot'));
      this.items = Array.from(this.querySelectorAll('.kora-look__item'));

      this.hotspots.forEach((hotspot) => {
        hotspot.addEventListener('click', () => {
          const isOpen = hotspot.getAttribute('aria-expanded') === 'true';
          this.setActive(isOpen ? null : hotspot.dataset.lookIndex, !isOpen);
        });
      });

      this.items.forEach((item) => {
        const index = item.dataset.lookIndex;
        item.addEventListener('mouseenter', () => this.setHovered(index));
        item.addEventListener('mouseleave', () => this.setHovered(null));
        item.addEventListener('focusin', () => this.setHovered(index));
        item.addEventListener('focusout', () => this.setHovered(null));
      });

      this.onKeyUp = (event) => {
        if (event.key === 'Escape') this.setActive(null, false);
      };
      this.addEventListener('keyup', this.onKeyUp);
    }

    setActive(index, scrollToItem) {
      this.hotspots.forEach((hotspot) => {
        hotspot.setAttribute('aria-expanded', String(hotspot.dataset.lookIndex === index));
      });

      let activeItem = null;
      this.items.forEach((item) => {
        const isActive = item.dataset.lookIndex === index;
        item.classList.toggle('is-active', isActive);
        if (isActive) activeItem = item;
      });

      // On phones the list sits under the image, so bring the product up.
      if (scrollToItem && activeItem && window.matchMedia('(max-width: 989px)').matches) {
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        activeItem.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' });
      }
    }

    setHovered(index) {
      this.hotspots.forEach((hotspot) => {
        hotspot.classList.toggle('is-hovered', hotspot.dataset.lookIndex === index);
      });
    }
  }

  customElements.define('kora-shop-the-look', KoraShopTheLook);
}
