from setuptools import setup, find_packages

setup(
    name="case-mappings",
    packages=find_packages(include=['case_mapping', 'case_mapping.case', 'case_mapping.uco']),
    version="0.1.0",
    description="Case Mappings Utility",
    author="Cyber Domain Ontology Maintainers <operations@cyberdomainontology.org>",
    license="Apache-2.0",
    install_requires=[
        "pytz==2023.3.post1"
    ]
)
