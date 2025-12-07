# src/database/init.py
from sqlalchemy import text
from ..config.database import engine, Base

# Import all models to register them
from ..models import (
    User, Address, Product, Category, ProductVariant,
    Order, OrderItem, Payment, Wishlist, Review,
    ProductView, Session, Image,
)

# Import enum types from models
from ..models.product import product_status_enum
from ..models.order import order_status_enum
from ..models.payment import payment_method_enum, payment_status_enum
from ..models.user import auth_provider_enum
from ..models.image import image_type_enum

def create_enum_types():
    """Create PostgreSQL ENUM types"""
    with engine.begin() as conn:
        product_status_enum.create(conn, checkfirst=True)
        order_status_enum.create(conn, checkfirst=True)
        payment_method_enum.create(conn, checkfirst=True)
        payment_status_enum.create(conn, checkfirst=True)
        auth_provider_enum.create(conn, checkfirst=True)
        image_type_enum.create(conn, checkfirst=True)
        print("✅ Enum types created")

def create_tables():
    print("Tables in metadata:", Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

def create_indexes():
    """Create additional indexes - ensure tables exist first"""
    with engine.begin() as conn:
        # First, commit any pending transactions
        conn.execute(text("COMMIT"))

        # Check if orders table exists before creating indexes
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'orders'
            );
        """))

        if result.scalar():
            # Table exists, create indexes
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_orders_user ON orders (user_id);
                CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status);
            """))
            print("✅ Database indexes created")
        else:
            print("⚠️  Orders table doesn't exist yet, skipping indexes")

def init_database():
    """Initialize the database"""
    print("🔄 Initializing database...")
    create_enum_types()
    create_tables()
    create_indexes()
    print("✅ Database initialization complete!")