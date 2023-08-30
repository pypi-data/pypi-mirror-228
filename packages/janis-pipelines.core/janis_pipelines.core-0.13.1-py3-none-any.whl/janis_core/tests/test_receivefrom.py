import unittest

from janis_core.types import UnionType

from janis_core import String, Array, File, Int, Stdout
from janis_core.types.common_data_types import Filename


class FileSubclass(File):
    def name(self):
        return "test_receivefrom_subclass"


class FileSubclassSubclass(FileSubclass):
    def name(self):
        return super().name() + "_2"


class Test_ReceiveFrom(unittest.TestCase):
    def test_str_str(self):
        s1 = String()
        s2 = String()
        self.assertTrue(s2.can_receive_from(s1))

    def test_str_optstr(self):
        s1 = String(optional=False)
        s2 = String(optional=True)
        self.assertTrue(s2.can_receive_from(s1))

    def test_optstr_str(self):
        s1 = String(optional=True)
        s2 = String(optional=False)
        self.assertFalse(s2.can_receive_from(s1))

    def test_optstr_optstr(self):
        s1 = String(optional=True)
        s2 = String(optional=True)
        self.assertTrue(s2.can_receive_from(s1))

    def test_int_str(self):
        i = Int()
        s = String()
        self.assertFalse(s.can_receive_from(i))

    def test_arraystr_arraystr(self):
        ar1 = Array(String())
        ar2 = Array(String())
        self.assertTrue(ar2.can_receive_from(ar1))

    def test_arraystr_arrayoptstr(self):
        ar1 = Array(String())
        ar2 = Array(String(optional=True))
        self.assertTrue(ar2.can_receive_from(ar1))

    def test_arrayoptstr_arraystr(self):
        ar1 = Array(String(optional=True))
        ar2 = Array(String(optional=False))
        self.assertFalse(ar2.can_receive_from(ar1))

    def test_arrayoptstr_arrayoptstr(self):
        ar1 = Array(String(optional=True))
        ar2 = Array(String(optional=True))
        self.assertTrue(ar2.can_receive_from(ar1))

    def test_arrayarraystr_arraystr(self):
        ar1 = Array(Array(String()))
        ar2 = Array(String())
        self.assertFalse(ar2.can_receive_from(ar1))

    def test_inheritance_forward(self):
        f1 = FileSubclass()
        f2 = File()
        self.assertTrue(f2.can_receive_from(f1))

    def test_inheritance_backward(self):
        f1 = File()
        f2 = FileSubclass()
        self.assertFalse(f2.can_receive_from(f1))

    def test_generatedFilename(self):
        s1 = String()
        s2 = Filename()
        self.assertTrue(s2.can_receive_from(s1))

    def test_receiveFromGeneratedFilename(self):
        s1 = Filename()
        s2 = String()
        self.assertTrue(s2.can_receive_from(s1))


class TestRecieveFromStdout(unittest.TestCase):
    def test_receivefromstdout_file(self):
        s1 = Stdout()
        s2 = File()
        self.assertTrue(s2.can_receive_from(s1))

    def test_recievefromstdout_optional(self):
        s1 = Stdout()
        s2 = File(optional=True)
        self.assertTrue(s2.can_receive_from(s1))

    def test_recievefromstdout_subtype(self):
        s1 = Stdout(FileSubclass())
        s2 = File()
        self.assertTrue(s2.can_receive_from(s1))

    def test_receivefromstdout_reverse(self):
        s1 = File()
        s2 = Stdout(FileSubclass())
        self.assertFalse(s2.can_receive_from(s1))

    def test_receive_from_nonfile_stdout(self):
        s1 = FileSubclass()
        s2 = Stdout(FileSubclass())
        self.assertTrue(s2.can_receive_from(s1))


class TestReceiveFromUnion(unittest.TestCase):
    def test_union_str_str(self):
        s1 = UnionType(String, String)
        s2 = String()
        self.assertTrue(s2.can_receive_from(s1))

    def test_union_str_int(self):
        s1 = UnionType(String, Int)
        s2 = String()
        self.assertFalse(s2.can_receive_from(s1))
