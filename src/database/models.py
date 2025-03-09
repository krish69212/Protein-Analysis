"""
Database models for the Protein Analysis project.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Protein(Base):
    """
    Model representing a protein structure from PDB.
    """
    __tablename__ = 'proteins'

    id = Column(Integer, primary_key=True)
    pdb_id = Column(String(10), unique=True, nullable=False, index=True)
    title = Column(String(255))
    classification = Column(String(100))
    experimental_method = Column(String(100))
    resolution = Column(Float)
    deposition_date = Column(DateTime)
    release_date = Column(DateTime)
    revision_date = Column(DateTime)
    
    # Relationships
    chains = relationship("Chain", back_populates="protein", cascade="all, delete-orphan")
    authors = relationship("Author", back_populates="protein", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Protein(pdb_id='{self.pdb_id}', title='{self.title}')>"


class Chain(Base):
    """
    Model representing a protein chain.
    """
    __tablename__ = 'chains'

    id = Column(Integer, primary_key=True)
    protein_id = Column(Integer, ForeignKey('proteins.id'), nullable=False)
    chain_id = Column(String(10))
    entity_id = Column(String(10))
    sequence = Column(Text)
    length = Column(Integer)
    type = Column(String(50))  # protein, DNA, RNA, etc.
    
    # Relationships
    protein = relationship("Protein", back_populates="chains")
    residues = relationship("Residue", back_populates="chain", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Chain(chain_id='{self.chain_id}', length={self.length})>"


class Residue(Base):
    """
    Model representing an amino acid residue in a protein chain.
    """
    __tablename__ = 'residues'

    id = Column(Integer, primary_key=True)
    chain_id = Column(Integer, ForeignKey('chains.id'), nullable=False)
    residue_number = Column(Integer)
    residue_name = Column(String(10))
    secondary_structure = Column(String(20))  # alpha-helix, beta-sheet, etc.
    
    # Relationships
    chain = relationship("Chain", back_populates="residues")
    
    def __repr__(self):
        return f"<Residue(residue_number={self.residue_number}, residue_name='{self.residue_name}')>"


class Author(Base):
    """
    Model representing an author of a protein structure.
    """
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    protein_id = Column(Integer, ForeignKey('proteins.id'), nullable=False)
    name = Column(String(100))
    institution = Column(String(255))
    
    # Relationships
    protein = relationship("Protein", back_populates="authors")
    
    def __repr__(self):
        return f"<Author(name='{self.name}')>"


def create_tables(engine):
    """
    Create all database tables.
    """
    Base.metadata.create_all(engine) 