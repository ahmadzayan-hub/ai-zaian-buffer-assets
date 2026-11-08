import unittest, importlib.util, struct, tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location("validator",Path(__file__).with_name("ValidateContentRelease.py"))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class TestGate(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name)
        (self.root/"Slide.png").write_bytes(b"\x89PNG\r\n\x1a\n"+struct.pack(">I",13)+b"IHDR"+struct.pack(">II",1080,1350))
        self.m={"content_id":"test","platform":"instagram_carousel","brand_colors":list(v.COLORS),"assets":["Slide.png"],"checks":{k:{"status":"PASS","evidence":"verified receipt"} for k in v.REQUIRED},"publication_authorised":True,"unresolved_defects":[]}
    def tearDown(self):self.t.cleanup()
    def test_valid_manifest(self):self.assertFalse(v.validate(self.m,self.root))
    def test_no_font(self):
        self.m["checks"]["dubai_font_integrity"]={"status":"BLOCKED"}
        self.assertTrue(v.validate(self.m,self.root))
    def test_no_independent_qa(self):
        del self.m["checks"]["editorial_independent_review"]
        self.assertTrue(v.validate(self.m,self.root))
    def test_no_permission(self):
        self.m["publication_authorised"]=False
        self.assertTrue(v.validate(self.m,self.root))
    def test_missing_asset(self):
        self.m["assets"]=["missing.png"]
        self.assertTrue(v.validate(self.m,self.root))
    def test_wrong_size(self):
        self.m["platform"]="instagram_story"
        self.assertTrue(v.validate(self.m,self.root))
    def test_path_escape(self):
        self.m["assets"]=["../../private.png"]
        self.assertTrue(v.validate(self.m,self.root))
    def test_palette(self):
        self.m["brand_colors"]=["#000000"]
        self.assertTrue(v.validate(self.m,self.root))
    def test_open_defects(self):
        self.m["unresolved_defects"]=["D-006"]
        self.assertTrue(v.validate(self.m,self.root))
if __name__=="__main__":unittest.main()
