from libc.limits cimport INT_MAX

cdef extern from "<float.h>" nogil:
    const double DBL_MAX



























cdef class atomic_object:
    cdef readonly str mode
    cdef readonly size_t size
    cdef void * x2

    cdef dict x5

    cdef void * y1(self)
    cpdef void change_mode(self, str newmode=*, bint windows_unix_compatibility=*) except *
    cdef size_t y2(self, long long input) except? INT_MAX
    cdef long long y3(self, size_t input) except? INT_MAX
    cdef bytes y4(self, size_t input, size_t length, bint threadlocal=*)

