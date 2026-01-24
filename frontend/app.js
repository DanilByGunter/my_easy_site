(() => {
  const $ = (sel, el=document) => el.querySelector(sel);
  const $$ = (sel, el=document) => Array.from(el.querySelectorAll(sel));

  const routes = [
    { path: '/', label: 'Home', render: renderHome },
    { path: '/vinyl', label: 'Vinyl', render: renderVinyl },
    { path: '/books', label: 'Books', render: renderBooks },
    { path: '/coffee', label: 'Coffee', render: renderCoffee },
    { path: '/figures', label: 'Figures', render: renderFigures },
    { path: '/projects', label: 'Projects', render: renderProjects },
    { path: '/research', label: 'Research', render: renderResearch },
    { path: '/plants', label: 'Plants', render: renderPlants },
    { path: '/media', label: 'Media', render: renderMedia },
  ];

  const state = {
    vinyl: {
      q: '',
      selectedGenres: new Set(),
    },
    coffee: {
      mode: 'brands', // brands | coffees
      selectedBrandId: null,
    }
  };

  // ---------- UI helpers ----------
  function toast(msg){
    const el = $('#toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(() => el.classList.remove('show'), 1400);
  }

  function clamp(n, a, b){ return Math.max(a, Math.min(b, n)); }

  // rating 0..10 -> HSL-ish background
  function ratingColor(r){
    const rr = clamp(r ?? 0, 0, 10);
    // 0 => 0 (red), 10 => 120 (green)
    const hue = Math.round((rr/10) * 120);
    return `hsl(${hue} 70% 18% / 0.9)`;
  }
  function ratingBorder(r){
    const rr = clamp(r ?? 0, 0, 10);
    const hue = Math.round((rr/10) * 120);
    return `hsl(${hue} 70% 55% / 0.35)`;
  }

  function avgRating(reviews){
    if(!reviews || !reviews.length) return null;
    const s = reviews.reduce((a,x) => a + (x.rating ?? 0), 0);
    return s / reviews.length;
  }

  function openModal(title, bodyHtml){
    $('#modalTitle').textContent = title;
    $('#modalBody').innerHTML = bodyHtml;
    const m = $('#modal');
    m.classList.add('open');
    m.setAttribute('aria-hidden','false');
  }
  function closeModal(){
    const m = $('#modal');
    m.classList.remove('open');
    m.setAttribute('aria-hidden','true');
    $('#modalBody').innerHTML = '';
  }

  // ---------- Router ----------
  function getPath(){
    const h = location.hash || '#/';
    const p = h.replace(/^#/, '');
    return p.startsWith('/') ? p : '/';
  }

  function setActiveNav(path){
    $$('#nav a').forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === `#${path}`);
    });
  }

  function render(){
    const main = $('#main');
    const path = getPath();
    const r = routes.find(x => x.path === path) || routes[0];
    setActiveNav(r.path);
    main.innerHTML = '';
    const page = document.createElement('div');
    page.className = 'fadeIn';
    page.appendChild(r.render());
    main.appendChild(page);
    // close mobile nav if open
    $('#nav').classList.remove('open');
  }

  // ---------- Pages ----------
  function sectionHead(title, sub){
    const wrap = document.createElement('div');
    const h = document.createElement('h1'); h.className='h1'; h.textContent = title;
    const p = document.createElement('p'); p.className='sub'; p.textContent = sub || '';
    wrap.append(h,p);
    return wrap;
  }

  function renderHome(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Home', window.DATA.about.bio));

    const grid = document.createElement('div');
    grid.className = 'grid';

    const cards = [
      {to:'#/vinyl', kicker:'Vinyl', title:'Пластинки', desc:'Круги-диски + поиск и фильтр по жанрам.'},
      {to:'#/books', kicker:'Books', title:'Книги', desc:'Полки по жанрам, корешки с шириной от названия.'},
      {to:'#/coffee', kicker:'Coffee', title:'Кофе', desc:'2 режима: бренды и кофе, отзывы по способам (espresso/cappuccino/filter).'},
      {to:'#/figures', kicker:'Figures', title:'Фигурки', desc:'Подвешенные карточки с легким покачиванием.'},
      {to:'#/projects', kicker:'GitHub', title:'Проекты', desc:'Карточки проектов (в прототипе мок-данные).'},
      {to:'#/research', kicker:'Research', title:'Исследования', desc:'Публикации + инфографика.'},
      {to:'#/plants', kicker:'Plants', title:'Растения', desc:'Фото (заглушка) + семейство/род/вид.'},
      {to:'#/media', kicker:'Media', title:'Контакты', desc:'Открыть / копировать + ссылка на внешний ресурс.'},
    ];

    cards.forEach(c => {
      const a = document.createElement('a');
      a.href = c.to;
      a.className = 'card';
      a.innerHTML = `
        <div class="kicker">${c.kicker}</div>
        <div class="title">${c.title}</div>
        <p class="desc">${c.desc}</p>
      `;
      grid.appendChild(a);
    });

    root.appendChild(grid);

    const note = document.createElement('div');
    note.className = 'item';
    note.style.marginTop = '14px';
    note.innerHTML = `
      <div class="itemTitle">Что здесь важно</div>
      <div class="itemMeta">
        На сайте отображается только то, что уже есть. Прототип без API — позже подключим Python backend и Telegram-бота.
      </div>
    `;
    root.appendChild(note);

    return root;
  }

  function renderVinyl(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Vinyl', 'Поиск по исполнителю/названию + фильтр по жанрам (чипсы).'));

    const controls = document.createElement('div');
    controls.className = 'row';

    const input = document.createElement('input');
    input.className = 'input';
    input.placeholder = 'Поиск: исполнитель или альбом…';
    input.value = state.vinyl.q;
    input.addEventListener('input', (e) => {
      state.vinyl.q = e.target.value;
      repaint();
    });

    const chips = document.createElement('div');
    chips.className = 'chips';

    window.DATA.vinylGenres.forEach(g => {
      const ch = document.createElement('button');
      ch.type='button';
      ch.className = 'chip' + (state.vinyl.selectedGenres.has(g) ? ' active' : '');
      ch.textContent = g;
      ch.addEventListener('click', () => {
        if(state.vinyl.selectedGenres.has(g)) state.vinyl.selectedGenres.delete(g);
        else state.vinyl.selectedGenres.add(g);
        repaint();
      });
      chips.appendChild(ch);
    });

    const clear = document.createElement('button');
    clear.className = 'btn';
    clear.textContent = 'Сбросить фильтры';
    clear.addEventListener('click', () => {
      state.vinyl.q='';
      state.vinyl.selectedGenres.clear();
      render();
    });

    controls.appendChild(input);
    controls.appendChild(clear);

    root.appendChild(controls);
    root.appendChild(chips);

    const grid = document.createElement('div');
    grid.className = 'vinylGrid';
    grid.style.marginTop = '12px';

    function matches(v){
      const q = state.vinyl.q.trim().toLowerCase();
      const okQ = !q || v.artist.toLowerCase().includes(q) || v.title.toLowerCase().includes(q);
      const sel = state.vinyl.selectedGenres;
      const okG = sel.size === 0 || v.genres.some(g => sel.has(g));
      return okQ && okG;
    }

    const items = window.DATA.vinyl.filter(matches);

    items.forEach(v => {
      const card = document.createElement('div');
      card.className = 'vinylCard';
      card.innerHTML = `
        <div class="disc"><div class="label"></div></div>
        <div class="vmeta">
          <div class="a">${escapeHtml(v.artist)}</div>
          <div class="t">${escapeHtml(v.title)}${v.year ? ` • ${v.year}` : ''}</div>
          <div class="t">${v.genres.map(escapeHtml).join(' · ')}</div>
        </div>
      `;
      grid.appendChild(card);
    });

    if(items.length === 0){
      const empty = document.createElement('div');
      empty.className = 'item';
      empty.textContent = 'Ничего не найдено по текущим фильтрам.';
      root.appendChild(empty);
    } else {
      root.appendChild(grid);
    }

    function repaint(){
      // перерендерим только страницу целиком (достаточно для прототипа)
      render();
    }

    return root;
  }

  function renderBooks(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Books', 'Полки по жанрам. Ширина корешка зависит от длины названия.'));

    // группируем по жанрам
    const byGenre = new Map();
    window.DATA.books.forEach(b => {
      const g = b.genre || 'Other';
      if(!byGenre.has(g)) byGenre.set(g, []);
      byGenre.get(g).push(b);
    });

    for(const [genre, books] of byGenre.entries()){
      const shelf = document.createElement('div');
      shelf.className = 'shelf';
      shelf.style.marginBottom = '12px';
      shelf.innerHTML = `
        <div class="shelfTitle">
          <div class="g">${escapeHtml(genre)}</div>
          <div class="bar"></div>
        </div>
      `;

      const spines = document.createElement('div');
      spines.className = 'spines';

      books.forEach(b => {
        const w = spineWidth(b.title);
        const spine = document.createElement('div');
        spine.className = 'spine';
        spine.style.width = w + 'px';
        spine.title = `${b.title} — ${b.author || ''}`;
        spine.innerHTML = `
          <div class="spineSmall">${escapeHtml(b.language || '')} ${escapeHtml(b.format || '')}</div>
          <div class="spineText">${escapeHtml(b.title)}</div>
        `;
        spine.addEventListener('click', () => {
          openModal('Книга', `
            <div class="list">
              <div class="item">
                <div class="itemTitle">${escapeHtml(b.title)}</div>
                <div class="itemMeta">Автор: ${escapeHtml(b.author || '—')}</div>
                <div class="itemMeta">Язык: ${escapeHtml(b.language || '—')}</div>
                <div class="itemMeta">Формат: ${escapeHtml(b.format || '—')}</div>
                <div class="itemMeta">Жанр: ${escapeHtml(b.genre || '—')}</div>
              </div>
            </div>
          `);
        });
        spines.appendChild(spine);
      });

      shelf.appendChild(spines);
      root.appendChild(shelf);
    }

    return root;
  }

  function spineWidth(title){
    const len = (title || '').length;
    // мягкая нелинейность: короткие книги не слишком тонкие, длинные не слишком широкие
    const w = 32 + Math.sqrt(len) * 18;
    return Math.round(clamp(w, 44, 140));
  }

  function renderCoffee(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Coffee', '2 режима: бренды и кофе. У кофе несколько отзывов по способам.'));

    const tabs = document.createElement('div');
    tabs.className = 'tabs';

    const tabBrands = document.createElement('button');
    tabBrands.className = 'tab' + (state.coffee.mode === 'brands' ? ' active' : '');
    tabBrands.textContent = 'Бренды';
    tabBrands.addEventListener('click', () => { state.coffee.mode='brands'; state.coffee.selectedBrandId=null; render(); });

    const tabCoffees = document.createElement('button');
    tabCoffees.className = 'tab' + (state.coffee.mode === 'coffees' ? ' active' : '');
    tabCoffees.textContent = 'Кофе';
    tabCoffees.addEventListener('click', () => { state.coffee.mode='coffees'; state.coffee.selectedBrandId=null; render(); });

    tabs.append(tabBrands, tabCoffees);
    root.appendChild(tabs);

    if(state.coffee.mode === 'brands'){
      const grid = document.createElement('div');
      grid.className = 'brandGrid';
      grid.style.marginTop = '12px';

      window.DATA.coffeeBrands.forEach(br => {
        const coffees = window.DATA.coffee.filter(c => c.brandId === br.id);
        const avgs = coffees.map(c => avgRating(c.reviews)).filter(x => x != null);
        const avg = avgs.length ? (avgs.reduce((a,x)=>a+x,0)/avgs.length) : null;

        const tile = document.createElement('div');
        tile.className = 'brandTile';
        tile.style.background = avg != null ? ratingColor(avg) : 'rgba(17,22,37,.55)';
        tile.style.borderColor = avg != null ? ratingBorder(avg) : 'rgba(232,238,252,.12)';
        tile.innerHTML = `
          <div class="bn">${escapeHtml(br.name)}</div>
          <div class="avg">Средняя оценка: ${avg != null ? avg.toFixed(2) : '—'}</div>
          <div class="avg">Кофе: ${coffees.length}</div>
        `;
        tile.addEventListener('click', () => {
          state.coffee.selectedBrandId = br.id;
          showBrandCoffees(br);
        });
        grid.appendChild(tile);
      });

      root.appendChild(grid);

      if(state.coffee.selectedBrandId){
        const br = window.DATA.coffeeBrands.find(b => b.id === state.coffee.selectedBrandId);
        if(br) showBrandCoffees(br);
      }

      function showBrandCoffees(br){
        // перерендерим секцию ниже — простым способом: модалка
        const coffees = window.DATA.coffee.filter(c => c.brandId === br.id);
        const body = coffees.map(c => coffeeCardHtml(c, br)).join('');
        openModal(`Кофе бренда: ${br.name}`, `
          <div class="coffeeGrid">${body}</div>
          <div style="height:6px"></div>
          <div class="sub">Нажми на кофе, чтобы открыть таблицу отзывов.</div>
        `);
        // подвесим обработчик кликов внутри модалки
        setTimeout(() => {
          $$('#modalBody .coffeeCard').forEach(el => {
            el.addEventListener('click', () => {
              const id = el.getAttribute('data-id');
              const coffee = window.DATA.coffee.find(x => x.id === id);
              if(coffee) openCoffeeDetails(coffee);
            });
          });
        }, 0);
      }

    } else {
      const grid = document.createElement('div');
      grid.className = 'coffeeGrid';
      grid.style.marginTop = '12px';

      window.DATA.coffee.forEach(c => {
        const br = window.DATA.coffeeBrands.find(b => b.id === c.brandId);
        const card = document.createElement('div');
        card.className = 'coffeeCard';
        card.innerHTML = coffeeCardHtml(c, br);
        card.addEventListener('click', () => openCoffeeDetails(c));
        grid.appendChild(card);
      });

      root.appendChild(grid);
    }

    return root;
  }

  function coffeeCardHtml(c, br){
    const avg = avgRating(c.reviews);
    const bg = avg != null ? ratingColor(avg) : 'rgba(255,255,255,.04)';
    const bd = avg != null ? ratingBorder(avg) : 'rgba(232,238,252,.14)';

    return `
      <div class="pack" style="background:${bg}; border-color:${bd}">
        <div class="packLabel">${escapeHtml(c.name)}</div>
      </div>
      <div class="vmeta" style="margin-top:10px">
        <div class="a">${escapeHtml(br?.name || '—')}</div>
        <div class="t">${escapeHtml(c.region || '—')} • ${escapeHtml(c.processing || '—')}</div>
        <div class="t">Средняя оценка: ${avg != null ? avg.toFixed(2) : '—'}</div>
      </div>
    `;
  }

  function openCoffeeDetails(c){
    const br = window.DATA.coffeeBrands.find(b => b.id === c.brandId);
    const avg = avgRating(c.reviews);

    const rows = (c.reviews || []).map(r => `
      <tr>
        <td>${escapeHtml(r.method)}</td>
        <td>${(r.rating ?? '—')}</td>
        <td>${escapeHtml(r.notes || '—')}</td>
      </tr>
    `).join('');

    openModal(`${br?.name || 'Coffee'} — ${c.name}`, `
      <div class="item">
        <div class="itemTitle">${escapeHtml(c.name)}</div>
        <div class="itemMeta">Бренд: ${escapeHtml(br?.name || '—')}</div>
        <div class="itemMeta">Регион: ${escapeHtml(c.region || '—')}</div>
        <div class="itemMeta">Обработка: ${escapeHtml(c.processing || '—')}</div>
        <div class="itemMeta">Средняя оценка: ${avg != null ? avg.toFixed(2) : '—'}</div>
      </div>

      <div style="height:10px"></div>

      <table class="table">
        <thead>
          <tr>
            <th>Способ</th>
            <th>Оценка</th>
            <th>Заметки</th>
          </tr>
        </thead>
        <tbody>
          ${rows || '<tr><td colspan="3">Нет отзывов</td></tr>'}
        </tbody>
      </table>
    `);
  }

  function renderFigures(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Figures', 'Фигурки “висят на ниточке” + лёгкая анимация покачивания.'));

    const grid = document.createElement('div');
    grid.className = 'hangerWrap';

    window.DATA.figures.forEach(f => {
      const card = document.createElement('div');
      card.className = 'hanger';
      card.innerHTML = `
        <div class="string"></div>
        <div class="figure"></div>
        <div class="figureName">${escapeHtml(f.name)}</div>
        <div class="figureBrand">${escapeHtml(f.brand)}</div>
      `;
      grid.appendChild(card);
    });

    root.appendChild(grid);
    return root;
  }

  function renderProjects(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('GitHub Projects', 'В прототипе — мок-данные. Позже можно подтягивать через GitHub API или ботом.'));

    const grid = document.createElement('div');
    grid.className = 'grid';

    window.DATA.projects.forEach(p => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div class="kicker">Repository</div>
        <div class="title">${escapeHtml(p.name)}</div>
        <p class="desc">${escapeHtml(p.desc)}</p>
        <div style="height:8px"></div>
        <div class="chips">
          ${(p.tags||[]).map(t => `<span class="chip" style="cursor:default">${escapeHtml(t)}</span>`).join('')}
        </div>
      `;
      grid.appendChild(card);
    });

    root.appendChild(grid);
    return root;
  }

  function renderResearch(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Research & Infographics', 'Публикации + примеры инфографики (заглушки).'));

    const pub = document.createElement('div');
    pub.className = 'item';
    pub.innerHTML = `<div class="itemTitle">Публикации</div>`;

    const pubList = document.createElement('div');
    pubList.className = 'list';
    pubList.style.marginTop = '10px';

    window.DATA.publications.forEach(x => {
      const it = document.createElement('div');
      it.className = 'item';
      it.innerHTML = `
        <div class="itemTop">
          <div class="spacer">
            <div class="itemTitle">${escapeHtml(x.title)}</div>
            <div class="itemMeta">${escapeHtml(x.venue || '—')} • ${escapeHtml(String(x.year || '—'))}</div>
          </div>
          <button class="btn" data-open="${escapeHtml(x.url || '')}">Открыть</button>
        </div>
      `;
      it.querySelector('button')?.addEventListener('click', () => {
        if(x.url) window.open(x.url, '_blank', 'noopener');
      });
      pubList.appendChild(it);
    });

    pub.appendChild(pubList);

    const info = document.createElement('div');
    info.className = 'item';
    info.style.marginTop = '12px';
    info.innerHTML = `<div class="itemTitle">Инфографика</div>`;

    const grid = document.createElement('div');
    grid.className = 'grid';
    grid.style.marginTop = '10px';

    window.DATA.infographics.forEach(i => {
      const c = document.createElement('div');
      c.className = 'card';
      c.innerHTML = `
        <div class="kicker">${escapeHtml(i.topic || 'Topic')}</div>
        <div class="title">${escapeHtml(i.title)}</div>
        <p class="desc">Заглушка изображения. Позже здесь будет ассет из Object Storage.</p>
      `;
      grid.appendChild(c);
    });

    info.appendChild(grid);

    root.append(pub, info);
    return root;
  }

  function renderPlants(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Plants', 'Фото (заглушка) + семейство/род/вид. 1 фото на объект.'));

    const grid = document.createElement('div');
    grid.className = 'grid';

    window.DATA.plants.forEach(p => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div class="pack" style="height:140px; background: rgba(255,255,255,.03)">
          <div class="packLabel">Фото растения</div>
        </div>
        <div class="title" style="margin-top:10px">${escapeHtml(p.commonName || `${p.genus || ''} ${p.species || ''}`.trim() || 'Plant')}</div>
        <p class="desc">${escapeHtml(p.family || '—')} / ${escapeHtml(p.genus || '—')} / ${escapeHtml(p.species || '—')}</p>
      `;
      grid.appendChild(card);
    });

    root.appendChild(grid);
    return root;
  }

  function renderMedia(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Media / Contacts', 'Открыть / копировать. Wishlist — по ссылке на внешний ресурс.'));

    const ext = document.createElement('div');
    ext.className = 'item';
    ext.innerHTML = `
      <div class="itemTop">
        <div class="spacer">
          <div class="itemTitle">Внешний ресурс</div>
          <div class="itemMeta">Там будет wishlist/changelog и любая доп. информация.</div>
        </div>
        <button class="btn primary" id="openWish">Открыть</button>
      </div>
    `;
    ext.querySelector('#openWish')?.addEventListener('click', () => {
      window.open(window.DATA.media.externalWishUrl, '_blank', 'noopener');
    });

    const list = document.createElement('div');
    list.className = 'list';
    list.style.marginTop = '12px';

    window.DATA.media.links.forEach(l => {
      const item = document.createElement('div');
      item.className = 'item';
      item.innerHTML = `
        <div class="itemTop">
          <div class="spacer">
            <div class="itemTitle">${escapeHtml(l.type)}</div>
            <div class="itemMeta">${escapeHtml(l.label || l.value)}</div>
          </div>
          <button class="btn" data-open="1">Открыть</button>
          <button class="btn" data-copy="1">Копировать</button>
        </div>
      `;

      const openBtn = item.querySelector('[data-open]');
      const copyBtn = item.querySelector('[data-copy]');

      openBtn?.addEventListener('click', () => {
        if(isProbablyUrl(l.value)) window.open(l.value, '_blank', 'noopener');
        else toast('Это не ссылка — используйте копирование.');
      });

      copyBtn?.addEventListener('click', async () => {
        try{
          await navigator.clipboard.writeText(l.value);
          toast('Скопировано');
        }catch{
          // fallback
          const ta = document.createElement('textarea');
          ta.value = l.value;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          ta.remove();
          toast('Скопировано');
        }
      });

      list.appendChild(item);
    });

    root.append(ext, list);
    return root;
  }

  // ---------- Utilities ----------
  function escapeHtml(s){
    return String(s ?? '')
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'",'&#039;');
  }

  function isProbablyUrl(s){
    return /^https?:\/\//i.test(String(s||''));
  }

  // ---------- Init ----------
  function initNav(){
    const nav = $('#nav');
    nav.innerHTML = routes.map(r => `<a href="#${r.path}">${r.label}</a>`).join('');

    $('#burger').addEventListener('click', () => {
      nav.classList.toggle('open');
    });

    // close nav on outside click (mobile)
    document.addEventListener('click', (e) => {
      const navOpen = nav.classList.contains('open');
      if(!navOpen) return;
      const inNav = nav.contains(e.target) || e.target === $('#burger');
      if(!inNav) nav.classList.remove('open');
    });
  }

  function initModal(){
    $('#modalClose').addEventListener('click', closeModal);
    $('#modal').addEventListener('click', (e) => {
      const t = e.target;
      if(t && t.getAttribute && t.getAttribute('data-close') === '1') closeModal();
    });
    window.addEventListener('keydown', (e) => {
      if(e.key === 'Escape') closeModal();
    });
  }

  window.addEventListener('hashchange', render);
  initNav();
  initModal();
  if(!location.hash) location.hash = '#/';
  render();
})();
