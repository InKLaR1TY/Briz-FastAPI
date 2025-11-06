import React from "react";
import './test.css';

export default function TestPage() {
  return (
    <div>
      <article className="card">
        <h3 className="profession">Парикмахер</h3>
        <img src="https://as2.ftcdn.net/v2/jpg/04/09/99/43/1000_F_409994330_ELd9lKuGdzpfZtiXeE8KPHmYyqzj7BBC.jpg" alt="Имя мастера" className="photo" />
        <p className="name">Иван Иванов</p>
        <p className="experience">Стаж работы: 5 лет</p>
      </article>
    </div>
  );
}