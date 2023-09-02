import os
import sys
import sqlite3
import unittest
import filecmp
import shutil
import tempfile
import io
import string
import random

from kocher_tools.misc import confirmExecutable
from tests.functions import randomGenerator

# Run tests for miscellaneous functions
class test_misc (unittest.TestCase):

	@classmethod
	def setUpClass (cls):

		# Create a temporary directory
		cls.test_dir = tempfile.mkdtemp()

		# Assign the expected output directory
		cls.expected_dir = 'test_files'

	@classmethod
	def tearDownClass (cls):

		# Remove the test directory after the tests
		shutil.rmtree(cls.test_dir)

	# Check confirmExecutable from misc.py 
	def test_01_confirmExecutable (self):

		# Create list of executables
		executable_list = ['vsearch', 'fastq-multx', 'blastn']

		# Loop the executables
		for executable_str in executable_list:

			# Check that the non-standard executables were installed
			self.assertIsNotNone(confirmExecutable(executable_str), '%s not found. Please install' % executable_str)

		# Check that the function fails with a fake executable
		self.assertIsNone(confirmExecutable('retrieve_samples.py' + randomGenerator()))
	

if __name__ == "__main__":
	unittest.main(verbosity = 2)