// Тестовые данные. Здесь нет API — всё локально.
// В дальнейшем эти структуры лягут на БД + телеграм-бота.

window.DATA = {
  about: {
    title: "Обо мне",
    bio: "Личный сайт с моими интересами: винил, книги, кофе, фигурки, проекты, исследования, растения и контакты. Всё, что здесь — уже есть у меня.",
  },

  vinylGenres: ["Electronic", "Rock", "Jazz", "Ambient", "Hip-Hop"],
  vinyl: [
    { id: "v1", artist: "Daft Punk", title: "Random Access Memories", genres: ["Electronic"], year: 2013 },
    { id: "v2", artist: "Radiohead", title: "In Rainbows", genres: ["Rock", "Ambient"], year: 2007 },
    { id: "v3", artist: "Nirvana", title: "Nevermind", genres: ["Rock"], year: 1991 },
    { id: "v4", artist: "Nujabes", title: "Modal Soul", genres: ["Hip-Hop", "Jazz"], year: 2005 },
    { id: "v5", artist: "Miles Davis", title: "Kind of Blue", genres: ["Jazz"], year: 1959 },
    { id: "v6", artist: "Aphex Twin", title: "Selected Ambient Works 85–92", genres: ["Ambient", "Electronic"], year: 1992 },
  ],

  bookGenres: ["Sci‑Fi", "Non‑fiction", "Design", "Computing"],
  books: [
    { id: "b1", genre: "Sci‑Fi", title: "Dune", author: "Frank Herbert", language: "EN", format: "Hardcover" },
    { id: "b2", genre: "Sci‑Fi", title: "Neuromancer", author: "William Gibson", language: "EN", format: "Paperback" },
    { id: "b3", genre: "Non‑fiction", title: "Thinking, Fast and Slow", author: "Daniel Kahneman", language: "EN", format: "Paperback" },
    { id: "b4", genre: "Design", title: "The Design of Everyday Things", author: "Don Norman", language: "EN", format: "Hardcover" },
    { id: "b5", genre: "Computing", title: "Designing Data‑Intensive Applications", author: "Martin Kleppmann", language: "EN", format: "Hardcover" },
  ],

  coffeeBrands: [
    { id: "cb1", name: "April Coffee" },
    { id: "cb2", name: "Tim Wendelboe" },
    { id: "cb3", name: "Friedhats" },
  ],
  coffee: [
    {
      id: "c1",
      brandId: "cb1",
      name: "Ethiopia Guji",
      region: "Guji",
      processing: "Washed",
      reviews: [
        { method: "Filter", rating: 9.0, notes: "bergamot, jasmine, clean finish" },
        { method: "Espresso", rating: 8.4, notes: "citrus, floral, slightly sharp" },
        { method: "Cappuccino", rating: 8.6, notes: "sweet, tea-like" },
      ]
    },
    {
      id: "c2",
      brandId: "cb2",
      name: "Colombia Huila",
      region: "Huila",
      processing: "Natural",
      reviews: [
        { method: "Filter", rating: 7.6, notes: "cherry, cacao, heavier body" },
        { method: "Espresso", rating: 7.9, notes: "chocolate, red fruits" },
      ]
    },
    {
      id: "c3",
      brandId: "cb3",
      name: "Kenya Nyeri",
      region: "Nyeri",
      processing: "Washed",
      reviews: [
        { method: "Filter", rating: 8.8, notes: "blackcurrant, bright acidity" },
        { method: "Espresso", rating: 8.1, notes: "berry, syrupy" },
      ]
    }
  ],

  figures: [
    { id: "f1", brand: "Good Smile", name: "Nendoroid Example 01" },
    { id: "f2", brand: "Medicom", name: "BE@RBRICK Example 100%" },
    { id: "f3", brand: "Bandai", name: "Figure Example 03" },
    { id: "f4", brand: "Kotobukiya", name: "Figure Example 04" },
  ],

  projects: [
    { id: "p1", name: "awesome-tooling", desc: "Небольшие утилиты для автоматизации личных задач.", tags: ["python", "cli"] },
    { id: "p2", name: "data-viz-notes", desc: "Коллекция заметок и примеров визуализации данных.", tags: ["viz", "notebooks"] },
    { id: "p3", name: "infra-sandbox", desc: "Песочница под инфраструктуру в облаке (прототипы).", tags: ["cloud", "iac"] },
  ],

  publications: [
    { id: "pub1", title: "Research Paper Example 01", venue: "Workshop", year: 2024, url: "https://example.com" },
    { id: "pub2", title: "Research Paper Example 02", venue: "Conference", year: 2023, url: "https://example.com" },
  ],
  infographics: [
    { id: "i1", title: "Infographic Example 01", topic: "Networks" },
    { id: "i2", title: "Infographic Example 02", topic: "ML" },
    { id: "i3", title: "Infographic Example 03", topic: "Product" },
  ],

  plants: [
    { id: "pl1", family: "Araceae", genus: "Monstera", species: "deliciosa", commonName: "Monstera" },
    { id: "pl2", family: "Cactaceae", genus: "Mammillaria", species: "elongata", commonName: "Mammillaria" },
    { id: "pl3", family: "Moraceae", genus: "Ficus", species: "elastica", commonName: "Rubber plant" },
  ],

  media: {
    externalWishUrl: "https://example.com/my-wishlist",
    links: [
      { type: "Telegram", label: "@mytelegram", value: "https://t.me/mytelegram" },
      { type: "GitHub", label: "github.com/myuser", value: "https://github.com/myuser" },
      { type: "Email", label: "me@example.com", value: "me@example.com" },
    ]
  }
};
