from setuptools import setup, find_packages

with open('README.md') as fr:
    long_description = fr.read()

setup(
    name='emlclient',
    version='1.0.0',
    author='Linsuiyuan',
    author_email='linsuiyuan@icloud.com',
    description='一个简单易用的邮件客户端，支持发送和接收邮件，支持 QQ 邮箱、163邮箱等邮箱 ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/linsuiyuan/email-client',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[],
)
