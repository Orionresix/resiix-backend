from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define models

class Tenant(db.Model):
    __tablename__ = 'tenants'
    __table_args__ = {'schema': 'maintenance'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    leases = db.relationship('Lease', backref='tenant', lazy=True)

class PropertyManager(db.Model):
    __tablename__ = 'property_managers'
    __table_args__ = {'schema': 'maintenance'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    properties_managed = db.relationship('Property', backref='property_manager', lazy=True)

class Artisan(db.Model):
    __tablename__ = 'artisans'
    __table_args__ = {'schema': 'maintenance'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    skills = db.Column(db.String(255))
    tasks = db.relationship('Task', backref='artisan', lazy=True)
    properties_served = db.relationship('Property', backref='property_manager', lazy=True)

class Property(db.Model):
    __tablename__ = 'properties'
    __table_args__ = {'schema': 'maintenance'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    num_units = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('maintenance.property_managers.id'), nullable=False)
    units = db.relationship('Unit', backref='property', lazy=True)
    country = db.Column(db.Integer, nullable=False)
    City = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    zipcode = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    latitude = db.Column(DECIMAL(precision=15, scale=10), nullable=True)
    longitude = db.Column(DECIMAL(precision=15, scale=10), nullable=True)
    elevation = db.Column(DECIMAL(precision=15, scale=10), nullable=True)


class Unit(db.Model):
    __tablename__ = 'units'
    __table_args__ = {'schema': 'maintenance'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(400), nullable=True)
    property_id = db.Column(db.Integer, db.ForeignKey('maintenance.properties.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('maintenance.tenants.id'))
    lease = db.relationship('Lease', uselist=False, backref='unit', lazy=True)


class Lease(db.Model):
    __tablename__ = 'leases'
    __table_args__ = {'schema': 'maintenance'}

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    rent = db.Column(db.Float, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('maintenance.units.id'), nullable=False)


class Issue(db.Model):
    __tablename__ = 'issues'
    __table_args__ = {'schema': 'maintenance'}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    reported_by = db.Column(db.String(100), nullable=False)
    reported_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    assigned_to = db.Column(db.Integer, db.ForeignKey('maintenance.artisans.id'))
    assigned_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
