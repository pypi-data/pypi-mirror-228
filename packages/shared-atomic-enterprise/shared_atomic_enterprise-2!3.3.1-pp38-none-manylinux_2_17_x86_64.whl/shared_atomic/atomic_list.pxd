from shared_atomic.atomic_object_backend cimport atomic_object
from libc.limits cimport ULLONG_MAX

cpdef size_t list_get_int(atomic_list input_list) except ?ULLONG_MAX
cpdef void list_set_int(atomic_list input_list, size_t integer) except *
cpdef list list_get_list(atomic_list input_list)
cpdef void list_set_list(atomic_list input_list, list data) except *
cpdef list list_get_and_set(atomic_list input_list, list data)
cpdef list list_compare_and_set_value(atomic_list input_list, list i, list n)
cpdef void list_store(atomic_list n, atomic_list i) except*
cpdef void list_shift(atomic_list n, atomic_list i, atomic_list j) except *
cpdef bint list_compare_and_set(atomic_list j, atomic_list i, list data) except *

cdef class atomic_list(atomic_object):
    cpdef void delete(self) except*
    cdef readonly char x13
    cdef readonly str x14
    cdef list l1(self, bytes bits_in_bytes)
    cdef tuple l2(self, list input_list)
    cdef tuple l3(self, size_t data_prefix, char accumulate_length, char input_length, char kind)
    cpdef size_t get_int(self) except ?ULLONG_MAX
    cpdef void set_int(self, size_t integer) except *
    cpdef list get_list(self)
    cpdef void set_list(self, list data) except *
    cpdef list list_get_and_set(self, list data)
    cpdef list list_compare_and_set_value(self, list i, list n)
    cpdef void list_store(self, atomic_list i) except*
    cpdef void list_shift(self, atomic_list i, atomic_list j) except*
    cpdef bint list_compare_and_set(self, atomic_list i, list data) except*
    cpdef void reencode(self, str newencode) except *