# auto-generated file
import _cffi_backend

ffi = _cffi_backend.FFI('_pypy_winbase_cffi',
    _version = 0x2601,
    _types = b'\x00\x00\x01\x0D\x00\x00\x07\x01\x00\x00\x00\x0F\x00\x00\x01\x0D\x00\x00\x07\x01\x00\x00\x07\x01\x00\x00\x00\x0F\x00\x00\x01\x0D\x00\x00\x07\x01\x00\x00\x07\x01\x00\x00\x09\x01\x00\x00\x00\x0F\x00\x00\x01\x0D\x00\x00\x19\x01\x00\x00\x07\x01\x00\x00\x00\x0F\x00\x00\x01\x0D\x00\x00\x00\x0F\x00\x00\x01\x0D\x00\x00\x64\x03\x00\x00\x13\x11\x00\x00\x67\x03\x00\x00\x15\x11\x00\x00\x07\x01\x00\x00\x0A\x01\x00\x00\x13\x11\x00\x00\x13\x11\x00\x00\x63\x03\x00\x00\x62\x03\x00\x00\x02\x0F\x00\x00\x01\x0D\x00\x00\x15\x03\x00\x00\x1F\x11\x00\x00\x15\x11\x00\x00\x0A\x01\x00\x00\x02\x0F\x00\x00\x01\x0D\x00\x00\x15\x11\x00\x00\x02\x0F\x00\x00\x01\x0D\x00\x00\x15\x11\x00\x00\x08\x01\x00\x00\x02\x0F\x00\x00\x01\x0D\x00\x00\x15\x11\x00\x00\x18\x03\x00\x00\x02\x0F\x00\x00\x01\x0D\x00\x00\x15\x11\x00\x00\x15\x11\x00\x00\x15\x11\x00\x00\x1F\x11\x00\x00\x0A\x01\x00\x00\x07\x01\x00\x00\x0A\x01\x00\x00\x02\x0F\x00\x00\x01\x0D\x00\x00\x5B\x03\x00\x00\x39\x11\x00\x00\x15\x11\x00\x00\x15\x11\x00\x00\x07\x01\x00\x00\x0A\x01\x00\x00\x39\x11\x00\x00\x39\x11\x00\x00\x1B\x11\x00\x00\x1C\x11\x00\x00\x02\x0F\x00\x00\x0D\x0D\x00\x00\x07\x01\x00\x00\x00\x0F\x00\x00\x29\x0D\x00\x00\x08\x01\x00\x00\x02\x0F\x00\x00\x18\x0D\x00\x00\x15\x11\x00\x00\x0A\x01\x00\x00\x02\x0F\x00\x00\x18\x0D\x00\x00\x15\x11\x00\x00\x39\x11\x00\x00\x0A\x01\x00\x00\x02\x0F\x00\x00\x18\x0D\x00\x00\x02\x0F\x00\x00\x56\x0D\x00\x00\x06\x01\x00\x00\x00\x0F\x00\x00\x56\x0D\x00\x00\x00\x0F\x00\x00\x56\x0D\x00\x00\x10\x01\x00\x00\x00\x0F\x00\x00\x15\x0D\x00\x00\x0A\x01\x00\x00\x02\x0F\x00\x00\x15\x0D\x00\x00\x02\x0F\x00\x00\x00\x09\x00\x00\x01\x09\x00\x00\x02\x01\x00\x00\x66\x03\x00\x00\x04\x01\x00\x00\x00\x01',
    _globals = (b'\x00\x00\x24\x23CloseHandle',0,b'\x00\x00\x1E\x23CreatePipe',0,b'\x00\x00\x12\x23CreateProcessA',0,b'\x00\x00\x38\x23CreateProcessW',0,b'\x00\x00\x2F\x23DuplicateHandle',0,b'\x00\x00\x60\x23GetCurrentProcess',0,b'\x00\x00\x2B\x23GetExitCodeProcess',0,b'\x00\x00\x4E\x23GetModuleFileNameW',0,b'\x00\x00\x5D\x23GetStdHandle',0,b'\x00\x00\x53\x23GetVersion',0,b'\xFF\xFF\xFF\x1FSEM_FAILCRITICALERRORS',1,b'\xFF\xFF\xFF\x1FSEM_NOALIGNMENTFAULTEXCEPT',4,b'\xFF\xFF\xFF\x1FSEM_NOGPFAULTERRORBOX',2,b'\xFF\xFF\xFF\x1FSEM_NOOPENFILEERRORBOX',32768,b'\x00\x00\x47\x23SetErrorMode',0,b'\x00\x00\x27\x23TerminateProcess',0,b'\x00\x00\x4A\x23WaitForSingleObject',0,b'\x00\x00\x44\x23_get_osfhandle',0,b'\x00\x00\x10\x23_getch',0,b'\x00\x00\x10\x23_getche',0,b'\x00\x00\x58\x23_getwch',0,b'\x00\x00\x58\x23_getwche',0,b'\x00\x00\x10\x23_kbhit',0,b'\x00\x00\x07\x23_locking',0,b'\x00\x00\x0C\x23_open_osfhandle',0,b'\x00\x00\x00\x23_putch',0,b'\x00\x00\x5A\x23_putwch',0,b'\x00\x00\x03\x23_setmode',0,b'\x00\x00\x00\x23_ungetch',0,b'\x00\x00\x55\x23_ungetwch',0),
    _struct_unions = ((b'\x00\x00\x00\x62\x00\x00\x00\x02$PROCESS_INFORMATION',b'\x00\x00\x15\x11hProcess',b'\x00\x00\x15\x11hThread',b'\x00\x00\x18\x11dwProcessId',b'\x00\x00\x18\x11dwThreadId'),(b'\x00\x00\x00\x63\x00\x00\x00\x02$STARTUPINFO',b'\x00\x00\x18\x11cb',b'\x00\x00\x13\x11lpReserved',b'\x00\x00\x13\x11lpDesktop',b'\x00\x00\x13\x11lpTitle',b'\x00\x00\x18\x11dwX',b'\x00\x00\x18\x11dwY',b'\x00\x00\x18\x11dwXSize',b'\x00\x00\x18\x11dwYSize',b'\x00\x00\x18\x11dwXCountChars',b'\x00\x00\x18\x11dwYCountChars',b'\x00\x00\x18\x11dwFillAttribute',b'\x00\x00\x18\x11dwFlags',b'\x00\x00\x56\x11wShowWindow',b'\x00\x00\x56\x11cbReserved2',b'\x00\x00\x65\x11lpReserved2',b'\x00\x00\x15\x11hStdInput',b'\x00\x00\x15\x11hStdOutput',b'\x00\x00\x15\x11hStdError')),
    _typenames = (b'\x00\x00\x00\x1CLPPROCESS_INFORMATION',b'\x00\x00\x00\x1BLPSTARTUPINFO',b'\x00\x00\x00\x62PROCESS_INFORMATION',b'\x00\x00\x00\x63STARTUPINFO',b'\x00\x00\x00\x56wint_t'),
)
