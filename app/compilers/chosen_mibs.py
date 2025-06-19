import argparse
import os
import logging
from pysmi import debug
from pysmi.reader import FileReader
from pysmi.writer import PyFileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import PySnmpCodeGen
from pysmi.compiler import MibCompiler
from ..enums import MIBS, COMPILED_MIBS

def setup_logging(debug_mode):
  """Sets up logging for pysmi."""
  log_file = 'pysmi_debug.log'
  logger = logging.getLogger('pysmi')
  logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
  
  # Avoid adding handlers multiple times
  if not logger.handlers:
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

  if debug_mode:
    debug_instance = debug.Debug('all')
    debug.set_logger(debug_instance)


def main(mibs_to_compile, debug_mode):
  """
  Compiles a specific list of MIBs.

  :param mibs_to_compile: A list of MIB name strings to compile.
  :param debug_mode: Boolean to enable or disable debug logging.
  """
  setup_logging(debug_mode)

  source_mib_dir = MIBS
  output_mib_dir = COMPILED_MIBS
  os.makedirs(output_mib_dir, exist_ok=True)

  # Initialize MIB compiler
  mib_compiler = MibCompiler(
    SmiStarParser(),
    PySnmpCodeGen(),
    PyFileWriter(output_mib_dir)
  )

  # Add the source directory for MIBs
  mib_compiler.add_sources(FileReader(source_mib_dir))

  print(f"Attempting to compile {len(mibs_to_compile)} specified MIB(s).")
  print(f"MIBs to compile: {', '.join(mibs_to_compile)}")

  # Standard dependencies that are often required. Compiling them first can prevent issues.
  dependencies = ['SNMPv2-SMI', 'SNMPv2-TC', 'SNMPv2-CONF', 'SNMPv2-MIB', 'IF-MIB', 'BRIDGE-MIB', 'RFC-1212', 'NMS-SMI']

  print("\nFirst, attempting to compile common dependencies...")
  # This step is optional but recommended. We'll attempt to compile dependencies that are also in our target list.
  for dep in dependencies:
    if dep in mibs_to_compile:
      try:
        result = mib_compiler.compile(dep, noDeps=False, rebuild=True)
        print(f"Compiled dependency '{dep}': {result.get(dep, 'unknown result')}")
      except Exception as e:
        print(f"Error compiling dependency '{dep}': {e}")
        # We will still attempt to compile it in the next step, in case the error was transient.

  print("\nNow compiling the requested MIBs...")
  for mib in mibs_to_compile:
    try:
      # The 'rebuild' flag ensures that the MIB is recompiled even if a .py file already exists.
      # 'noDeps=False' allows the compiler to automatically fetch and compile any required dependencies.
      result = mib_compiler.compile(mib, noDeps=False, rebuild=True)
      status = result.get(mib, "unknown status")
      print(f"Compilation result for '{mib}': {status}")
    except Exception as e:
      print(f"An error occurred while compiling '{mib}': {e}")

  print(f"\nAll requested compilations completed. Please check the '{output_mib_dir}' directory for the results.")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Compile a specific list of MIB files using pysmi.",
    formatter_class=argparse.RawTextHelpFormatter
  )
  parser.add_argument(
    'mibs',
    nargs='+',  # This makes 'mibs' a required argument that accepts one or more values.
    help='A list of MIB names to compile (e.g., IF-MIB SNMPv2-TC).'
  )
  parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help='Enable debug mode, which creates a detailed pysmi_debug.log file.'
  )

  args = parser.parse_args()
  
  # The list of MIBs to compile is now taken from the command line.
  mibs_to_run = args.mibs
  
  main(mibs_to_run, args.debug)