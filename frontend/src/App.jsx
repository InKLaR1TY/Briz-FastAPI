import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import TestPage from './pages/test.jsx';

const COLORS = {
  darkBlue: '#155a8a',
  lightBlue: '#2196f3',
  skyBlue: '#b3d8f7',
  white: '#fff',
};

const NAV_ITEMS = [
  { id: 'record', label: 'Записаться', target: 'top' },
  { id: 'services', label: 'Услуги', target: 'services' },
  { id: 'masters', label: 'Мастера', target: 'masters' },
  { id: 'location', label: 'Адрес', target: 'location' },
  { id: 'contacts', label: 'Контакты', target: 'contacts' },
];

const SERVICES = [
  'Парикмахерские услуги',
  'Маникюр и педикюр',
  'Косметология',
  'Массаж',
  'Брови и ресницы',
  'Эпиляция',
  'SPA-процедуры',
  'Макияж',
  'Наращивание волос',
  'Ламинирование ресниц',
  'Пирсинг',
  'Тату и перманентный макияж',
  'Солярий',
];

const MASTERS = [
  { profile: 'Парикмахер', name: 'Иванова Анна', exp: 'Стаж: 5 лет' },
  { profile: 'Косметолог', name: 'Петрова Мария', exp: 'Стаж: 3 года' },
  { profile: 'Мастер маникюра', name: 'Сидорова Ольга', exp: 'Стаж: 4 года' },
  { profile: 'Массажист', name: 'Козлова Елена', exp: 'Стаж: 7 лет' },
  { profile: 'Визажист', name: 'Морозова Алина', exp: 'Стаж: 6 лет' },
  { profile: 'Мастер эпиляции', name: 'Волкова Ирина', exp: 'Стаж: 4 года' },
  { profile: 'SPA-мастер', name: 'Соколова Наталья', exp: 'Стаж: 8 лет' },
  { profile: 'Мастер наращивания', name: 'Лебедева Юлия', exp: 'Стаж: 5 лет' },
  { profile: 'Мастер бровей', name: 'Новикова Татьяна', exp: 'Стаж: 3 года' },
  { profile: 'Мастер пирсинга', name: 'Кузнецова Анжела', exp: 'Стаж: 4 года' },
];

export default function App() {
  const [activeNav, setActiveNav] = useState('record');
  const sectionRefs = {
    services: useRef(null),
    masters: useRef(null),
    location: useRef(null),
    contacts: useRef(null),
  };

  // Scrollspy: определяем активную секцию по верхней границе (или центру экрана)
  useEffect(() => {
    const handleScroll = () => {
      const navHeight = document.querySelector('.briz-nav')?.offsetHeight || 0;
      const scrollPosition = window.scrollY + navHeight + 10;
      let current = 'record';
      for (const item of NAV_ITEMS) {
        if (item.target === 'top') {
          if (window.scrollY < (sectionRefs.services.current?.offsetTop || 0) - navHeight - 20) {
            current = 'record';
          }
          continue;
        }
        const ref = sectionRefs[item.target];
        if (ref && ref.current) {
          const offsetTop = ref.current.offsetTop;
          if (scrollPosition >= offsetTop) {
            current = item.id;
          }
        }
      }
      setActiveNav(current);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Плавный скролл с учётом высоты навигации
  const handleNavClick = (target) => {
    if (target === 'top') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    const ref = sectionRefs[target];
    if (ref && ref.current) {
      const navHeight = document.querySelector('.briz-nav')?.offsetHeight || 0;
      const top = ref.current.getBoundingClientRect().top + window.scrollY - navHeight;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  };

  // Функции для карусели мастеров
  const nextMasters = () => {
    const container = document.querySelector('.masters-list');
    if (container) {
      const cardWidth = 220 + 32; // ширина карточки + gap
      container.scrollBy({ left: cardWidth, behavior: 'smooth' });
    }
  };

  const prevMasters = () => {
    const container = document.querySelector('.masters-list');
    if (container) {
      const cardWidth = 220 + 32; // ширина карточки + gap
      container.scrollBy({ left: -cardWidth, behavior: 'smooth' });
    }
  };

  return (
    <Routes>
      <Route path="/" element={
        <div className="briz-app">
          {/* Шапка */}
          <header className="briz-header">
            <div className="logo-placeholder">Briz</div>
            <button className="header-btn">Для мастеров</button>
          </header>

          {/* Слайдшоу */}
          <section className="briz-slideshow" id="top">
            <div className="slideshow-overlay">
              <h1 className="slideshow-title">Салон красоты Briz</h1>
              <button className="slideshow-btn">Записаться</button>
            </div>
          </section>

          {/* Навигация */}
          <nav className="briz-nav">
            {NAV_ITEMS.map(item => (
              <button
                key={item.id}
                className={`nav-btn${activeNav === item.id ? ' active' : ''}`}
                onClick={() => handleNavClick(item.target)}
              >
                {item.label}
              </button>
            ))}
          </nav>

          {/* Секции */}
          <main className="briz-main">
            {/* Услуги */}
            <section className="services-section" id="services" ref={sectionRefs.services}>
              <h2>Услуги</h2>
              <div className="services-list">
                {SERVICES.map((service, idx) => (
                  <button className="service-btn" key={idx}>{service}</button>
                ))}
              </div>
            </section>

            {/* Мастера */}
            <section className="masters-section" id="masters" ref={sectionRefs.masters}>
              <h2>Наши мастера</h2>
              <div className="masters-carousel">
                <button className="carousel-btn prev-btn" onClick={prevMasters}>
                  ‹
                </button>
                <div className="masters-list">
                  {MASTERS.map((m, idx) => (
                    <button
                      className="master-card"
                      key={idx}
                      onClick={() => alert(`Переход на страницу мастера: ${m.name}`)}
                      type="button"
                    >
                      <div className="master-profile">{m.profile}</div>
                      <div className="master-photo" />
                      <div className="master-name">{m.name}</div>
                      <div className="master-exp">{m.exp}</div>
                    </button>
                  ))}
                </div>
                <button className="carousel-btn next-btn" onClick={nextMasters}>
                  ›
                </button>
              </div>
            </section>

            {/* Адрес и карта */}
            <section className="location-section" id="location" ref={sectionRefs.location}>
              <h2>Наш адрес</h2>
              <div className="location-address">г. Москва, ул. Примерная, д. 1</div>
              <div className="location-map-placeholder">[Здесь будет карта Яндекс]</div>
            </section>

            {/* Контакты */}
            <section className="contacts-section" id="contacts" ref={sectionRefs.contacts}>
              <h2>Контактная информация</h2>
              <div className="contacts-list">
                {[
                  { type: 'Телефон', value: '+7 (999) 123-45-67' },
                  { type: 'WhatsApp', value: '@briz_salon' },
                  { type: 'Instagram', value: '@briz_beauty' },
                ].map((contact, idx) => (
                  <button
                    className="contact-item"
                    key={idx}
                    type="button"
                    onClick={() => alert(`${contact.type}: ${contact.value}`)}
                  >
                    <div className="contact-icon">[icon]</div>
                    <div className="contact-type">{contact.type}</div>
                    <div className="contact-value">{contact.value}</div>
                  </button>
                ))}
              </div>
            </section>
          </main>

          {/* Футер */}
          <footer className="briz-footer">
            <div>© {new Date().getFullYear()} Briz — салон красоты. Все права защищены.</div>
            <div>Сайт разработан для демонстрации макета.</div>
          </footer>
        </div>
      } />
      <Route path="/test" element={<TestPage />} />
    </Routes>
  );
}

