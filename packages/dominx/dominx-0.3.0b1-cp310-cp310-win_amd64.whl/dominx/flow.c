#include "dominx/flow.h"

static int
dmxPy_Flow_traverse(dmxPy_FlowObject *self, visitproc visit, void *arg)
{
    return 0;
}

static int
dmxPy_Flow_clear(dmxPy_FlowObject *self)
{
    return 0;
}

static void
dmxPy_Flow_dealloc(dmxPy_FlowObject *self)
{
    PyObject_GC_UnTrack(self);
    dmxPy_Flow_clear(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

PyMODINIT_FUNC
PyInit_flow(void)
{
    PyObject *m;

    if (PyType_Ready(&dmxPy_FlowType) < 0)
        return NULL;

    m = PyModule_Create(&dmxPy_module_flow);
    if (m == NULL)
        return NULL;

    Py_INCREF(&dmxPy_FlowType);
    if (PyModule_AddObject(m, "Flow", (PyObject *)&dmxPy_FlowType) < 0) {
        Py_DECREF(&dmxPy_FlowType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
