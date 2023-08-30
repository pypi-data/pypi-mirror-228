import unittest
import time
from pyappi.document import VolatileDocument, Document

test_documents = [(Document,"test")]#, (VolatileDocument,"vdtest")] Volatile needs history to be implemented

class TestAppiLog(unittest.TestCase):
    def setUp(self):
        [doc(name,"test").delete() for (doc,name) in test_documents]

    def _test_log_base(self,_doc_type, _doc_name):
        with _doc_type(_doc_name,"test") as doc:
        
            doc["comments~log"] = {}
            log  = doc["comments~log"]

            log._depth = 8
            log._size = 256
            log._interval = 1000* 60 * 60
            log._mode = -1

            now = int(time.time())

            for i in range(9):
                log[now + i] = { "message": "message"+str(i) }

            self.assertEqual(log.get(now+0,None), None)

            for i in range(1, 9):
                self.assertEqual(log[now+i].message, "message"+str(i))

            long_message = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 1234567890"
            log[now+10] = { "message": long_message}

            self.assertEqual(log[now+10].message, long_message)

            history_id = f'_{doc["$id"].serial}.{now - (now % (1000 * 60 * 60))}'

            with _doc_type(history_id,"test") as history:
                hlog = history.comments

                for i in range(1, 9):
                    self.assertEqual(hlog[now+i].message, "message"+str(i))

                self.assertEqual(hlog[now+10].message, long_message)

    def test_log(self):
        [self._test_log_base(doc,name) for (doc,name) in test_documents]



if __name__ == "__main__":
    unittest.main()
