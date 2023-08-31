import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

from seaplane_framework.flow import processor


class TestMsg(unittest.TestCase):
    def test_encode_decode(self):
        msg = processor._Msg(b"foo", {"bar": "baz"})
        raw = msg.encode()
        decoded_msg = processor._Msg.decode(raw)
        self.assertEqual(msg, decoded_msg)

    def test_passthrough_compatibility(self):
        msg = b"foobar"
        self.assertEqual(msg, processor._Msg.decode(msg))

    def test_bad_version(self):
        msg = processor._Msg(b"foo", {"bar": "baz"})
        with self.assertRaises(processor.MissingVersionException):
            msg.encode(65535)  # missing version
        # missing version
        raw_msg = processor.MAGIC_NUMBER + b"\xFF\xFF" + b"foo"
        with self.assertRaises(processor.MissingVersionException):
            processor._Msg.decode(raw_msg)


class TestEndToEndBenthos(unittest.TestCase):
    stdpipe = shutil.which("stdpipe")
    benthos = shutil.which("benthos")

    def setUp(self):
        self.fifo_dir = tempfile.mkdtemp()
        self.input_path = os.path.join(self.fifo_dir, "input.fifo")
        self.output_path = os.path.join(self.fifo_dir, "output.fifo")
        processor._default_processor_io._input_fifo_path = self.input_path
        processor._default_processor_io._output_fifo_path = self.output_path
        self.cleanup_fifo()

    def teardown(self):
        self.cleanup_fifo()

    def cleanup_fifo(self):
        try:
            os.remove(self.input_path)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.output_path)
        except FileNotFoundError:
            pass

    @unittest.skipIf(not (stdpipe and benthos), "test requires benthos and stdpipe")
    def test_benthos_codec_v1(self):
        HERE = pathlib.Path(__file__).parent
        benthos_env = os.environ.copy()
        benthos_env["FIFO_TEMP"] = self.fifo_dir
        # Run the benthos test (then proceed to act as processor).
        benthos_test = subprocess.Popen(
            [self.benthos, "test", "{}/encoder_v1_test.yaml".format(HERE)],
            env=benthos_env,
        )
        # Process exactly one message from benthos.
        processor.start()
        msg = processor.read()
        msg.body = msg.body.upper()
        msg.meta["example_key"] = "mutated metadata value"
        processor.write(msg)
        processor.flush()
        # Assert benthos passed as well.
        self.assertEqual(benthos_test.wait(), 0)

    @unittest.skipIf(not (stdpipe and benthos), "test requires benthos and stdpipe")
    def test_benthos_codec_v0(self):
        HERE = pathlib.Path(__file__).parent
        benthos_env = os.environ.copy()
        benthos_env["FIFO_TEMP"] = self.fifo_dir
        # Run the benthos test (then proceed to act as processor).
        benthos_test = subprocess.Popen(
            [self.benthos, "test", "{}/encoder_v0_test.yaml".format(HERE)],
            env=benthos_env,
        )
        # Process exactly one message from benthos.
        processor.start()
        msg = processor.read()
        msg = msg.upper()
        processor.write(msg)
        processor.flush()
        # Assert benthos passed as well.
        self.assertEqual(benthos_test.wait(), 0)
