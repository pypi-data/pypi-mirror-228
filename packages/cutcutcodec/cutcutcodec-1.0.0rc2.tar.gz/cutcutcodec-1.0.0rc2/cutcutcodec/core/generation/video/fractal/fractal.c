#define PY_SSIZE_T_CLEAN
#include <Python.h>



int square(int num) {
    return num * num;
}

static PyObject *py_square(PyObject *self, PyObject *args) {
  int n_num, result;
  if (!PyArg_ParseTuple(args, "i", &n_num)) {
    return NULL;
  }
  result = square(n_num);

  return Py_BuildValue("i", result);
}

static PyMethodDef fractalMethods[] = {
  {"square", py_square, METH_VARARGS, "Function for calculating square in C"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fractal = {
  PyModuleDef_HEAD_INIT,
  "fractal",
  "Custom fractal module",
  -1,
  fractalMethods
};

PyMODINIT_FUNC PyInit_fractal(void)
{
    return PyModule_Create(&fractal);
}

