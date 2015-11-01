Title: APBS and PDB2PQR
Date: 2004-01-15 09:01
Modified: 2017-02-28 14:01
Category: Research
Tags: electrostatics, solvation, software, titration, mathematics, current_research
Authors: Nathan Baker
Summary: APBS and PDB2PQR are software packages designed to assist in the understanding of biomolecular solvation and electrostatics.

[APBS and PDB2PQR](http://www.poissonboltzmann.org/) are software packages designed to assist in the understanding of biomolecular solvation and electrostatics.

APBS is a software package for modeling biomolecular solvation through solution of the Poisson-Boltzmann equation (PBE), one of the most popular continuum models for describing electrostatic interactions between molecular solutes in salty, aqueous media. Continuum electrostatics plays an important role in several areas of biomolecular simulation, including: simulation of diffusional processes to determine ligand-protein and protein-protein binding kinetics, implicit solvent molecular dynamics of biomolecules, solvation and binding energy calculations to determine ligand-protein and protein-protein equilibrium binding constants and aid in rational drug design, and biomolecular titration studies. APBS was designed to efficiently evaluate electrostatic properties for such simulations for a wide range of length scales to enable the investigation of molecules with tens to millions of atoms. We also provide implicit solvent models of nonpolar solvation which accurately account for both repulsive and attractive solute-solvent interactions.

PDB2PQR is a Python software package that automates many of the common tasks of preparing structures for continuum electrostatics calculations, providing a platform-independent utility for converting protein files in PDB format to PQR format. These tasks include: adding a limited number of missing heavy atoms to biomolecular structures, determining side-chain pKas, placing missing hydrogens, optimizing the protein for favorable hydrogen bonding, assigning charge and radius parameters from a variety of force fields.

This work was supported by NIH grants R01 GM069702 and P41 GM103426, NPACI, and XSEDE/TeraGrid.
