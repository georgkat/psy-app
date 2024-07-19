from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, JSON, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)
role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

user_permissions = Table(
    'user_permissions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

user_groups = Table(
    'user_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    permissions = relationship('Permission', secondary=user_permissions, back_populates='users')
    groups = relationship('Group', secondary=user_groups, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    users = relationship('User', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    details = Column(JSON, nullable=False)
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')
    users = relationship('User', secondary=user_permissions, back_populates='permissions')

class Group(Base):
    __tablename__ = 'groups's
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    users = relationship('User', secondary=user_groups, back_populates='groups')

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    change_type = Column(String(50))
    change_details = Column(JSON)
    changed_at = Column(TIMESTAMP, server_default=func.now())
    user = relationship('User')

# Database setup
DATABASE_URL = "mariadb+mariadbconnector://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)