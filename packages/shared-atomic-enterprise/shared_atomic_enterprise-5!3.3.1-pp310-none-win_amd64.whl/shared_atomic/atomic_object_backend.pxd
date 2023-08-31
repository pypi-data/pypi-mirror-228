









































cdef class atomic_object:
    cdef readonly str mode
    cdef readonly size_t size
    cdef bint x3
    cdef long x4
    cdef long x5
    cdef int x6
    cdef long long x7
    cdef long long x8


    cdef dict x12
    cpdef void delete(self) except *
    cdef bytes y1(self, long long input, size_t length, bint threadlocal=*)
    cpdef void y2(self,
                                            object_id: int,
                                            bint windows_unix_compatibility,
                                            long long reference_m,
                                            size_t size,
                                            int creation_pid,
                                            size_t total_size_including_ending_zeros=*,
                                            str encoding=*) except *
    cpdef void change_mode(self, str newmode=*, bint windows_unix_compatibility=*) except*
    cdef size_t y3(self, long long input)
    cdef long long y4(self, size_t input)
    cdef  void y5(self) except *
    cdef y6(self, bint windows_unix_compatibility)


cdef class subprocess_reference:
    cdef long long x1
    cdef long long x2

    cdef char y41(self) except? CHAR_MAX
    cdef void y42(self, char n) except *
    cdef char y43(self, char n) except? CHAR_MAX
    cdef char y44(self, char e, char n) except? CHAR_MAX
    cdef char y45(self, char n) except? CHAR_MAX
    cdef char y46(self, char n) except? CHAR_MAX
    cdef char y47(self, char n) except? CHAR_MAX
    cdef char y48(self, char n) except? CHAR_MAX
    cdef char y49(self, char n) except? CHAR_MAX

    cdef long long y1(self) except? LLONG_MAX
    cdef void y2(self, long long n) except *
    cdef long long y3(self, long long n) except? LLONG_MAX
    cdef long long y4(self, long long e, long long n)  except? LLONG_MAX
    cdef long long y5(self, long long n) except? LLONG_MAX
    cdef long long y6(self, long long n) except? LLONG_MAX
    cdef long long y7(self, long long n) except? LLONG_MAX
    cdef long long y8(self, long long n) except? LLONG_MAX
    cdef long long y9(self, long long n) except? LLONG_MAX
    cdef long long y10(self, long long n) except? LLONG_MAX
    cdef long long y11(self, long long n) except? LLONG_MAX
    cdef unsigned char y12(self, long long offset) except 2
    cdef unsigned char y13(self, long long offset) except 2
    cdef short y14(self) except? SHRT_MAX
    cdef void y15(self, short n) except *
    cdef short y16(self, short n) except? SHRT_MAX
    cdef short y17(self, short e, short n) except? SHRT_MAX

    cdef short y18(self, short n) except? SHRT_MAX
    cdef short y19(self, short n) except? SHRT_MAX
    cdef short y20(self, short n) except? SHRT_MAX
    cdef short y21(self, short n) except? SHRT_MAX
    cdef short y22(self, short n) except? SHRT_MAX

    cdef long y23(self) except? INT_MAX
    cdef void y24(self, long n) except *
    cdef long y25(self, long n) except? INT_MAX
    cdef long y26(self, long e, long n) except? INT_MAX
    cdef long y27(self, long n) except? INT_MAX
    cdef long y28(self, long n) except? INT_MAX
    cdef long y29(self, long n) except? INT_MAX
    cdef long y30(self, long n) except? INT_MAX
    cdef long y34(self, long n) except? INT_MAX
    cdef long y35(self, long n) except? INT_MAX
    cdef long y36(self, long n) except? INT_MAX
    cdef unsigned char y37(self, long offset) except 2
    cdef unsigned char y38(self, long offset) except 2
    cdef int y39(self, int size,
                                                     char *i, int i_length,  char * n, int n_length,
                                                     char * out) except -1
    cdef int y40(self,  char *i,  char *n,
                                                   size_t offset, size_t size, size_t total_size_including_ending_zeros, int length,
                                                    char * result) except -1

cdef class multiprocessing_reference(subprocess_reference):
    cdef long long x3
    cdef dict x4

    cdef void close_reference(self, bint windows_unix_compatibility) except *


cpdef subprocess_reference get_reference(atomic_object a)
cpdef void release_reference(subprocess_reference a) except *

