/*
  Kora Threads product page behaviour:
  - <kora-size-guide>: opens the size chart in a native <dialog> and
    switches the table between inches and cm.
  - <kora-whatsapp-order>: keeps the WhatsApp link in sync with the
    selected variant.
*/

if (!customElements.get('kora-size-guide')) {
  const UNIT_KEY = 'kora-size-unit';

  class KoraSizeGuide extends HTMLElement {
    connectedCallback() {
      this.dialog = this.querySelector('dialog');
      this.opener = this.querySelector('.kora-size-guide__opener');
      if (!this.dialog || !this.opener) return;

      this.opener.addEventListener('click', () => this.open());

      // A click on the <dialog> element itself (not its panel) is a click
      // on the backdrop, so treat it like the close button.
      this.dialog.addEventListener('click', (event) => {
        if (event.target === this.dialog || event.target.closest('[data-kora-close]')) {
          this.dialog.close();
        }
      });

      this.dialog.addEventListener('close', () => {
        document.body.classList.remove('overflow-hidden');
        this.opener.focus();
      });

      this.querySelectorAll('[data-unit]').forEach((button) => {
        button.addEventListener('click', () => this.setUnit(button.dataset.unit));
      });

      this.setUnit(this.savedUnit());
    }

    open() {
      if (typeof this.dialog.showModal === 'function') {
        this.dialog.showModal();
        document.body.classList.add('overflow-hidden');
      } else {
        this.dialog.setAttribute('open', '');
      }
    }

    savedUnit() {
      try {
        return localStorage.getItem(UNIT_KEY) === 'cm' ? 'cm' : 'in';
      } catch (error) {
        return 'in';
      }
    }

    setUnit(unit) {
      this.querySelectorAll('[data-unit]').forEach((button) => {
        button.setAttribute('aria-pressed', String(button.dataset.unit === unit));
      });

      this.querySelectorAll('td[data-inches]').forEach((cell) => {
        const inches = parseFloat(cell.dataset.inches);
        if (Number.isNaN(inches)) return;
        cell.textContent = unit === 'cm' ? String(Math.round(inches * 2.54)) : cell.dataset.inches;
      });

      try {
        localStorage.setItem(UNIT_KEY, unit);
      } catch (error) {
        // Private mode or storage blocked: the switch still works for this page.
      }
    }
  }

  customElements.define('kora-size-guide', KoraSizeGuide);
}

if (!customElements.get('kora-whatsapp-order')) {
  class KoraWhatsAppOrder extends HTMLElement {
    connectedCallback() {
      this.link = this.querySelector('a[id^="KoraWhatsApp-"]');
      if (!this.link || typeof subscribe !== 'function' || typeof PUB_SUB_EVENTS === 'undefined') return;

      // Dawn publishes variantChange with the section re-rendered for the
      // new variant. Our Liquid already built the right link in there.
      this.unsubscribe = subscribe(PUB_SUB_EVENTS.variantChange, (event) => {
        const data = event && event.data;
        if (!data || data.sectionId !== this.dataset.section || !data.html) return;

        const freshLink = data.html.getElementById(this.link.id);
        if (freshLink) this.link.href = freshLink.getAttribute('href');
      });
    }

    disconnectedCallback() {
      if (this.unsubscribe) this.unsubscribe();
    }
  }

  customElements.define('kora-whatsapp-order', KoraWhatsAppOrder);
}
