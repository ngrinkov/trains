CREATE TABLE employees1 (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(100),
    manager_id INT REFERENCES employees1(id)
);

INSERT INTO employees1 (name, position, manager_id) VALUES
('Иванов', 'Генеральный директор', NULL),
('Петрова', 'Финансовый директор', 1),
('Сидоров', 'Технический директор', 1),
('Кузнецова', 'Менеджер по продажам', 2),
('Смирнов', 'Ведущий разработчик', 3),
('Васильев', 'Младший разработчик', 5),
('Федорова', 'Бухгалтер', 2),
('Николаев', 'Тестировщик', 5);

-- Задача: Найти всех подчиненных (прямых и косвенных) для заданного руководителя

WITH RECURSIVE employee_hierarchy AS (
    -- Базовый случай: начальный руководитель
    SELECT id, name, position, manager_id, 1 AS level
    FROM employees1
    WHERE id = 1 -- Начинаем с генерального директора
    
    UNION ALL
    
    -- Рекурсивный случай: все подчиненные
    SELECT e.id, e.name, e.position, e.manager_id, eh.level + 1
    FROM employees1 e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT id, name, position, level
FROM employee_hierarchy
ORDER BY level, name;

------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE user_sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

INSERT INTO user_sessions (user_id, start_time, end_time) VALUES
(1, '2023-01-01 10:00:00', '2023-01-01 10:30:00'),
(1, '2023-01-01 10:25:00', '2023-01-01 10:45:00'),
(2, '2023-01-01 11:00:00', '2023-01-01 11:30:00'),
(1, '2023-01-01 14:00:00', '2023-01-01 15:00:00'),
(3, '2023-01-02 09:00:00', '2023-01-02 09:30:00'),
(2, '2023-01-02 10:00:00', '2023-01-02 10:15:00'),
(3, '2023-01-02 10:10:00', '2023-01-02 10:40:00');

-- Задача: Найти пересекающиеся сессии для каждого пользователя

SELECT 
    a.user_id,
    a.session_id AS session1,
    b.session_id AS session2,
    a.start_time AS start1,
    a.end_time AS end1,
    b.start_time AS start2,
    b.end_time AS end2
FROM user_sessions a
JOIN user_sessions b ON a.user_id = b.user_id 
    AND a.session_id < b.session_id
    AND a.start_time < b.end_time 
    AND a.end_time > b.start_time
ORDER BY a.user_id, a.start_time;

------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE user_events (
    event_id SERIAL PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(50),
    event_time TIMESTAMP
);

INSERT INTO user_events (user_id, event_type, event_time) VALUES
(1, 'login', '2023-01-01 10:00:00'),
(1, 'search', '2023-01-01 10:05:00'),
(1, 'view_product', '2023-01-01 10:10:00'),
(1, 'add_to_cart', '2023-01-01 10:15:00'),
(2, 'login', '2023-01-01 11:00:00'),
(2, 'search', '2023-01-01 11:05:00'),
(1, 'purchase', '2023-01-01 10:20:00'),
(3, 'login', '2023-01-02 09:00:00'),
(3, 'view_product', '2023-01-02 09:05:00'),
(3, 'search', '2023-01-02 09:10:00');

-- Задача: Найти пользователей, которые выполнили последовательность 
-- login -> search -> view_product -> add_to_cart -> purchase в течение 30 минут

WITH event_sequences AS (
    SELECT 
        user_id,
        event_type,
        event_time,
        LEAD(event_type, 1) OVER (PARTITION BY user_id ORDER BY event_time) AS next_event1,
        LEAD(event_type, 2) OVER (PARTITION BY user_id ORDER BY event_time) AS next_event2,
        LEAD(event_type, 3) OVER (PARTITION BY user_id ORDER BY event_time) AS next_event3,
        LEAD(event_type, 4) OVER (PARTITION BY user_id ORDER BY event_time) AS next_event4,
        LEAD(event_time, 4) OVER (PARTITION BY user_id ORDER BY event_time) AS next_time4
    FROM user_events
)
SELECT DISTINCT user_id
FROM event_sequences
WHERE event_type = 'login'
    AND next_event1 = 'search'
    AND next_event2 = 'view_product'
    AND next_event3 = 'add_to_cart'
    AND next_event4 = 'purchase'
    AND (next_time4 - event_time) <= INTERVAL '30 minutes';

------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_date DATE,
    amount DECIMAL(10,2)
);

INSERT INTO transactions (transaction_date, amount) VALUES
('2023-01-01', 1000.00),
('2023-01-02', 1500.00),
('2023-01-03', 1200.00),
('2023-01-05', 1800.00),
('2023-01-06', 900.00),
('2023-01-08', 2000.00),
('2023-01-09', 1100.00),
('2023-01-10', 1300.00),
('2023-01-12', 1700.00);

-- Задача: Найти все пропущенные даты в последовательности транзакций
-- (даты, когда не было ни одной транзакции)

WITH date_range AS (
    SELECT generate_series(
        MIN(transaction_date), 
        MAX(transaction_date), 
        INTERVAL '1 day'
    )::DATE AS date
    FROM transactions
)
SELECT date AS missing_date
FROM date_range
WHERE date NOT IN (SELECT transaction_date FROM transactions)
ORDER BY date;

------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INT,
    sale_date DATE,
    quantity INT,
    price DECIMAL(10,2)
);

INSERT INTO sales (product_id, sale_date, quantity, price) VALUES
(1, '2023-01-01', 5, 100.00),
(2, '2023-01-01', 3, 200.00),
(1, '2023-01-02', 2, 100.00),
(3, '2023-01-02', 1, 300.00),
(2, '2023-01-03', 4, 200.00),
(1, '2023-01-03', 1, 100.00),
(3, '2023-01-04', 2, 300.00),
(1, '2023-01-05', 3, 100.00),
(2, '2023-01-05', 2, 200.00),
(3, '2023-01-06', 1, 300.00);

-- Задача: Для каждого товара найти дни, когда его продажи были выше средних продаж этого товара

WITH product_avg_sales AS (
    SELECT 
        product_id,
        AVG(quantity) AS avg_quantity
    FROM sales
    GROUP BY product_id
)
SELECT 
    s.product_id,
    s.sale_date,
    s.quantity,
    a.avg_quantity
FROM sales s
JOIN product_avg_sales a ON s.product_id = a.product_id
WHERE s.quantity > a.avg_quantity
ORDER BY s.product_id, s.sale_date;

------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    stock_symbol VARCHAR(10),
    price_date DATE,
    closing_price DECIMAL(10,2)
);

INSERT INTO stock_prices (stock_symbol, price_date, closing_price) VALUES
('AAPL', '2023-01-01', 150.00),
('AAPL', '2023-01-02', 152.50),
('AAPL', '2023-01-03', 151.75),
('AAPL', '2023-01-04', 153.25),
('AAPL', '2023-01-05', 154.50),
('AAPL', '2023-01-06', 155.75),
('AAPL', '2023-01-07', 156.25),
('AAPL', '2023-01-08', 157.00),
('AAPL', '2023-01-09', 155.50),
('AAPL', '2023-01-10', 156.75);

-- Задача: Рассчитать 3-дневное скользящее среднее цены акции

SELECT 
    stock_symbol,
    price_date,
    closing_price,
    AVG(closing_price) OVER (
        ORDER BY price_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3day
FROM stock_prices
WHERE stock_symbol = 'AAPL'
ORDER BY price_date;