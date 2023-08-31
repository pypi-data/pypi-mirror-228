ProvablyFairRandomNumberGenerator Library
=========================================



.. image:: https://pyup.io/repos/github/sarthakvijayvergiya/hbc_random_number/shield.svg
     :target: https://pyup.io/repos/github/sarthakvijayvergiya/hbc_random_number/
     :alt: Updates

The **ProvablyFairRandomNumberGenerator** is a Python library that provides a provably fair mechanism for generating random numbers. This library uses cryptographic techniques to ensure transparency and fairness in generating random numbers, making it suitable for applications where unbiased randomness is essential.

Features
--------

- Generates random numbers within a specified range using provably fair methods.
- Uses cryptographic techniques to ensure fairness and security.

Installation
------------

.. code-block:: bash

   pip install provablyfairrandomnumbergenerator

Usage
-----

.. code-block:: python

   from provablyfairrandomnumbergenerator import ProvablyFairRandomNumberGenerator

   # Initialize the generator with a secret key
   secret_key = "mySecretKey"
   generator = ProvablyFairRandomNumberGenerator(secret_key)

   # Generate a random number within a range
   user_seed = "userSeed123"
   min_value = 1
   max_value = 100
   random_number = generator.generate_random_number(user_seed, min_value, max_value)

   print(f"Generated Random Number: {random_number}")

Dependencies
------------

- Python 3.x


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
