import sys, shlex
from utrunner import debug
from nose_utils import TeamcityNoseRunner

try:
  from nose.core import TestProgram
  from nose.plugins.base import Plugin
  from nose.config import Config
  from nose.plugins.manager import DefaultPluginManager
except:
  raise NameError("Please, install nosetests")

def process_args():
  tests = []

  opts = None
  if sys.argv[-1].startswith("-"):
    test_names = sys.argv[1:-1]
    opts = sys.argv[-1]
  else:
    test_names = sys.argv[1:]

  for arg in test_names:
    arg = arg.strip()
    if len(arg) == 0:
      return

    a = arg.split("::")
    if len(a) == 1:
      # From module or folder
      a_splitted = a[0].split(";")
      if len(a_splitted) != 1:
        # means we have pattern to match against
        if a_splitted[0].endswith("/"):
          debug("/ from folder " + a_splitted[0] + ". Use pattern: " + a_splitted[1])
          tests.append(a_splitted[0])
      else:
        if a[0].endswith("/"):
          debug("/ from folder " + a[0])
          tests.append(a[0])
        else:
          debug("/ from module " + a[0])
          tests.append(a[0])

    elif len(a) == 2:
      # From testcase
      debug("/ from testcase " + a[1] + " in " + a[0])
      tests.append(a[0] + ":" + a[1])
    else:
      # From method in class or from function
      debug("/ from method " + a[2] + " in testcase " +  a[1] + " in " + a[0])
      if a[1] == "":
          # test function, not method
          tests.append(a[0] + ":" + a[2])
      else:
          tests.append(a[0] + ":" + a[1] + "." + a[2])

  argv = ['nosetests']

  if opts:
    options = shlex.split(opts)
    argv.extend(options)

  argv.extend(tests)
  config = Config(plugins=DefaultPluginManager())
  config.configure(argv)
  config.plugins.loadPlugins()

  ind = [argv.index(x) for x in argv if x.startswith('--processes')]
  if ind:
    processes = argv.pop(ind[0]).split('=')[-1]
    ind_timeout = [argv.index(x) for x in argv if x.startswith('--process-timeout')]
    if ind_timeout:
      timeout = argv.pop(ind_timeout[0]).split('=')[-1]
    else:
      timeout = 10
    from nose_multiprocess import MultiProcessTeamcityNoseRunner
    TestProgram(argv=argv, testRunner=MultiProcessTeamcityNoseRunner(verbosity=config.verbosity, config=config, processes=processes,
                                                                     timeout=timeout))
  else:
    TestProgram(argv=argv, testRunner=TeamcityNoseRunner(verbosity=config.verbosity, config=config))#, addplugins=[TeamcityPlugin()])

if __name__ == "__main__":
  process_args()