from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Boolean, func
from sqlalchemy.orm import relationship, sessionmaker
from __init__ import engine, Base


# Определение моделей Category и Product
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


# Создание таблиц
Base.metadata.create_all(engine)

# Настройка сессии
Session = sessionmaker(bind=engine)
session = Session()

# Добавление категорий и продуктов
categories = [
Category(name="Электроника", description="Гаджеты и устройства."),
Category(name="Книги", description="Печатные книги и электронные книги."),
Category(name="Одежда", description="Одежда для мужчин и женщин.")
]

session.add_all(categories)
session.commit()

# Поиск категорий
electronics_category = session.query(Category).filter_by(name="Электроника").first()
books_category = session.query(Category).filter_by(name="Книги").first()
clothing_category = session.query(Category).filter_by(name="Одежда").first()

# Добавление продуктов
products = [
Product(name="Смартфон", price=299.99, in_stock=True, category=electronics_category),
Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics_category),
Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books_category),
Product(name="Джинсы", price=40.50, in_stock=True, category=clothing_category),
Product(name="Футболка", price=20.00, in_stock=True, category=clothing_category)
]

session.add_all(products)
session.commit()

# Вывод всех категорий и продуктов в них
categories = session.query(Category).all()

for category in categories:
    print(f"Категория: {category.name} - {category.description}")
for product in category.products:
    print(f" Продукт: {product.name}, Цена: {product.price}")

# Обновление цены продукта "Смартфон"
smartphone = session.query(Product).filter_by(name="Смартфон").first()

# Проверка, был ли найден продукт
if smartphone:
    print(f"Найден продукт: {smartphone.name} - текущая цена: {smartphone.price}")

# Обновляем цену на 349.99
smartphone.price = 349.99

# Пробуем зафиксировать изменения
try:
    session.commit()
    print(f"Цена обновлена: {smartphone.name} - новая цена: {smartphone.price}")
except Exception as e:
    session.rollback()
    print(f"Ошибка при сохранении изменений: {e}")
else:
    print("Продукт с названием 'Смартфон' не найден")

# Агрегация: Подсчет общего количества продуктов в каждой категории
category_counts = session.query(
Category.name,
func.count(Product.id).label('product_count')
).outerjoin(Product).group_by(Category.id).all()

for category_name, product_count in category_counts:
    print(f"Категория: {category_name}, Количество продуктов: {product_count}")

# Группировка с фильтрацией: Категории с более чем одним продуктом
categories_with_multiple_products = session.query(
Category.name
).outerjoin(Product).group_by(Category.id).having(func.count(Product.id) > 1).all()

print("Категории с более чем одним продуктом:")
for category_name, in categories_with_multiple_products:
    print(f" {category_name}")

# Закрытие сессии
session.close()