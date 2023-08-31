import setuptools

with open("./README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="HybridUI", 
    version="0.0.1",
    author="Ari Bermeki",
    author_email="ari.bermeki.de@gmail.com",
    description="Create an efficient and enjoyable work experience with pure Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AriBermeki/foundation",
    packages=setuptools.find_packages(),
    package_data={
        "hybrid": ["charts/*", "core/*", "elements/*", "eventarguments/*", "libary_images/*", "static/**","templates/*"]  # Include all files in the other_folder
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fastapi',
        'fastapi_socketio',
        'python-socketio',
        'uvicorn[standard]',
        'psutil', 
        'python-dateutil', 
        'jinja2',
        'python-multipart',
    ],
    include_package_data=False,
    python_requires='>=3.9',
)

