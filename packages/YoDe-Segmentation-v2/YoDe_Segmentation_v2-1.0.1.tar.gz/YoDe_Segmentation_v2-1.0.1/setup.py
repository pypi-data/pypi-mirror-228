import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# with open('requirements.txt', 'r') as reqs:
#     requirements = reqs.read().split()

setuptools.setup(
    name="YoDe_Segmentation_v2",
    version="1.0.1",
    author="zconechorm",
    author_email="Email:zconechorm@163.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OneChorm/YoDe-Segmentation",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'yode_seg = YODE_Segmentation.predict_molecular:run_main',
        ]
    },
    # install_requires=[
    #     'numpy',
    #     'pandas >= 1.4.0, != 1.4.4, <= 2.0.3',
    # ],
    # install_requires=requirements,
)