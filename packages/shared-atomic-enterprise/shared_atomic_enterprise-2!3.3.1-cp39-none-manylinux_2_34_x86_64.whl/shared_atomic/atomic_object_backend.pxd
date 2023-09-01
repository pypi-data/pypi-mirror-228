


cdef extern from "<float.h>" nogil:
    const double DBL_MAX


























cdef class atomic_object:
    cdef readonly str mode
    cdef readonly size_t size
    cdef void * x2

    cdef dict x5

    cdef void * y1(self)
    cpdef void change_mode(self, str newmode=*, bint windows_unix_compatibility=*) except *
    cdef size_t y2(self, long long input) except? 1
    cdef long long y3(self, size_t input) except? 1
    cdef bytes y4(self, size_t input, size_t length, bint threadlocal=*)

cdef class array2d:
    cdef void * x1
    cdef bint x2
    cdef size_t x3
    cdef size_t x4
    cdef size_t x5
    cdef Py_ssize_t x6[2]
    cdef Py_ssize_t x7[2]

