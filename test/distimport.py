def distimport(pathdir,modulename):
    import importlib
    import sys
    sys.path.append(pathdir)
    return importlib.import_module(modulename)
