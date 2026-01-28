(() => {
  const $ = (sel, el=document) => el.querySelector(sel);
  const $$ = (sel, el=document) => Array.from(el.querySelectorAll(sel));

  // Global data store
  let DATA = null;

  // API configuration
  const API_BASE = '/api/v1';

  // Load data from API
  async function loadData() {
    try {
      const response = await fetch(`${API_BASE}/all`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      DATA = await response.json();
      return DATA;
    } catch (error) {
      console.error('Failed to load data from API:', error);
      toast('Ошибка загрузки данных. Попробуйте обновить страницу.');
      // Fallback to empty data structure
      DATA = {
        about: { bio: 'Ошибка загрузки данных' },
        vinylGenres: [],
        vinyl: [],
        books: [],
        coffeeBrands: [],
        coffee: [],
        figures: [],
        projects: [],
        publications: [],
        infographics: [],
        plants: [],
        media: { externalWishUrl: '', links: [] }
      };
      return DATA;
    }
  }

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
    books: {
      q: '',
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
    root.appendChild(sectionHead('Home', DATA.about.bio));

    const grid = document.createElement('div');
    grid.className = 'grid';

    const cards = [
      {to:'#/vinyl', kicker:'Vinyl', title:'Пластинки', desc:'Поиск и фильтр по жанрам.'},
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
      updateVinylResults();
    });

    const chips = document.createElement('div');
    chips.className = 'chips';

    DATA.vinylGenres.forEach(g => {
      const ch = document.createElement('button');
      ch.type='button';
      ch.className = 'chip' + (state.vinyl.selectedGenres.has(g) ? ' active' : '');
      ch.textContent = g;
      ch.addEventListener('click', () => {
        if(state.vinyl.selectedGenres.has(g)) state.vinyl.selectedGenres.delete(g);
        else state.vinyl.selectedGenres.add(g);
        updateVinylResults();
      });
      chips.appendChild(ch);
    });

    const clear = document.createElement('button');
    clear.className = 'btn';
    clear.textContent = 'Сбросить фильтры';
    clear.addEventListener('click', () => {
      state.vinyl.q='';
      state.vinyl.selectedGenres.clear();
      input.value = '';
      updateVinylResults();
    });

    controls.appendChild(input);
    controls.appendChild(clear);

    root.appendChild(controls);
    root.appendChild(chips);

    const resultsContainer = document.createElement('div');
    resultsContainer.id = 'vinylResults';

    function matches(v){
      const q = state.vinyl.q.trim().toLowerCase();
      const okQ = !q || v.artist.toLowerCase().includes(q) || v.title.toLowerCase().includes(q);
      const sel = state.vinyl.selectedGenres;
      const okG = sel.size === 0 || v.genres.some(g => sel.has(g));
      return okQ && okG;
    }

    function updateVinylResults(){
      const container = document.getElementById('vinylResults');
      if (!container) return;

      container.innerHTML = '';

      const items = DATA.vinyl.filter(matches);

      if(items.length === 0){
        const empty = document.createElement('div');
        empty.className = 'item';
        empty.textContent = 'Ничего не найдено по текущим фильтрам.';
        container.appendChild(empty);
      } else {
        const grid = document.createElement('div');
        grid.className = 'vinylGrid';
        grid.style.marginTop = '12px';

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

        container.appendChild(grid);
      }
    }

    root.appendChild(resultsContainer);

    // Вызываем updateVinylResults после добавления в DOM
    setTimeout(() => updateVinylResults(), 0);

    return root;
  }

  function renderBooks(){
    const root = document.createElement('div');
    root.appendChild(sectionHead('Books', 'Полки по жанрам. Ширина корешка зависит от длины названия.'));

    // Добавляем поиск
    const searchContainer = document.createElement('div');
    searchContainer.className = 'row';
    searchContainer.style.marginBottom = '16px';

    const searchInput = document.createElement('input');
    searchInput.className = 'input';
    searchInput.placeholder = 'Поиск по названию или автору...';
    searchInput.value = state.books.q;
    searchInput.addEventListener('input', (e) => {
      state.books.q = e.target.value;
      updateBooksResults();
    });

    const clearBtn = document.createElement('button');
    clearBtn.className = 'btn';
    clearBtn.textContent = 'Сбросить';
    clearBtn.addEventListener('click', () => {
      state.books.q = '';
      searchInput.value = '';
      updateBooksResults();
    });

    searchContainer.appendChild(searchInput);
    searchContainer.appendChild(clearBtn);
    root.appendChild(searchContainer);

    const resultsContainer = document.createElement('div');
    resultsContainer.id = 'booksResults';
    root.appendChild(resultsContainer);

    function updateBooksResults(){
      const container = document.getElementById('booksResults');
      if (!container) return;

      container.innerHTML = '';

      // Фильтруем книги по поиску
      const filteredBooks = DATA.books.filter(b => {
        const q = state.books.q.trim().toLowerCase();
        return !q || b.title.toLowerCase().includes(q) || (b.author && b.author.toLowerCase().includes(q));
      });

      if (filteredBooks.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'item';
        empty.textContent = 'Ничего не найдено по запросу.';
        container.appendChild(empty);
        return;
      }

      // группируем по жанрам
      const byGenre = new Map();
      filteredBooks.forEach(b => {
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
            openBookModal(b);
          });
          spines.appendChild(spine);
        });

        shelf.appendChild(spines);
        container.appendChild(shelf);
      }
    }

    // Вызываем updateBooksResults после добавления в DOM
    setTimeout(() => updateBooksResults(), 0);
    return root;
  }

  function openBookModal(book) {
    const quotes = book.quotes || [];
    const opinion = book.opinion || '';

    const modalContent = `
      <div class="item">
        <div class="itemTitle">${escapeHtml(book.title)}</div>
        <div class="itemMeta">Автор: ${escapeHtml(book.author || '—')}</div>
        <div class="itemMeta">Язык: ${escapeHtml(book.language || '—')}</div>
        <div class="itemMeta">Формат: ${escapeHtml(book.format || '—')}</div>
        <div class="itemMeta">Жанр: ${escapeHtml(book.genre || '—')}</div>
      </div>

      <div style="height:16px"></div>

      <div class="tabs" id="bookTabs">
        <button class="tab active" data-tab="quotes">Цитаты</button>
        <button class="tab" data-tab="opinion">Авторское мнение</button>
      </div>

      <div style="height:12px"></div>

      <div id="bookTabContent">
        <div id="quotesTab" class="book-tab-panel">
          ${quotes.length > 0 ?
            quotes.map(quote => `
              <div class="quote-block" style="margin-bottom: 12px; padding: 14px; border-radius: var(--radius2); border: 1px solid var(--line); background: rgba(255,255,255,.02); position: relative;">
                <div style="font-style: italic; line-height: 1.5; margin-bottom: 8px;">"${escapeHtml(quote.text)}"</div>
                ${quote.page ? `<div style="color: var(--muted); font-size: 12px;">Стр. ${quote.page}</div>` : ''}
                <button class="copy-quote-btn" style="position: absolute; top: 8px; right: 8px; padding: 4px 8px; border: 1px solid var(--line); background: rgba(255,255,255,.04); border-radius: 6px; font-size: 11px; cursor: pointer;" data-text="${escapeHtml(quote.text)}">📋</button>
              </div>
            `).join('')
            : '<div class="item"><div class="itemMeta">Цитаты пока не добавлены</div></div>'
          }
        </div>

        <div id="opinionTab" class="book-tab-panel" style="display: none;">
          ${opinion ?
            `<div class="item"><div class="itemMeta" style="line-height: 1.6;">${escapeHtml(opinion).replace(/\n/g, '<br>')}</div></div>`
            : '<div class="item"><div class="itemMeta">Авторское мнение пока не добавлено</div></div>'
          }
        </div>
      </div>
    `;

    openModal(`${book.title}`, modalContent);

    // Добавляем обработчики для вкладок
    setTimeout(() => {
      const tabs = document.querySelectorAll('#bookTabs .tab');
      const panels = document.querySelectorAll('.book-tab-panel');

      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const targetTab = tab.getAttribute('data-tab');

          // Обновляем активную вкладку
          tabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');

          // Показываем соответствующую панель
          panels.forEach(panel => {
            panel.style.display = 'none';
          });
          document.getElementById(targetTab + 'Tab').style.display = 'block';
        });
      });

      // Обработчики для копирования цитат
      const copyBtns = document.querySelectorAll('.copy-quote-btn');
      copyBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
          e.stopPropagation();
          const text = btn.getAttribute('data-text');
          try {
            await navigator.clipboard.writeText(text);
            toast('Цитата скопирована');
          } catch {
            // fallback
            const ta = document.createElement('textarea');
            ta.value = text;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            ta.remove();
            toast('Цитата скопирована');
          }
        });
      });
    }, 0);
  }

  function spineWidth(title){
    const len = (title || '').length;
    // мягкая нелинейность: короткие книги не слишком тонкие, длинные не слишком широкие
    const w = (len > 4) ? 28 + Math.sqrt(len) * 10 : 66;
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
      grid.className = 'brandGrid coffee-grid-animate';
      grid.style.marginTop = '12px';

      DATA.coffeeBrands.forEach((br, index) => {
        const coffees = DATA.coffee.filter(c => c.brandId === br.id);
        const avgs = coffees.map(c => avgRating(c.reviews)).filter(x => x != null);
        const avg = avgs.length ? (avgs.reduce((a,x)=>a+x,0)/avgs.length) : null;

        const tile = document.createElement('div');
        tile.className = 'brandTile';
        tile.style.background = avg != null ? ratingColor(avg) : 'rgba(17,22,37,.55)';
        tile.style.borderColor = avg != null ? ratingBorder(avg) : 'rgba(232,238,252,.12)';
        tile.style.animationDelay = `${index * 0.1}s`;
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
        const coffees = DATA.coffee.filter(c => c.brandId === br.id);
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
              const coffee = DATA.coffee.find(x => x.id === id);
              if(coffee) openCoffeeDetails(coffee);
            });
          });
        }, 0);
      }

    } else {
      const grid = document.createElement('div');
      grid.className = 'coffeeGrid coffee-grid-animate';
      grid.style.marginTop = '12px';

      DATA.coffee.forEach((c, index) => {
        const br = DATA.coffeeBrands.find(b => b.id === c.brandId);
        const card = document.createElement('div');
        card.className = 'coffeeCard';
        card.style.animationDelay = `${index * 0.1}s`;
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
    const br = DATA.coffeeBrands.find(b => b.id === c.brandId);
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

    DATA.figures.forEach(f => {
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

    DATA.projects.forEach(p => {
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

    DATA.publications.forEach(x => {
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

    DATA.infographics.forEach(i => {
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
    root.appendChild(sectionHead('Plants', 'Последние фото растений. Нажмите на карточку для просмотра галереи изменений.'));

    const grid = document.createElement('div');
    grid.className = 'grid';

    DATA.plants.forEach(p => {
      const card = document.createElement('div');
      card.className = 'card';
      card.style.cursor = 'pointer';

      // Получаем последнее фото (самое новое по дате)
      const photos = p.photos || [];
      const latestPhoto = photos.length > 0 ? photos[photos.length - 1] : null;

      card.innerHTML = `
        <div class="plant-photo" style="height:140px; border-radius: var(--radius2); background: rgba(255,255,255,.03); position: relative; overflow: hidden; border: 1px solid var(--line);">
          ${latestPhoto ?
            `<img src="${latestPhoto.url}" alt="Фото растения" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
             <div style="display: none; width: 100%; height: 100%; align-items: center; justify-content: center; color: var(--muted);">Фото недоступно</div>` :
            `<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: var(--muted);">Фото пока нет</div>`
          }
          ${photos.length > 1 ? `<div style="position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,.7); color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">${photos.length} фото</div>` : ''}
        </div>
        <div class="title" style="margin-top:10px">${escapeHtml(p.commonName || `${p.genus || ''} ${p.species || ''}`.trim() || 'Plant')}</div>
        <p class="desc">${escapeHtml(p.family || '—')} / ${escapeHtml(p.genus || '—')} / ${escapeHtml(p.species || '—')}</p>
        ${latestPhoto ? `<p class="desc" style="font-size: 12px; margin-top: 4px;">Последнее фото: ${new Date(latestPhoto.date).toLocaleDateString('ru-RU')}</p>` : ''}
      `;

      card.addEventListener('click', () => {
        openPlantGallery(p);
      });

      grid.appendChild(card);
    });

    root.appendChild(grid);
    return root;
  }

  function openPlantGallery(plant) {
    const photos = plant.photos || [];

    if (photos.length === 0) {
      toast('У этого растения пока нет фотографий');
      return;
    }

    const galleryContent = `
      <div class="item">
        <div class="itemTitle">${escapeHtml(plant.commonName || `${plant.genus || ''} ${plant.species || ''}`.trim() || 'Plant')}</div>
        <div class="itemMeta">${escapeHtml(plant.family || '—')} / ${escapeHtml(plant.genus || '—')} / ${escapeHtml(plant.species || '—')}</div>
        <div class="itemMeta">Всего фотографий: ${photos.length}</div>
      </div>

      <div style="height:16px"></div>

      <div class="plant-gallery" style="position: relative;">
        <div class="gallery-container" style="display: flex; overflow-x: auto; gap: 12px; padding: 8px 0; scroll-behavior: smooth;">
          ${photos.map((photo, index) => `
            <div class="gallery-item" style="flex: 0 0 280px; position: relative;">
              <div style="width: 280px; height: 200px; border-radius: var(--radius2); overflow: hidden; border: 1px solid var(--line); position: relative;">
                <img src="${photo.url}" alt="Фото растения от ${new Date(photo.date).toLocaleDateString('ru-RU')}"
                     style="width: 100%; height: 100%; object-fit: cover;"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                <div style="display: none; width: 100%; height: 100%; align-items: center; justify-content: center; color: var(--muted); background: rgba(255,255,255,.03);">Фото недоступно</div>
              </div>
              <div style="margin-top: 8px; text-align: center;">
                <div style="font-size: 13px; color: var(--fg);">${new Date(photo.date).toLocaleDateString('ru-RU')}</div>
                ${photo.notes ? `<div style="font-size: 12px; color: var(--muted); margin-top: 2px;">${escapeHtml(photo.notes)}</div>` : ''}
              </div>
            </div>
          `).join('')}
        </div>

        ${photos.length > 1 ? `
          <div style="display: flex; justify-content: center; gap: 8px; margin-top: 12px;">
            <button class="btn" onclick="document.querySelector('.gallery-container').scrollBy({left: -300, behavior: 'smooth'})">← Назад</button>
            <button class="btn" onclick="document.querySelector('.gallery-container').scrollBy({left: 300, behavior: 'smooth'})">Вперед →</button>
          </div>
        ` : ''}
      </div>
    `;

    openModal(`Галерея: ${plant.commonName || 'Растение'}`, galleryContent);
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
      window.open(DATA.media.externalWishUrl, '_blank', 'noopener');
    });

    const list = document.createElement('div');
    list.className = 'list';
    list.style.marginTop = '12px';

    DATA.media.links.forEach(l => {
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

  // Initialize app
  async function init() {
    // Show loading state
    const main = $('#main');
    main.innerHTML = '<div class="fadeIn" style="text-align: center; padding: 2rem;">Загрузка данных...</div>';

    // Load data from API
    await loadData();

    // Initialize UI
    initNav();
    initModal();
    if(!location.hash) location.hash = '#/';
    render();
  }

  window.addEventListener('hashchange', render);

  // Start the app
  init().catch(error => {
    console.error('Failed to initialize app:', error);
    const main = $('#main');
    main.innerHTML = '<div class="fadeIn" style="text-align: center; padding: 2rem; color: #ff6b6b;">Ошибка загрузки приложения. Попробуйте обновить страницу.</div>';
  });
})();
